import unittest
import os
import sys
import os.path as path
import numpy as np
import scipy

# Path to where the bindings live
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
if os.name == 'nt': # if Windows
    # handle default location where VS puts binary
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "build", "Debug")))
else:
    # normal / unix case
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "build")))


import potpourri3d as pp3d


def generate_verts(n_pts=999):
    np.random.seed(777)        
    return np.random.rand(n_pts, 3)

def generate_faces(n_pts=999):
    # n_pts should be a multiple of 3 for indexing to work out
    np.random.seed(777)        
    rand_faces = np.random.randint(0, n_pts, size=(2*n_pts,3))
    coverage_faces = np.arange(n_pts).reshape(-1, 3)
    faces = np.vstack((rand_faces, coverage_faces))
    return faces

def is_symmetric(A, eps=1e-6):
    resid = A - A.T
    return np.all(np.abs(resid.data) < eps)

def is_nonnegative(A, eps=1e-6):
    return np.all(A.data > -eps)

class TestCore(unittest.TestCase):
    
    def test_write_read_mesh(self):

        for ext in ['obj']:

            V = generate_verts()
            F = generate_faces()

            fname = "test." + ext

            # write
            pp3d.write_mesh(V,F,fname)

            Vnew, Fnew = pp3d.read_mesh(fname)

            
            self.assertLess(np.amax(np.abs(V-Vnew)), 1e-6)
            self.assertTrue((F==Fnew).all())
    
    def test_write_read_point_cloud(self):

        for ext in ['obj', 'ply']:

            V = generate_verts()

            fname = "test_cloud." + ext

            # write
            pp3d.write_point_cloud(V, fname)

            Vnew = pp3d.read_point_cloud(fname)
            
            self.assertLess(np.amax(np.abs(V-Vnew)), 1e-6)

        # self.assertTrue(is_nonnegative(off_L)) # positive edge weights
        # self.assertGreater(L.sum(), -1e-5)
        # self.assertEqual(M.sum(), M.diagonal().sum())

if __name__ == '__main__':
    unittest.main()