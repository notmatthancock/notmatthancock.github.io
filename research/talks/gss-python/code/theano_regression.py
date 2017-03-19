import theano
import theano.tensor as T
import numpy as np
import matplotlib.pyplot as plt

rs = np.random.RandomState(seed=1234)

x = np.linspace(0,1,101).astype(np.float32)
X = theano.shared(x, name='X')

a = np.pi
A = theano.shared(rs.randn(), name='A')

y = a*x*x + 0.2 * rs.randn(x.shape[0])
Y = theano.shared(y, name='Y')

SSE = ((Y-A*X**2)**2).sum()

dSSE_dA = theano.grad(SSE, wrt=A)

step_size = 0.01
grad_desc = theano.function(inputs=[], outputs=SSE,
                            updates=[(A, A-step_size*dSSE_dA)])

niters = 10
mse = np.zeros(niters)
for i in range(niters):
    mse[i] = grad_desc()

aa = A.eval()

fig, ax = plt.subplots(1,2,figsize=(10,5))


ax[0].plot(x, y, 'o', label='Points')
ax[0].plot(x, aa*x*x, '-', lw=3, label='Fit')

ax[0].grid(); ax[0].set_axisbelow(True)
ax[0].legend(loc=2)

ax[1].plot(np.arange(1,niters+1), mse, label='SSE')
ax[1].set_xlabel('Gradient Descent Iteration')
ax[1].set_ylabel('Sum of Squared Errors')
ax[1].legend(loc=1)
ax[1].grid()

plt.show()
