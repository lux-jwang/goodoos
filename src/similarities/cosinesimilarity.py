import numpy as np
from similarity import Similarity
from distances import cosine_distances

class CosineSimilarity(Similarity):
    def __init__(self,model):
        super(CosineSimilarity,self).__init__(model)
        return

    def calculate_similarity(self,user_id, target_id):
        if user_id == target_id:
            return 1.0
        comm_i_ids = self.model.get_mutual_item_ids(user_id,target_id)
        if not comm_i_ids:
            return 0.0

        pref_u = []
        pref_t = []

        for i_id in comm_i_ids:
            rat_u, ts = self.model.get_rate(user_id,i_id)
            rat_t, ts = self.model.get_rate(target_id,i_id)
            if int(rat_u)<1 or int(rat_u)<1:
                continue
            pref_u.append(float(rat_u))    
            pref_t.append(float(rat_t))

        sim = cosine_distances([pref_u],[pref_t]).flatten()[0]
        #print user_id, target_id, ": ", sim
        return sim  #if sim < 1.0 else 1.0
    
