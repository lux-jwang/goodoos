from similarity import Similarity
from dataset import get_reputation
import numpy as np

class ReputationSimilarity(Similarity):
    def __init__(self,model):
        super(ReputationSimilarity,self).__init__(model)
        #self.reputation_cache = {}
        #self.reputation_cache,self.s_max,self.s_min,self.fee_max,self.fee_min,self.fer_max,self.fer_min,self.t_max,self.t_min = self.get_repu_mat()

    def calculate_similarity(self,user_id, target_id):
        return 1.0 #self.get_scores(user_id, target_id)

    def get_scores(self,user_id, target_id):
       t_items = self.model.get_items(target_id)
       t_mean = self.model.get_user_rate_mean(target_id)
       u_mean = self.model.get_user_rate_mean(user_id)
       m_ids = len(self.model.get_mutual_item_ids(user_id, target_id))
       dif = np.abs(u_mean-t_mean)
       return len(t_items)
       #(float(m_ids)/len(t_items))*(float(len(t_items))/float(dif+1))
       #(float(len(t_items))/float(dif+1))

    def get_reputation(self, user_id):
        if not user_id in self.reputation_cache:
            return 0.0
        return self.reputation_cache[user_id]

        if user_id in self.reputation_cache:
            return self.reputation_cache[user_id]

        repo = self.model.get_reputation(user_id)
        if not repo:
            return None

        fer, fee, twt = repo
        fer, fee, twt = float(fer), float(fee), float(twt)

        if not fee*fer:
            return None

        #repu = 1.0 - float(fer)/float((fer+fee))
        repu = (float(fer)/float(fee))*(float(twt)/float(fer))
        self.reputation_cache[user_id] = repu    

        return repu

    def get_repu_mat(self):
        repu_data = self.model.reputation_data
        s_max = -9999
        s_min = 9999
        fee_max = -9999
        fee_min = 9999
        fer_max = -9999
        fer_min = 9999
        t_max = -9999
        t_min = 9999
        reputation_cache = {}
        for ky in repu_data.keys():
            fer, fee, twt = repu_data[ky]
            fer, fee, twt = float(fer), float(fee), float(twt)
            sim = self.get_one_repu(fer, fee, twt)
            reputation_cache[ky] = sim
            s_max = max(s_max,sim)
            s_min = min(s_min,sim)
            fee_max = max(fee_max,fee)
            fee_min = min(fee_min,fee)
            fer_max = max(fer_max,fer)
            fer_min = min(fer_min,fer)
            t_max = max(t_max,twt)
            t_min = min(t_min,twt)
        return reputation_cache, s_max,s_min,fee_max,fee_min,fer_max,fer_min,t_max,t_min


    def get_one_repu(self,fer, fee, twt):
        return fer+fee


    def update_cache(self,user_id1, user_id2, sim_value):
        self.similarities.setdefault(user_id1,{})
        self.similarities[user_id1][user_id2] = sim_value



