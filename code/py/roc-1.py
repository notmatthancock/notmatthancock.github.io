import numpy as np
import matplotlib.pyplot as plt
from scipy.special import beta, betainc

Beta = lambda a,b,x: x**(a-1) * (1-x)**(b-1) / beta(a,b)

t = np.linspace(0,1,101)

fig = plt.figure(figsize=(4,4))
plt.plot( 1-betainc(2,6,t), 1-betainc(3,5,t), lw=2 )
plt.xlim(-0.1,1.1)
plt.ylim(-0.1,1.1)
plt.xlabel('$P(T > t | Y=0)$', fontsize=16)
plt.ylabel('$P(T > t | Y=1)$', fontsize=16)
plt.grid()
plt.savefig('../../images/roc-1.png', bbox_inches='tight')
