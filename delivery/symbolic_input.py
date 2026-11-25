"""Restricted expression transport; no solver or verifier logic."""
import ast
import sympy as sp


class Expressions:
    """Small expression language; no eval, attributes, arbitrary calls or imports."""
    def __init__(self, symbols=(), functions=(), positive=()):
        self.names={n:sp.Symbol(n,positive=True) if n in positive else sp.Symbol(n,real=True) for n in symbols}
        self.functions={n:sp.Function(n) for n in functions}
        self.calls={'D':sp.diff,'Derivative':sp.Derivative,'Subs':sp.Subs,'exp':sp.exp,
                    'log':sp.log,'sqrt':sp.sqrt,'tanh':sp.tanh,'sin':sp.sin,'cos':sp.cos,'sinh':sp.sinh,'cosh':sp.cosh,'atan':sp.atan,'asin':sp.asin,'acos':sp.acos,'erf':sp.erf,'Abs':sp.Abs}
    def read(self, text):
        def walk(node):
            if isinstance(node,ast.Constant) and type(node.value) in (int,float):return sp.Rational(str(node.value))
            if isinstance(node,ast.Name) and node.id in self.names:return self.names[node.id]
            if isinstance(node,ast.Tuple):return tuple(walk(v) for v in node.elts)
            if isinstance(node,ast.UnaryOp) and isinstance(node.op,(ast.USub,ast.UAdd)):
                v=walk(node.operand);return -v if isinstance(node.op,ast.USub) else v
            if isinstance(node,ast.BinOp):
                a,b=walk(node.left),walk(node.right)
                if isinstance(node.op,ast.Add):return a+b
                if isinstance(node.op,ast.Sub):return a-b
                if isinstance(node.op,ast.Mult):return a*b
                if isinstance(node.op,ast.Div):return a/b
                if isinstance(node.op,ast.Pow):return a**b
            if isinstance(node,ast.Call) and isinstance(node.func,ast.Name) and not node.keywords:
                fn=self.calls.get(node.func.id,self.functions.get(node.func.id))
                if fn is not None:return fn(*(walk(v) for v in node.args))
            raise ValueError('unsupported expression syntax: '+ast.dump(node))
        return walk(ast.parse(str(text),mode='eval').body)
