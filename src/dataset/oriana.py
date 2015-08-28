import numpy as np

from datawasher import get_original_UI, get_original_friends_data, get_user_item_matrix, get_friends_data


def get_twd_min_max_mean():
    ori_mat = get_original_UI(1)

    user_ids = {}
    item_ids = {}
    indx = 0
    r_max = 0
    r_min = 99999999
    rs = []

    print len(ori_mat.keys())

    for u_id in ori_mat.keys():
        items = ori_mat[u_id]
        user_ids[u_id] = 1

        item_num = len(items)
        r_max = max(r_max,item_num)
        r_min = min(r_min,item_num)
        rs.append(item_num)
        if item_num == 856:
            print u_id

        for i_id in items.keys():
            r,ts = items[i_id]
            item_ids[i_id] = 1
            indx += 1

    print len(user_ids.keys()), len(item_ids.keys()), indx
    print np.mean(rs), r_max, r_min



def get_ftwd_basic_info():
    mat = get_original_UI(1)
    f_data = get_original_friends_data(1)
    print len(f_data.keys())
    f_ids = {}
    item_ids = {}

    indx = 0
    r_max = 0
    r_min = 99999999
    rs = []
    f_max = 0
    f_min = 9999999
    f_means = []

    for f_id in f_data.keys():
        if f_id in mat:
            f_ids[f_id] = 1
            items = mat[f_id]
            item_num = len(items)
            r_max = max(r_max,item_num)
            r_min = min(r_min,item_num)
            rs.append(item_num)

            f_num = len(f_data[f_id])
            f_max = max(f_max,f_num)
            f_min = min(f_min,f_num)
            f_means.append(f_num)


            for i_id in items.keys():
                item_ids[i_id] = 1
                indx += 1

    print len(f_ids.keys()), len(item_ids.keys()), indx
    print r_max, r_min, np.mean(rs)
    print f_max, f_min, np.mean(f_means)


def get_sftwd_basic_info():

    mat = get_user_item_matrix()
    f_data = get_friends_data()
    print len(f_data.keys())
    f_ids = {}
    item_ids = {}

    indx = 0
    r_max = 0
    r_min = 99999999
    rs = []
    f_max = 0
    f_min = 9999999
    f_means = []

    for f_id in f_data.keys():
        if f_id in mat:
            f_ids[f_id] = 1
            items = mat[f_id]
            item_num = len(items)
            r_max = max(r_max,item_num)
            r_min = min(r_min,item_num)
            rs.append(item_num)

            f_num = len(f_data[f_id])
            f_max = max(f_max,f_num)
            f_min = min(f_min,f_num)
            f_means.append(f_num)


            for i_id in items.keys():
                item_ids[i_id] = 1
                indx += 1

    print len(f_ids.keys()), len(item_ids.keys()), indx
    print r_max, r_min, np.mean(rs)
    print f_max, f_min, np.mean(f_means)



if __name__ == '__main__':
    #get_twd_min_max_mean()

    #get_ftwd_basic_info()

    get_sftwd_basic_info()
