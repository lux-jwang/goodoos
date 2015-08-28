
from predictor import Predictor

class JphPredictor(Predictor):
    def __init__(self,contributors):
        super(JphPredictor,self).__init__()
        self.contributors = contributors
        self.model = self.contributors.get_model()
        return

    def predict(self, user_id, item_id):
        nbs = self.contributors.get_neighbors(user_id,110)
        new_nbs = nbs #self.adjust_similariry(user_id,nbs)
        t_rate = 0.0
        t_sim = 0.0

        for f_id, sim in new_nbs:
            rate = self.model.get_rate(f_id,item_id)
            if not rate is None:
                ri, ts = rate
                ri =  float(ri)*sim
                t_rate += ri
                t_sim += sim

        if t_sim > 0:
            return round(t_rate/t_sim,4)


        return 0

    def adjust_similariry(self, user_id, friends):
        new_sims = []
        for f_id,sim in friends:
            t_sim = 0.0
            if self.model.is_a_friend(user_id,f_id):
                t_sim = sim
            if self.model.is_a_friend(f_id,user_id):
                t_sim += sim
            #print round(sim,4), round(t_sim/2.0,4), t_sim
            new_sims.append((f_id,t_sim/2.0))

        return new_sims