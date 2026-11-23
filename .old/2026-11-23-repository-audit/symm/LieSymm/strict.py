"""Equation-first strict analysis; incomplete CAS output never certifies a result.

This module deliberately does not import a classification or profile registry.
The current CAS transport retains raw output; solution parsing and a complete
characteristic solver remain explicit outstanding obligations.
"""
from __future__ import annotations

import hashlib
import json
import ast
import os
from pathlib import Path
import re
import subprocess
import tempfile
import time

import psutil
import sympy as sp
from sympy.core.function import AppliedUndef

from .core import (JetSpace, EvolutionShell, arbitrary_generator, characteristic,
                   prolongation_coefficients, point_action, split_free_jets)


def _reduce_names(symbols):
    names = {}
    reserved = {'df','sin','cos','exp','log','sqrt','pi','e','i','t','nil',
                'operator','depend','end','on','off','write','quit','strictresult'}
    # REDUCE accepts t as an algebraic independent variable in LIEPDE.
    reserved.remove('t')
    for i, symbol in enumerate(symbols):
        name = str(symbol).lower()
        if not re.fullmatch('[a-z][a-z0-9]*', name) or name in names.values() or name in reserved:
            name = f'lsvar{i}'
        names[symbol] = name
    if len(set(names.values())) != len(names):
        raise ValueError('Ambiguous REDUCE symbol names')
    return names


class StrictMixedShell:
    """J^2 shell: prolong only first-order rows, never the second-order bed row."""
    def __init__(self, space, equations):
        if len(equations) != len(space.u) or space.order(equations) not in (1, 2):
            raise ValueError('Unsupported mixed evolution system')
        self.space = space
        self.leader_order = 1
        leaders = [space.jet(a, space.unit(0)) for a in range(len(space.u))]
        matrix, rhs = sp.linear_eq_to_matrix(equations, leaders)
        determinant = sp.factor(matrix.det())
        if determinant == 0:
            raise ValueError('Singular evolution matrix')
        self.divisors = [determinant]
        self.rhs = tuple(matrix.inv()*rhs)
        if any(v.has(*leaders) for v in self.rhs):
            raise ValueError('Unresolved time leaders')
        self.rules = dict(zip(leaders, self.rhs))
        if space.order(equations) == 2:
            for axis in (*range(1, len(space.x)), 0):
                for a, rhs_value in enumerate(self.rhs):
                    if space.order((leaders[a]-rhs_value,)) == 1:
                        index = tuple(int(i == 0)+int(i == axis) for i in range(len(space.x)))
                        self.rules[space.jet(a, index)] = sp.expand(space.D(self.rhs[a], axis).xreplace(self.rules))

    def reduce(self, expression):
        return sp.expand(expression.xreplace(self.rules))


def _branch_guards(guards, symbols, substitutions):
    """Check declared guards using a small AST grammar (no eval/sympify text)."""
    names = dict(symbols) if isinstance(symbols, dict) else {str(s): s for s in symbols}
    def visit(node):
        if isinstance(node, ast.Name) and node.id in names:
            return sp.sympify(names[node.id]).subs(substitutions)
        if isinstance(node, ast.Constant) and type(node.value) is int:
            return sp.Integer(node.value)
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
            return (-1 if isinstance(node.op, ast.USub) else 1)*visit(node.operand)
        if isinstance(node, ast.BinOp):
            a,b=visit(node.left),visit(node.right)
            ops={ast.Add:lambda:a+b,ast.Sub:lambda:a-b,ast.Mult:lambda:a*b,
                 ast.Div:lambda:a/b,ast.Pow:lambda:a**b}
            if type(node.op) in ops:
                return ops[type(node.op)]()
        if isinstance(node, ast.Compare):
            values=[visit(node.left),*(visit(n) for n in node.comparators)]
            ops={ast.Eq:sp.Eq,ast.NotEq:sp.Ne,ast.Lt:sp.Lt,ast.LtE:sp.Le,ast.Gt:sp.Gt,ast.GtE:sp.Ge}
            if all(type(op) in ops for op in node.ops):
                return sp.And(*(ops[type(op)](a,b) for a,op,b in zip(values,node.ops,values[1:])))
        raise ValueError('Unsupported guard syntax')
    result=[]
    for guard in guards:
        text=re.sub(r'(?<![<>=!])=(?!=)','==',str(guard))
        try:
            condition=visit(ast.parse(text,mode='eval').body)
            evaluated=sp.simplify(condition.subs(substitutions))
            result.append(dict(guard=str(guard),condition=evaluated,
                               status='false' if evaluated == sp.false else 'true' if evaluated == sp.true else 'conditional'))
        except (ValueError,SyntaxError,TypeError):
            result.append(dict(guard=str(guard),status='unparsed'))
    return result


def guard_environment(space, parameters, branch_conditions):
    """Bind fixed parameters and named first jets without guessing from guards."""
    names = {str(s): s for s in (*space.x, *space.u, *parameters)}
    for a, field in enumerate(space.u):
        for i, x in enumerate(space.x):
            names[f'{field}_{x}'] = space.jet(a, space.unit(i))
    names.update({str(k): sp.sympify(v) for k,v in branch_conditions.get('fixed_parameters', {}).items()})
    return names


def input_fingerprint(independent_variables, dependent_fields, equations, parameters,
                      branch_conditions, data_case=None):
    """Hash the mathematical contract, including assumptions and data."""
    def canonical(value):
        if isinstance(value, sp.Basic):
            return {'sympy': sp.srepr(value)}
        if isinstance(value, dict):
            return {str(k): canonical(v) for k,v in sorted(value.items(), key=lambda p:str(p[0]))}
        if isinstance(value, (tuple,list)):
            return [canonical(v) for v in value]
        return value
    payload=canonical([independent_variables,dependent_fields,equations,parameters,branch_conditions,data_case])
    return hashlib.sha256(json.dumps(payload,sort_keys=True,separators=(',',':')).encode()).hexdigest()


def match_branch_conditions(branches, traces, keys, parameters, coordinates):
    """Match finite linear families independently of order and free-constant names.

    Span comparison is conditional on the reported nonzero rank minors.
    Matching terminal outputs is not a proof of parameter-space coverage.
    """
    def substitution(branch):
        return {p: branch['assignments'][p] for p in parameters if p in branch['assignments']}
    def basis(branch):
        values=[branch['assignments'][k].subs(substitution(branch)) for k in keys]
        free=[c for c in branch['free'] if c not in parameters]
        vectors=[tuple(sp.diff(v,c) for v in values) for c in free]
        if any(sp.simplify(v-sum(c*b[i] for c,b in zip(free,vectors)))!=0 for i,v in enumerate(values)):
            raise ValueError('Nonlinear or affine free family')
        if any(v.atoms(AppliedUndef) for b in vectors for v in b):
            raise ValueError('Unparsed function family')
        return vectors
    def equal(a,b):
        sa,sb=substitution(a),substitution(b)
        if sa.keys()!=sb.keys() or any(sp.simplify(sa[k]-sb[k])!=0 for k in sa):
            return None
        if a['remaining'] or b['remaining'] or any(k not in a['assignments'] or k not in b['assignments'] for k in keys):
            return None
        if all(sp.simplify(a['assignments'][k]-b['assignments'][k])==0 for k in keys) and set(a['free'])==set(b['free']):
            return []
        va,vb=basis(a),basis(b);columns=[];terms=set()
        for vector in va+vb:
            column={}
            for i,expression in enumerate(vector):
                for term in sp.Add.make_args(sp.expand(expression)):
                    coefficient,monomial=term.as_independent(*coordinates,as_Add=False)
                    key=(i,monomial);column[key]=column.get(key,0)+coefficient;terms.add(key)
            columns.append(column)
        terms=sorted(terms,key=str)
        matrix=sp.Matrix([[c.get(t,0) for c in columns] for t in terms])
        ma,mb=matrix[:,:len(va)],matrix[:,len(va):]
        if ma.rank()!=mb.rank() or matrix.rank()!=ma.rank():
            return None
        guards=[]
        for mat in (ma,mb):
            pivots=mat.rref()[1]
            if pivots:
                independent=mat[:,list(pivots)];rows=independent.T.rref()[1]
                minor=sp.factor(independent[list(rows),:].det())
                if minor.free_symbols: guards.append(sp.Ne(minor,0))
        return list(dict.fromkeys(guards))
    matches=[]
    for i,branch in enumerate(branches):
        candidates=[]
        for k,trace in enumerate(traces):
            try: guards=equal(branch,trace)
            except (ValueError,TypeError,KeyError,NotImplementedError): guards=None
            if guards is not None: candidates.append((k,guards))
        if len(candidates)!=1:
            return dict(matched=False,reason='Missing or ambiguous terminal branch',branch_index=i,
                        candidates=[k for k,_ in candidates],parameter_coverage='unverified')
        k,guards=candidates[0]
        matches.append(dict(branch_index=i,trace_index=k,nonzero_conditions=traces[k]['nonzero_conditions'],
                            matching_rank_guards=guards))
    bijective=len(matches)==len(traces)==len({v['trace_index'] for v in matches})
    return dict(matched=bijective,matches=matches,parameter_coverage='unverified',
                scope='Terminal-family correspondence; not a completeness proof')


def _mixed_split(space, expression, shell):
    jets = sorted((s for s in expression.free_symbols & space.reverse.keys()
                   if any(space.reverse[s][1]) and s not in shell.rules), key=str)
    polynomial = sp.Poly(expression, *jets, domain='EX') if jets else None
    terms = polynomial.terms() if polynomial is not None else [((), expression)]
    equations = list(dict.fromkeys(sp.factor_terms(c) for _, c in terms if c != 0))
    return dict(status='complete_jet_split', equations=equations, jets=jets,
                denominator=sp.denom(sp.together(expression)))


def _chart_simplify(expression, positive_bases=()):
    """Use only declared positive bases for real-power simplification."""
    value=sp.simplify(expression)
    for base in positive_bases:
        if value == 0:
            break
        positive=sp.Dummy('strict_positive_base',positive=True)
        # The second substitution applies the defining relation after factoring.
        transformed=sp.factor(value.subs(base,positive)).subs(base,positive)
        value=sp.simplify(transformed.subs(positive,base))
    return value


def parse_liepde_output(stdout, symbols=None, *, _crack_frame=False):
    """Parse a restricted REDUCE list grammar, never eval vendor output.

    `solved` means returned residual lists are empty, not maximality or
    exhaustive parameter coverage. Unreported branch inequations remain open.
    """
    match = re.search(r'LIESYMM_RESULT_BEGIN\$\s*(?:\d+:\s*)?(.*?)\$\s*(?:\d+:\s*)?LIESYMM_END\$', stdout, re.S)
    if not match:
        raise ValueError('Missing or incomplete LIEPDE result frame')
    symbols = dict(symbols or {})
    def split(text):
        depth, start, result = 0, 0, []
        for i, ch in enumerate(text):
            if ch in '{(':
                depth += 1
            elif ch in '})':
                depth -= 1
                if depth < 0:
                    raise ValueError('Unbalanced CAS expression')
            elif ch == ',' and depth == 0:
                result.append(text[start:i]); start = i+1
        if depth:
            raise ValueError('Unbalanced CAS expression')
        if text[start:].strip():
            result.append(text[start:])
        return result
    def expression(text):
        def visit(node):
            if isinstance(node, ast.Name) and re.fullmatch('[a-z][a-z0-9_]*', node.id):
                return symbols.setdefault(node.id, sp.Symbol(node.id))
            if isinstance(node, ast.Constant) and type(node.value) is int:
                return sp.Integer(node.value)
            if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.USub, ast.UAdd)):
                return (-1 if isinstance(node.op, ast.USub) else 1)*visit(node.operand)
            if isinstance(node, ast.BinOp):
                a, b = visit(node.left), visit(node.right)
                operations = {ast.Add: lambda: a+b, ast.Sub: lambda: a-b,
                              ast.Mult: lambda: a*b, ast.Div: lambda: a/b, ast.Pow: lambda: a**b}
                if type(node.op) in operations:
                    return operations[type(node.op)]()
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and not node.keywords:
                functions = {'sin': sp.sin, 'cos': sp.cos, 'exp': sp.exp, 'log': sp.log,
                             'sqrt': sp.sqrt, 'df': lambda *args: sp.Function('unevaluated_df')(*args)}
                if node.func.id in functions:
                    return functions[node.func.id](*(visit(a) for a in node.args))
            raise ValueError('Unsupported or unsafe CAS expression')
        try:
            return visit(ast.parse(' '.join(text.split()), mode='eval').body)
        except (SyntaxError, TypeError) as exc:
            raise ValueError('Malformed CAS expression') from exc
    def parse(text):
        text = text.strip()
        if text.startswith('{') and text.endswith('}'):
            return [parse(part) for part in split(text[1:-1])]
        if '=' in text:
            left, right = text.split('=', 1)
            return (expression(left), expression(right))
        return expression(text)
    raw = parse(match.group(1))
    branches = []
    if not isinstance(raw, list) or not raw:
        raise ValueError('Missing solution branches')
    for row in raw:
        if not isinstance(row, list) or len(row) != (4 if _crack_frame else 3) or not all(isinstance(v, list) for v in row):
            raise ValueError('Malformed LIEPDE branch')
        if not all(isinstance(v, tuple) and len(v) == 2 and isinstance(v[0], sp.Symbol) for v in row[1]):
            raise ValueError('Malformed generator assignments')
        if len({v[0] for v in row[1]}) != len(row[1]):
            raise ValueError('Duplicate generator assignments')
        branch=dict(remaining=row[0], assignments=dict(row[1]), free=row[2])
        if _crack_frame:
            branch['nonzero_conditions']=row[3]
        branches.append(branch)
    return dict(branches=branches, solved=all(not b['remaining'] for b in branches),
                parameter_coverage='unverified', inequalities='not_returned_by_liepde')


CRACK_CALLBACK='''
algebraic procedure crack_out(eqns,assigns,freef,ineq,solno);
begin
  off nat;
  write "STRICT_CRACK_BRANCH_BEGIN";
  write {eqns,assigns,freef,ineq};
  write "STRICT_CRACK_BRANCH_END";
  on nat;
  return {}
end$
lisp(call_crack_out:=t)$
'''


def parse_crack_output(stdout,symbols=None):
    frames=re.findall(r'STRICT_CRACK_BRANCH_BEGIN\$?(.*?)STRICT_CRACK_BRANCH_END',stdout,re.S)
    branches=[]
    for frame in frames:
        body=frame.strip().rstrip('$').strip()
        wrapper='LIESYMM_RESULT_BEGIN$\n{'+body+'}$\nLIESYMM_END$'
        branches.extend(parse_liepde_output(wrapper,symbols,_crack_frame=True)['branches'])
    return dict(branches=branches,parameter_coverage='unverified',
                scope='Raw CRACK terminal-branch conditions; correspondence to final LIEPDE families unverified')


def run_reduce(command, script, *, timeout=60, memory_bytes=1_800_000_000,
               artifact_prefix=None):
    """Run one explicit command without a shell, retaining bounded raw receipts."""
    if isinstance(timeout,bool) or not isinstance(timeout,(int,float)) or not 0 < timeout <= 1800:
        raise ValueError('timeout must be positive and at most 1800 seconds')
    if not command or isinstance(command, str) or memory_bytes <= 0:
        raise ValueError('command must be a nonempty argv sequence and memory positive')
    record = dict(command=list(command), input_sha256=hashlib.sha256(script.encode()).hexdigest(),
                  status='backend-unavailable', verified=False, returncode=None,
                  stdout='', stderr='', timeout_seconds=timeout, memory_bytes=memory_bytes)
    started = time.monotonic()
    if artifact_prefix is not None:
        prefix=Path(artifact_prefix)
        prefix.parent.mkdir(parents=True,exist_ok=True)
        paths=[Path(str(prefix)+suffix) for suffix in ('.input.red','.stdout.log','.stderr.log')]
        if any(p.exists() for p in paths):
            raise FileExistsError('Raw CAS evidence already exists; use a fresh artifact prefix')
        streams=[p.open('xb+') for p in paths]
        record['raw_files']=[str(p) for p in paths]
    else:
        streams=[tempfile.TemporaryFile() for _ in range(3)]
    with streams[0] as inp, streams[1] as out, streams[2] as err:
        inp.write(script.encode()); inp.seek(0)
        try:
            process = subprocess.Popen(command, stdin=inp, stdout=out, stderr=err, shell=False)
        except OSError as exc:
            record['stderr'] = str(exc)
            return record
        status = 'unparsed'
        peak = 0
        while process.poll() is None:
            try:
                parent = psutil.Process(process.pid)
                children = parent.children(recursive=True)
                rss = sum(p.memory_info().rss for p in [parent, *children] if p.is_running())
                peak = max(peak, rss)
            except psutil.NoSuchProcess:
                rss = 0
            if time.monotonic()-started > timeout:
                status = 'timeout'
            elif rss > memory_bytes:
                status = 'memory-limit'
            elif os.fstat(out.fileno()).st_size + os.fstat(err.fileno()).st_size > 8_000_000:
                status = 'output-limit'
            if status != 'unparsed':
                try:
                    for child in psutil.Process(process.pid).children(recursive=True):
                        child.kill()
                except psutil.NoSuchProcess:
                    pass
                process.kill()
                break
            time.sleep(.05)
        process.wait()
        out.seek(0); err.seek(0)
        record.update(stdout=out.read(8_000_000).decode('utf-8', errors='replace'),
                      stderr=err.read(8_000_000).decode('utf-8', errors='replace'),
                      returncode=process.returncode, peak_rss_bytes=peak,
                      elapsed_seconds=time.monotonic()-started)
        if status == 'unparsed' and process.returncode == 124:
            status = 'timeout'
        elif status == 'unparsed' and (process.returncode != 0 or '*****' in record['stdout']):
            status = 'error'
        record['status'] = status
    return record


def liepde_script(independent_variables, dependent_fields, equations, parameters,
                  branch_conditions, data_case=None):
    """Serialize the equation interface to LIEPDE's unrestricted point mode.

    Guard strings are not executable REDUCE input. They remain Python report
    obligations; only explicit substitutions are applied here.
    """
    j = JetSpace(independent_variables, dependent_fields)
    names = _reduce_names((*j.x, *j.u, *parameters))
    def emit(expr):
        expr = sp.sympify(expr)
        if expr in names:
            return names[expr]
        if expr in j.reverse:
            a, index = j.reverse[expr]
            args = [names[j.u[a]]]
            for x, count in zip(j.x, index):
                if count:
                    args.append(names[x])
                    if count != 1:
                        args.append(str(count))
            return 'df(' + ','.join(args) + ')'
        if isinstance(expr, sp.Integer):
            return str(expr)
        if isinstance(expr, sp.Rational):
            return f'({expr.p}/{expr.q})'
        if isinstance(expr, (sp.Add, sp.Mul)):
            return '(' + ('+' if isinstance(expr, sp.Add) else '*').join(emit(a) for a in expr.args) + ')'
        if isinstance(expr, sp.Pow):
            return '(' + emit(expr.base) + '**' + emit(expr.exp) + ')'
        if expr.func in (sp.sin, sp.cos, sp.exp, sp.log):
            return expr.func.__name__ + '(' + emit(expr.args[0]) + ')'
        raise ValueError(f'Unsupported REDUCE expression: {expr}')
    eqs = tuple(sp.sympify(e).subs(branch_conditions.get('substitutions', {}), simultaneous=True) for e in equations)
    # LIEPDE requires solved leading derivatives, not a residual list.
    shell = EvolutionShell(j, eqs)
    leaders = [j.jet(a, (shell.leader_order,) + (0,)*(len(j.x)-1)) for a in range(len(j.u))]
    solved = '{' + ','.join(emit(a)+'='+emit(b) for a, b in zip(leaders, shell.rhs)) + '}'
    fields = '{'+','.join(names[u] for u in j.u)+'}'
    coords = '{'+','.join(names[x] for x in j.x)+'}'
    depends = '\n'.join('depend '+names[u]+','+','.join(names[x] for x in j.x)+'$' for u in j.u)
    nonzero = []
    parameter_names = {str(p): p for p in parameters}
    for guard in branch_conditions.get('guards', []):
        match = re.fullmatch(r'([A-Za-z][A-Za-z0-9]*)(!=|>|<)(-?\d+)', str(guard).replace(' ', ''))
        if match and match[1] in parameter_names:
            value = parameter_names[match[1]]-sp.Integer(match[3])
            if value not in nonzero:
                nonzero.append(value)
    parameter_input = '{'+','.join(names[p] for p in parameters)+'}'
    inequ_input = '{'+','.join(emit(p) for p in nonzero)+'}'
    return ('off echo$\nload_package crack,liepde,applysym$\n'+CRACK_CALLBACK+'\non nat$\n'
            'lisp(print_:=nil)$\nlisp(prelim_:=nil)$\nlisp(individual_:=nil)$\n'
            + depends + '\nstrictresult:=liepde({' + solved+','+fields+','+coords+'},{"point"},'+parameter_input+','+inequ_input+')$\n'
            'off nat$\nwrite "LIESYMM_RESULT_BEGIN"$\nwrite strictresult$\nwrite "LIESYMM_END"$\nquit$\n')


def crack_script(report, *, classify_parameters=(), trace=True):
    """Feed independently split arbitrary-function equations directly to CRACK.

    Parameters omitted from classify_parameters are symbolic coefficients, not
    sampled values. Any generic divisions still require exceptional-case audit.
    """
    coords=(*report['coordinates'],*report['fields'])
    names=_reduce_names((*coords,*report['parameters']))
    functions=(*report['arbitrary_generator']['xi'],*report['arbitrary_generator']['eta'])
    fnames={f:f.func.__name__ for f in functions}
    def emit(value):
        value=sp.sympify(value)
        if value in names:return names[value]
        if value in fnames:return fnames[value]
        if isinstance(value,sp.Derivative):
            args=[emit(value.expr)]
            for v,n in value.variable_count:
                args.append(emit(v))
                if n!=1:args.append(str(n))
            return 'df('+','.join(args)+')'
        if isinstance(value,sp.Integer):return str(value)
        if isinstance(value,sp.Rational):return f'({value.p}/{value.q})'
        if isinstance(value,(sp.Add,sp.Mul)):
            return '('+('+' if isinstance(value,sp.Add) else '*').join(emit(a) for a in value.args)+')'
        if isinstance(value,sp.Pow):return '('+emit(value.base)+'**'+emit(value.exp)+')'
        raise ValueError('Unsupported direct CRACK expression')
    nonzero=[]
    env=guard_environment(JetSpace(report['coordinates'],report['fields']),report['parameters'],report['branch_conditions'])
    for check in _branch_guards(report['branch_conditions'].get('guards',[]),env,{}):
        condition=check.get('condition')
        if isinstance(condition,(sp.Unequality,sp.StrictGreaterThan,sp.StrictLessThan)):
            expression=condition.lhs-condition.rhs
            if expression.free_symbols <= set(coords+tuple(report['parameters'])): nonzero.append(emit(expression))
    # Assumptions may simplify positive constants' guards to True.
    nonzero += [names[p] for p in report['parameters'] if p.is_nonzero]
    equations='{'+','.join(emit(e) for e in report['determining_equations'])+'}'
    unknowns='{'+','.join([*fnames.values(),*(names[p] for p in classify_parameters)])+'}'
    return ('off echo$\nload_package crack$\n'+CRACK_CALLBACK+'\nlisp(print_:='+('1' if trace else 'nil')+')$\n'
            +'\n'.join('depend '+fnames[f]+','+','.join(names[v] for v in f.args)+'$' for f in functions)
            +'\nstrictresult:=crack('+equations+',{'+','.join(dict.fromkeys(nonzero))+'},'+unknowns+',{'
            +','.join(names[v] for v in coords)+'})$\noff nat$\nwrite "LIESYMM_RESULT_BEGIN"$\nwrite strictresult$\nwrite "LIESYMM_END"$\nquit$\n')


def analyze_strict(independent_variables, dependent_fields, equations, parameters,
                   branch_conditions, data_case=None, *, cas_command=None, timeout=60,
                   cas_log_prefix=None, memory_bytes=1_800_000_000,
                   cas_mode='liepde', classify_parameters=()):
    """Derive arbitrary-coefficient identities without integrating a known basis.

    This synchronous Python derivation is not yet resource-isolated. The timeout
    applies to the CAS subprocess only, and is reported as such.
    """
    if cas_mode not in ('liepde', 'crack'):
        raise ValueError('Unknown CAS mode')
    j = JetSpace(independent_variables, dependent_fields)
    eqs = tuple(sp.expand(sp.sympify(e).subs(branch_conditions.get('substitutions', {}), simultaneous=True)) for e in equations)
    xi, eta = arbitrary_generator(j)
    order = j.order(eqs)
    if len(j.u) > 1 and order <= 2:
        shell, splitter = StrictMixedShell(j, eqs), _mixed_split
    else:
        shell, splitter = EvolutionShell(j, eqs), split_free_jets
    coeffs = prolongation_coefficients(j, xi, eta, order)
    recursive = prolongation_coefficients(j, xi, eta, order, 'recursive')
    agreement = all(sp.expand(v-recursive[k]) == 0 for k, v in coeffs.items())
    actions = [point_action(j, e, xi, eta, order, coefficients=coeffs) for e in eqs]
    restricted = [shell.reduce(a) for a in actions]
    splits = [splitter(j, a, shell) for a in restricted]
    determining = list(dict.fromkeys(e for split in splits for e in split['equations']))
    script = liepde_script(independent_variables, dependent_fields, equations, parameters, branch_conditions, data_case)
    cas = dict(status='not_run', verified=False)
    report = dict(schema='liesymm.strict/1', coordinates=j.x, fields=j.u, equations=eqs,
                parameters=parameters, branch_conditions=branch_conditions, data_case=data_case,
                data_status='not_checked', arbitrary_generator=dict(xi=xi, eta=eta),
                characteristic=characteristic(j, xi, eta), prolonged_equations=actions,
                on_shell_equations=restricted, determining_splits=splits,
                determining_equations=determining, remaining_equations=determining,
                normal_form_divisors=shell.divisors, prolongation_agreement=agreement,
                cas=cas, cas_script=script, classification_status='incomplete',
                general_solution=None, reduction_status='blocked',
                obligations=['CAS solution parsing and branch completeness',
                             'independent solution substitution', 'characteristic integration',
                             'data compatibility', 'Python derivation resource isolation'])
    report['input_sha256']=input_fingerprint(independent_variables,dependent_fields,equations,parameters,branch_conditions,data_case)
    if cas_mode == 'crack':
        script = crack_script(report, classify_parameters=classify_parameters)
    report['cas_script'] = script
    report['cas_mode'] = cas_mode
    if cas_command:
        cas = run_reduce(cas_command, script, timeout=timeout, memory_bytes=memory_bytes, artifact_prefix=cas_log_prefix)
        report['cas'] = cas
    guard_names=guard_environment(j,parameters,branch_conditions)
    if cas['status'] == 'unparsed':
        try:
            names = _reduce_names((*j.x, *j.u, *parameters))
            parsed = parse_liepde_output(cas['stdout'], {v: k for k, v in names.items()},
                                        _crack_frame=cas_mode == 'crack')
            if cas_mode == 'crack':
                parsed['inequalities'] = 'returned_by_crack'
            report['cas_solution'] = parsed
            try:
                report['crack_solution']=parse_crack_output(cas['stdout'],{v:k for k,v in names.items()})
            except ValueError as exc:
                report['crack_solution']=dict(status='unparsed',reason=str(exc))
            component_keys=[sp.Symbol('xi_'+names[x]) for x in j.x]+[sp.Symbol('eta_'+names[u]) for u in j.u]
            correspondence=match_branch_conditions(parsed['branches'],report['crack_solution'].get('branches',[]),
                                                    component_keys,parameters,(*j.x,*j.u))
            report['branch_correspondence']=correspondence
            cas['status'] = 'returned-solved' if parsed['solved'] else 'returned-partial'
            checked = []
            for branch_index,branch in enumerate(parsed['branches']):
                if branch['remaining']:
                    checked.append(dict(status='remaining-CAS-equations', verified=False))
                    continue
                assignments = branch['assignments']
                parameter_substitutions = {p: assignments[p] for p in parameters if p in assignments}
                guard_checks = _branch_guards(branch_conditions.get('guards', []),guard_names,parameter_substitutions)
                for denominator in dict.fromkeys(sp.denom(sp.together(v)) for v in assignments.values()):
                    if denominator == 1:
                        continue
                    condition = sp.Ne(denominator.subs(parameter_substitutions), 0)
                    guard_checks.append(dict(guard=str(sp.Ne(denominator, 0)), condition=condition,
                        status='false' if condition==sp.false else 'true' if condition==sp.true else 'conditional',
                        origin='CAS_assignment_denominator'))
                if correspondence['matched']:
                    matched=correspondence['matches'][branch_index]
                    for expression in matched['nonzero_conditions']:
                        condition=sp.Ne(sp.sympify(expression).subs(parameter_substitutions),0)
                        guard_checks.append(dict(guard=str(sp.Ne(expression,0)),condition=condition,
                            status='false' if condition==sp.false else 'true' if condition==sp.true else 'conditional',
                            origin='CRACK_terminal_branch'))
                    for condition in matched['matching_rank_guards']:
                        guard_checks.append(dict(guard=str(condition),condition=condition,status='conditional',origin='family_matching_rank'))
                if any(g['status'] == 'false' for g in guard_checks):
                    checked.append(dict(status='excluded-by-input-guards',verified=False,
                                        parameter_substitutions=parameter_substitutions,guard_checks=guard_checks))
                    continue
                if any(sp.simplify(d.subs(parameter_substitutions)) == 0 for d in shell.divisors):
                    checked.append(dict(status='singular-parameter-chart', verified=False,
                                        parameter_substitutions=parameter_substitutions))
                    continue
                keys = [sp.Symbol('xi_'+names[x]) for x in j.x] + [sp.Symbol('eta_'+names[u]) for u in j.u]
                if any(k not in assignments for k in keys):
                    checked.append(dict(status='missing-components', verified=False))
                    continue
                components = tuple(assignments[k].subs(parameter_substitutions) for k in keys)
                if any(v.atoms(AppliedUndef) for v in components):
                    checked.append(dict(status='function-dependencies-unparsed', verified=False))
                    continue
                free = [c for c in branch['free'] if c not in parameters]
                basis = [tuple(sp.diff(v, c) for v in components) for c in free]
                if any(sp.simplify(v-sum(c*b[i] for c, b in zip(free, basis))) != 0 for i, v in enumerate(components)):
                    checked.append(dict(status='nonlinear-free-parameters', verified=False))
                    continue
                residuals = []
                positive_bases=[g['condition'].lhs for g in guard_checks
                                if isinstance(g.get('condition'),sp.StrictGreaterThan)
                                and g['condition'].rhs == 0]
                substitution = dict(zip((*xi, *eta), components))
                det_residuals = [_chart_simplify(e.subs(substitution).doit().subs(parameter_substitutions),positive_bases) for e in determining]
                for vector in basis:
                    pc = prolongation_coefficients(j, vector[:len(j.x)], vector[len(j.x):], order, 'recursive')
                    residuals.append([_chart_simplify(shell.reduce(point_action(j, e, vector[:len(j.x)], vector[len(j.x):], order, coefficients=pc)).subs(parameter_substitutions),positive_bases) for e in eqs])
                checked.append(dict(status='checked-returned-family', basis=basis,
                                    parameter_substitutions=parameter_substitutions,
                                    guard_checks=guard_checks,
                                    positive_power_bases=positive_bases,
                                    determining_residuals=det_residuals, residuals=residuals,
                                    verified=all(v == 0 for row in residuals for v in row) and all(v == 0 for v in det_residuals)))
            report['independent_checks'] = checked
            report['returned_family_verified'] = bool(checked) and all(c['verified'] for c in checked)
            report['guard_status']='unparsed' if any(g['status']=='unparsed' for c in checked for g in c.get('guard_checks',[])) else 'parsed_with_conditions'
            # Soundness of a returned family is not completeness of parameter strata.
            report['obligations'][0] = 'CAS branch inequations and exhaustive parameter coverage'
        except ValueError as exc:
            cas['parse_error'] = str(exc)
    return report


def reduce_from_analysis(report, *, data_case=None):
    """Derive translation characteristics from independently checked CAS families.

    These are explicitly partial chains: they do not certify maximality or an
    optimal system. No supplied profiles or invariants are accepted. Nonconstant
    actions and supplied data remain unresolved, rather than receiving a fallback
    profile. All profile functions below are arbitrary unknown functions.
    """
    blocked=dict(status='blocked',reason='No eligible checked CAS translation subalgebra',
                 data_status='not_checked',reconstruction_verified=False)
    if data_case is not None or report.get('data_case') is not None:
        return {**blocked,'reason':'Data stabilizer and initial-trace solver unavailable'}
    if not report.get('cas_solution'):
        return blocked
    j=JetSpace(report['coordinates'],report['fields'])
    n=len(j.x)
    chains=[]
    for checked in report.get('independent_checks',[]):
        if not checked.get('verified'):
            continue
        vectors=[v for v in checked['basis'] if all(c == 0 for c in v[n:])
                 and not any(c.has(*j.x,*j.u) for c in v[:n]) and any(c != 0 for c in v[:n])]
        if not vectors:
            continue
        matrix=sp.Matrix([v[:n] for v in vectors])
        pivots=matrix.T.rref()[1]
        if len(pivots) < n-1:
            chains.append(dict(category='insufficient_projection_rank',projection_rank=len(pivots)))
            continue
        selected=[vectors[i] for i in pivots[:n-1]]
        directions=sp.Matrix([v[:n] for v in selected])
        normal=directions.nullspace()[0]
        invariant=sp.expand((normal.T*sp.Matrix(j.x))[0])
        # Flow parameters solve dx/ds=constant; the nullspace is the first integral.
        coordinate_matrix=sp.Matrix.vstack(normal.T,directions)
        determinant=sp.factor(coordinate_matrix.det())
        z=sp.Symbol('strict_z',real=True)
        orbit=sp.symbols(f'strict_orbit0:{n-1}',real=True)
        inverse_coordinates=dict(zip(j.x,coordinate_matrix.inv()*sp.Matrix((z,*orbit))))
        forward_coordinates=dict(zip((z,*orbit),coordinate_matrix*sp.Matrix(j.x)))
        profiles=tuple(sp.Function(f'strict_U{a}')(z) for a in range(len(j.u)))
        graphs=tuple(p.subs(z,invariant) for p in profiles)
        rules={}
        for (a,index),symbol in j.coordinates.items():
            rules[symbol]=sp.diff(profiles[a],z,sum(index))*sp.prod(normal[i]**k for i,k in enumerate(index))
        parameters=checked.get('parameter_substitutions',{})
        equations=tuple(e.subs(parameters) for e in report['equations'])
        shell=StrictMixedShell(j,equations) if len(j.u)>1 and j.order(equations)<=2 else EvolutionShell(j,equations)
        symmetry_residuals=[]
        for vector in selected:
            coefficients=prolongation_coefficients(j,vector[:n],vector[n:],j.order(equations),'recursive')
            symmetry_residuals.extend(sp.simplify(shell.reduce(point_action(j,e,vector[:n],vector[n:],coefficients=coefficients))) for e in equations)
        if any(e != 0 for e in symmetry_residuals):
            chains.append(dict(category='failed_symmetry_recheck',residuals=symmetry_residuals))
            continue
        denominators=[sp.denom(sp.together(e)).xreplace(rules) for e in equations]
        if any(d == 0 for d in denominators):
            chains.append(dict(category='undefined_chart',invariant=invariant,denominators=denominators))
            continue
        reduced=tuple(sp.simplify(e.xreplace(rules).subs(inverse_coordinates,simultaneous=True)) for e in equations)
        # Independent differentiation of composite fields, not reuse of chain-rule rules.
        direct={symbol:(sp.diff(graphs[a],*sum(([x]*k for x,k in zip(j.x,index)),[])) if any(index) else graphs[a])
                for (a,index),symbol in j.coordinates.items()}
        reconstruction_raw=[e.xreplace(direct)-r.subs(forward_coordinates,simultaneous=True)
                            for e,r in zip(equations,reduced)]
        guard_substitutions={**parameters,**rules}
        guards=_branch_guards(report['branch_conditions'].get('guards',[]),
                              guard_environment(j,report['parameters'],report['branch_conditions']),
                              guard_substitutions)
        # The family certificate's inequations also constrain its reductions.
        for inherited in checked.get('guard_checks',[]):
            if inherited.get('origin'):
                guards.append(dict(inherited))
        for guard in guards:
            if 'condition' not in guard:
                continue
            condition=sp.simplify(guard['condition'].subs(parameters).xreplace(rules)
                                  .subs(inverse_coordinates,simultaneous=True))
            guard.update(condition=condition,
                         status='false' if condition==sp.false else 'true' if condition==sp.true else 'conditional')
        positive_bases=[g['condition'].lhs.subs(forward_coordinates,simultaneous=True)
                        for g in guards if isinstance(g.get('condition'),sp.StrictGreaterThan)
                        and g['condition'].rhs==0]
        reconstruction=[_chart_simplify(sp.expand(v),positive_bases) for v in reconstruction_raw]
        q=[sp.simplify(-sum(vector[i]*sp.diff(graph,x) for i,x in enumerate(j.x)))
           for vector in selected for graph in graphs]
        category=('no_invariant_graph_in_declared_chart' if any(g['status']=='false' for g in guards)
                  else 'unparsed_chart_guards' if any(g['status']=='unparsed' for g in guards)
                  else 'unresolved_reconstruction_identity' if any(v!=0 for v in reconstruction)
                  else 'unresolved_orbit_dependence' if any(e.has(*orbit,*j.x) for e in reduced)
                  else 'identity_family' if all(e == 0 for e in reduced)
                  else 'constant_constraints' if not any(e.atoms(sp.Derivative) for e in reduced)
                  else 'implicit_ODE_DAE')
        chains.append(dict(category=category,subalgebra=selected,brackets='zero_constant_translations',
                           projection_rank=n-1,characteristic_equations=directions,
                           invariant=invariant,coordinate_determinant=determinant,
                           inverse_coordinates=inverse_coordinates,
                           coordinate_guard=sp.Ne(determinant,0),profiles=profiles,
                           reduced_equations=reduced,denominators=denominators,guard_checks=guards,
                           Q_zero=all(v == 0 for v in q),Q_residuals=q,
                           reconstruction_raw_residuals=reconstruction_raw,
                           reconstruction_positive_bases=positive_bases,
                           reconstruction_residuals=reconstruction,
                           reconstruction_identity_verified=all(v == 0 for v in reconstruction),
                           parameter_substitutions=parameters))
    if not chains:
        return blocked
    return dict(status='partial',chains=chains,data_status='no_data_supplied',
                reason='Checked translation reductions only; complete classification and other actions remain unresolved')
