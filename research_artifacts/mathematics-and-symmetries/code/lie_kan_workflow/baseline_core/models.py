"""Dimensionless smooth 2+1 SWE/Grass-SVE model and declared test families."""
from dataclasses import asdict, dataclass, replace
import numpy as np


@dataclass(frozen=True)
class Case:
    name: str
    m: float = 3.0
    kappa: float = 0.01  # includes the constant porosity factor
    coriolis: float = 0.0
    drag: float = 0.0  # linear drag; not a Manning law
    amplitude: float = 0.03
    bed_amplitude: float = 0.02
    phase_x: float = 0.0
    phase_y: float = 0.0
    u0: float = 0.25
    v0: float = 0.15
    g: float = 1.0
    control: str = "wave"

    def metadata(self):
        return asdict(self)

    def context(self):
        return np.array([(self.m - 3) / .2, self.amplitude / .04,
                         self.bed_amplitude / .02, self.kappa / .01,
                         self.coriolis, self.drag], dtype=float)


def initial_np(x, y, case):
    x, y = x - case.phase_x, y - case.phase_y
    bed = case.bed_amplitude * np.sin(x) * np.sin(y)
    depth = 1 + case.amplitude * np.cos(x) * np.cos(y)
    if case.control == "lake":
        depth = 1 - bed
    return np.stack([depth, np.full_like(depth, case.u0),
                     np.full_like(depth, case.v0), bed], axis=-1)


def initial_torch(points, case):
    import torch
    x, y = points[:, 1] - case.phase_x, points[:, 2] - case.phase_y
    bed = case.bed_amplitude * torch.sin(x) * torch.sin(y)
    h = 1 + case.amplitude * torch.cos(x) * torch.cos(y)
    if case.control == "lake":
        h = 1 - bed
    return torch.stack([h, torch.full_like(h, case.u0),
                        torch.full_like(h, case.v0), bed], dim=1)


def suite():
    return {
        "flat": Case("flat", kappa=0, bed_amplitude=0),
        "topography": Case("topography", kappa=0),
        "rotation_drag": Case("rotation_drag", kappa=0, coriolis=.2, drag=.05),
        **{f"sve_m{m:g}": Case(f"sve_m{m:g}", m=m)
           for m in (2.9, 3.0, 3.1, 4.0)},
    }


def conditional_family():
    base = Case("family")
    train = [replace(base, name=f"train_m{m:g}_a{a:g}", m=m, amplitude=a)
             for m in (2.9, 3.0, 3.1) for a in (.02, .04)]
    # Neither exponent nor initial amplitude appears in training at these values.
    test = [replace(base, name=f"test_m{m:g}_a0.03", m=m, amplitude=.03)
            for m in (2.95, 3.05)]
    test.append(replace(test[0], name="test_translated", phase_x=.37, phase_y=.51))
    return train, test


def residual_torch(jet, case):
    """Jet layout: [t,x,y,h,u,v,b, ht,hx,hy, ut,ux,uy, vt,vx,vy, bt,bx,by]."""
    import torch
    h, u, v, _ = jet[:, 3:7].unbind(1)
    d = jet[:, 7:].reshape(-1, 4, 3)
    ht, hx, hy = d[:, 0].unbind(1)
    ut, ux, uy = d[:, 1].unbind(1)
    vt, vx, vy = d[:, 2].unbind(1)
    bt, bx, by = d[:, 3].unbind(1)
    if case.kappa:
        r2 = u*u + v*v
        speed_factor = r2.pow((case.m - 1) / 2)
        cross_factor = (case.m - 1) * r2.pow((case.m - 3) / 2)
        flux_div = case.kappa * (speed_factor * (ux + vy) + cross_factor *
                    (u*u*ux + u*v*vx + u*v*uy + v*v*vy))
    else:
        flux_div = torch.zeros_like(bt)
    return torch.stack([
        ht + u*hx + v*hy + h*(ux + vy),
        ut + u*ux + v*uy + case.g*(hx + bx) - case.coriolis*v + case.drag*u,
        vt + u*vx + v*vy + case.g*(hy + by) + case.coriolis*u + case.drag*v,
        bt + flux_div,
    ], dim=1)


def equation_scales(case):
    return np.array([.08, .12, .12, max(.02*case.kappa, 1e-4)])


def subgroup_coeff_torch(jet, name):
    """First prolongation, not a total derivative of the sampled residual."""
    import torch
    z, fields = jet[:, :3], jet[:, 3:7]
    d = jet[:, 7:].reshape(-1, 4, 3)
    xi, eta = torch.zeros_like(z), torch.zeros_like(fields)
    if name in ("Tx", "Ty", "Tt"):
        xi[:, {"Tt": 0, "Tx": 1, "Ty": 2}[name]] = 1
        prolonged = torch.zeros_like(d)
    elif name == "D":
        xi = z
        prolonged = -d
    elif name == "V":
        xi = torch.stack([z[:, 0]*0, z[:, 1], z[:, 2]], dim=1)
        weights = jet.new_tensor([2., 1., 1., 2.])
        eta = fields * weights
        prolonged = d * (weights[None, :, None] - jet.new_tensor([0., 1., 1.]))
    elif name == "J":
        xi = torch.stack([z[:, 0]*0, -z[:, 2], z[:, 1]], dim=1)
        eta = torch.stack([fields[:, 0]*0, -fields[:, 2], fields[:, 1], fields[:, 3]*0], 1)
        rotated = torch.stack([d[:, 0]*0, -d[:, 2], d[:, 1], d[:, 3]*0], 1)
        correction = torch.stack([d[:, :, 0]*0, -d[:, :, 2], d[:, :, 1]], 2)
        prolonged = rotated + correction
    else:
        raise ValueError(name)
    return torch.cat([xi, eta, prolonged.reshape(-1, 12)], dim=1)


def multiplier(name):
    matrix = np.zeros((4, 4))
    if name == "D":
        matrix = -np.eye(4)
    elif name == "V":
        matrix = np.diag([2., 1., 1., 2.])
    elif name == "J":
        matrix[1, 2], matrix[2, 1] = -1, 1
    return matrix


def finite_action(jet,name,epsilon):
    """Exact supplied one-parameter subgroup action on first jets (bulk PDE)."""
    import torch
    independent=torch.eye(3,dtype=jet.dtype,device=jet.device)
    dependent=torch.eye(4,dtype=jet.dtype,device=jet.device)
    shift=torch.zeros(3,dtype=jet.dtype,device=jet.device)
    if name in ('Tt','Tx','Ty'):
        shift[{'Tt':0,'Tx':1,'Ty':2}[name]]=epsilon
    elif name=='D':
        independent*=np.exp(epsilon)
    elif name=='V':
        independent[1,1]=independent[2,2]=np.exp(epsilon)
        dependent=torch.diag(jet.new_tensor(np.exp(epsilon*np.array([2.,1.,1.,2.]))))
    elif name=='J':
        c,s=np.cos(epsilon),np.sin(epsilon)
        rotation=jet.new_tensor([[c,-s],[s,c]])
        independent[1:,1:]=rotation;dependent[1:3,1:3]=rotation
    else:
        raise ValueError(name)
    coordinates=jet[:,:3]@independent.T+shift
    fields=jet[:,3:7]@dependent.T
    derivatives=torch.einsum('ab,nbc,cd->nad',dependent,jet[:,7:].reshape(-1,4,3),torch.linalg.inv(independent))
    return torch.cat([coordinates,fields,derivatives.reshape(-1,12)],1)
