
from distances import jaccard_coefficient, cosine_distances
#model includes friends information
class Similarity(object):
    def __init__(self,model):
        self.model = model
        self.similarities = {}
        self.sim_mat_done = False
        return

    def get_model(self):
        return self.model
        
    def get_similarities_matrix(self):
        if sim_mat_done:
            return self.similarities
    
        all_users_ids = self.model.get_user_ids()
        cidx = 0
        for u_id in all_users_ids:
            get_similarities(u_id,all_users_ids[cidx:])
            cidx += 1

        self.sim_mat_done = True
        return self.similarities

    def get_similarities(self,user_id, target_ids=None):
        sims = []
        if target_ids is None:
            target_ids = list(self.model.get_user_ids())
            target_ids.remove(user_id)

        for u_id in target_ids:
            i_sim = self.get_similarity(user_id,u_id)
            if i_sim > 0:
                sims.append((u_id,i_sim))

        tops = sorted(sims, key=lambda x: -x[1])
        return tops
        

    def calculate_similarity(self,user_id, target_id):
        raise NotImplementedError("cannot instantiate Abstract Base Class")

    
    def get_similarity(self,user_id, target_id):
        if self.is_calculated(user_id, target_id):
            return self.similarities[user_id][target_id]

        sim = self.calculate_similarity(user_id, target_id)
        self.update_cache(user_id, target_id, sim)
        return sim

    def update_cache(self,user_id1, user_id2, sim_value):
        self.similarities.setdefault(user_id1,{})
        self.similarities[user_id1][user_id2] = sim_value
        self.similarities[user_id1][user_id1] = 1.0
        
        self.similarities.setdefault(user_id2,{})
        self.similarities[user_id2][user_id1] = sim_value
        self.similarities[user_id2][user_id2] = 1.0

    def is_calculated(self,user_id1,user_id2):
        if not user_id1 in self.similarities:
            return False
        if not user_id2 in self.similarities[user_id1]:
            return False
        return True
