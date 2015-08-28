
import numpy as np
#data_set: 2-d dict
class KFold(object):
    def __init__(self,k,data_set):
        self.K = int(k) if k>2 else 5
        self.data_set = data_set

    def constuct_data_set(self,ith):
        u_ids = self.data_set.keys()
        train_set = {}
        test_set = {}
        for u_id in u_ids:
            i_ids = self.data_set[u_id].keys()
            training_set, testing_set = self.slice_ith(i_ids,ith)
            self.__constuct_data_set(u_id,training_set,train_set)
            self.__constuct_data_set(u_id,testing_set,test_set)
        return train_set, test_set
 

    def __constuct_data_set(self,user_id, src_set,dst_set):
        for ky in src_set:
            dst_set.setdefault(user_id,{})
            dst_set[user_id][ky] = self.data_set[user_id][ky]
        return    

    def slice_ith(self,items,ith):
        #how to deal if len(items) < k
        item_num = len(items)
        if item_num < self.K:
            #FIXme!!!!!
           raise NotImplementedError("too few the rated items") 
        step = item_num/self.K

        start = step*(ith)
        end = step*(ith+1)
        testing_set = items[start:end]
        #any graceful method,except numpy ?
        training_set = []
        training_set.extend(items[:start])
        training_set.extend(items[end:])
        return training_set, testing_set

    def cross_validate(self):
        #multiprocess
        rs_mae = []
        rs_rmse = []
        for ith in range(0,self.K):
            train_set, test_set = self.constuct_data_set(ith)
            result = self.validate(train_set,test_set)
            print "result ", ith, ":    ", result
            rs_mae.append(result["MAE"])
            rs_rmse.append(result["RMSE"])
        return np.mean(rs_mae)

    def validate(self,train_set,test_set):
        raise NotImplementedError("cannot instantiate Abstract Base Class")



