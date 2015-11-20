import sys
from os import path
import pickle
import numpy as np

from recsys.datamodel.data import Data
from recsys.algorithm.factorize import SVD
from recsys.evaluation.prediction import RMSE, MAE

from datawasher import get_twittermovie_matrix, get_moive100k, get_moive1m

PERCENT_TRAIN = 80
KKK = 100
MIN_ITEM = 10

def prepare_data(raw_data):
    idata = Data()
    u_idx = 0
    for u_id in raw_data.keys():
        i_idx = 0
        u_idx += 1
        pre_u_raw_data = raw_data[u_id]
        for i_id in pre_u_raw_data.keys():
            i_idx += 1
            rate, _ = pre_u_raw_data[i_id]
            idata.add_tuple((float(rate),u_idx,i_idx))

    return idata


def statis_data(raw_data):   
    i_id_list = []
    user_num = 0
    rate_num = 0
    for u_id in raw_data.keys():
        pre_raw_data = raw_data[u_id]
        if len(pre_raw_data.keys()) < MIN_ITEM:
        	continue
        user_num += 1
        rate_num += len(pre_raw_data.keys())
        for i_id in pre_raw_data.keys():
            i_id_list.append(i_id)

    i_id_list = list(set(i_id_list))
    item_num = len(i_id_list)

    print "user_num: ", user_num
    print "item_num: ", item_num
    print "rate_num: ", rate_num


def evaulte(train_set, test_set):
    svd = SVD()
    svd.set_data(train_set)
    svd.compute(k=KKK, min_values=MIN_ITEM, pre_normalize=None, mean_center=True, post_normalize=True)

    mae = MAE()
    k_err = 0
    for rating, item_id, user_id in test_set.get():
        try:
            pred_rating = svd.predict(item_id, user_id)
            mae.add(rating, pred_rating)
        except KeyError:
            #print "keyerror: ===========================================================>"
            k_err += 1
            continue
    
    print "k_err", k_err, " -- ", "test-len: ", len(test_set.get()), "train-len: ", len(train_set.get())
    result = mae.compute()/2.0
    return result
 


def cross_validate(idata, count=5):
    maes = []
    for i in range(count):
        print i, "....."
        train, test = idata.split_train_test(percent=PERCENT_TRAIN)
        mae = evaulte(train,test)
        maes.append(round(mae,4))
    print maes
    print "mean: ", np.mean(maes)



if __name__ == '__main__':
    raw_data = get_twittermovie_matrix() # get_moive100k() #
    statis_data(raw_data)
    idata = prepare_data(raw_data)
    cross_validate(idata,5)

