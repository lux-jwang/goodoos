import numpy as np
from similarity import Similarity

class DeltaMatrix(Similarity):
    def __init__(self,model,phi_mat):
        super(DeltaMatrix,self).__init__(model)
        self.phi_mat = phi_mat
        return

    def get_similarities_matrix(self):
        if self.sim_mat_done:
            return self.similarities
    
        all_item_ids = self.model.get_item_ids()
        cidx = 0
        for i_id in all_item_ids:
            self.get_similarities(i_id,all_item_ids[cidx:])
            cidx += 1

        self.sim_mat_done = True
        return self.similarities

    def calculate_similarity(self,user_id, target_id):  #user_id -> item_id, debt for bad framework
        if user_id == target_id:
            return 0
        phiab = self.phi_mat[user_id][target_id]
        if phiab < 1:
            return -1000
        comm_list = self.model.get_mutual_user_ids(user_id,target_id)
        t_num = 0
        for c_i in comm_list:
            ia = self.model.get_rate(c_i,user_id,ts=False)
            ib = self.model.get_rate(c_i,target_id,ts=False)
            t_num += (ia-ib)

        return t_num/phiab


    def update_cache(self,user_id1, user_id2, sim_value):
        self.similarities.setdefault(user_id1,{})
        self.similarities[user_id1][user_id2] = sim_value
        self.similarities[user_id1][user_id1] = 0
        
        self.similarities.setdefault(user_id2,{})
        self.similarities[user_id2][user_id1] = -sim_value
        self.similarities[user_id2][user_id2] = 0
