
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
        tnb_delta = self.get_delta(ts,item_id)
        pref = ru+tnb_delta

        return pref

    def get_delta(self,users,item_id):
        t_delta = 0
        t_sim = 0
        for u_id, sim in users:
            delta = self.get_one_delta(u_id,item_id)
            if delta is None:
                continue
            t_delta += float(delta)*float(sim)
            t_sim += sim
        
        if t_sim == 0:
            return 0.0
        r_d = float(t_delta)/float(t_sim)
        return r_d

    def get_one_delta(self,user_id,item_id):
        delta = None
        ru  = self.model.get_user_rate_mean(user_id)
        rate = self.model.get_rate(user_id,item_id)
        if not rate is None:
            ri, ts = rate
            delta = float(ri)-ru

        return delta
