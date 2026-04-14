from sympy import *
class openMethod:

    def __init__(self, fun='', initguess=0,x='x', maxIter=50, eps=1e-5):
        self.fun = sympify(fun)
        self.initguess = initguess
        self.x = var(x)
        self.maxIter = maxIter
        self.eps = eps
        self.epsf=1e-5

    def f(self,Xo,fun=None):
        if not fun:
            fun=self.fun
        return fun.subs(self.x,Xo)

    def isroot(self,fx):
        if -self.epsf<fx<self.epsf:
            return true
        return false
    def fixedPoint(self,gx):
        try:
            # create the table
            gx = sympify(gx)
            table,row = [['i', 'Xi', 'relative_error']],[]
            iter,xr = 0,0
            # if the initial guess is the root
            if self.isroot(self.f(self.initguess)):
                return [table], self.initguess, true
            if self.f(self.initguess,fun=diff(gx))>1:
                print('f(x) will not converge')
                return table, 0.0, false
            x0=self.initguess
            while iter<self.maxIter:
                iter+=1
                xr = float(self.f(x0,fun=gx))
                error=abs(xr-x0)
                row=[iter,xr,error]
                table.append(row)
                if error<self.eps :
                    break
                x0=xr
            return table,xr,true
        except:
            return [],0.0,false

    def newtonian(self):
        try:
            x0=self.initguess
            table, row = [['i', 'Xi', 'relative_error']], []
            iter,x1= 0,0
            while iter < self.maxIter:
                # x(i+1) = x(i) - f(x) / f'(x)
                iter += 1
                h = float(self.f(x0) / self.f((x0), fun=diff(self.fun)))
                x1=x0-h
                error=abs(x1-x0)
                row=[iter,x1,error]
                table.append(row)
                if error< self.eps or self.isroot(self.f(x1)):break
                x0=x1
            return table, x1, true
        except:
            return [], 0.0, false


    def secant(self,x0,x1):
        try:
            table, row = [['i', 'Xi-1','Xi','Xi+1','f(Xi+1)', 'relative_error']], []
            iter,x2=0,0
            while iter < self.maxIter:
                iter += 1
                x2 = x1 - (x1 - x0) * float(self.f(x1))/float((self.f(x1)-self.f(x0)))
                error = abs(x2 - x1)
                row = [iter, x0,x1,x2,str(self.f(x2)), error]
                table.append(row)
                if error< self.eps: break
                x0 = x1
                x1=x2
            return table, x2, true
        except:
            return [], 0.0, false
