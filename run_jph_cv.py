import numpy as np
import sys
import datetime
import matplotlib.pyplot as plt
sys.path.append("./src")
from models import Model, FriendsModel
from similarities import CosineSimilarity, JaccardSimilarity
from dataset import get_friends_data, get_user_item_matrix, get_user_item_matrix_sub, \
                    get_reputation, get_original_user_item_matrix,get_original_UI, \
                    get_moive100k, get_moive1m
from evaluators import GlobalJaccardKfold,FriendsJaccardKfold,FriendsCosineKfold, \
                       GlobalCosineKfold,NMFKfold, FriendsReputationKfold, \
                       GlobalReputationKfold, FriendStrangerKfold,\
                       JphKfold
from evaluators import root_mean_square_error, mean_absolute_error

def get_metrics_methods():
    return {"RMSE":root_mean_square_error,
            "MAE": mean_absolute_error}

def  get_moive100k_acc_cv():
    raw_data = get_moive100k()
    mtrs = get_metrics_methods()
    jkx = JphKfold(5,raw_data,metrics=mtrs)
    mscore = jkx.cross_validate()
    print mscore
    return

def  get_moive1m_acc_cv():
    raw_data = get_moive1m()
    mtrs = get_metrics_methods()
    jkx = JphKfold(5,raw_data,metrics=mtrs)
    mscore = jkx.cross_validate()
    print mscore
    return

if __name__ == '__main__':
    get_moive100k_acc_cv()