import unittest
from module5.last import Last


class TestLast(unittest.TestCase):
    """Last is an iterator that provides the last n values of a provided collection"""
    def test_normal_collection(self):
        collection = [1,2,3,4,5,6,7,8]
        # should return last n values of provided collection
        self.assertEqual([6,7,8], [i for i in Last(collection, 3)])

    def test_big_count(self):
        collection = [1,2,3,4,5,6,7,8]
        #if n is greater than the size of the provided collection, the iterator should return all elements
        self.assertEqual(collection, [i for i in Last(collection, 20)])

    def test_zero_count(self):
        collection = [1,2,3,4,5,6,7,8]
        #if n is 0 then no elements should be returned by the iterator
        self.assertEqual([], [i for i in Last(collection, 0)])

    def test_same_count(self):
         collection = [1,2,3,4,5,6,7,8]
         #if n is equal to the size of the collection, all values should be returned by the iterator
         self.assertEqual(collection, [i for i in Last(collection, 8)])
