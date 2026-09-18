import numpy as np

def lp_max(c, A, b, tol=1e-11, itmax=200000):
    """max c^T x s.t. A x <= b, x free. Two-phase simplex.
    Returns (status, x, val)."""
    n = len(c)
    # x = x+ - x-, x+, x- >= 0. 2n vars.
    # A [x+ - x-] <= b  =>  A x+ - A x- <= b
    A2 = np.hstack([A, -A]).astype(float)
    c2 = np.concatenate([c, -c])
    m = len(b)
    # Standard form: A2 y + s = b, s >= 0, y >= 0.
    # Phase I: for rows with b_i < 0, flip and add artificial.
    T = np.zeros((m+1, 2*n + m + 1))
    basis = []
    art = []
    for i in range(m):
        if b[i] >= -tol:
            T[i, :2*n] = A2[i]
            T[i, 2*n+i] = 1.0
            T[i, -1] = b[i]
            basis.append(2*n+i)
        else:
            T[i, :2*n] = -A2[i]
            T[i, 2*n+i] = -1.0
            T[i, -1] = -b[i]
            # add artificial at col 2*n+m (shared) -- no, need per-row. Use col 2*n+m+i? 
            # Simpler: put artificial in its own column per flipped row.
            basis.append(None)  # placeholder
            art.append(i)
    # Redo with per-row artificial columns.
    nart = len(art)
    T = np.zeros((m+1, 2*n + m + nart + 1))
    basis = []
    for i in range(m):
        if b[i] >= -tol:
            T[i, :2*n] = A2[i]
            T[i, 2*n+i] = 1.0
            T[i, -1] = b[i]
            basis.append(2*n+i)
        else:
            T[i, :2*n] = -A2[i]
            T[i, 2*n+i] = -1.0
            T[i, 2*n+m+art.index(i)] = 1.0
            T[i, -1] = -b[i]
            basis.append(2*n+m+art.index(i))
    # Phase I obj: min sum art => row = -1 at art cols
    for j, i in enumerate(art):
        T[m, 2*n+m+j] = -1.0
    for j, i in enumerate(art):
        T[m] = T[m] + T[i]
    def run(T, basis, objrow, tol, itmax):
        m_ = T.shape[0]-1
        ncol = T.shape[1]-1
        for it in range(itmax):
            obj = T[objrow, :ncol]
            j = int(np.argmin(obj))
            if obj[j] >= -tol:
                return 'optimal'
            col = T[:m_, j]
            ratios = []
            for i in range(m_):
                if col[i] > tol:
                    ratios.append((T[i,-1]/col[i], i))
            if not ratios:
                return 'unbounded'
            ratios.sort()
            i = ratios[0][1]
            piv = T[i,j]
            T[i] = T[i]/piv
            for r in range(m_+1):
                if r != i:
                    T[r] = T[r] - T[i]*T[r,j]
            basis[i] = j
        return 'maxit'
    st = run(T, basis, m, tol, itmax)
    if st != 'optimal':
        return st, None, None
    if -T[m,-1] > 1e-7:
        return 'infeasible', None, None
    # Phase II
    T[m, :2*n] = -c2
    T[m, 2*n:] = 0.0
    for i, bv in enumerate(basis):
        if bv < 2*n:
            T[m] = T[m] + T[i]*c2[bv]
    st2 = run(T, basis, m, tol, itmax)
    if st2 != 'optimal':
        return st2, None, None
    y = np.zeros(2*n)
    for i, bv in enumerate(basis):
        if bv < 2*n:
            y[bv] = T[i,-1]
    x = y[:n] - y[n:]
    return 'optimal', x, float(c @ x)

# Tests
st,x,v = lp_max(np.array([1.,1.]), np.array([[1.,1.],[1.,0.],[0.,1.]]), np.array([1.,1.,1.]))
print("T1 max x+y s.t. x+y<=1,x<=1,y<=1: st=%s x=%s v=%.4f (expect 1)"%(st,x,v))
st,x,v = lp_max(np.array([1.]), np.array([[1.],[-1.]]), np.array([1.,1.]))
print("T2 infeasible: st=%s (expect infeasible)"%st)
st,x,v = lp_max(np.array([1.]), np.array([[1.]]), np.array([1.]))
print("T3 max x s.t. x<=1: st=%s x=%s v=%.4f (expect 1)"%(st,x,v))
