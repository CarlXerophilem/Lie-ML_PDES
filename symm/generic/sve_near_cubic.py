"""Scoped first-order obstruction certificate for the cubic Lagrangian SVE symmetry.

This module does not classify the unrestricted point-symmetry algebra.  It
records an exact obstruction inside the declared diagonal-scaling class and a
separate corollary conditional on the published generic classification.
"""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
import hashlib
import json
from pathlib import Path
from typing import Any

import sympy as sp

from .core import JetSpace, PointGenerator
from .jets import jet_coordinates, prolonged_action, total_derivative


_ROOT = Path(__file__).resolve().parents[2]
_SOURCE_PDF = (
    _ROOT
    / "ref"
    / "pdfs"
    / "Lie Symmetries and Similarity Solutions for a Shallow-Water Model "
    "with Bed Elevation in Lagrange Variables-mathematics-14-00433-v3.pdf"
)


def _dimensionless_velocity_description(velocity_scale: str) -> str:
    return (
        f"v = d(phi_bar)/d(t_bar) = d(phi_phys)/d(t_phys)/{velocity_scale} > 0"
    )


@dataclass(frozen=True)
class P0ModelContract:
    """The regular branch on which the logarithmic expansion is meaningful."""

    velocity_scale: str = "U_star"
    positive_time: bool = True
    positive_material_coordinate: bool = True
    positive_phi_s: bool = True
    positive_velocity: bool = True
    fixed_kappa: bool = True
    beta_rule: str = "beta_tr = m*kappa"
    jet_order: int = 3
    multiplier_convention: str = "pr(X)(E) = M*E"
    source_doi: str = "10.3390/math14030433"

    def guard_failures(self) -> tuple[str, ...]:
        """Return all contract failures without preventing a failure certificate."""
        failures: list[str] = []
        if not self.positive_velocity:
            failures.append("the near-cubic expansion requires a positive dimensionless velocity")
        if not self.positive_phi_s:
            failures.append("the regular branch requires phi_s > 0")
        if not self.positive_time or not self.positive_material_coordinate:
            failures.append("the declared local chart requires t > 0 and s > 0")
        if not self.fixed_kappa:
            failures.append("P0 freezes kappa while beta_tr changes through m*kappa")
        if self.beta_rule != "beta_tr = m*kappa":
            failures.append("P0 requires beta_tr = m*kappa")
        if self.jet_order != 3:
            failures.append("the printed Lagrangian master equation has jet order three")
        if not self.velocity_scale:
            failures.append("a positive reference velocity scale is required before log(v)")
        return tuple(failures)

    def as_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["dimensionless_velocity"] = _dimensionless_velocity_description(
            self.velocity_scale
        )
        data["branch_guards"] = [
            guard
            for guard, present in (
                ("t > 0", self.positive_time),
                ("s > 0", self.positive_material_coordinate),
                ("phi_s > 0", self.positive_phi_s),
                ("v > 0", self.positive_velocity),
            )
            if present
        ]
        data["missing_required_guards"] = [
            guard
            for guard, present in (
                ("t > 0", self.positive_time),
                ("s > 0", self.positive_material_coordinate),
                ("phi_s > 0", self.positive_phi_s),
                ("v > 0", self.positive_velocity),
            )
            if not present
        ]
        data["divisions_and_log_guards"] = ["phi_s != 0", "v > 0", f"{self.velocity_scale} > 0"]
        return data


def _nondimensional_chart(contract: P0ModelContract) -> dict[str, Any]:
    """State the scale convention that makes the logarithm well-defined."""
    return {
        "coordinate_rescaling": (
            "t_phys = T_star*t_bar, s_phys = S_star*s_bar, "
            f"phi_phys = {contract.velocity_scale}*T_star*phi_bar"
        ),
        "velocity": _dimensionless_velocity_description(contract.velocity_scale),
        "engine_jet_interpretation": (
            "after dropping bars, phi_x = phi_t = v and phi_y = phi_s in the nondimensional chart"
        ),
        "logarithm_argument": "v",
        "family_status": "dimensionless-formal-parameter-family",
        "coefficient_convention": "g and kappa are fixed dimensionless constants of the rescaled normal form",
        "source_units_nonclaim": (
            "P0 does not infer m-independent physical units for the source coefficient beta_tr "
            "across different exponents."
        ),
    }


def _units_and_divisions(contract: P0ModelContract) -> dict[str, Any]:
    """Record every non-polynomial guard and explicit denominator in P0."""
    return {
        "unit_convention": {
            "t": "dimensionless t_bar, written t after bars are dropped",
            "s": "dimensionless s_bar, written s after bars are dropped",
            "phi": (
                f"dimensionless phi_bar after phi_phys = {contract.velocity_scale}*T_star*phi_bar"
            ),
            "v": "dimensionless",
            "g": "fixed dimensionless coefficient in the rescaled normal form",
            "kappa": "fixed dimensionless coefficient in the rescaled normal form",
        },
        "division_records": [
            {
                "location": "fluid inner term",
                "expression": "phi_ss/phi_s**2",
                "guard": "phi_s != 0",
            },
            {
                "location": "transport inner term",
                "expression": "phi_ts/phi_s",
                "guard": "phi_s != 0",
            },
            {
                "location": "near-cubic expansion",
                "expression": "log(v)",
                "guard": "v > 0",
            },
        ],
        "scaling_constraint_divisions": "none",
    }


@dataclass(frozen=True)
class TransportExpansion:
    """Expansion of m v**(m-1) at m=3 with kappa held fixed."""

    leading: sp.Expr
    first_order: sp.Expr


@dataclass(frozen=True)
class CubicDefectIdentity:
    """The independently prolonged first-order defect of the unchanged X5."""

    lhs: sp.Expr
    rhs: sp.Expr
    regular_sample_value: sp.Expr


@dataclass(frozen=True)
class _JetExpressions:
    space: JetSpace
    t: sp.Symbol
    s: sp.Symbol
    g: sp.Symbol
    kappa: sp.Symbol
    phi: sp.Symbol
    phi_t: sp.Symbol
    phi_s: sp.Symbol
    fluid_inner: sp.Expr
    transport_inner: sp.Expr
    e0: sp.Expr
    e1: sp.Expr


def transport_factor_expansion(velocity: sp.Expr) -> TransportExpansion:
    """Derive the coefficient expansion of (3+delta)*v**(2+delta)."""
    velocity = sp.sympify(velocity)
    if velocity.is_positive is False:
        raise ValueError("transport expansion requires a positive dimensionless velocity")
    delta = sp.Symbol("delta", real=True)
    factor = (3 + delta) * velocity ** (2 + delta)
    return TransportExpansion(
        leading=sp.simplify(factor.subs(delta, 0)),
        first_order=sp.simplify(sp.diff(factor, delta).subs(delta, 0)),
    )


def _build_jet_expressions() -> _JetExpressions:
    t, s = sp.symbols("t s", positive=True)
    g, kappa = sp.symbols("g kappa", positive=True)
    phi = sp.Symbol("phi")
    space = JetSpace((t, s), (phi,), 3)
    jet = space.jet_symbol
    phi_t = jet(0, (1, 0))
    phi_s = jet(0, (0, 1))
    fluid_inner = phi_s * jet(0, (2, 0)) - g * jet(0, (0, 2)) / phi_s**2
    transport_inner = phi_t**2 * jet(0, (1, 1)) / phi_s
    e0 = total_derivative(space, fluid_inner, 0) - 3 * g * kappa * total_derivative(
        space, transport_inner, 1
    )
    e1 = -g * kappa * total_derivative(
        space, transport_inner * (1 + 3 * sp.log(phi_t)), 1
    )
    return _JetExpressions(
        space=space,
        t=t,
        s=s,
        g=g,
        kappa=kappa,
        phi=phi,
        phi_t=phi_t,
        phi_s=phi_s,
        fluid_inner=fluid_inner,
        transport_inner=transport_inner,
        e0=sp.cancel(e0),
        e1=sp.cancel(e1),
    )


def _full_equation(space: JetSpace, g: sp.Symbol, kappa: sp.Symbol, m: sp.Expr) -> sp.Expr:
    jet = space.jet_symbol
    phi_t = jet(0, (1, 0))
    phi_s = jet(0, (0, 1))
    fluid_inner = phi_s * jet(0, (2, 0)) - g * jet(0, (0, 2)) / phi_s**2
    transport_inner = phi_t ** (m - 1) * jet(0, (1, 1)) / phi_s
    return sp.cancel(
        total_derivative(space, fluid_inner, 0)
        - g * m * kappa * total_derivative(space, transport_inner, 1)
    )


def _regular_sample_substitution(expressions: _JetExpressions) -> dict[sp.Symbol, sp.Expr]:
    values: dict[sp.Symbol, sp.Expr] = {
        expressions.t: sp.Rational(5, 4),
        expressions.s: sp.Rational(7, 5),
        expressions.g: sp.Rational(3, 2),
        expressions.kappa: sp.Rational(2, 5),
        expressions.phi: sp.Rational(1, 3),
    }
    for field, multi_index in jet_coordinates(expressions.space):
        symbol = expressions.space.jet_symbol(field, multi_index)
        if multi_index == (1, 0):
            values[symbol] = sp.Rational(3, 2)
        elif multi_index == (0, 1):
            values[symbol] = sp.Rational(5, 4)
        else:
            derivative_order = sum(multi_index)
            values[symbol] = sp.Rational(derivative_order + 1, derivative_order + 7)
    return values


def cubic_generator_first_order_defect() -> CubicDefectIdentity:
    """Verify pr(X5)E1 + E1 = 3*g*kappa*D_s(phi_t**2*phi_ts/phi_s)."""
    expressions = _build_jet_expressions()
    x5 = PointGenerator((expressions.t, -2 * expressions.s), (0,))
    lhs = sp.cancel(prolonged_action(expressions.space, expressions.e1, x5) + expressions.e1)
    rhs = sp.cancel(
        3
        * expressions.g
        * expressions.kappa
        * total_derivative(expressions.space, expressions.transport_inner, 1)
    )
    sample = sp.simplify(lhs.subs(_regular_sample_substitution(expressions)))
    return CubicDefectIdentity(lhs=lhs, rhs=rhs, regular_sample_value=sample)


def _scaling_data() -> dict[str, sp.Expr]:
    """Derive scaling constraints from the weights of all master-equation terms."""
    m, a, b, c, delta = sp.symbols("m a b c delta", real=True)
    a1, b1, c1 = sp.symbols("a1 b1 c1", real=True)

    fluid_product_weight = (c - b) + (c - 2 * a)
    pressure_weight = (c - 2 * b) - 2 * (c - b)
    inner = sp.expand(fluid_product_weight - pressure_weight)

    water_outer_weight = pressure_weight - a
    transport_inner_weight = (m - 1) * (c - a) + (c - a - b) - (c - b)
    transport_outer_weight = transport_inner_weight - b
    outer = sp.factor(
        sp.expand(transport_outer_weight - water_outer_weight).subs(b, 3 * c - 2 * a)
    )
    deformation = {m: 3 + delta, a: 1 + delta * a1, b: -2 + delta * b1, c: delta * c1}
    inner_linear = sp.expand(inner.subs(deformation)).coeff(delta, 1)
    outer_linear = sp.expand(sp.series(outer.subs(deformation), delta, 0, 2).removeO()).coeff(delta, 1)
    return {
        "m": m,
        "a": a,
        "b": b,
        "c": c,
        "delta": delta,
        "a1": a1,
        "b1": b1,
        "c1": c1,
        "inner": sp.factor(inner),
        "outer": sp.factor(outer),
        "inner_linear": sp.factor(inner_linear),
        "outer_linear": sp.factor(outer_linear),
    }


def _direct_prolongation_agreement(data: dict[str, sp.Expr]) -> tuple[bool, sp.Expr, sp.Expr]:
    """Compare the weight obstruction with an independent jet prolongation result."""
    expressions = _build_jet_expressions()
    a1, b1, c1 = data["a1"], data["b1"], data["c1"]
    x5 = PointGenerator((expressions.t, -2 * expressions.s), (0,))
    x1 = PointGenerator((a1 * expressions.t, b1 * expressions.s), (c1 * expressions.phi,))
    m0, m1 = sp.Integer(-1), -(a1 + c1)
    first_order_residual = sp.cancel(
        prolonged_action(expressions.space, expressions.e0, x1)
        + prolonged_action(expressions.space, expressions.e1, x5)
        - m0 * expressions.e1
        - m1 * expressions.e0
    )
    restricted = sp.cancel(first_order_residual.subs(b1, 3 * c1 - 2 * a1))
    expected = sp.cancel(
        -data["outer_linear"]
        * 3
        * expressions.g
        * expressions.kappa
        * total_derivative(expressions.space, expressions.transport_inner, 1)
    )
    return sp.simplify(restricted - expected) == 0, restricted, expected


def _multiplier_identities(expressions: _JetExpressions) -> tuple[bool, bool]:
    x5 = PointGenerator((expressions.t, -2 * expressions.s), (0,))
    cubic = sp.cancel(prolonged_action(expressions.space, expressions.e0, x5) + expressions.e0)

    x4 = PointGenerator((expressions.t, expressions.s), (expressions.phi,))
    e4 = _full_equation(expressions.space, expressions.g, expressions.kappa, sp.Integer(4))
    generic = sp.cancel(prolonged_action(expressions.space, e4, x4) + 2 * e4)
    return sp.simplify(cubic) == 0, sp.simplify(generic) == 0


def two_sided_delta_check() -> dict[str, Any]:
    """Secondary high-precision evidence for the unmodified X5 linear defect."""
    expressions = _build_jet_expressions()
    delta = sp.Symbol("delta", real=True)
    e_delta = _full_equation(
        expressions.space, expressions.g, expressions.kappa, 3 + delta
    )
    x5 = PointGenerator((expressions.t, -2 * expressions.s), (0,))
    residual = sp.cancel(prolonged_action(expressions.space, e_delta, x5) + e_delta)
    sampled = sp.cancel(residual.subs(_regular_sample_substitution(expressions)))
    h = sp.Rational(1, 10**12)
    positive_h = abs(sp.N(sampled.subs(delta, h), 80))
    positive_half_h = abs(sp.N(sampled.subs(delta, h / 2), 80))
    negative_h = abs(sp.N(sampled.subs(delta, -h), 80))
    negative_half_h = abs(sp.N(sampled.subs(delta, -h / 2), 80))
    return {
        "classification": "linear-defect-secondary-evidence",
        "sample_jet": "regular rational jet with phi_t=3/2 and phi_s=5/4",
        "h": "1e-12",
        "absolute_defect_at_h": float(positive_h),
        "absolute_ratio_h_over_half_h": float(sp.N(positive_h / positive_half_h, 30)),
        "absolute_ratio_negative_h_over_half_h": float(
            sp.N(negative_h / negative_half_h, 30)
        ),
        "symbolic_status": "secondary only; exact coefficients determine the certificate",
    }


def _hash_if_present(path: Path) -> str | None:
    if not path.is_file():
        return None
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _source_conditioned_corollary() -> dict[str, Any]:
    return {
        "status": "qualified",
        "requires_published_exhaustiveness": True,
        "published_premise": (
            "For generic m, the published source lists translations and the single dilation "
            "X4=t*d_t+s*d_s+phi*d_phi."
        ),
        "continuity_requirement": "generator coefficients converge as delta approaches zero",
        "argument": (
            "A generic dilation coefficient would have to converge to both 1 from the t "
            "component and -2 from the s component in order to reach X5, which is impossible."
        ),
        "independent_classification_claim": False,
        "excluded": [
            "unrestricted determining-system proof",
            "generalized or nonclassical symmetry analysis",
            "parameter equivalence transformations",
        ],
    }


def _regularity_failed_certificate(
    contract: P0ModelContract, guard_failures: tuple[str, ...]
) -> dict[str, Any]:
    """Preserve a rejected input as a replayable, non-symbolic result."""
    return {
        "schema": "lieml.sve.near-cubic-obstruction.v1",
        "status": "regularity-failed",
        "outcome": "regularity-failed",
        "model_contract": contract.as_dict(),
        "nondimensional_chart": _nondimensional_chart(contract),
        "units_and_divisions": _units_and_divisions(contract),
        "source_hashes": {
            "draft_main_tex_sha256": _hash_if_present(_ROOT / "draft" / "main.tex"),
            "published_source_pdf_sha256": _hash_if_present(_SOURCE_PDF),
        },
        "scope": {
            "symmetry_class": "diagonal scalings a*t*d_t+b*s*d_s+c*phi*d_phi",
            "unrestricted_determining_system": "not-solved",
            "full_point_statement": "not-evaluated",
            "parameter_perturbation": "not-evaluated",
        },
        "guard_failures": list(guard_failures),
        "checks": {},
        "nonclaims": [
            "No symbolic expansion or symmetry calculation was attempted after a failed guard.",
            "No unrestricted point-symmetry classification is established.",
            "ML training is intentionally excluded from P0",
        ],
    }


def build_scaling_obstruction_certificate(
    contract: P0ModelContract | None = None,
) -> dict[str, Any]:
    """Build a JSON-serializable P0 certificate for the declared scaling class."""
    contract = P0ModelContract() if contract is None else contract
    guard_failures = contract.guard_failures()
    if guard_failures:
        return _regularity_failed_certificate(contract, guard_failures)
    expressions = _build_jet_expressions()
    velocity = sp.Symbol("v", positive=True)
    expansion = transport_factor_expansion(velocity)
    scaling = _scaling_data()
    cubic_identity, generic_identity = _multiplier_identities(expressions)
    defect_identity = cubic_generator_first_order_defect()
    prolongation_agrees, direct_residual, expected_residual = _direct_prolongation_agreement(scaling)
    defect_identity_agrees = sp.simplify(defect_identity.lhs - defect_identity.rhs) == 0
    checks = {
        "transport_expansion_includes_beta_change": sp.simplify(
            expansion.first_order - velocity**2 * (1 + 3 * sp.log(velocity))
        )
        == 0,
        "cubic_multiplier_identity": cubic_identity,
        "generic_x4_multiplier_identity": generic_identity,
        "cubic_first_order_defect_identity": defect_identity_agrees,
        "prolonged_residual_agrees": prolongation_agrees,
        "nonzero_first_order_scaling_defect": scaling["outer_linear"] == -1,
    }
    status = "verified" if all(checks.values()) else "inconsistent"
    outcome = "obstruction-verified-scaling" if status == "verified" else "inconsistent"
    return {
        "schema": "lieml.sve.near-cubic-obstruction.v1",
        "status": status,
        "outcome": outcome,
        "model_contract": contract.as_dict(),
        "nondimensional_chart": _nondimensional_chart(contract),
        "units_and_divisions": _units_and_divisions(contract),
        "source_hashes": {
            "draft_main_tex_sha256": _hash_if_present(_ROOT / "draft" / "main.tex"),
            "published_source_pdf_sha256": _hash_if_present(_SOURCE_PDF),
        },
        "scope": {
            "symmetry_class": "diagonal scalings a*t*d_t+b*s*d_s+c*phi*d_phi",
            "unrestricted_determining_system": "not-solved",
            "full_point_statement": "source-conditioned only",
            "parameter_perturbation": "m = 3 + delta with kappa fixed",
        },
        "multiplier_convention": {
            "identity": contract.multiplier_convention,
            "cubic_multiplier": "M0 = -1",
            "first_order_multiplier": "M1 = -(a1 + c1) after inner homogeneity",
        },
        "transport_expansion": {
            "factor": "(3 + delta)*v**(2 + delta)",
            "leading": sp.sstr(expansion.leading),
            "first_order": sp.sstr(expansion.first_order),
        },
        "equation_expansion": {
            "E0": sp.sstr(expressions.e0),
            "E1": sp.sstr(expressions.e1),
            "engine_symbol_map": {
                "phi_x": "v = phi_t in the nondimensional chart",
                "phi_y": "phi_s",
                "phi_xx": "phi_tt",
                "phi_xy": "phi_ts",
                "phi_yy": "phi_ss",
            },
            "H_canonical": "v**2*phi_ts/phi_s",
            "E0_canonical": (
                "D_t(phi_s*phi_tt - g*phi_ss/phi_s**2) - 3*g*kappa*D_s(H)"
            ),
            "E1_canonical": "-g*kappa*D_s(H*(1 + 3*log(v)))",
            "order": "E_(3+delta) = E0 + delta*E1 + O(delta**2)",
        },
        "scaling_constraints": {
            "inner": "3*c - b - 2*a",
            "outer": "(m - 3)*(c - a)",
            "inner_first_order": sp.sstr(scaling["inner_linear"]),
            "outer_first_order": sp.sstr(scaling["outer_linear"]),
        },
        "first_order_defect": sp.sstr(scaling["outer_linear"]),
        "direct_prolongation": {
            "restricted_residual": sp.sstr(direct_residual),
            "expected_residual": sp.sstr(expected_residual),
            "comparison": "direct jet prolongation after inner-homogeneity substitution",
        },
        "cubic_first_order_defect": {
            "identity": "pr(X5)(E1) + E1 = 3*g*kappa*D_s(H)",
            "regular_sample_value": sp.sstr(defect_identity.regular_sample_value),
        },
        "checks": checks,
        "source_conditioned_corollary": _source_conditioned_corollary(),
        "secondary_numerical_check": two_sided_delta_check(),
        "nonclaims": [
            "No unrestricted point-symmetry classification is established.",
            "No generalized, nonclassical, or equivalence-symmetry obstruction is established.",
            "No Eulerian/Lagrangian physical-equivalence theorem is established.",
            "No solution existence, error bound, or ML acceleration claim is established.",
            "ML training is intentionally excluded from P0",
        ],
        "next_analytic_gate": (
            "Derive and verify the response PDE in r=log(t), z=s*t**2 before assuming a "
            "one-profile correction or training a model."
        ),
    }


def write_scaling_obstruction_certificate(
    path: str | Path, contract: P0ModelContract | None = None
) -> dict[str, Any]:
    """Write the scoped certificate without mutating any existing reduction artifact."""
    certificate = build_scaling_obstruction_certificate(contract)
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(certificate, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return certificate


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True, help="certificate JSON path")
    args = parser.parse_args(argv)
    certificate = write_scaling_obstruction_certificate(args.output)
    print(json.dumps({"status": certificate["status"], "outcome": certificate["outcome"]}, indent=2))
    return 0 if certificate["status"] == "verified" else 2


if __name__ == "__main__":
    raise SystemExit(main())
