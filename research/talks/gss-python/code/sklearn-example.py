import numpy as np
import matplotlib.pyplot as plt
from sklearn.svm import LinearSVC

rs = np.random.RandomState(seed=1234)

# Generate fake data with two class clusters.
X0 = rs.multivariate_normal(mean=np.ones(2),
                            cov=np.eye(2),
                            size=500)

X1 = rs.multivariate_normal(mean=-np.ones(2),
                            cov=np.eye(2),
                            size=500)

X = np.vstack((X0, X1))

# Label vector.
Y = np.zeros(X.shape[0])
Y[500:] = 1

# Plot the generated data.
fig,ax = plt.subplots(1,1,figsize=(5,5))
ax.plot(X0[:,0], X0[:,1], 'o', label="Class 0", alpha=0.6)
ax.plot(X1[:,0], X1[:,1], 's', label="Class 1", alpha=0.6)

# Create and fit the Support Vector Classifier.
svc = LinearSVC()
svc.fit(X,Y)

# Create function for drawing the decision boundary.
line = lambda t: -(svc.intercept_[0] +\
                   svc.coef_[0,0]*t) / svc.coef_[0,1]
t = np.linspace(-4,4,101)

# Plot the determined boundary between classes.
ax.plot(t, line(t), '-', label="Decision Boundary")

ax.set_xlim(-4,4)
ax.set_ylim(-4,4)
ax.grid()
ax.legend(loc=2)
ax.set_axisbelow(True)

plt.show()
