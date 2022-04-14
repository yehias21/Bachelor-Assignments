from sympy import *
import math
class BracketingMethod:

    def __init__(self, fun='', upbound=-1, lowbound=1,x='x', maxIter=50, eps=1e-5):
        self.fun = sympify(fun)
        self.upbound = upbound
        self.lowbound = lowbound
        if(self.lowbound>self.upbound):
            self.upbound,self.lowbound=self.lowbound,self.upbound
        self.x = var(x)
        self.maxIter = maxIter
        self.eps = eps
        self.epsf=1e-5
    def f(self,Xo):
        return self.fun.subs(self.x,Xo)
    def isvalid(self):
        try:
            fup = self.f(self.upbound)
            flow = self.f(self.lowbound)
            if int(fup) * int(flow)>0:
                print('Roots boundry not valid! 404 root not found')
                return true
            else:
                 return false
        except:
            return false

    def iterNum(self):
        return math.ceil(math.log2(abs(self.upbound - self.lowbound))- math.log2(self.eps))
    def isroot(self,fx):
        if -self.epsf<fx<self.epsf:
            return true
        return false
    def bisection(self):
        try:
            # create the table
            iterNum=self.iterNum()
            table,row = [['i','Xu', 'Xl', 'Xr', 'F(Xr)', 'relative_error']],[]
            if self.isvalid():
                return table, 0.0, false
            elif self.isroot(self.f(self.upbound)) :
                return table, self.upbound, true
            elif self.isroot(self.f(self.lowbound)):
                return table, self.lowbound, true
            xrOld,xr = self.upbound,0
            for iter in range(1,min(iterNum+1,self.maxIter+1)):
                xr = (self.upbound + self.lowbound)/2
                fxr = self.f(xr)
                error=abs(xr-xrOld)/xr*100
                row = [iter,str(self.upbound), str(self.lowbound), str(xr), str(fxr), str(abs(error))]
                table.append(row)
                if fxr * self.f(self.upbound) < 0:
                    self.lowbound = xr
                elif fxr * self.f(self.lowbound) < 0:
                    self.upbound = xr
                elif self.isroot(fxr) :
                    table[1][-1] = ''
                    return table, xr, true
                else:
                    print('Two root existed or function is not continous!')
                    return [], 0.0, false
                xrOld=xr
            table[1][-1]=''
            return table, xr, true
        except:
            print('Error while computing bisection!')
            return [], 0.0, false

    def regulaFalsi(self):
        try:
            # create the table
            table,row = [['i,''Xu', 'Xl', 'Xr', 'F(Xr)', 'relative_error']],[]
            if self.isvalid():
                return table, 0.0, false
            elif self.isroot(self.f(self.upbound)) :
                return table, self.upbound, true
            elif self.isroot(self.f(self.lowbound)):
                return table, self.lowbound, true
            xrOld,xr = self.upbound,0
            for iter in range(1,self.maxIter+1):
                xr = float(self.upbound-self.f(self.upbound)*(self.lowbound -self.upbound)/(self.f(self.lowbound)-self.f(self.upbound)))
                fxr = self.f(xr)
                error=abs(xr-xrOld)/xr*100
                row = [iter,self.upbound, self.lowbound, xr, fxr,round(abs(error),2)]
                table.append(row)
                if (self.upbound - self.lowbound)<self.eps or abs(fxr)<self.eps:
                    return table, xr, true
                if fxr * self.f(self.upbound) < 0:
                    self.lowbound = xr
                elif fxr * self.f(self.lowbound) < 0:
                    self.upbound = xr
                elif self.isroot(fxr) :
                    table[1][-1] = None
                    return table, xr, true
                else:
                    print('Two root existed or function is not continous!')
                    return [], 0.0, false
                xrOld=xr
            table[1][-1]=None
            return table, xr, true
        except:
            print('Error while computing bisection!')
            return [], 0.0, false