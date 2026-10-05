# Hosted long-time fluid simulation

The live service extends the verified fluid baseline with stateful stepping,
paired reference/comparison fields, checkpoints and parameter changes. It uses
the same Rusanov/SSPRK3 and dealiased Fourier/RK4 methods as the baseline; it does
not add a new symmetry theorem or a neural solver.

## Working interface

Open <http://127.0.0.1:8879/> on this machine. The original static baseline
remains at port 8878. The live port is forwarded over SSH to a service bound
only to `127.0.0.1` on `priestess`.

Default: periodic, unforced 2D incompressible Navier–Stokes, interacting-vortex
initial data, viscosity `nu=0.01`, a 128×128 computational grid, and a
nondimensional horizon `t=100`. It advances 0.05 units of simulation time per
worker iteration with a 0.5-second wall-time pause between iterations. Actual
wall speed also includes computation and checkpoint I/O. The horizon can be
extended up to 1000; reaching it pauses evolution but leaves the service ready.
Original one-spatial-dimensional Eulerian SVE and constant-drift Oseen are
selectable new-run targets. New runs preserve earlier run directories.

The long horizon is numerical, not a claim of global existence or uniformly
small numerical error. Unforced viscous flows decay; the interface should not
add forcing merely to keep the animation busy. The SVE discretization remains
a smooth positive-branch baseline, not a well-balanced or shock-certified
hydrodynamics package. Inspect grid resolution and conservation diagnostics
before treating a perturbation plot as a research conclusion.

## Meaning of a parameter perturbation

Let `t*` be the simulation time when **Apply perturbation** succeeds. The
comparison field is continuous at that instant:

\[
u_{\mathrm{comparison}}(t_*^+)=u_{\mathrm{comparison}}(t_*^-),
\qquad \lambda(t\ge t_*)=\lambda_{\mathrm{new}}.
\]

The reference continues with its original fixed parameters. A second parameter
change continues the existing comparison field, and the event list retains the
time and coefficients. Rebase copies the current reference field and parameters
into the comparison. It does not rewind time. A new run restarts both fields
from the prescribed initial data and stores the old run separately.

For NS, adjust viscosity. For SVE, adjust the Grass exponent `m`, transport
coefficient `kappa`, or gravity `g`; a small change from `m=3` can be entered
directly as, for example, `m=3.02`. Noninteger powers require the retained
positive-velocity branch. These are model-coefficient changes, distinct from
the Lie group parameter epsilon. The simulation integrates the original PDE
after a change; it does not continue to impose a cubic-only symmetry ansatz.

Both fields advance to the same time before being committed. A nonfinite
stage or departure from an enforced physical branch stops the run and retains
the last good pair. The displayed L2 difference is an RMS spatial discrepancy
in vorticity for NS/Oseen, and depth for SVE; it is not an error bound or an
automatic sensitivity derivative.

## Persistence and data

Remote release: `/home/carl/lieml/releases/20260925-live-v1`.
Persistent state: `/home/carl/lieml/live-state`.
User service: `lieml-live.service`, running with Python from conda `pinn`.
The user service has restart-on-failure enabled. Lingering is enabled for
`carl`, allowing it to run after SSH logout and start after a host reboot.

Every 0.5 units of simulated time, and at coefficient changes, full-precision
states are archived. An atomic checkpoint stores both fields, time, parameters,
paused/running state and recent history. Graceful shutdown also checkpoints.
An abrupt kill can lose work since the last checkpoint (normally at most
0.5 simulated units); restart resumes that checkpoint. A run's `events.jsonl`
and `diagnostics.jsonl` retain the experiment record. The browser shows the
most recent 4000 diagnostic samples and 200 events; the disk logs retain older
records. Stored-frame browsing is separate from pausing the simulation.

The local tunnel supervisor reconnects if SSH drops. It runs while this
Windows session/process remains available; it is not installed as a Windows
login task. To restart it after closing it or restarting this machine:

```powershell
cd 'D:\MATHs\math 4890 LieML'
python -B -m symm.fluid_baselines.live_tunnel --background
```

To stop just this live tunnel:

```powershell
python -B -m symm.fluid_baselines.live_tunnel --stop
```

Remote operations:

```bash
ssh priestess
systemctl --user status lieml-live.service
journalctl --user -u lieml-live.service -n 40 --no-pager
systemctl --user restart lieml-live.service
```

The service uses `pinn`'s absolute Python path and does not rely on an
interactive shell remaining open. API health is available at `/api/health`;
`/api/checkpoint` downloads the current full-precision checkpoint. Control
requests use same-origin JSON with `X-LieML-Control: 1`.

## Verification record

Verified on 2026-09-25; evidence is stored in
`research_artifacts/live-simulation-20260925/`.

- **212 tests passed locally and remotely**. The Windows run retained its
  pre-existing pytest temporary-directory cleanup warning after exit 0.
- The separate long-time pilot passed **9 checks through t=100**. An analytic
  shear with a viscosity change at t=0.2 had maximum velocity error below
  `7e-17` at t=100. This exact low-mode control is not a claim of that accuracy
  for general flow.
- NS 128² versus 256² at t=5 gave vorticity RMS discrepancy `4.43e-7`.
  At the tested times through t=100, energy/enstrophy decreased, divergence
  stayed below `2.86e-14`, and the spectral-tail indicator stayed below
  `1.53e-8`. Later diagnostics do not replace a long-time refinement study.
- Original SVE with `m=3 -> 3.02` at t=1 retained positive depth/velocity
  and conserved periodic mass/bed integrals through t=100. It produced a
  nonzero response; the largest sampled depth discrepancy was about `3.87e-5`.
- Browser controls changed NS viscosity, SVE exponent and Oseen drift while
  preserving all current fields. Subsequent steps produced nonzero differences.
  Actual plots and local probes matched API values; saved-frame inspection
  and 1D/2D model transitions worked. The complete dashboard was inspected.
- A paused service restart preserved both **full-precision arrays bitwise**,
  time, parameters, run id and pause state. A separate SIGKILL test verified
  systemd's automatic recovery, followed by successful resume.
- Terminating only the owned SSH tunnel child caused the local supervisor to
  create a new SSH connection and restore HTTP access automatically.

The final handed-over run is unperturbed NS at `nu=0.01`, with both branches
advancing toward t=100. Verification experiments are retained as separate
archived runs. The source archive hash, final deployment overrides and service
state are recorded in `deployment.json`. SCP connections were closed by the
host during deployment; byte transfer over the working SSH channel succeeded
and the archive and deployed files were SHA256-verified.
