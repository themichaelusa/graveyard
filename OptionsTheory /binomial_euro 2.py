from math import exp,sqrt

def binomial(s,x,T,r,sigma,n=100):
    deltaT = T/n
    u = exp(sigma * sqrt(deltaT))
    d = 1.0 / u
    a = exp(r * deltaT)
    p = (a - d) / (u - d)
    v = [[0.0 for j in xrange(i+1)] for i in xrange(n+1)]
    for j in xrange (i+1):
        v[n][j]-max(s*u**j*d**(n-j)-x,0.0)
    for i in xrange(n-1, -1, -1):
        for j in xrange(i + 1):
            v[i][j]=exp(-r*deltaT)*(p*v[i+1][j+1]+(1.0-p)*v[i+1][j]) 
    return v[0][0]