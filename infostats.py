import sys
sys.path.append("./src")
from similarities import CosineSimilarity, JaccardSimilarity
from dataset import get_friends_data, get_user_item_matrix
from models.friendsmodel import FriendsModel
import matplotlib.pyplot as plt
import matplotlib
import numpy as np


def create_model():
    raw_data = get_user_item_matrix()
    friend_data = get_friends_data()
    i_model = FriendsModel(raw_data, friend_data)
    return i_model

def get_friends_level_2(model):
    f_ids = model.get_friends_roster()
    #f_s = {}
    t_f = []
    min_f = 999999
    max_f = 0
    for f_id in f_ids:
        ff_ids = model.get_friends(f_id,2)
        #f_s[f_id] = len(ff_ids)
        t_f.append(len(ff_ids))
        min_f = min(len(ff_ids),min_f)
        max_f = max(len(ff_ids),max_f)

    print "avg", int(np.mean(t_f)+0.5)
    print "min_f", min_f
    print "max_f", max_f

    matplotlib.rcParams.update({'font.size':28})

    plt.hist(t_f, bins=10, facecolor='grey')
    plt.title("Friend Num Level-2 Histogram")
    plt.xlabel("Friend Num")
    plt.ylabel("Frequency")
    plt.axis('tight')
    plt.show()


if __name__ == '__main__':
    i_model = create_model()
    get_friends_level_2(i_model)