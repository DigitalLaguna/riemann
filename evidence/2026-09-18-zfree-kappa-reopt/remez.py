import numpy as np

def remez(g, n, a, b, x0, grid_n=40001, itmax=300, tol=1e-13):
    """Minimax approx of g on [a,b] by span{x^1..x^n} (zero constant term).
    Returns (c[1..n] as array len n, E, extremal points, iters)."""
    m = n + 1
    xs = np.array(sorted(x0), float)
    grid = np.linspace(a, b, grid_n)
    ggrid = np.array([g(x) for x in grid])
    E = 0.0
    for it in range(itmax):
        # solve sum c_m x_i^m - (-1)^i E = g(x_i)  for i=0..m-1
        A = np.zeros((m, n+1)); bv = np.zeros(m)
        for i,xi in enumerate(xs):
            for mm in range(1, n+1):
                A[i, mm-1] = xi**mm
            A[i, n] = -((-1.0)**i)
            bv[i] = g(xi)
        sol = np.linalg.solve(A, bv)
        c = sol[:n]; E = sol[n]
        # error on grid
        q = np.zeros_like(grid)
        for mm in range(1, n+1):
            q += c[mm-1]*grid**mm
        err = q - ggrid
        imax = int(np.argmax(np.abs(err)))
        xstar = grid[imax]
        if abs(err[imax]) <= abs(E) + tol:
            break
        # Remez replacement: drop the extremal point with same sign as err(xstar)
        sstar = np.sign(err[imax])
        # find interval
        j = int(np.searchsorted(xs, xstar, side='right')) - 1
        j = max(0, min(j, m-2))
        # signs at xs[j], xs[j+1]
        sj = np.sign(err[int(np.argmin(np.abs(grid-xs[j])))] )
        sj1 = np.sign(err[int(np.argmin(np.abs(grid-xs[j+1])))] )
        # drop the one whose sign equals sstar
        if sj == sstar:
            xs = np.delete(xs, j)
        else:
            xs = np.delete(xs, j+1)
        xs = np.append(xs, xstar)
        xs = np.sort(xs)
    return c, E, xs, it

# ---- TEST on a known case: approx g(x)=x^2 on [0,1] by span{x} (n=1) ----
# best c: min max|x^2 - c x|. By symmetry of error, c=1/2 gives error 1/4 at x=1 and ... 
# Actually minimax of x^2 by c x on [0,1]: equioscillate at 2 pts. err(0)=0 always.
# The best is c=1/2? err(x)=x^2-x/2 = x(x-1/2), max at x=1: 1/2, at x=1/2: -1/8. Not equioscillating.
# Let's just check it converges and error is small-ish; compare to brute force.
c,E,xs,it = remez(lambda x: x*x, 1, 0.0, 1.0, [0.2,0.8])
print("TEST n=1 g=x^2: c=%.6f E=%.6f iters=%d extremal=%s"%(c[0],E,it,xs))
# brute force best c
best=None
for cc in np.linspace(0,1,200001):
    e=max(abs(np.linspace(0,1,2001)**2 - cc*np.linspace(0,1,2001)))
    if best is None or e<best[1]: best=(cc,e)
print("  brute-force best c=%.6f E=%.6f"%best)
