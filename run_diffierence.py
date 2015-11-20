import sys
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import matplotlib
import numpy as np
sys.path.append("./src")
from similarities import CosineSimilarity
from dataset import get_friends_data, get_user_item_matrix
from models.friendsmodel import FriendsModel
from evaluators import EsoricsSingleUserValidation


def show_data(ivector):
    print "len of ivector: ", len(ivector)
    print "average Difference: ", np.mean(ivector)
    #hist
    #font = {'family':'normal', 'weight':'bold', 'size':22}
    matplotlib.rcParams.update({'font.size':28})
    title = "Single Friend's Influence ( Avg: "+str(round(np.mean(ivector),4))+" )"
    n, bins, patches = plt.hist(ivector, bins=200, facecolor='grey')
    plt.title(title)
    plt.xlabel("Difference")
    plt.ylabel("Frequency")
    

    plt.axis('tight')
    plt.show()

def show_statistic(ivector):
    sumx = {}
    for item in ivector:
        if item in sumx:
            sumx[item] += 1
        else:
            sumx[item] = 1
    colors = list("rgbcmyk")
    plt.scatter(sumx.keys(),sumx.values(),color=colors.pop())
    plt.legend(sumx.keys())
    plt.show()


def run_single_influence(raw_data, friend_data):
    f_n = 10
    t_n = 11
    ratio = 0.8
    esvlidation = EsoricsSingleUserValidation(5,raw_data,friend_data,f_n,t_n,ratio)
    results = esvlidation.cross_validate()
    return results


if __name__ == '__main__':
    friend_data = get_friends_data()
    raw_data = get_user_item_matrix()
    results = run_single_influence(raw_data,friend_data)
    show_data(results)
