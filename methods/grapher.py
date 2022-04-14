import numpy as np
from sympy import symbols,lambdify
from sympy.solvers import solve
def grapher(func,xr):
    x=symbols('x')
    xs=np.linspace(-50,50,10000000)
    y=lambdify(x, func, modules=['numpy'])
    ys = y(xs)
    yr=y(xr)
    exact=solve(func,x)
    return xs,ys,exact,yr

