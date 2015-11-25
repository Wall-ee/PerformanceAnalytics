import scipy.stats
from pandas import DataFrame as df
import pandas as pd
import numpy as np




def setalphaprob(p):
    if (p >= 0.51):
        alpha = 1 - p
    else:
        alpha = p
    return alpha


def pvalJB(R):
   # m2 = scipy.stats.moment(R,moment=2)
   # m3 = scipy.stats.moment(R,moment=3)
   # m4 = scipy.stats.moment(R,moment=4)
   r=R.dropna()
   skew = scipy.stats.skew(r)
   exkur = scipy.stats.kurtosis(r)
   JB = (len(r) /6 )*( skew^2 + (1/4)*(exkur^2) )
   out = 1-scipy.stats.chi2.cdf(JB,2)

def VaRGaussian(R,p):
    alpha=setalphaprob(p)
    r=R.dropna()
    VaR = -np.mean(r) - scipy.stats.norm.ppf(alpha) * np.std(r)
    return VaR
def ESGaussian(R,p):
    alpha=setalphaprob(p)
    r=R.dropna()
    GES= - np.mean(r) + scipy.stats.norm.pdf(scipy.stats.norm.ppf(alpha)) * np.std(r) / alpha
    return GES

def VaRCornishFisher(R,p):
    alpha=setalphaprob(p)
    z = scipy.stats.norm.ppf(alpha)

    r = R.dropna()
    skew=scipy.stats.skew(r)
    exkurt=scipy.stats.kurtosis(r)

    h = z + (1/6)*(z*z -1)*skew + (1/24)*(z**3 - 3*z)*exkurt - (1/36)*(2*(z**3) - 5*z)*skew*skew

    VaR = - np.mean(r) - h * np.std(r)

    return VaR

def ESCornishFiser(R,p,c=2):
    r=R.dropna()
    alpha = setalphaprob(p)
    p = alpha
    z = scipy.stats.norm.ppf(p)
    skew = scipy.stats.skew(r, axis=0)
    exkurt = scipy.stats.kurtosis(r, axis=0)
    h = z + (1 / 6.0) * (z * z - 1) * skew
    if (c == 2):
        h = h + (1 / 24.0) * (z * z * z - 3 * z) * exkurt - (1 / 36.0) * (2 * z * z * z - 5 * z) * skew * skew
    MES = scipy.stats.norm.pdf(h)
    MES = MES + (1 / 24) * (Ipower(4, h) - 6 * Ipower(2, h) + 3 * scipy.stats.norm.pdf(h)) * exkurt
    MES = MES + (1/6) * (Ipower(3, h) - 3 * Ipower(1, h)) * skew
    MES = MES + (1/72) * (Ipower(6, h) - 15 * Ipower(4, h) + 45 * Ipower(2, h) - 15 * scipy.stats.norm.pdf(h)) * (skew * skew)
    MES = -np.mean(r, axis=0) - np.std(r, axis=0) * min(-MES / alpha, h)

    return MES


def Ipower(power, h):
    fullprod = 1
    if ((power % 2) == 0):
        pstar = power / 2.0
        for j in range(1, int(pstar)+1):
            fullprod = fullprod * (2 * j)
        I = fullprod * scipy.stats.norm.pdf(h)
        for i in range(1, int(pstar)+1):
            prod = 1
            for j in range(1, i+1):
                prod = prod * (2 * j)
            I = I + (fullprod / prod) * (h ** (2 * i)) * scipy.stats.norm.pdf(h)
    else:
        pstar = (power - 1) / 2
        for j in range(0, int(pstar)+1):
            fullprod = fullprod * ((2 * j) + 1)
        I = -fullprod * scipy.stats.norm.cdf(h)
        for i in range(0, int(pstar)+1):
            prod = 1
            for j in range(0, i+1):
                prod = prod * ((2 * j) + 1)
            I = I + (fullprod / prod) * (h ** ((2 * i) + 1)) * scipy.stats.norm.pdf(h)
    return I







