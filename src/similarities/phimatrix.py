import numpy as np
from similarity import Similarity

class PhiMatrix(Similarity):
    def __init__(self,model):
        super(PhiMatrix,self).__init__(model)
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
            return len(self.model.get_users(user_id))
        comm_list = self.model.get_mutual_user_ids(user_id,target_id)
        if comm_list is None:
            return 0
        return len(comm_list)

    def update_cache(self,user_id1, user_id2, sim_value):
        self.similarities.setdefault(user_id1,{})
        self.similarities[user_id1][user_id2] = sim_value
        self.similarities[user_id1][user_id1] = len(self.model.get_users(user_id1))
        
        self.similarities.setdefault(user_id2,{})
        self.similarities[user_id2][user_id1] = sim_value
        self.similarities[user_id2][user_id2] = len(self.model.get_users(user_id2))
