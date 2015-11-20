import numpy as np
from predictor import Predictor

class EsoricsPredictor(Predictor):
    def __init__(self, contributors, f_ratio):
        super(EsoricsPredictor,self).__init__()
        self.contributors = contributors
        self.model = self.contributors.get_model()
        self.f_ratio = f_ratio
        return

    def predict(self, user_id, item_id):
        pf = self.predict_by_friends(user_id,item_id)
        pt = self.predict_by_strangers(user_id,item_id)

        return self.f_ratio*pf + (1-self.f_ratio)*pt

    def predict_by_friends(self, user_id, item_id):
        ru  = self.model.get_user_rate_mean(user_id)
        fs = self.contributors.get_rand_friends(user_id)
        fnb_delta = self.get_delta(fs,item_id)
        pref = ru+fnb_delta
        return pref

    def predict_by_strangers(self, user_id, item_id):
        ru  = self.model.get_user_rate_mean(user_id)
        ts = self.contributors.get_rand_strangers(user_id)
        tnb_delta  = self.get_delta(ts,item_id)
        pref = ru+tnb_delta

        return pref

    def get_delta(self,users,item_id):
        t_delta = 0
        t_sim = 0
        r_d = 0.0

        for u_id, sim in users:
            delta = self.get_one_delta(u_id,item_id)
            if delta is None:
                continue
            t_delta += float(delta)*float(sim)
            t_sim += sim
        
        if np.abs(t_sim) > 0:
            r_d = float(t_delta)/float(t_sim)

        return r_d
        
        

    def get_one_delta(self,user_id,item_id):
        delta = None
        rate = self.model.get_rate(user_id,item_id)
        if not rate is None:
            ru  = self.model.get_user_rate_mean(user_id)
            ri, _ = rate
            delta = float(ri)-ru

        return delta


class EsoricsPredictor_F1(EsoricsPredictor):
    user_cache = {}
    def __init__(self, contributors, f_ratio):
        super(EsoricsPredictor_F1,self).__init__(contributors, f_ratio)
        #self.friends_cache = None
        self.oed = 0
        return

    def get_target_users(self,user_id):
        if user_id in EsoricsPredictor_F1.user_cache:
            t_users = EsoricsPredictor_F1.user_cache[user_id]
        else:
            t_users = self.contributors.get_rand_friends(user_id)
            EsoricsPredictor_F1.user_cache[user_id] = t_users
        return t_users

    def reset_user_cache(self,user_id):
        EsoricsPredictor_F1.user_cache = None
        return
    
    def get_rating_detail(self, u_ids, i_id):
        ratings = []
        for u_id,sim in u_ids:
            rating = self.model.get_rate(u_id,i_id, ts = False)
            if not rating:
                rating = 0
            else:
                rating = 1
            ratings.append(rating)
        return ratings
        

    def predict_by_friends(self, user_id, item_id):
        ru  = self.model.get_user_rate_mean(user_id)
        fs = None
        fnb_delta = 0
        t_fs = self.get_target_users(user_id)
        self.rating_x = self.get_rating_detail(t_fs,item_id)
        if self.oed%2 == 0:   
            fs = t_fs[:-1]
            fnb_delta = self.get_delta(fs,item_id)
        else:
            fs = t_fs[1:]
            fnb_delta = self.get_delta(fs,item_id)

        self.oed += 1

        pref = ru+fnb_delta
        return pref

class EsoricsPredictor_T1(EsoricsPredictor):
    user_cache = {}
    def __init__(self, contributors, f_ratio):
        super(EsoricsPredictor_T1,self).__init__(contributors, f_ratio)
        self.oed = 0
        return

    def reset_user_cache(self,user_id):
        EsoricsPredictor_T1.user_cache = None
        return

    def get_rating_detail(self, u_ids, i_id):
        ratings = []
        for u_id,sim in u_ids:
            rating = self.model.get_rate(u_id,i_id, ts = False)
            if not rating:
                rating = 0
            else:
                rating = 1
            ratings.append(rating)
        return ratings

    def predict_by_strangers(self, user_id, item_id):
        ru  = self.model.get_user_rate_mean(user_id)
        fs = []
        t_fs = self.get_target_users(user_id)
        self.rating_x = self.get_rating_detail(t_fs,item_id)
        if self.oed%2 == 0:   
            fs = t_fs[:-1]
        else:
            fs = t_fs[1:] 
        self.oed += 1
        fnb_delta = self.get_delta(fs,item_id)
        pref = ru+fnb_delta

        return pref

    def get_target_users(self,user_id):
        if user_id in EsoricsPredictor_T1.user_cache:
            t_users = EsoricsPredictor_T1.user_cache[user_id]
        else:
            t_users = self.contributors.get_rand_strangers(user_id)
            EsoricsPredictor_T1.user_cache[user_id] = t_users
        return t_users

