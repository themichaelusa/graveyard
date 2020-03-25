import math
import random
import pylab
from random import gauss
from math 
​import exp, sqrt
import matplotlib
import matplotlib.pyplot as plt
from numpy import *
import numpy as np

def american(n, T, sigma, s_nil, K):
   dt = T*252
   u = random.randn(dt)* sigma/sqrt(dt)
   z = cumprod(1+random.randn(n,dt)*(sigma/sqrt(dt), 1))*s_nil
   payoffs = (z[:,-1] - 100) * ((z[:,-1] - 100) > 0)
   price = mean(payoffs)
   print(payoffs, price)
