#import argparse
#from statistics import variance #python >= 3.4
import numpy as np
import sys
import datetime
import matplotlib.pyplot as plt
sys.path.append("./src")
from models import Model, FriendsModel
from similarities import CosineSimilarity, JaccardSimilarity
from dataset import get_friends_data, get_user_item_matrix, get_user_item_matrix_sub, \
                    get_reputation, get_original_user_item_matrix,get_original_UI
from evaluators import GlobalJaccardKfold,FriendsJaccardKfold,FriendsCosineKfold, \
                       GlobalCosineKfold,NMFKfold, FriendsReputationKfold, \
                       GlobalReputationKfold, FriendStrangerKfold,\
                       JphKfold
from evaluators import root_mean_square_error, mean_absolute_error


def calculate_cosine_similarity_friends(raw_data,friend_data):

    friend_model = FriendsModel(raw_data,friend_data)
    cosine_sim = CosineSimilarity(friend_model)
    c_sims = {}

    for ky in friend_model.get_friends_roster():
        f_ids = friend_model.get_friends(ky)
        sorted_sims = cosine_sim.get_similarities(ky, f_ids)
        c_sims[ky] = sorted_sims
        #print ky, len(sorted_sims), sorted_sims

    return c_sims

def calculate_jaccard_similarity_friends(raw_data,friend_data):

    friend_model = FriendsModel(raw_data,friend_data)
    jaccard_sim = JaccardSimilarity(friend_model)
    j_sims = {}
    
    for ky in friend_model.get_friends_roster():
        f_ids = friend_model.get_friends(ky)
        sorted_sims = jaccard_sim.get_similarities(ky, f_ids)
        j_sims[ky] = sorted_sims
        #print ky, sorted_sims

    return j_sims


def calculate_cosine_similarity_global(raw_data,friend_data):
    friend_model = FriendsModel(raw_data,friend_data)
    cosine_sim = CosineSimilarity(friend_model)
    c_sims = {}

    for u_id in friend_model.get_friends_roster():
    	f_num = len(friend_model.get_friends(u_id))
        target_ids = friend_model.get_strangers_in_roster(u_id)
        sorted_sims = cosine_sim.get_similarities(u_id,target_ids)
        c_sims[u_id] = sorted_sims[:f_num]
        #print u_id, sorted_sims

    return c_sims


def calculate_jaccard_similarity_global(raw_data,friend_data):
    friend_model = FriendsModel(raw_data,friend_data)
    jaccard_sim = JaccardSimilarity(friend_model)
    j_sims = {}

    for u_id in friend_model.get_friends_roster():
    	f_num = len(friend_model.get_friends(u_id))
        target_ids = friend_model.get_strangers_in_roster(u_id)
        sorted_sims = jaccard_sim.get_similarities(u_id,target_ids)
        j_sims[u_id] = sorted_sims[:f_num]
        #print u_id, sorted_sims

    return j_sims

def calculate_rate_average_friends(raw_data, friend_data):
    friend_model = FriendsModel(raw_data,friend_data)
    roster = friend_model.get_friends_roster()
    the_variance = {}
    for u_id in roster:
        f_ids = friend_model.get_friends(u_id)
        mean_rates = friend_model.get_multiple_users_mean_rate(f_ids)
        i_rate = friend_model.get_user_rate_mean(u_id)
        the_means = []

        for ky in mean_rates.keys():
            if mean_rates[ky] == 0:
                continue
            the_means.append(mean_rates[ky])

        if not i_rate == 0:
            #should always be here
            the_means.append(i_rate)

        the_variance[u_id] = np.var(the_means)
        #print u_id, the_variance[u_id]

    return the_variance

def calculate_rate_average_global(raw_data, friend_data):
    friend_model = FriendsModel(raw_data,friend_data)
    jaccard_sim = CosineSimilarity(friend_model)
    roster = friend_model.get_friends_roster()
    the_variance = {}
    for u_id in roster:
        f_ids = friend_model.get_strangers_in_roster(u_id)
        f_num = len(friend_model.get_friends(u_id))
        sorted_sims = jaccard_sim.get_similarities(u_id,f_ids)[:f_num]
        t_ids = []
        for u_id, sim in sorted_sims:
        	t_ids.append(u_id)

        mean_rates = friend_model.get_multiple_users_mean_rate(t_ids)
        i_rate = friend_model.get_user_rate_mean(u_id)
        the_means = []

        for ky in mean_rates.keys():
            if mean_rates[ky] == 0:
                continue
            the_means.append(mean_rates[ky])

        if not i_rate == 0:
            #should always be here
            the_means.append(i_rate)

        the_variance[u_id] = np.var(the_means)

    return the_variance


def calculate_rate_time_distribution_friends():
    return

def calculate_rate_time_distribution_global():
    return

def get_metrics_methods():
    return {"RMSE":root_mean_square_error,
            "MAE": mean_absolute_error}

def calculate_cosine_rmse_friends(raw_data,friend_data):
    mtrs = get_metrics_methods()
    fckx = FriendsCosineKfold(5,raw_data,friend_data,mtrs)
    fckx.cross_validate()
    return

def calculate_cosine_friends_strangers(raw_data,friend_data):
    f_ts = [(10,10),(20,10),(30,10),(40,10),(50,10)]
    #f_ts = [(50,10)]
    f_ratios = [0.5,0.6,0.7,0.8,0.9,1.0]
    mtrs = get_metrics_methods()
    results = {}

    for f_n, t_n in f_ts:
        for ratio in f_ratios:
            ky = str(f_n)+"-"+str(t_n)+"-"+str(ratio)
            print ky
            ftkflod = FriendStrangerKfold(5,raw_data,friend_data,mtrs,f_n,t_n,ratio)
            meanrs = ftkflod.cross_validate()
            results[ky] = round(meanrs,4)

    print results
    return results

def calculate_cosine_rmse_global(raw_data,friend_data):
    mtrs = get_metrics_methods()
    gckx = GlobalCosineKfold(5,raw_data,friend_data,mtrs)
    gckx.cross_validate()
    return 

def calculate_jaccard_rmse_friends(raw_data,friend_data):
    mtrs = get_metrics_methods()
    fjkx = FriendsJaccardKfold(5,raw_data,friend_data,mtrs)
    fjkx.cross_validate()
    return

def calculate_jaccard_rmse_global(raw_data,friend_data):
    mtrs = get_metrics_methods()
    gjkx = GlobalJaccardKfold(5,raw_data,friend_data,mtrs)
    gjkx.cross_validate()
    return

def calculate_nmf_rmse_global(raw_data):
    mtrs = get_metrics_methods()
    nkx = NMFKfold(5,raw_data,mtrs)
    nkx.cross_validate()
    return

def calculate_reputation_rmse_friends(raw_data,Friends_data,reputation_data):
    mtrs = get_metrics_methods()
    rkx = FriendsReputationKfold(5,raw_data,Friends_data,reputation_data,mtrs)
    rkx.cross_validate()
    return


def calculate_reputation_rmse_strangers(raw_data,Friends_data,reputation_data):
    mtrs = get_metrics_methods()
    gkx = GlobalReputationKfold(5,raw_data,Friends_data,reputation_data,mtrs)
    gkx.cross_validate()
    return

def calculate_jph(raw_data,Friends_data):
    mtrs = get_metrics_methods()
    jkx = JphKfold(5,raw_data,Friends_data,mtrs)
    mscore = jkx.cross_validate()
    print mscore
    return

def calculate_genre_distribution_friends():
    return

def calculate_genre_distribution_global():
    return

def calculate_time_by_hours_global(rw_data):
    print len(rw_data.keys())
    model = Model(rw_data)
    iplot = {}
    print len(model.get_user_ids())
    
    for u_id in model.get_user_ids():
        rates = model.get_rates(u_id)
        for i_id in rates.keys():
            ra, ts = rates[i_id]
            timestamp = float(ts)
            value = datetime.datetime.fromtimestamp(timestamp)
            hr = value.hour
            if hr in iplot:
                iplot[hr] = iplot[hr] + 1
            else:
                iplot[hr] = 1

    return iplot

def tidy_plot(data):
    xx = data.keys()
    yy = []
    for ky in data.keys():
        yy.append(data[ky])

    yy1 = yy[8:]
    yy1.extend(yy[:8])
    #print yy1

    return xx, yy1

def draw_plot(datas):
    xx = []
    yy = []
    for data in datas:
        x, y = tidy_plot(data)
        xx.append(x)
        yy.append(y)


    my_xticks = []

    for i in range(24):
        my_xticks.append((i+8)%24)

    print my_xticks

    plt.xticks(xx[0], my_xticks)
    plt.plot(xx[0],yy[0],label="$origin$",color="red",linewidth=2)
    plt.show()



def get_args():
    return

def show_dict(the_dict):
    total_v = 0.0
    for ky in the_dict.keys():
        total_v+=the_dict[ky]

    print len(the_dict.keys())
    print total_v/len(the_dict.keys())


if __name__ == '__main__':
    #raw_data = get_original_UI(1)#get_original_user_item_matrix() #get_user_item_matrix()
    friend_data_1 = get_friends_data()
    raw_data_1 = get_user_item_matrix()
    #calculate_jph(raw_data_1,friend_data_1)
    calculate_cosine_friends_strangers(raw_data_1,friend_data_1)
    
    #reputation_data = get_reputation()
    #calculate_reputation_rmse_friends(raw_data,friend_data,reputation_data)
    #calculate_reputation_rmse_strangers(raw_data,friend_data,reputation_data)
    #calculate_nmf_rmse_global(raw_data)
    #var_arr = calculate_rate_average_global(raw_data,friend_data)
    #total = 0.0
    #for u_id in var_arr.keys():
    #    var1 = var_arr[u_id]
    #    total += var1

    #avg = total/float(len(var_arr.keys()))
    #print avg
    #calculate_jaccard_rmse_global(raw_data,friend_data)
    '''
    sims = calculate_jaccard_similarity_global(raw_data,friend_data)

    sim_arr = []
    for u_id in sims.keys():
        for one in sims[u_id]:
            s_id, sim = one
            sim_arr.append(sim)

    print np.mean(sim_arr)

    '''
    #calculate_jaccard_rmse_global(raw_data,friend_data)
    #print "------------------------------------"
    #calculate_cosine_rmse_global(raw_data,friend_data)
    #print "------------------------------------"
    

    #calculate_rate_average_friends
    #print "------------------------------------"
    #calculate_rate_average_friends(raw_data,friend_data)

    #calculate_cosine_similarity_global(raw_data,friend_data)
    #print sims


    #print raw_data["207625110"]
    #print friend_data["207625110"]
    #calculate_cosine_similarity_friends
    #calculate_jaccard_similarity_friends
    #calculate_cosine_similarity_global
    #calculate_jaccard_similarity_global
    
    #calculate_rate_average_global
    #calculate_rate_average_friends
    #var_dic = calculate_rate_average_global(raw_data,friend_data)
    #show_dict(var_dic)
    #calculate_rmse_friends(raw_data,friend_data)

