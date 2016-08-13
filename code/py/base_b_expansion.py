import numpy as np

def expand_base_b(x, b, N):
    """
    Expand `x` in base, `b`, to `N` digits.

    Returns:
        approx_x: the truncated base-b expansion.
        string_x: the string of base-b digits with appropriately
                  placed decimal point.
    """
    assert isinstance(b, int)
    assert isinstance(N, int)
    assert b > 1
    assert x > 0
    assert N > 0

    x = float(x)
    b = float(b)
    e = np.floor(np.log(x) / np.log(b))
    be = b**e
    a = np.zeros(N+1, dtype=int)

    # Running sum: \sum_{k=0}^i a_k b^{-k}
    s = 0

    for i in range(0,N+1):
        fl = np.floor((x/be - s) * b**i)
        a[i] = fl
        s += a[i]*b**(-i)
    
    e = int(e)

    # Convert the base expansion list to a string.
    num = "".join(map(lambda n: str(int(n)), a))

    # Add the "decimal" point.
    if e < 0:
        num = "0." + ("0"*(-e-1)) + num
    elif e > 0:
        num = num[:e+1] + "." + num[e+1:]
    else:
        num = num[0] + "." + num[1:]

    return be*s, num
