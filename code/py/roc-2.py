import numpy as np
import matplotlib.pyplot as plt
from scipy.special import beta, betainc

Beta = lambda a,b,x: x**(a-1) * (1-x)**(b-1) / beta(a,b)

t = np.linspace(0,1,101)

fig = plt.figure(figsize=(10,5))
ax = fig.add_subplot(1,2,1)
for k in [5,4,3,2]:
    ax.plot( 1-betainc(2,6,t), 1-betainc(8-k,k,t), lw=2)
ax.set_xlim(-0.1,1.1)
ax.set_ylim(-0.1,1.1)
ax.set_xlabel('$P(T > t | Y=0)$', fontsize=16)
ax.set_ylabel('$P(T > t | Y=1)$', fontsize=16)
ax.grid()
ax.set_title('ROC curves')

ax = fig.add_subplot(1,2,2)
ax.plot( t, Beta(2,6,t), '--k', lw=2, label='$T|Y=0$')
for k in [5,4,3,2]:
    ax.plot(t, Beta(8-k,k,t), lw=2, label='$T|Y=1$')
ax.set_ylim(0,4)
ax.grid()
ax.set_title('Conditional classifier PDFs')


#plt.savefig('../../images/roc-2.png', bbox_inches='tight')
plt.show()
