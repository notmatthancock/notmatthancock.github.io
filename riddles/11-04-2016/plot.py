import numpy as np
from scipy.special import binom
import matplotlib.pyplot as plt

ptrue = lambda n: binom(n, n/2) / 2.0**n
pasym = lambda n: np.sqrt(2/(np.pi*n))

N = np.arange(2, 1025, 2)

plt.plot(N, ptrue(N), '-' , lw=3, label='$P\\left(\sum_i X_i = N/2\\right)$')
plt.plot(N, pasym(N), '--', lw=3, label='$\sqrt{2 / (\pi N)}$')

plt.xlabel('Population size ($N$)')
plt.ylabel('P(your vote determines election)')

plt.gca().set_axis_bgcolor('w')
plt.xscale('log', basex=2); plt.yscale('log', basey=2)
plt.grid('on', c='k', lw=0.5, ls=':'); plt.legend()

#plt.savefig('plot.svg', bbox_inches='tight')
