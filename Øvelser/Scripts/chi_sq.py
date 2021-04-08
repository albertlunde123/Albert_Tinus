from scipy.stats import chi2

def chi_sq(t, x, err, f, popt, df):
    chi_sq = sum((x - f(t, *popt))**2/err**2)
    p_value = 1 - chi2.cdf(chi_sq, df)
    print(popt)
    return chi_sq, p_value

def p_value(chi_sq, df):
    return round(1 - chi2.cdf(chi_sq, df), 3)

def other_chi(E, O):
    return sum((O-E)**2/E)

