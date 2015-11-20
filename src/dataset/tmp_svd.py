
#my mf / svd is not good enough, so I use SVD from python-recys as a substitution
import sys
from os import path
import pickle
import numpy as np
import matplotlib.pyplot as plt
#To show some messages:
import recsys.algorithm
recsys.algorithm.VERBOSE = True

from recsys.algorithm.factorize import SVD
from recsys.datamodel.data import Data
from recsys.evaluation.prediction import RMSE, MAE

from datawasher import get_friends_data, get_user_item_matrix, get_moive100k, get_moive1m

PERCENT_TRAIN = 80
local_dir = path.dirname(path.realpath(__file__))
#u_ids: [user_id,friend_id1,friend_id2...]

def get_friend_matrix(u_ids, raw_data):
    idata = Data()
    u_idx = 0
    for u_id in u_ids:
        u_idx += 1
        i_idx = 0
        i_ids = raw_data[u_id].keys()
        for i_id in i_ids:
            i_idx += 1
            rate, ts = raw_data[u_id][i_id]
            idata.add_tuple((float(rate),u_idx,i_idx))

    return idata

def is_in_train(u_id, i_id, train):
    t_d = train.get()
    u_true = False
    i_true = False
    for r,u,i in t_d:
        if u_id == u:
            u_true = True
        if i_id == i:
            i_true = False
        if u_true and i_true:
            return True
    return False

def test_in_train(test,train):
    t_d = test.get()
    for r,u,i in t_d:
        if not is_in_train(u,i, train):
            print "+===================================================+"
            print "train does not have u , i :", u, i
            print "+===================================================+"


    
def evaluate(data, count=5, K=100):
    results = []

    for i in range(count):
        train, test = data.split_train_test(percent=PERCENT_TRAIN)
        print len(data.get()), len(train.get()), len(test.get())
        #test_in_train(test, train)
        #print train.get()
        svd = SVD()
        svd.set_data(train)
        svd.compute(k=K, min_values=5, pre_normalize=None, mean_center=True, post_normalize=True)

        #Evaluation using prediction-based metrics
        rmse = RMSE()
        mae = MAE()
        for rating, item_id, user_id in test.get():
            try:
                pred_rating = svd.predict(item_id, user_id)
                rmse.add(rating, pred_rating)
                mae.add(rating, pred_rating)
            except KeyError:
                #print "keyerror: ===========================================================>"
                continue
        try:
            rsu = {}
            rsu["RMSE"] = rmse.compute()
            rsu["MAE"] = mae.compute()
            print rsu
            results.append(rsu)
        except:
            print "one error....++++++++++++++++++++++++++++++++++++++++++++++++++++"
        

    return results

def unique_list(my_list):
    uni_list = {}
    for item in my_list:
        uni_list[item] = 1

    return uni_list.keys()

def get_friend_2nd_level(f_ids,friends_data):
    second_friends = []
    for f_id in f_ids:
        if f_id in friends_data:
            scnd_fids = friends_data[f_id]
            second_friends.extend(scnd_fids)

    return unique_list(second_friends)


def friend_svd(raw_data, friends_data):
    results = {}
    ind = 0
    f_max = 0
    f_min = 999999
    f_means = []
    for u_id in friends_data.keys():
        ind += 1
        
        my_user = []
        my_user.extend(friends_data[u_id])
        f_list = get_friend_2nd_level(my_user,friends_data)
        my_user.extend(f_list)
        my_user.append(u_id)
        my_user = unique_list(my_user)
        print "----------------->: ", ind, "/", len(friends_data.keys()), len(my_user)

        
        #idata = get_friend_matrix(my_user,raw_data)
        #print "----------------------->: ", len(my_user)
        f_max = max(f_max,len(my_user))
        f_min = min(f_min, len(my_user))
        f_means.append(len(my_user))


        if len(my_user) < 1:
            print u_id, len(friends_data[u_id]), len(f_list)
            continue
        continue
        result = evaluate(idata)
        results[u_id] = result

    print f_max, f_min, np.mean(f_means)
    return

    dst_filename = local_dir+"/mid_data/ff_svd_result_friends_4.mat"
    pickle.dump(results,open(dst_filename, "w"),protocol=2)

    return results

def get_density(data):

    rating_num = len(data.get()) 
    u_all = {}
    i_all = {}
    for r,u,i in data.get():
        u_all[u] = 1
        i_all[i] = 1
    user_num = len(u_all.keys())
    item_num = len(i_all.keys())

    return float(rating_num)/float(user_num*item_num)

def get_dataset_density(friends_data,raw_data):
    ds = []
    for u_id in friends_data.keys():

        my_user = []
        my_user.extend(friends_data[u_id])
        f_list = get_friend_2nd_level(my_user,friends_data)
        my_user.extend(f_list)
        my_user.append(u_id)
        my_user = unique_list(my_user)

        idata = get_friend_matrix(my_user,raw_data)
        density = get_density(idata)*100.0
        ds.append(density)

    items_dict = {}
    rating_num = 0

    for u_id in friends_data.keys():
        items = raw_data[u_id].keys()
        for i_id in items:
            rating_num += 1
            items_dict[i_id] = 1

    item_num = len(items_dict.keys())
    user_num = len(friends_data.keys())
    wh_ds = float(rating_num)/float(item_num*user_num)
    print item_num, user_num, rating_num
    print "big mat density: ", float(rating_num)/float(item_num*user_num)
    print "friend density: ", np.mean(ds), np.min(ds),np.max(ds)
    return wh_ds, ds


def draw_me(raw_data,friends_data):
    wh_ds, ds = get_dataset_density(friends_data,raw_data)
    xx = range(len(ds))
    plt.xlim(0,830)
    plt.plot(xx,ds,"og",label="matrix density per user")
    plt.xlabel("Users")
    plt.ylabel("Density(%)")
    plt.axhline(y=wh_ds*100,color="r",linewidth = 2, label="SFMT matrix density: "+str(round(wh_ds*100,3))+"%")
    plt.legend()
    plt.show()




if __name__ == '__main__':

    friend_data_x = get_friends_data()
    raw_data_x = get_user_item_matrix()
    friend_svd(raw_data_x,friend_data_x) 


    """
    friend_data = get_friends_data()
    raw_data = get_user_item_matrix()
    results = friend_svd(raw_data,friend_data)
    for u_id in results.keys():
        print u_id
        print results[u_id]
        print "......................................"

    friends_data = get_friends_data()
    raw_data = get_user_item_matrix()
    get_dataset_density(friends_data,raw_data)
    """

