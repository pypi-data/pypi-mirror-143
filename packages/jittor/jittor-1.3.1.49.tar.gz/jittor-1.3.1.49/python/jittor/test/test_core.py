# ***************************************************************
# Copyright (c) 2021 Jittor. All Rights Reserved. 
# Maintainers: Dun Liang <randonlang@gmail.com>. 
# This file is subject to the terms and conditions defined in
# file 'LICENSE.txt', which is part of this source code package.
# ***************************************************************
import unittest
import jittor as jt
import numpy as np
import os

def expect_error(func):
    try:
        func()
    except Exception as e:
        return
    raise Exception("Expect an error, but nothing catched.")

class TestCore(unittest.TestCase):
    def test_number_of_hold_vars(self):
        assert jt.random([1,2,3]).peek() == "float32[1,2,3,]"
        assert jt.core.number_of_hold_vars() == 0
        x = jt.random([1,2,3])
        assert jt.core.number_of_hold_vars() == 1
        del x
        assert jt.core.number_of_hold_vars() == 0

    def test_fetch_sync(self):
        dtypes = ["float32", "float64"]
        for dtype in dtypes:
            x = jt.random([1,2,3], dtype)
            res = x.data
            assert res.dtype == dtype and res.shape == (1,2,3)

    def test_set_seed(self):
        a = jt.random([1,2,3]).data
        b = jt.random([1,2,3]).data
        assert str(a) != str(b)
        jt.set_seed(1)
        a = jt.random([1,2,3]).data
        jt.set_seed(1)
        b = jt.random([1,2,3]).data
        assert str(a) == str(b)
        
    def test_array_op(self):
        data = [
            np.array([1,2,3]),
            np.int32([1,2,3]),
            np.int64([1,2,3]),
            np.float32([1,2,3]),
            np.float64([1,2,3]),
        ]
        for a in data:
            assert sum(jt.array(a).data) == 6
        assert np.all(jt.array(np.int32([1,2,3])[::-1]).data == [3,2,1])
        assert jt.array(1).data.shape == (1,)
        
    def test_matmul_op(self):
        a = np.array([[1, 0], [0, 1]]).astype("float32")
        b = np.array([[4, 1], [2, 2]]).astype("float32")
        c = np.matmul(a, b)
        jtc = jt.matmul(jt.array(a), jt.array(b)).data
        assert np.allclose(jtc, c)

        a = np.random.random((128,3,10,20))
        b = np.random.random((20,30))
        c = np.matmul(a, b)
        jtc = jt.matmul(jt.array(a), jt.array(b)).data
        assert np.allclose(jtc, c)

        a = np.random.random((128,3,10,20))
        b = np.random.random((128,3,20,30))
        c = np.matmul(a, b)
        jtc = jt.matmul(jt.array(a), jt.array(b)).data
        assert np.allclose(jtc, c), np.abs(jtc-c).max()
        
    def test_var_holder(self):
        jt.clean()
        expect_error(lambda: jt.matmul(1,1))
        expect_error(lambda: jt.matmul([1],[1]))
        expect_error(lambda: jt.matmul([[1]],[1]))
        self.assertEqual(jt.number_of_lived_vars(), 0)
        a = jt.matmul(jt.float32([[3]]), jt.float32([[4]])).data
        assert a.shape == (1,1) and a[0,0] == 12
        a = np.array([[1, 0], [0, 1]]).astype("float32")
        b = np.array([[4, 1], [2, 2]]).astype("float32")
        c = np.matmul(a, b)
        jtc = jt.matmul(jt.array(a), jt.array(b)).data
        assert np.all(jtc == c)
        
    def test_save_load_sub_module(self):
        class Net(jt.Module):
            def __init__(self):
                self.conv1 = jt.nn.Conv(3,3,3)
        net = Net()
        assert list(net.state_dict().keys()) == ['conv1.weight', 'conv1.bias']
        assert list(net.conv1.state_dict().keys()) == ['weight', 'bias']
        pkl_name = os.path.join(jt.flags.cache_path, "sub.pkl")
        net.conv1.save(pkl_name)
        net.conv1.load(pkl_name)

    def test_module(self):
        a = jt.Module()
        a.__setattr__("x", 1)
        assert a.__getattr__("x") == 1
        a.y = 2
        assert a.y == 2

if __name__ == "__main__":
    unittest.main()