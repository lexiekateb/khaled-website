

force_use_cpu = False
try:
    import cupy as cp
    import cugraph
    import cupyx
    import cudf
except ImportError:
    print(f'cannot find GPU packages, forcing CPU')
    force_use_cpu = True

if not force_use_cpu:

    num_devices = cp.cuda.runtime.getDeviceCount()

    for device_id in range(num_devices):
        cp.cuda.runtime.setDevice(device_id)
        props = cp.cuda.runtime.getDeviceProperties(device_id)
        #for k in props.keys():
        #    print(k)
        print("Device ID:", device_id)
        print("Device Name:", props['name'].decode())

import scipy as sp
import math
import numpy as np

class Operand:
    def __init__(self, shape):
        self.shape = shape

    def gen(self):
        pass

class RandMat(Operand):
    def __init__(self, shape, density):
        self.shape = shape
        self.density = density

    def gen(self, device='gpu'):
        if device == 'cpu' or force_use_cpu:
            mat = sp.sparse.random(self.shape[0], self.shape[1], density=self.density, format='csr')
        else:
            mat = cupyx.scipy.sparse.random(self.shape[0], self.shape[1], density=self.density, format='csr')
        return mat

class IdMat(Operand):
    def __init__(self, shape, dtype='float32'):
        self.shape = shape
        self.dtype = dtype


    def gen(self):
        mat = sp.sparse.identity(self.shape, dtype=self.dtype, format='csr')
        return mat

class Initiator(Operand):
    def __init__(self, values, dtype='float32'):
        self.shape = int(math.sqrt(len(values)))
        self.dtype = dtype
        self.data = values
    
    def gen(self, device='gpu'):
        if device == 'cpu' or force_use_cpu:
            return np.array(self.data, dtype=self.dtype).reshape(self.shape,self.shape)
        else:
            return cp.array(self.data, dtype=self.dtype).reshape(self.shape, self.shape)

def kron(op1, op2):
    return sp.sparse.kron(op1.gen(), op2.gen(), format='csr')

def kront_cpu(op, times):
    op_data = op.gen()
    r = sp.sparse.kron(op_data, op_data, format='csr')
    for i in range(times-1):
        r = sp.sparse.kron(op_data, r, format='csr')
    r.eliminate_zeros()
    return r

def kront_gpu(op, times):
    op_data = op.gen_gpu()
    r = cupyx.scipy.sparse.kron(op_data, op_data, format='csr')
    for i in range(times-1):
        r = cupyx.scipy.sparse.kron(op_data, r, format='csr')
    r.eliminate_zeros()
    return r

def kront(op, times, device='cpu'):
    if device == 'cpu' or force_use_cpu:
        return kront_cpu(op, times)
    else:
        return kront_gpu(op, times)

def mask_cpu(matrix, mode,  random_seed_start=12345):

    call_eliminate_zeros = False
    random_seed = random_seed_start
    count_eliminated = 0
    print(f'[MASKING]total length = {len(matrix.data)}')
    for i in range(len(matrix.data)):
        if mode == 0 :
            np.random.seed(random_seed)
        prob = np.random.random()
        if matrix.data[i] < prob:
            matrix.data[i] = 0.0
            count_eliminated += 1
            call_eliminate_zeros = True
        if mode == 0:
            random_seed += 1
    if (call_eliminate_zeros):
        matrix.eliminate_zeros()
    print(f'[MASKING]total eliminated = {count_eliminated}')
    return matrix

# A GPU implementation for the masking operation using cuPy
def mask_gpu(matrix, mode, random_seed_start=12345):

    cupy_matrix = cp.sparse.coo_matrix(matrix)

    # Generate the random probability matrix for masking
    # First, we will have a unique seed for each element, starting from random_seed_start
    #        each following seed will be the previous seed + 1
    if mode == 0:
        cp.random.seed(random_seed_start + cp.arange(cupy_matrix.data.shape[0]).get())

    # Generate the random probabilty matrix using the seed
    random_props_gpu = cp.random.rand(*cupy_matrix.data.shape, dtype=cp.float32)

    # Mask the values
    mask = cupy_matrix.data < random_props_gpu
    cupy_matrix.data[mask] = 0

    # Transfer back to CPU
    cupy_matrix_cpu = cupy_matrix.get()

    cupy_matrix_cpu.eliminate_zeros()
    return cupy_matrix_cpu

# mode = 0 ==> deterministic
# mode = 1 ==> non-deterministic
def mask(matrix, random_seed_start=12345, mode=0, device='gpu'):
    if device == 'cpu' or force_use_cpu:
        return mask_cpu(matrix, mode,  random_seed_start)
    else:
        return mask_gpu(matrix, mode, random_seed_start)


def genKronGraph(init, times, masking_mode=0, device='gpu'):

    init_Mat = Initiator(init)
    # for now, default the Kronecker product to be done on CPU because GPU
    # memory seems to be never enough
    adj_mat = kront(init_Mat, times).tocoo()
    if force_use_cpu:
        device = 'cpu'
    adj_mat = mask(adj_mat, mode=masking_mode, device=device)

    return adj_mat

if __name__ == '__main__':


    myRand = RandMat([2,3], 0.5)
    myId = IdMat(2)

    result = kron(myRand, myId)

    print(f'result: {result}')

    sp.io.mmwrite('res.mtx', result)


