from os import path, remove
import pickle
import numpy as np
import ast

local_dir = path.dirname(path.realpath(__file__))



def get_user_id_map(src_filename='./twitter/users.dat',dst_filename="./mid_data/user_id_map.mat"):
    dat = np.loadtxt(src_filename, delimiter='::', dtype=str)
    mat = {}
    for pse_id, real_id in dat:
        mat[pse_id] = real_id
    pickle.dump(mat,open(dst_filename, "w"),protocol=2)
    return mat


def get_original_friends_data(f_num):
    src_filename=local_dir+"/mid_data/active_users.mat"        
    mat = pickle.load(open(src_filename,"rb"))
    friends_data = {}
    for ky in mat.keys():
        if len(mat[ky]) >= f_num:
            friends_data[ky] = mat[ky]
    return friends_data

def get_all_friend_ids(friends_data):
    f_f_ids = {}
    for ky in friends_data.keys():
        f_f_ids[ky] = 1
        for sub_id in friends_data[ky]:
            f_f_ids[sub_id] = 1
    return f_f_ids

def get_original_UI(rate_num):
    rating_file = local_dir+"/twitter/ratings.dat"
    id_map_file=local_dir+"/mid_data/user_id_map.mat"
    
    rate_dat = np.loadtxt(rating_file, delimiter='::', dtype=str)
    id_map = pickle.load(open(id_map_file, "rb"))

    mat = {}

    for u_id, i_id, rating, tm in rate_dat:
        if float(rating) < 0.1:
            continue

        if not u_id in id_map:
            print u_id, "!!! not exist"
            continue

        real_id = id_map[u_id]
        mat.setdefault(real_id,{})
        #print real_id, u_id
        mat[real_id][i_id] = (float(rating)/2.0,tm)

    for ky in mat.keys():
        r_nums = len(mat[ky].keys())
        if r_nums < rate_num:
            del mat[ky]

    return mat


def get_original_user_item_matrix(rate_num,friends_data):
    rating_file = local_dir+"/twitter/ratings.dat"
    id_map_file=local_dir+"/mid_data/user_id_map.mat"

    f_f_ids = get_all_friend_ids(friends_data)
    
    rate_dat = np.loadtxt(rating_file, delimiter='::', dtype=str)
    id_map = pickle.load(open(id_map_file, "rb"))

    mat = {}

    for u_id, i_id, rating, tm in rate_dat:
        if float(rating) < 0.1:
            continue

        if not u_id in id_map:
            print u_id, "!!! not exist"
            continue

        real_id = id_map[u_id]
        if real_id in f_f_ids:
            mat.setdefault(real_id,{})
            mat[real_id][i_id] = (float(rating)/2.0,tm)

    for ky in mat.keys():
        r_nums = len(mat[ky].keys())
        if r_nums < rate_num:
            del mat[ky]

    return mat


def wash_friends_data(friends_data, friends_num, ui_matrix):
    dst_filename = local_dir+"/mid_data/friends_data.mat"
    f_kys = friends_data.keys()
    l_f_d = {}
    
    for ky in f_kys:
        if ky in ui_matrix:
            f_set = []
            for u_id in friends_data[ky]:
                if u_id in ui_matrix:
                    f_set.append(u_id)
            if len(f_set) >= friends_num:
                l_f_d[ky] = f_set

    pickle.dump(l_f_d,open(dst_filename, "w"),protocol=2)

    return l_f_d

def wash_user_item_matrix(new_friends_data,ui_matrix):
    dst_filename = local_dir+"/mid_data/user_item_matrix.mat"
    f_ids = get_all_friend_ids(new_friends_data)

    f_mat = {}
    for u_id in ui_matrix.keys():
        if u_id in f_ids:
            f_mat[u_id] = ui_matrix[u_id]

    pickle.dump(f_mat,open(dst_filename, "w"),protocol=2)
    return f_mat

def construct_data_set(friend_num, rate_num):
    #0.
    if path.isfile(local_dir+"/mid_data/friends_data.mat"):
        remove(local_dir+"/mid_data/friends_data.mat")
    if path.isfile(local_dir+"/mid_data/user_item_matrix.mat"):
        remove(local_dir+"/mid_data/user_item_matrix.mat")

    #1.
    friends_data = get_original_friends_data(friend_num)
    #2.
    ui_matrix = get_original_user_item_matrix(rate_num,friends_data)
    #3.
    new_friends_data = wash_friends_data(friends_data,friend_num,ui_matrix)
    #4.
    new_ui_matrix = wash_user_item_matrix(new_friends_data,ui_matrix)

    print len(new_ui_matrix.keys())
    print len(get_all_friend_ids(new_friends_data).keys()), len(new_friends_data.keys())
    #5.

def formate_reputation_data():
    src_file = local_dir+"/mid_data/zfft.pdat"
    dst_filename = local_dir+"/mid_data/reputation.mat"
    repu = pickle.load(open(src_file,"rb"))
    for u_id in repu.keys():
        #print repu[u_id]
        tw_num, fing_num, fer_num = repu[u_id]
        tw_num = int(tw_num.replace(",", ""))
        fing_num = int(fing_num.replace(",", ""))
        fer_num = int(fer_num.replace(",", ""))
        repu[u_id] = [tw_num, fing_num, fer_num]
    pickle.dump(repu,open(dst_filename, "w"),protocol=2)   

def get_friends_data():
    dst_filename = local_dir+"/mid_data/friends_data.mat"
    if path.isfile(dst_filename):
        return pickle.load(open(dst_filename,"rb"))
    else:
        return None

def get_friends_data_index():
    friends_data = get_friends_data()
    map_dic = {}
    indx = 0
    for ky, val in friends_data.iteritems():
        if not str(ky) in map_dic:
            map_dic[str(ky)] = indx
            indx += 1
        for fitem in val:
            if not str(fitem) in map_dic:
                map_dic[str(fitem)] = indx
                indx += 1

    new_friend_data = {}

    for ky, val in friends_data.iteritems():
        new_ky = map_dic[ky]
        new_friend_data[new_ky] = []
        for fitem in val:
            new_fitem = map_dic[fitem]
            new_friend_data[new_ky].append(new_fitem)

        len1 = len(friends_data[ky])
        len2 = len(new_friend_data[new_ky])
        #print len1, len2
        if len1 != len2:
            print ky, "WRONG......................."

    if len(friends_data.keys()) != len(new_friend_data.keys()):
        print "WRONG!!!!!1111.........................."

    return (new_friend_data, map_dic)




def get_user_item_matrix():
    dst_filename = local_dir+"/mid_data/user_item_matrix.mat"
    if path.isfile(dst_filename):
        return pickle.load(open(dst_filename,"rb"))
    else:
        return None


def get_reputation():
    dst_filename = local_dir+"/mid_data/reputation.mat"
    if path.isfile(dst_filename):
        return pickle.load(open(dst_filename,"rb"))
    else:
        return None

def get_user_item_matrix_sub():
    mat = get_user_item_matrix()
    sub_mat = {}
    for u_id in mat.keys()[:5]:
        sub_mat[u_id] = mat[u_id]
        #print u_id, len(mat[u_id].keys())
    return sub_mat


def get_moive100k(load_timestamp=True):
    base_dir =  local_dir+'/movie100k/'
    #Read data
    if load_timestamp:
        data_m = np.loadtxt(base_dir + 'movielens100k.data',
                delimiter='\t', dtype=int)
        data_movies = {}
        for user_id, item_id, rating, timestamp in data_m:
            data_movies.setdefault(user_id, {})
            data_movies[user_id][item_id] = (int(rating),timestamp)
    else:
        data_m = np.loadtxt(base_dir + 'movielens100k.data',
                delimiter='\t', usecols=(0, 1, 2), dtype=int)

        data_movies = {}
        for user_id, item_id, rating in data_m:
            data_movies.setdefault(user_id, {})
            data_movies[user_id][item_id] = int(rating)

    return data_movies


def get_moive1m(load_timestamp=True):
    base_dir =  local_dir+'/movie1m/'
    #Read data
#    if load_timestamp:
#        data_m = np.loadtxt(base_dir + 'movielens1m.item',
#                delimiter='\t', dtype=int)
#        data_movies = {}
#        for user_id, item_id, rating, timestamp in data_m:
#            data_movies.setdefault(user_id, {})
#            data_movies[user_id][item_id] = (int(rating),timestamp)
#    else:
    data_m = np.loadtxt(base_dir + 'movielens1m.data',
            delimiter='\t', usecols=(0, 1, 2), dtype=int)
    data_movies = {}
    for user_id, item_id, rating in data_m:
        data_movies.setdefault(user_id, {})
        data_movies[user_id][item_id] = int(rating)

    return data_movies

	
def get_twittermovie_matrix():
    rating_file = local_dir+"/twitter/ratings.dat"
    rate_dat = np.loadtxt(rating_file, delimiter='::', dtype=str)
    mat = {}

    for u_id, i_id, rating, tm in rate_dat:
        if float(rating) < 0.1:
            continue
        mat.setdefault(u_id,{})
        mat[u_id][i_id] = (rating,tm)

    return mat


if __name__ == '__main__':
    #get_friends_data_index()
    construct_data_set(5,5)
    #formate_reputation_data()
    
