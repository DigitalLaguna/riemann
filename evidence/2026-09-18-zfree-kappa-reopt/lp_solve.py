import numpy as np

def simplex_two_phase(c, A, b, tol=1e-10, itmax=100000):
    """Solve min c^T x s.t. A x >= b, x >= 0 (Phase I + Phase II).
    Returns (status, x, objval) where status in {'optimal','infeasible','unbounded'}."""
    m, n = A.shape
    # Convert A x >= b to A' x <= b' by negating: (-A) x <= -b
    A2 = -A.astype(float); b2 = -b.astype(float)
    # Now solve min c^T x s.t. A2 x <= b2, x >= 0
    # Add slacks: A2 x + s = b2, s >= 0
    # Phase I: add artificials where b2 < 0
    # Standard form: A2 x + s = b2. Initial basis = slacks, feasible iff b2 >= 0.
    # For b2_i < 0, multiply row i by -1: -A2_i x - s_i = -b2_i, then add artificial a_i:
    #   -A2_i x - s_i + a_i = -b2_i  (so a_i = -b2_i > 0 initially)
    # Phase I: min sum a_i s.t. the modified system, x,s,a >= 0.
    # Build tableau.
    rows = []
    art_rows = []
    for i in range(m):
        if b2[i] >= -tol:
            rows.append((A2[i].copy(), 1.0, b2[i], False))  # (A_row, slack_coeff, b, is_art)
        else:
            # multiply by -1
            rows.append((-A2[i].copy(), -1.0, -b2[i], True))
            art_rows.append(len(rows)-1)
    # Tableau: columns = x (n), s (m), a (nart), rhs
    nart = len(art_rows)
    ncols = n + m + nart + 1
    T = np.zeros((m+1, ncols))
    for i, (Ar, sc, bi, isart) in enumerate(rows):
        T[i, :n] = Ar
        T[i, n+i] = sc
        if isart:
            T[i, n+m+art_rows.index(i)] = 1.0
        T[i, -1] = bi
    # Phase I objective: min sum a_i  =>  row m: -1 for each art col
    for j, ai in enumerate(art_rows):
        T[m, n+m+j] = -1.0
    # Eliminate artificials from objective using their rows
    for j, ai in enumerate(art_rows):
        T[m] = T[m] + T[ai]
    basis = list(range(n, n+m)) + [n+m+j for j in range(nart)]
    # Simplex loop
    def simplex(T, basis, obj_row, tol, itmax):
        m_, n_ = T.shape
        ncol = n_ - 1
        for it in range(itmax):
            obj = T[obj_row, :ncol]
            j = int(np.argmin(obj))
            if obj[j] >= -tol:
                return 'optimal'
            col = T[:m_, j]
            ratios = []
            for i in range(m_):
                if col[i] > tol:
                    ratios.append((T[i, -1]/col[i], i))
            if not ratios:
                return 'unbounded'
            ratios.sort()
            i = ratios[0][1]
            piv = T[i, j]
            T[i] = T[i]/piv
            for r in range(m_):
                if r != i:
                    T[r] = T[r] - T[i]*T[r, j]
            basis[i] = j
        return 'maxit'
    st = simplex(T, basis, m, tol, itmax)
    if st != 'optimal':
        return st, None, None
    # Check Phase I optimum
    phase1_val = -T[m, -1]
    if phase1_val > tol:
        return 'infeasible', None, phase1_val
    # Phase II: set objective to c, eliminate basic vars
    T[m, :n] = -c  # min c^T x => row = -c
    T[m, n:] = 0.0
    for i, bv in enumerate(basis):
        if bv < n:
            T[m] = T[m] + T[i]*c[bv]
    # Remove artificial columns (they should be non-basic now)
    st2 = simplex(T, basis, m, tol, itmax)
    if st2 != 'optimal':
        return st2, None, None
    x = np.zeros(n)
    for i, bv in enumerate(basis):
        if bv < n:
            x[bv] = T[i, -1]
    return 'optimal', x, -T[m, -1]

# Test: min -x1 - x2 s.t. x1+x2 >= 1, x1 >= 0, x2 >= 0  -> min = -1
st, x, v = simplex_two_phase(np.array([-1.,-1.]), np.array([[1.,1.]]), np.array([1.]))
print("T1: status=%s x=%s val=%.4f (expect -1)"%(st, x, v))
# Test infeasible: x1 >= 1, -x1 >= 1
st, x, v = simplex_two_phase(np.array([0.]), np.array([[1.],[-1.]]), np.array([1.,1.]))
print("T2: status=%s (expect infeasible)"%st)
