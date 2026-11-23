"""One-dimensional subalgebra representatives from actual adjoint matrices.

Supported class: V semidirect A, where V and A are abelian and A acts
diagonally on the supplied translation basis. This covers every declared
1D SVE algebra. The equivalence is connected inner adjoint action together
with nonzero rescaling of a line generator; no outer equivalences are added.
"""
from __future__ import annotations

from itertools import combinations, product

import sympy as sp

from main import algebra_structure, lie_bracket


# 1. Obtain ad matrices from brackets, then verify the semidirect decomposition.
def adjoint_structure(coordinates,basis):
    coordinates,basis = tuple(coordinates),tuple(sp.Matrix(v) for v in basis)
    closure = algebra_structure(coordinates,basis)
    if closure["status"] != "verified_bracket_closure":
        return {"status":"unresolved","reason":"basis closure/dependence unresolved","closure":closure}
    dim = len(basis)
    matrices = [sp.zeros(dim) for _ in basis]
    for key,coefficients in closure["structure_constants"].items():
        i,j = map(int,key.split(","))
        matrices[i][:,j] = sp.Matrix(coefficients)
        matrices[j][:,i] = -sp.Matrix(coefficients)
    bracket_checks = []
    for i in range(dim):
        for j in range(dim):
            represented = sum((matrices[i][k,j]*basis[k] for k in range(dim)),sp.zeros(len(coordinates),1))
            actual = sp.Matrix(lie_bracket(coordinates,basis[i],basis[j]))
            bracket_checks.extend(sp.simplify(z) for z in represented-actual)
    if any(z != 0 for z in bracket_checks):
        return {"status":"unresolved","reason":"adjoint reconstruction failed"}
    translations,scalings = [],[]
    for j,vector in enumerate(basis):
        if not any(v.has(*coordinates) for v in vector):
            translations.append(j)
        elif all(sp.simplify(v-sp.diff(v,c)*c)==0 and
                 not sp.diff(v,c).has(*coordinates) for v,c in zip(vector,coordinates)):
            scalings.append(j)
        else:
            return {"status":"unresolved","reason":"basis is not in a diagonal semidirect presentation"}
    if not translations or len(scalings)>2:
        return {"status":"unresolved","reason":"adapter requires nonempty V and at most two diagonal directions"}
    W = sp.Matrix(len(translations),len(scalings),
                  lambda i,j:matrices[scalings[j]][translations[i],translations[i]])
    structural = []
    for i in translations:
        for j in translations:
            structural.extend(matrices[i][:,j])
    for i in scalings:
        for j in scalings:
            structural.extend(matrices[i][:,j])
    for a,ai in enumerate(scalings):
        for k,vi in enumerate(translations):
            target = sp.zeros(dim,1)
            target[vi] = W[k,a]
            structural.extend(matrices[ai][:,vi]-target)
    structural = tuple(sp.simplify(v) for v in structural)
    if any(v != 0 for v in structural):
        return {"status":"unresolved","reason":"actual ad action is not diagonal abelian-by-abelian",
                "structure_residuals":structural}
    return {"status":"verified_diagonal_semidirect","coordinates":coordinates,"basis":basis,
            "adjoint_matrices":tuple(matrices),"translation_indices":tuple(translations),
            "scaling_indices":tuple(scalings),"weights":W,
            "bracket_reconstruction_residuals":tuple(bracket_checks),"structure_residuals":structural,
            "convention":"ad_X(Y)=[X,Y]; Ad(exp(eps X))=exp(eps ad_X)"}


# 2. Logarithmic normal forms for a positive diagonal action on one support.
def _subsets(indices,include_empty=False):
    for size in range(0 if include_empty else 1,len(indices)+1):
        yield from combinations(indices,size)


def _log_normalizer(matrix):
    """Rank/projector certificate for y -> y+M theta, with fixed support.

    Pivot rows are set to zero. Their independent minor gives an explicit
    normalization map. Nonzero minor conditions are retained as guards.
    """
    M = sp.Matrix(matrix)
    count = M.rows
    pivot_rows = tuple(M.T.rref()[1]) if M.cols else ()
    rank = len(pivot_rows)
    if rank:
        P = M.extract(pivot_rows,range(M.cols))
        pivot_columns = tuple(P.rref()[1])
        minor = P.extract(range(rank),pivot_columns)
        determinant = sp.factor(minor.det())
        inverse = minor.inv()
        select = sp.zeros(rank,count)
        for i,j in enumerate(pivot_rows):
            select[i,j]=1
        theta_map = sp.zeros(M.cols,count)
        chosen = -inverse*select
        for i,j in enumerate(pivot_columns):
            theta_map[j,:]=chosen[i,:]
    else:
        pivot_columns=()
        determinant=sp.S.One
        theta_map=sp.zeros(M.cols,count)
    projection = (sp.eye(count)+M*theta_map).applyfunc(sp.simplify)
    checks = list(projection*M)+list(projection*projection-projection)
    for row in pivot_rows:
        checks.extend(projection[row,:])
    higher_minors=[]
    if rank < min(M.shape):
        for rows in combinations(range(M.rows),rank+1):
            for cols in combinations(range(M.cols),rank+1):
                higher_minors.append(sp.factor(M.extract(rows,cols).det()))
        checks.extend(higher_minors)
    checks=tuple(sp.simplify(z) for z in checks)
    if any(z != 0 for z in checks):
        raise ValueError("unresolved rank/projector identity")
    remaining=tuple(i for i in range(count) if i not in pivot_rows)
    return {"matrix":M,"rank":rank,"pivot_rows":pivot_rows,"pivot_columns":pivot_columns,
            "independent_minor":determinant,"nonzero_guards":(sp.Ne(determinant,0,evaluate=False),) if determinant.free_symbols else (),
            "theta_map":theta_map,"invariant_projection":projection,"remaining_rows":remaining,
            "continuous_moduli":len(remaining),"verification_residuals":checks,
            "higher_minors":tuple(higher_minors)}


def _vector_from_coefficients(structure,coefficients):
    return sum((v*b for v,b in zip(coefficients,structure["basis"])),
               sp.zeros(len(structure["coordinates"]),1))


def _translation_families(structure,W):
    indices=structure["translation_indices"]
    families=[]
    for support in _subsets(tuple(range(len(indices)))):
        action=sp.ones(len(support),1).row_join(W.extract(support,range(W.cols)))
        normalizer=_log_normalizer(action)
        for tail in product((-1,1),repeat=len(support)-1):
            signs=(1,)+tail
            coefficients=sp.zeros(len(structure["basis"]),1)
            moduli=[]
            for pos,index in enumerate(support):
                if pos in normalizer["remaining_rows"]:
                    rho=sp.Symbol("rho_"+"_".join(map(str,support))+"_"+str(pos),positive=True)
                    moduli.append(rho)
                    magnitude=rho
                else:
                    magnitude=sp.S.One
                coefficients[indices[index]]=signs[pos]*magnitude
            families.append({"kind":"translation_line","support":support,"signs":signs,
                             "parameters":tuple(moduli),"parameter_guards":tuple(sp.Gt(v,0,evaluate=False) for v in moduli),
                             "coefficients":coefficients,"generator":_vector_from_coefficients(structure,coefficients),
                             "normalizer":normalizer})
    return families


# 3. Nonzero A projections. Their projective direction is an inner invariant.
def _a_direction_strata(W):
    rank=W.cols
    if rank==0:
        return []
    if rank==1:
        return [{"label":"A coefficient normalized to one","direction":sp.Matrix([1]),
                 "parameters":(),"guards":()}]
    rho=sp.Symbol("a_ratio",real=True)
    direction=sp.Matrix([1,rho])
    affine_weights=W*direction
    roots=set()
    for value in affine_weights:
        if value==0 or not value.has(rho):
            continue
        candidates=sp.solve(value,rho)
        if any(v.free_symbols or v.is_real is not True for v in candidates):
            raise ValueError("parameter-dependent A-direction intersections require further splitting")
        roots.update(candidates)
    roots=tuple(sorted(roots,key=sp.default_sort_key))
    records=[{"label":"finite generic A direction","direction":direction,"parameters":(rho,),
              "guards":tuple(sp.Ne(rho,value) for value in roots)}]
    records += [{"label":"finite exceptional A direction","direction":direction.subs(rho,value),
                 "parameters":(),"guards":(),"a_ratio":value} for value in roots]
    records.append({"label":"infinite A direction","direction":sp.Matrix([0,1]),"parameters":(),"guards":()})
    return records


def _a_families(structure,W):
    v_indices,a_indices=structure["translation_indices"],structure["scaling_indices"]
    families=[]
    for direction in _a_direction_strata(W):
        a=direction["direction"]
        eigenvalues=(W*a).applyfunc(sp.factor)
        kernel=tuple(i for i,value in enumerate(eigenvalues) if value==0)
        removable=tuple(i for i in range(W.rows) if i not in kernel)
        elimination_guards=tuple(sp.Ne(eigenvalues[i],0,evaluate=False) for i in removable
                                 if eigenvalues[i].free_symbols)
        for support in _subsets(kernel,include_empty=True):
            action=W.extract(support,range(W.cols))
            normalizer=_log_normalizer(action)
            # A has fixed normalization, so a global sign flip is no longer
            # available: every sign of a nonzero surviving V coefficient stays.
            for signs in product((-1,1),repeat=len(support)):
                coefficients=sp.zeros(len(structure["basis"]),1)
                for j,index in enumerate(a_indices):
                    coefficients[index]=a[j]
                moduli=[]
                for pos,index in enumerate(support):
                    if pos in normalizer["remaining_rows"]:
                        rho=sp.Symbol("sigma_"+"_".join(map(str,support))+"_"+str(pos),positive=True)
                        moduli.append(rho)
                        magnitude=rho
                    else:
                        magnitude=sp.S.One
                    coefficients[v_indices[index]]=signs[pos]*magnitude
                families.append({"kind":"nonzero_A_line","A_direction":direction,
                                 "kernel":kernel,"removable_indices":removable,
                                 "elimination_eigenvalues":eigenvalues,"elimination_guards":elimination_guards,
                                 "support":support,"signs":signs,
                                 "parameters":direction["parameters"]+tuple(moduli),
                                 "parameter_guards":direction["guards"]+tuple(sp.Gt(v,0,evaluate=False) for v in moduli),
                                 "coefficients":coefficients,"generator":_vector_from_coefficients(structure,coefficients),
                                 "normalizer":normalizer})
    return families


# 4. Parameter splitting is driven by actual eigenvalues and their collisions.
def resonance_strata(structure,parameter=None,domain=None):
    W=structure["weights"]
    symbols=set().union(*(v.free_symbols for v in W))
    if not symbols:
        return [{"label":"fixed algebra","substitutions":{},"guards":()}]
    if parameter is None or symbols != {parameter} or W.cols != 1:
        raise ValueError("symbolic weight classification needs one declared parameter and one scaling direction")
    domain=sp.S.Reals if domain is None else domain
    factors=list(W)
    factors += [W[i,0]-W[j,0] for i,j in combinations(range(W.rows),2)]
    roots=set()
    for value in factors:
        value=sp.factor(value)
        if value==0 or not value.has(parameter):
            continue
        solutions=sp.solveset(value,parameter,domain=domain)
        if not isinstance(solutions,sp.FiniteSet):
            raise ValueError("resonance set is not a certified finite set")
        roots.update(solutions)
    roots=tuple(sorted(roots,key=sp.default_sort_key))
    generic={"label":"generic parameter stratum","substitutions":{},
             "guards":(sp.Contains(parameter,domain,evaluate=False),)+tuple(sp.Ne(parameter,value) for value in roots),
             "excluded_resonances":roots,"resonance_factors":tuple(map(sp.factor,factors))}
    return [generic]+[{"label":str(parameter)+"="+str(value),"substitutions":{parameter:value},
                       "guards":(sp.Eq(parameter,value,evaluate=False),)} for value in roots]


def classify_subalgebra_lines(coordinates,basis,parameter=None,domain=None):
    """Return disjoint symbolic representative families and coverage witnesses.

    The proof is in SUBALGEBRAS.md. Certification concerns inner-adjoint line
    orbits of the supplied algebra; it does not certify maximal point symmetry.
    A symbolic one-scaling weight family requires explicit parameter/domain.
    """
    structure=adjoint_structure(coordinates,basis)
    if structure["status"] != "verified_diagonal_semidirect":
        return structure
    try:
        strata=resonance_strata(structure,parameter,domain)
        records=[]
        for cell in strata:
            substitutions=cell["substitutions"]
            specialized={**structure,
                         "basis":tuple(v.subs(substitutions,simultaneous=True) for v in structure["basis"]),
                         "weights":structure["weights"].subs(substitutions,simultaneous=True),
                         "adjoint_matrices":tuple(v.subs(substitutions,simultaneous=True) for v in structure["adjoint_matrices"])}
            W=specialized["weights"]
            families=_translation_families(specialized,W)+_a_families(specialized,W)
            records.append({**cell,"weights":W,"families":families,
                            "coverage_status":"proved_exhaustive_for_connected_inner_line_orbits",
                            "uniqueness_status":"one representative per orbit within the stated parameter domains"})
    except (ValueError,NotImplementedError) as exc:
        return {"status":"unresolved","reason":str(exc),"structure":structure}
    return {"status":"certified_line_orbit_classification","structure":structure,"strata":records,
            "equivalence":"connected inner adjoint action and arbitrary nonzero rescaling of a generator",
            "maximal_point_algebra_claim":False,"subalgebra_dimension":1,
            "optimality_status":"complete and nonredundant for the stated inner equivalence, subject to fresh review",
            "review_status":"pending_fresh_review",
            "outer_automorphism_classification":"not_claimed",
            "higher_dimensional_subalgebras":"not_claimed",
            "reduction_usefulness":"not_inferred"}


# 5. Exact witnesses using exp(actual ad), useful for independent orbit tests.
def adjoint_action(structure,coordinates_of_X,coordinates_of_Y,epsilon=1):
    algebra=structure["adjoint_matrices"]
    matrix=sum((sp.sympify(c)*A for c,A in zip(coordinates_of_X,algebra)),sp.zeros(len(algebra)))
    return ((epsilon*matrix).exp()*sp.Matrix(coordinates_of_Y)).applyfunc(sp.simplify)


def canonicalize_translation_line(structure,coefficients):
    """Normalize one concrete real translation line and return its orbit witness.

    Unknown signs or undecidable support are unresolved, never guessed.
    ``coefficients`` uses the complete supplied algebra basis ordering.
    """
    vector=sp.Matrix(coefficients)
    v_indices,a_indices=structure["translation_indices"],structure["scaling_indices"]
    if vector.rows!=len(structure["basis"]) or any(vector[i]!=0 for i in a_indices):
        return {"status":"unresolved","reason":"input must be a translation-only coefficient vector"}
    if any(vector[i].is_zero is None for i in v_indices):
        return {"status":"unresolved","reason":"translation support is undecidable"}
    support=tuple(k for k,i in enumerate(v_indices) if vector[i]!=0)
    if not support:
        return {"status":"unresolved","reason":"zero vector does not generate a line"}
    first_sign=sp.sign(vector[v_indices[support[0]]])
    if first_sign not in (-1,1):
        return {"status":"unresolved","reason":"real sign is undecidable"}
    if any(sp.sign(vector[v_indices[k]]) not in (-1,1) for k in support):
        return {"status":"unresolved","reason":"real signs are undecidable"}
    W=structure["weights"]
    M=sp.ones(len(support),1).row_join(W.extract(support,range(W.cols)))
    normalizer=_log_normalizer(M)
    logarithms=sp.Matrix([sp.log(sp.Abs(vector[v_indices[k]])) for k in support])
    theta=(normalizer["theta_map"]*logarithms).applyfunc(sp.simplify)
    scaling=sp.zeros(len(vector),1)
    for j,index in enumerate(a_indices):
        scaling[index]=theta[j+1]
    line_factor=sp.simplify(first_sign*sp.exp(theta[0]))
    canonical=(line_factor*adjoint_action(structure,scaling,vector)).applyfunc(sp.simplify)
    expected=sp.zeros(len(vector),1)
    invariant_logs=normalizer["invariant_projection"]*logarithms
    for pos,index in enumerate(support):
        expected[v_indices[index]]=sp.simplify(first_sign*sp.sign(vector[v_indices[index]])*sp.exp(invariant_logs[pos]))
    residual=(canonical-expected).applyfunc(sp.simplify)
    return {"status":"verified_orbit_witness" if all(v==0 for v in residual) else "unresolved",
            "support":support,"canonical_coefficients":canonical,"line_factor":line_factor,
            "adjoint_scaling_coordinates":scaling,"normalizer":normalizer,
            "verification_residuals":tuple(residual)}
