import numpy as np

rs = np.random.RandomState(1234)
p = 0.6 
mean1 = np.r_[1,1.]
mean0 = -mean1

Y = (rs.rand(200) > p).astype(int)
X = np.zeros((200,2))
X[Y==0] = rs.multivariate_normal(mean0, np.eye(2), size=(Y==0).sum())
X[Y==1] = rs.multivariate_normal(mean1, np.eye(2), size=(Y==1).sum())

import matplotlib.pyplot as plt 
plt.plot(X[Y==0,0], X[Y==0,1], 'ob', label='Class 0')
plt.plot(X[Y==1,0], X[Y==1,1], 'sr', label='Class 1')
plt.legend(loc=2, numpoints=1)

#plt.show()

def gradient_ascent(w, b, lamb, eta, n_iters):
    for iter in range(n_iters):
        #G is P(Y=1|X) under the current parameters.
        G = 1 / (1. + np.exp(-b-np.dot(X,w)))
        # loss is the function we're maximizing
        loss = -lamb * np.log(w**2).sum() + np.log(G[Y==1]).sum() + np.log(1-G[Y==0]).sum()

        print "iteration:", iter, "| loss:", loss, "| accuracy:", ((G>0.5) == Y).mean()

        # Now, do gradient ascent.
        gmy    = G-Y
        grad_b = gmy.sum()
        grad_w = -lamb * w + np.dot(gmy,X)

        b -= eta*grad_b
        w -= eta*grad_w

    G = 1 / (1. + np.exp(-b-np.dot(X,w)))
    print ((G>0.5) == Y).mean()

gradient_ascent(w=rs.randn(X.shape[1]), b=rs.rand()*50-25, lamb=0.5, eta=0.01, n_iters=10)
