## Author: Matt Hancock
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('ggplot')

n_dim = 10
n_samples = 150
variance = 0.5**2

rs = np.random.RandomState(1234)
true_w = rs.randn(n_dim); true_w /= np.linalg.norm(true_w)
true_t = rs.rand()*5
true_Q = np.c_[true_w, np.zeros((n_dim,n_dim-1))]
true_Q,R = np.linalg.qr(true_Q)
true_Q = -true_Q if R[0,0] < 0 else true_Q
true_D = np.diag(np.r_[variance,np.ones(n_dim-1)])
true_S = np.dot(true_Q,np.dot(true_D,true_Q.T))

X = rs.multivariate_normal(true_t*true_w, true_S, size=n_samples)
true_Y = np.dot(X,true_w) - true_t > 0
dist = np.dot(X,true_w)-true_t
vals,bins = np.histogram(dist,20,density=True)

Y = true_Y.copy()
for i in range(n_samples):
    j = np.searchsorted(bins,dist[i])
    if rs.rand() < (bins[j]-bins[j-1])*vals[j-1]:
        Y[i] = not Y[i]


from sklearn.svm import LinearSVC
svc = LinearSVC()
svc.fit(X,Y)
estm_w = svc.coef_[0].copy()
estm_t = -svc.intercept_[0] / np.linalg.norm(estm_w)
estm_w /= np.linalg.norm(estm_w)

Z = X - estm_t*estm_w
estm_Q = np.c_[estm_w, np.zeros((n_dim,n_dim-1))]
estm_Q,R = np.linalg.qr(estm_Q)
estm_Q = -estm_Q if R[0,0] < 0 else estm_Q

u,s,vt = np.linalg.svd( np.dot(Z,np.dot(estm_Q,estm_Q.T)), full_matrices=False )
P1 = np.c_[np.dot(Z,estm_w), np.dot(Z,vt[0])]

u,s,vt = np.linalg.svd(X - X.mean(axis=0), full_matrices=False)
P2 = np.dot(X-X.mean(axis=0), vt[:2].T)

import matplotlib.pyplot as plt
fig = plt.figure(figsize=(10,5))
ax = fig.add_subplot(121)
ax.plot(P1[ Y,0], P1[ Y,1], 's', ms=6)
ax.plot(P1[~Y,0], P1[~Y,1], 'o', ms=6)
ax.axis('equal')
ax.set_title('Boundary-preserving PCA')

ax = fig.add_subplot(122)
ax.plot(P2[ Y,0], P2[ Y,1], 's', ms=6)
ax.plot(P2[~Y,0], P2[~Y,1], 'o', ms=6)
ax.axis('equal')
ax.set_title('Standard PCA')

plt.tight_layout()
plt.show()
