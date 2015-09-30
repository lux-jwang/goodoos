import numpy as np
import sys
import time
sys.path.append("./src")

from dataset import get_moive100k
from similarities import PhiMatrix, DeltaMatrix
from models import Model

from pylab import *



def get_model():
    raw_data = get_moive100k()
    model = Model(raw_data)
    return model


def get_matrix_delta(model,phi_mat):
    delm = DeltaMatrix(model,phi_mat)
    sim_m = delm.get_similarities_matrix() #history issue--- bad name :(
    return sim_m

def get_matrix_phi(model):
    phim = PhiMatrix(model)
    sim_m = phim.get_similarities_matrix()
    return sim_m

def get_predict(u_id, i_id, model, mat_delta,mat_phi):
    item_ids = list(model.get_items(u_id))
    nom = 0
    denom = 0

    pre_delta_xa = mat_delta[i_id]
    pre_phi_xa = mat_phi[i_id]
    pre_ratings = model.raw_data[u_id]

    for a_id in item_ids:
        if a_id == i_id:
            continue
        delta_xa = pre_delta_xa[a_id] #mat_delta[i_id][a_id]
        phi_xa = pre_phi_xa[a_id] #mat_phi[i_id][a_id]

        if delta_xa == -1000 or phi_xa == 0: #avoid such a case
            continue
        r_ua, _ = pre_ratings[a_id] #model.get_rate(u_id,a_id,ts=False)

        nom += (delta_xa+r_ua)*phi_xa
        denom += phi_xa

    if denom < 1:
        return 0
    
    return nom/denom


def get_matrix_predict(model,mat_delta,mat_phi):
    user_ids = model.get_user_ids()
    item_ids = model.get_item_ids()
    pred_matrix = {} #only predict un_rated u-i pair

    for u_id in user_ids:
        pred_matrix.setdefault(u_id,{})
        pre_model = model.raw_data[u_id]
        for i_id in item_ids:
            if i_id in pre_model:
                continue
            prid_rate = get_predict(u_id,i_id,model,mat_delta,mat_phi)
            pred_matrix[u_id][i_id] = prid_rate
            #print "predict: ", u_id, " ", i_id, " ", prid_rate

    return pred_matrix


if __name__ == '__main__':
    print "start to load data..."
    model = get_model()
    print "model is created..."
    ist = time.time()
    phi = get_matrix_phi(model)
    iend = time.time()
    print "phi cost time: ", iend-ist
    delta = get_matrix_delta(model,phi)
    ist = time.time()
    print "delta cost time: ", ist-iend
    pred = get_matrix_predict(model, delta, phi)
    iend = time.time()
    print "prediction cost time: ", iend-ist