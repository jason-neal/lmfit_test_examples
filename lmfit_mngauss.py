#!/usr/bin/python
## Implementation of a function to fit n gaussians (Normalized absorption lines - 1 (to put continuum at 0))
## using lmfit (https://lmfit.github.io/lmfit-py/)

##imports:

from lmfit.models import GaussianModel, ConstantModel

## My functions:

def lmfit_mngauss(x,y, *params):
    """
    Fit multiple gaussians from two spectra that are multiplied together

    INPUT:
    x - is the wavelength array
    y - is the normalized flux
    params - is a tuple of 2 list/arrays of initial guess values for the each spectras parameters
             (this controls the number of gaussians to be fitted
                 number of gaussians: len(params)/3 - 3 parameters per Gaussian)
    OUTPUT:
    mod - the lmfit model object used for the fit
    out - the lmfit fit object that contains all the results of the fit
    init- array with the initial guess model (usefull to see the initial guess when plotting)
    """
    
    m_params = params[0]
    
    m_mods = []
    prefixes = []
    for i in range(0, len(m_params), 3):
        pref = "gm%02i_" % (i/3)
        gauss_i = GaussianModel(prefix=pref)

        if i == 0:
            pars = gauss_i.guess(y, x=x)
        else:
            pars.update(gauss_i.make_params())
    
        A = m_params[i]
        l_cen = m_params[i+1]
        sigma = m_params[i+2]

        pars[pref+'amplitude'].set(A)
        pars[pref+'center'].set(l_cen)
        pars[pref+'sigma'].set(sigma)

        m_mods.append(gauss_i)
        prefixes.append(pref)
    
    m_mod = m_mods[0]
    if len(m_mods) > 1:
      for m in m_mods[1:]:
            m_mod += m

    m_one = ConstantModel(prefix="m_one_")
    prefixes.append("m_one_")
    pars.update(m_one.make_params())
    pars['m_one_c'].set(value=1, vary=False)

    try: 
        n_params = params[1]
        n_mods = []
        #prefixes = []
        for j in range(0, len(n_params), 3):
            pref = "gn%02i_" % (j/3)
            gauss_j = GaussianModel(prefix=pref)
            pars.update(gauss_j.make_params())
        
            A = n_params[j]
            l_cen = n_params[j+1]
            sigma = n_params[j+2]

            pars[pref+'amplitude'].set(A)
            pars[pref+'center'].set(l_cen)
            pars[pref+'sigma'].set(sigma)

            n_mods.append(gauss_j)
            prefixes.append(pref)
        
        n_mod = n_mods[0]
        if len(n_mods) > 1:
            for n in n_mods[1:]:
                n_mod += n
        
        n_one = ConstantModel(prefix="n_one_")
        prefixes.append("n_one_")
        pars.update(n_one.make_params())
        pars['n_one_c'].set(value=1, vary=False)

        mod = (m_one + m_mod) * (n_one + n_mod)
    except:
    	print("Error with second spectra, only fitting first")
        mod = m_one + m_mod
    
    

    init = mod.eval(pars, x=x)
    out = mod.fit(y, pars, x=x)
    
    print("Printed prefixes", prefixes)
    #print(init)
    return mod, out, init



### Main program:
def main():
    print "Hello"
  

if __name__ == "__main__":
    main()
