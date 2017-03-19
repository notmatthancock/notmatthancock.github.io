import numpy as np

rs = np.random.RandomState(seed=1234)

A = rs.randn(400,500)
print A.shape
# => (400, 500)

# Indexing starts at 0. Negative indices access
# elements in reverse.
print A[0,0], A[-1,-2]
# => 0.471435163732, -1.42055605398

print A.mean(), A.std()
# => -0.000354821940337, 1.00081407567

I = np.eye(500)
B = np.dot(A, I) # Computes matrix product betwen A and I.

# Compute the Frobenius norm of A-B.
print np.linalg.norm(A-B, ord='fro')
# => 0.0

# ".npy" is analogous to ".mat" in Matlab
np.save('a_matrix.npy', A)

# Load the matrix.
AA = np.load('a_matrix.npy')
