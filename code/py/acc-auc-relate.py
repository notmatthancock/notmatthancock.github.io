import numpy as np
import matplotlib; matplotlib.use('cairo')
import matplotlib.pyplot as plt

f = lambda p,auc: p*(1-p)*(2*auc-1)+0.5
p = np.linspace(0,1,101)
aucs = np.linspace(0.5,1,5)

fig = plt.figure(figsize=(6,6))

for auc in aucs:
    plt.plot(p, f(p,auc), lw=2, label="AUC=%.3f"%auc)

plt.ylim(0.4,1)
plt.xlabel('p')
plt.ylabel('expected accuracy')
plt.grid()
plt.legend()
#plt.savefig('../../images/acc-auc-relate.png', bbox_inches='tight')
