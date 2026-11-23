"""Loopback HTTP service for live, checkpointed fluid perturbation experiments."""
import argparse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import signal
import threading
from urllib.parse import parse_qs, urlparse

from plotly.offline import get_plotlyjs

from .live_state import FRAME_DT, Simulation


def make_server(simulation, port=8879):
    assets=Path(__file__).resolve().parent
    plotly=get_plotlyjs().encode("utf-8")

    class Handler(BaseHTTPRequestHandler):
        def send_bytes(self,body,content_type="application/json; charset=utf-8",status=200):
            self.send_response(status)
            self.send_header("Content-Type",content_type)
            self.send_header("Content-Length",str(len(body)))
            self.send_header("Cache-Control","no-store")
            self.send_header("X-Content-Type-Options","nosniff")
            self.end_headers()
            try:self.wfile.write(body)
            except (BrokenPipeError,ConnectionResetError):pass

        def send_json(self,value,status=200):
            self.send_bytes(json.dumps(value,allow_nan=False,separators=(",",":")).encode(),status=status)

        def do_GET(self):
            parsed=urlparse(self.path)
            try:
                if parsed.path in ("/","/index.html"):
                    self.send_bytes((assets/"live_dashboard.html").read_bytes(),"text/html; charset=utf-8")
                elif parsed.path=="/plotly.min.js":
                    self.send_bytes(plotly,"application/javascript; charset=utf-8")
                elif parsed.path in ("/api/state","/api/health"):
                    if parsed.path.endswith("health"):
                        with simulation.lock:
                            self.send_json({"service":"ready","run_id":simulation.run_id,
                                            "time":simulation.time,"running":simulation.running,
                                            "status":simulation.status,"error":simulation.error})
                    else:self.send_json(simulation.snapshot())
                elif parsed.path=="/api/frames":
                    with simulation.lock:self.send_json({"times":list(simulation.frame_times),"run_id":simulation.run_id})
                elif parsed.path=="/api/frame":
                    index=int(parse_qs(parsed.query).get("index",["-1"])[0])
                    self.send_json(simulation.frame(index))
                elif parsed.path=="/api/checkpoint":
                    with simulation.lock:
                        simulation.checkpoint()
                        self.send_bytes((simulation.directory/"checkpoint.npz").read_bytes(),"application/octet-stream")
                else:self.send_json({"error":"not found"},404)
            except (ValueError,TypeError) as exc:self.send_json({"error":str(exc)},400)

        def do_POST(self):
            # The SSH-forwarded localhost service has no public control endpoint.
            # A custom header blocks browser form CSRF; no CORS is granted.
            host=self.headers.get("Host","")
            origin=self.headers.get("Origin")
            if self.headers.get("X-LieML-Control")!="1" or (origin and origin!=f"http://{host}"):
                self.send_json({"error":"same-origin control header required"},403);return
            if self.path!="/api/control":
                self.send_json({"error":"not found"},404);return
            try:
                if self.headers.get_content_type()!="application/json":
                    raise ValueError("application/json required")
                length=int(self.headers.get("Content-Length","0"))
                if not 0<length<=4096:raise ValueError("invalid control body size")
                command=json.loads(self.rfile.read(length))
                self.send_json(simulation.control(command))
            except (ValueError,TypeError,OverflowError) as exc:self.send_json({"error":str(exc)},400)

        def log_message(self,format,*args):
            if self.command!="GET" or (len(args)>1 and str(args[1])!="200"):
                super().log_message(format,*args)

    return ThreadingHTTPServer(("127.0.0.1",port),Handler)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state-dir",type=Path,required=True)
    parser.add_argument("--port",type=int,default=8879)
    parser.add_argument("--n",type=int,default=128)
    parser.add_argument("--horizon",type=float,default=100)
    parser.add_argument("--wall-interval",type=float,default=.5,
                        help="wall seconds between .05 units of simulated time")
    args=parser.parse_args()
    if not .05<=args.wall_interval<=10:parser.error("wall interval must be between .05 and 10 seconds")
    sim=Simulation(args.state_dir,n=args.n,horizon=args.horizon)
    server=make_server(sim,args.port)
    stop=threading.Event()

    def evolve():
        while not stop.wait(args.wall_interval):
            with sim.lock:
                if not sim.running:continue
                try:sim.advance(min(sim.time+FRAME_DT,sim.horizon))
                except Exception as exc:print(f"Simulation stopped at t={sim.time}: {exc}",flush=True)

    worker=threading.Thread(target=evolve,daemon=True)
    worker.start()
    def shutdown(signum,frame):
        stop.set()
        threading.Thread(target=server.shutdown,daemon=True).start()
    signal.signal(signal.SIGTERM,shutdown)
    signal.signal(signal.SIGINT,shutdown)
    print(f"LieML live: http://127.0.0.1:{args.port}; run={sim.run_id}; t={sim.time}; horizon={sim.horizon}",flush=True)
    try:server.serve_forever(poll_interval=.2)
    finally:
        stop.set();worker.join(timeout=10);sim.checkpoint();server.server_close()


if __name__=="__main__":main()
