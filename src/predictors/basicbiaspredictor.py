
from predictor import Predictor

class BasicBiasPredictor(Predictor):
    def __init__(self, contributors):
        super(BasicBiasPredictor,self).__init__()
        self.contributors = contributors
        self.model = self.contributors.get_model()
        #self.user_delta_rates = {}

    def predict(self,user_id, item_id):
        ru  = self.model.get_user_rate_mean(user_id)
        nbs = self.contributors.get_neighbors(user_id,-1)
        nb_delta = self.get_delta(nbs, item_id)
        pref = ru+nb_delta
        return pref

    def get_delta(self,users,item_id):
        t_delta = 0
        t_sim = 0
        for u_id, sim in users:
            #sim = 1.0
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

