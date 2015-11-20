#from collections import Counter
import numpy as np

'''
raw_data: 2-d dict
'''
class Model(object):
    def __init__(self,raw_data):
        self.build_model(raw_data)
        
        return

    def __get_item_ids(self, order_by_id = False):
        u_ids = self.raw_data.keys()
        item_ids = []
        for u_id in u_ids:
            utem = self.raw_data[u_id]
            item_ids.extend(utem.keys())
        tem_set = set(item_ids)
        item_ids = list(tem_set)
        if order_by_id:
            return item_ids.sort()
        return item_ids

    def get_max_min_pref(self):
        max_rate = -np.inf
        min_rate = np.inf
        u_ids = self.raw_data.keys()
        for u_id in u_ids:
            for i_id in self.raw_data[u_id].keys():
                rate = self.raw_data[u_id][i_id]
                if rate > max_rate:
                    max_rate = rate
                if rate < min_rate:
                    min_rate = rate
        return max_rate, min_rate

    def get_item_ids(self):
        return self.__item_ids

    def get_user_ids(self):
        return self.__user_ids 

    def get_item_num(self):
        return len(self.__item_ids)

    def get_user_num(self):
        return len(self.__user_ids)

    def get_rates(self,user_id, ts=True):
        if not user_id in self.raw_data:
            return None
        if ts:
            return self.raw_data[user_id]
        else:
            rates = {}
            for ky in self.raw_data[user_id].keys():
                rate, ts = self.raw_data[user_id][ky]
                rates[ky] = float(rate)
            return rates


    def get_rate(self, user_id, item_id, ts=True):
        if not user_id in self.raw_data:
            #print "raw_data: user_id ", user_id
            return None
        if not item_id in self.raw_data[user_id]:
            #print "raw_data: user_id, item_id ", user_id, item_id
            return None
        if ts:
            return self.raw_data[user_id][item_id]
        else:
            rate = self.raw_data[user_id][item_id]
            return float(rate)

    def get_items(self,user_id):
        #if not user_id in self.raw_data:
        #    return None
        return self.raw_data[user_id].keys()

    def get_users(self,item_id):
        if item_id in self.__tmp_items:
            return self.__tmp_items[item_id]

        for u_id in self.__user_ids:
            if not item_id in self.raw_data[u_id]:
                continue
            if item_id in self.__tmp_items:
                self.__tmp_items[item_id].append(u_id)
            else:
                self.__tmp_items[item_id] = [u_id]

        return self.__tmp_items[item_id]

    def are_valid(self,user_ids):
        for u_id in user_ids:
            if not u_id in self.raw_data:
                return False
        return True

    def is_valid(self,user_id,item_id):
        if not user_id in self.raw_data:
            return False
        if not item_id in self.raw_data[user_id]:
            return False
        return True

    def build_model(self,raw_data, **kargs):
        self.raw_data = raw_data
        self.__item_ids = self.__get_item_ids()
        self.__user_ids = self.raw_data.keys()
        self.max_pref, self.min_pref = self.get_max_min_pref()

        self.__tmp_items = {}
        self.users_mean_rate = {}
        self.items_mean_rate = {}
        self.user_id_to_no = {}
        self.item_id_to_no = {}      
        return

    #output: [1,2,3]
    def get_mutual_item_ids(self,user_id1, user_id2):
        i_ids1 = self.get_items(user_id1)
        i_ids2 = self.get_items(user_id2)
        if len(i_ids1) < 1 or len(i_ids2) < 1:
            print "should not be x..x: ", user_id1,user_id2
            return None
        comm = list(set(i_ids1).intersection(i_ids2))
        #comm = list((Counter(i_ids1) & Counter(i_ids2)).elements())
        return comm

    def get_mutual_user_ids(self,item_id1, item_id2):
        u_ids1 = self.get_users(item_id1)
        u_ids2 = self.get_users(item_id2)
        if len(u_ids1) < 1 or len(u_ids2) < 1:
            print "should not be x..x!!!!!!! "
            return None
        comm = list(set(u_ids1).intersection(u_ids2))
        #comm = list((Counter(i_ids1) & Counter(i_ids2)).elements())
        return comm

    def get_multiple_users_mean_rate(self,user_ids):
        mean_rates = {}
        for u_id in user_ids:
            m_r = self.get_user_rate_mean(u_id)
            mean_rates[u_id] = m_r

        return mean_rates

#0: unrate
    def get_user_rate_mean(self, user_id):
        if user_id in self.users_mean_rate:
            return self.users_mean_rate[user_id]

        u_rates = self.get_rates(user_id)
        item_num = len(u_rates.keys())

        if  item_num < 1:
            self.users_mean_rate[user_id] = 0
            return 0

        total_rate = 0.0
        for i_id in u_rates.keys():
            rate, ts = u_rates[i_id]
            total_rate += float(rate)

        mean_rate = float(total_rate)/float(item_num)
        self.users_mean_rate[user_id] = mean_rate

        return mean_rate

    def get_items_mean_rate(self,items):
        return

    def map_user_item_id_no(self):
        for user_no, user_id in enumerate(self.get_user_ids()):
            self.user_id_to_no[user_id] = user_no
        for item_no, item_id in enumerate(self.get_item_ids()):
            self.item_id_to_no[item_id] = item_no


    def get_data_matrix(self):
        user_num = self.get_user_num()
        item_num = self.get_item_num()
        #print user_num, item_num
        self.map_user_item_id_no()
        self.data_mat = np.zeros(shape=(user_num, item_num))
        for user_no, user_id in enumerate(self.get_user_ids()):
            for item_no, item_id in enumerate(self.get_item_ids()):
                if item_id in self.raw_data[user_id]:
                    rate, ts = self.raw_data[user_id][item_id]
                    #print user_no, item_no, rate
                else:
                    rate = 0.0
                self.data_mat[user_no, item_no] = rate
        #print self.data_mat
        return self.data_mat



    