import unittest
import pickle
import sys
from os import path

#sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
from dataset import datawasher as dw

class TestDataWasher(unittest.TestCase):

	def setUp(self):
		self.dw_active_users = "./fakedataset/dw_active_users.mat"

		if path.isfile("./fakedataset/dw_active_users.mat"):
			return

		test_mat = {"1111":["1115","3","5","11117","200"],
		            "1113":["37","1117","59","78","1"],
		            "1115":["33","1113","6"],
		            "1117":["39","42","56","78","1"],
		            "1119":["31"],
		            "11111":["12","31","51","111","11116"],
		            "11113":["137","122","11119","1119","667788"],
		            "11115":["133","322","516"],
		            "11117":["139","422","53","784","16"],
		            "11119":["11111"]
		            }

		pickle.dump(test_mat,open("./fakedataset/dw_active_users.mat", "w"),protocol=2)

	def tearDown(self):
		#self.dw_mat = None
		return

	def test_get_total_active_user_num(self):
		num = dw.get_total_active_user_num(self.dw_active_users,3)
		self.assertEqual(num,6)
		return

	def test_get_orignal_data(self):
		self.test_get_active_users_all_num()
		self.test_get_user_id_map()
		rating_file = "./fakedataset/dw_rating.dat"
		id_map_file = "./fakedataset/dw_id_map.mat"
		active_user_file = "./fakedataset/dw_active_users_all.mat"
		dst_filename = "./fakedataset/dw_user_item_matrix.mat"
		mat = dw.get_orignal_data(rating_file,id_map_file,active_user_file,dst_filename)
		user_num = len(mat.keys())
		self.assertEqual(user_num,9)
		self.assertTrue((not "2004" in mat))
		return

	def test_get_active_users_all_num(self):

		src_filename = self.dw_active_users
		dst_filename = "./fakedataset/dw_active_users_all.mat"
		mat = dw.get_active_users_all_num(3,src_filename, dst_filename)
		user_num = len(mat.keys())
		self.assertEqual(user_num,32)
		self.assertTrue(path.isfile(dst_filename))
		return

	def test_get_active_users_num(self):
		src_filename = self.dw_active_users
		dst_filename = "./fakedataset/dw_active_users_keys.mat"
		mat = dw.get_active_users_num(3,src_filename, dst_filename)
		user_num = len(mat.keys())
		self.assertEqual(user_num,10)
		self.assertTrue(path.isfile(dst_filename))
		return

	def test_get_user_id_map(self):
		src_filename = "./fakedataset/dw_users.dat"
		dst_filename = "./fakedataset/dw_id_map.mat"
		mat = dw.get_user_id_map(src_filename,dst_filename)
		user_num = len(mat.keys())
		self.assertEqual(user_num,15)
		self.assertTrue(path.isfile(dst_filename))
		return



if __name__ == '__main__':
    unittest.main()