def inner_product(x, y):
    z = 0.0
    for i in range(x.shape[0]):
        z += x[i]*y[i]
    return z
