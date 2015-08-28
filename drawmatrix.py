import sys
sys.path.append("./src")
from similarities import CosineSimilarity, JaccardSimilarity
from dataset import get_friends_data, get_user_item_matrix
from models.friendsmodel import FriendsModel
#import matplotlib.pyplot as plt
from pylab import *

if __name__ == '__main__':
    raw_data = get_user_item_matrix()
    friend_data = get_friends_data()
    i_model = FriendsModel(raw_data, friend_data)
    data = i_model.get_data_matrix()

    figure(1)
    imshow(data,interpolation='bilinear')
    grid(True)
    show()