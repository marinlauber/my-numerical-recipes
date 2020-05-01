import numpy as np
from scipy.linalg import solve_banded,solve
import time
from scipy import sparse

# random profile
def Gaussian(x, v=3., sigma=1.):
    return np.exp(-(x - v)**2 / (2 * sigma**2)) / (np.sqrt(2 * np.pi)* sigma)
        
# number of grid points
N = 100

# build ugly matrix
print('scipy.linalg.solve() :')
start  = time.time()
A = sparse.diags([1,-2,1],[-1,0,1],shape=(N**2,N**2)).toarray()
end  = time.time()
print('Time to build a %dx%d Poisson matrix is : %.3f s' % (N, N, end-start))

# source term
sigma = Gaussian(np.linspace(-10.,10.,N**2),v=0.)

# solve it, should be zero pressure
start = time.time()
p = np.linalg.solve(A, sigma)
end  = time.time()
Linf = np.max(np.abs(np.matmul(A,p)-sigma))
print('The L-inf norm of the error is : %.6e' % Linf)
print('Time to solve a %dx%d Poisson matrix is : %.3f s' % (N, N, end-start))

# build only diagonals
print('scipy.linalg.solve_banded() :')
start  = time.time()
LU = np.ones((3, N**2))
LU[1,:] *= -2
LU[0,0] = LU[-1,-1] = 0.0
end  = time.time()
print('Time to build a %dx%d Poisson matrix is : %.3f s' % (N, N, end-start))

start = time.time()
p2 = solve_banded((1, 1), LU, sigma)
end  = time.time()
Linf = np.max(np.abs(np.matmul(A,p2)-sigma))
print('The L-inf norm of the error is : %.6e' % Linf)
print('Time to solve a %dx%d Poisson matrix is : %.3f s' % (N, N, end-start))
