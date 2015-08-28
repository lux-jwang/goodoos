
from sklearn.decomposition import ProjectedGradientNMF
import numpy as np
from predictor import Predictor
import time


class NMFpredictor(Predictor):
    def __init__(self,model,beta=1, eta=0.1, init='nndsvd', max_iter=500,
        n_components=100, nls_max_iter=2000, random_state=0, sparseness=None,tol=0.0001):

        self.check_non_negtive(model)
        self.model = model
        super(NMFpredictor,self).__init__()
        
        self.nmf = ProjectedGradientNMF(beta=beta, eta=eta, init=init, max_iter=max_iter,
                   n_components=n_components, nls_max_iter=nls_max_iter, random_state=random_state, 
                   sparseness=sparseness,tol=tol)
        self.user_latent_M, self.item_latent_M = self.construct_latent_matrics()

    def construct_latent_matrics(self):
    	start = time.time()
        data_matrix = self.model.get_data_matrix()
        user_latent_M = self.nmf.fit_transform(data_matrix)
        item_latent_M = self.nmf.components_
        print "use time: ", time.time() - start
        return user_latent_M, item_latent_M

    def predict(self,user_id, item_id):
        user_no = self.model.user_id_to_no[user_id]
        item_no = self.model.item_id_to_no[item_id]
        pref = np.dot(self.user_latent_M[user_no,:], self.item_latent_M[:,item_no])

        if pref > self.model.max_pref:
            pref = self.model.max_pref
        if pref < self.model.min_pref:
            pref = self.model.min_pref

        return pref

    def check_non_negtive(self,model):
        if model.min_pref < 0:
            raise NotImplementedError("non_negtive!")
