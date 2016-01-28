#!/usr/bin/env python
#<examples/doc_nistgauss.py>
import numpy as np
from lmfit.models import GaussianModel
import sys
import matplotlib.pyplot as plt
from numpy import sqrt, pi, exp, linspace, loadtxt
from astropy.io import fits

from lmfit_mngauss import lmfit_mngauss


def gaussian(x, amp, cen, wid):
  "1-d gaussian: gaussian(x, amp, cen, wid)"
  return (amp/(sqrt(2*pi)*wid)) * exp(-(x-cen)**2 /(2*wid**2))


def test_4synthlines_with_mngaussians():

  x = np.linspace(5800, 5803, num=1000)
  y = (gaussian(x, -0.8, 5801.1, 0.2) + gaussian(x, -0.6, 5802.1, 0.2)) * \
      (gaussian(x, -0.3, 5801.7, 0.2) + gaussian(x, -0.2, 5802.8, 0.2)) + \
      np.random.normal(0, 0.01, x.shape[0])
  
  #params = [-0.9, 5801, 0.1, -0.4, 5802, 0.1,-0.4, 5801.5, 0.1, -0.1, 5803, 0.1]
  m_params = [-0.9, 5801.05, 0.1, -0.7, 5802, 0.1]
  n_params = [-0.4, 5801.6, 0.1, -0.1, 5803, 0.1]

  mod, out, init = lmfit_mngauss(x,y, m_params, n_params)
  #mod, out, init = lmfit_mngauss(x,y, m_params)
  plt.plot(x, y)
  plt.plot(x, init, 'k--')

  print(out.fit_report(min_correl=0.5))

  plt.plot(x, out.best_fit, 'r-', label="best fit")
  plt.legend()
  plt.show()



def test_4synthlines_with_mngaussians_atone():

  x = np.linspace(5800, 5803, num=1000)
  y1 = (gaussian(x, -0.8, 5801.1, 0.2) + gaussian(x, -0.4, 5802.1, 0.2)) + \
      np.random.normal(0, 0.02, x.shape[0]) + 1.0
  y2 = (gaussian(x, -0.3, 5801.7, 0.2) + gaussian(x, -0.2, 5802.8, 0.2)) + \
      np.random.normal(0, 0.01, x.shape[0]) + 1.0

  y = y1 * y2

  m_params = [-0.6, 5801, 0.1, -0.3, 5802.3, 0.1]
  n_params = [-0.4, 5801.4, 0.1, -0.2, 5802.8, 0.1]

  mod, out, init = lmfit_mngauss(x, y, m_params, n_params)
  #mod, out, init = lmfit_mngauss(x,y, m_params)
  plt.plot(x, y, label="y")
  plt.plot(x, init, 'k--', label="init fit")

  print(out.fit_report(min_correl=0.5))
  
  plt.plot(x, out.best_fit, 'r-', label="best fit")
  ax = plt.gca()
  ax.get_xaxis().get_major_formatter().set_useOffset(False)
  plt.legend(loc=0)
  plt.show()



test_4synthlines_with_mngaussians_atone()

#test_4synthlines_with_mngaussians()