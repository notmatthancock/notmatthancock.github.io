import numpy as np
import statsrecorder as sr

rs = np.random.RandomState(323)

mystats = sr.StatsRecorder()

# Hold all observations in "data" to check for correctness.
ndims = 42
data = np.empty((0, ndims))

for i in range(1000):
    nobserv = rs.randint(10,101)
    newdata = rs.randn(nobserv, ndims)
    data = np.vstack((data, newdata))

    # Update stats recorder object
    mystats.update(newdata)

    # Check stats recorder object is doing its business right.
    assert np.allclose(mystats.mean, data.mean(axis=0))
    assert np.allclose(mystats.std, data.std(axis=0))
