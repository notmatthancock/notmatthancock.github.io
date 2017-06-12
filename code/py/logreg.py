import numpy as np

rs = np.random.RandomState(1234)
p = 2
n = 200
py1 = 0.6
mean1 = np.r_[1,1.]
mean0 = -mean1

Y = (rs.rand(n) > py1).astype(int)
X = np.zeros((n,p))
X[Y==0] = rs.multivariate_normal(mean0, np.eye(p), size=(Y==0).sum())
X[Y==1] = rs.multivariate_normal(mean1, np.eye(p), size=(Y==1).sum())

import matplotlib.pyplot as plt 
plt.plot(X[Y==0,0], X[Y==0,1], 'ob', label='Class 0')
plt.plot(X[Y==1,0], X[Y==1,1], 'sr', label='Class 1')
plt.legend(loc=2, numpoints=1)

plt.show()

def gradient_ascent(w, b, lamb, eta, n_iters):
    # G is P(Y=1|X) under the current parameters.
    G = 1 / (1. + np.exp(-b-np.dot(X,w)))
    # loss is the function we're maximizing
    loss = -lamb * (w**2).sum() + np.log(G[Y==1]).sum() + np.log(1-G[Y==0]).sum()
    print "iteration:", 0, "| loss:", loss, "| accuracy:", ((G>0.5) == Y).mean()

    for iter in range(1, n_iters+1):
        G = 1 / (1. + np.exp(-b-np.dot(X,w)))
        loss = -lamb * 0.5 * (w**2).sum() + np.log(G[Y==1]).sum() + np.log(1-G[Y==0]).sum()
        print "iteration:", iter, "| loss:", loss, "| accuracy:", ((G>0.5) == Y).mean()

        # Now, do gradient ascent.
        ymg    = Y-G
        grad_b = ymg.sum()
        grad_w = -lamb * w + np.dot(ymg,X)

        b += eta*grad_b
        w += eta*grad_w
    return w,b

init_w = rs.randn(X.shape[1])
init_b = rs.rand()*50-25

w,b=gradient_ascent(w=init_w.copy(), b=init_b, lamb=0., eta=0.01, n_iters=10)

print "\n"

print "Parameters found ... w:", w, "b:", b

# Generate some new testing data
Y_ = (rs.rand(n) > py1).astype(int)
X_ = np.zeros((n,p))
X_[Y_==0] = rs.multivariate_normal(mean0, np.eye(p), size=(Y_==0).sum())
X_[Y_==1] = rs.multivariate_normal(mean1, np.eye(p), size=(Y_==1).sum())

G = 1 / (1. + np.exp(-b-np.dot(X_,w)))

print "\n"

print "Accuracy on test data:", ((G>0.5) == Y_).mean()

x,y = np.mgrid[-4:4:61j,-4:4:61j]
xy = np.c_[ x.flatten(), y.flatten() ]

G = 1 / (1. + np.exp(-b-np.dot(xy,w)))

fig = plt.figure()
# This is a color coding of the numerical prediction over the region.
plt.contourf(x, y, G.reshape(x.shape), cmap=plt.cm.bwr, alpha=0.6)

x1 = (-b-4*w[1]) / w[0]
x2 = (-b+4*w[1]) / w[0]
# This draws the decision boundary.
plt.plot( [x1,x2], [4, -4.], '-k', lw=3)

plt.plot(X[Y==0,0], X[Y==0,1], 'ob')
plt.plot(X[Y==1,0], X[Y==1,1], 'sr')

plt.show()
