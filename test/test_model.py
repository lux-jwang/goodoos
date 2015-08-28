import unittest
import pickle
import sys
from os import path

sys.path.append( path.dirname( path.dirname( path.abspath(__file__))))
from dataset import datawasher as dw
from src import model

class TestModel(unittest.TestCase):
    def setUp(self):
        rating_file = "./fakedataset/dw_rating.dat"
        id_map_file = "./fakedataset/dw_id_map.mat"
        active_user_file = "./fakedataset/dw_active_users_all.mat"
        dst_filename = "./fakedataset/dw_user_item_matrix.mat"
        self.mat = dw.get_orignal_data(rating_file,id_map_file,active_user_file,dst_filename)
        self.model = model.Model(self.mat)

    def test_get_user_ids(self):
        u_ids = model.Model(self.mat).get_user_ids()
        self.assertEqual(len(u_ids),9)
        u_ids2 = model.Model(self.mat).get_user_ids()
        self.assertSequenceEqual(u_ids,u_ids2)
    
    def test_get_item_ids(self):
        i_ids1 = model.Model(self.mat).get_item_ids()
        i_ids2 = model.Model(self.mat).get_item_ids()
        self.assertSequenceEqual(i_ids1,i_ids2)
        self.assertEqual(len(i_ids1),10)

    def test_get_rates(self):
    	u_ids = self.model.get_user_ids()
    	for u_id in u_ids:
    		rate = self.model.get_rates(u_id)
    		self.assertTrue(len(rate)>0)

    def test_get_rate(self):
    	u_ids = self.model.get_user_ids()
    	i_ids = self.model.get_item_ids()

        cidx = 0
    	for u_id in u_ids:
    		for i_id in i_ids:
    			rate = self.model.get_rate(u_id, i_id)
    			if not rate is -1:
    				cidx += 1

    	self.assertTrue(cidx is 17)

    def test_get_users(self):
    	i_ids = self.model.get_item_ids()
    	for i_id in i_ids:
    		users = self.model.get_users(i_id)
    	self.assertTrue(1>0)

    def test_get_items(self):
    	u_ids = self.model.get_user_ids()
    	for u_id in u_ids:
    		items = self.model.get_items(u_id)
    		print u_id
    		if u_id == "1111":
    			self.assertEqual(len(items),2)
    	
    	self.assertTrue(1>0)


    

if __name__ == '__main__':
    unittest.main()