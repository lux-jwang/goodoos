from evaluator import Evaluator
from models.model import Model
from models.friendsmodel import FriendsModel
from models.reputationmodel import ReputationModel
from predictors.basicbiaspredictor import BasicBiasPredictor
from predictors.esoricspredictor import EsoricsPredictor
from predictors.nmfpredictor import NMFpredictor
from predictors.jphpredictor import JphPredictor
from predictors.contributors import Neighbors, Friends, Neighbors_Friends, Friends_Strangers,JphNeighbors
from similarities.cosinesimilarity import CosineSimilarity
from similarities.jaccardsimilarity import JaccardSimilarity
from similarities.reputationsimilarity import ReputationSimilarity


class GlobalConsineEvaluator(Evaluator):
    def __init__(self,training_set, testing_set, friends_data):
        self.friends_data = friends_data
        super(GlobalConsineEvaluator,self).__init__(training_set, testing_set)
        
        return

    def build_model(self,train_set):
        i_model = FriendsModel(train_set,self.friends_data)
        return i_model

    def build_predictor(self, model):
        similarity = CosineSimilarity(model)
        ctrbtor = Neighbors_Friends(similarity)
        predictor = BasicBiasPredictor(ctrbtor)
        return predictor

    def get_testing_users(self):
        return self.friends_data.keys()

class GlobalJaccardEvaluator(Evaluator):
    def __init__(self,training_set, testing_set, friends_data):
        self.friends_data = friends_data
        super(GlobalJaccardEvaluator,self).__init__(training_set, testing_set)
        
        return

    def build_model(self,train_set):
        i_model = FriendsModel(train_set,self.friends_data)
        return i_model

    def build_predictor(self, model):
        similarity = JaccardSimilarity(model)
        ctrbtor = Neighbors_Friends(similarity)
        predictor = BasicBiasPredictor(ctrbtor)
        return predictor

    def get_testing_users(self):
        return self.friends_data.keys()


class FriendsConsineEvaluator(Evaluator):
    def __init__(self,training_set, testing_set, friends_data):
        self.friends_data = friends_data
        super(FriendsConsineEvaluator,self).__init__(training_set, testing_set)      
        return

    def build_model(self,train_set):
        i_model = FriendsModel(train_set,self.friends_data)
        return i_model

    def build_predictor(self, model):
        similarity = CosineSimilarity(model)
        ctrbtor = Friends(similarity)
        predictor = BasicBiasPredictor(ctrbtor)
        return predictor

    def get_testing_users(self):
        return self.friends_data.keys()

class FriendsJaccardEvaluator(Evaluator):
    def __init__(self,training_set, testing_set, friends_data):
        self.friends_data = friends_data
        super(FriendsJaccardEvaluator,self).__init__(training_set, testing_set)     
        return

    def build_model(self,train_set):
        i_model = FriendsModel(train_set, self.friends_data)
        return i_model

    def build_predictor(self, model):
        similarity = JaccardSimilarity(model)
        ctrbtor = Friends(similarity)
        predictor = BasicBiasPredictor(ctrbtor)
        return predictor

    def get_testing_users(self):
        return self.friends_data.keys()

class NMFevaluator(Evaluator):
    def __init__(self,training_set, testing_set):
        super(NMFevaluator,self).__init__(training_set, training_set)     
        return

    def build_model(self,train_set):
        i_model = Model(train_set)
        return i_model

    def build_predictor(self, model):
        predictor = NMFpredictor(model=model,n_components=10,tol=0.0001)
        return predictor

class FriendsReputationEvaluator(Evaluator):
    def __init__(self,training_set, testing_set, friends_data, reputation_data):
        self.reputation_data = reputation_data
        self.friends_data = friends_data
        super(FriendsReputationEvaluator,self).__init__(training_set, testing_set)     
        return


    def build_model(self,train_set):
        i_model = ReputationModel(train_set, self.friends_data, self.reputation_data)
        return i_model

    def build_predictor(self, model):
        similarity = ReputationSimilarity(model)
        ctrbtor = Friends(similarity)
        predictor = BasicBiasPredictor(ctrbtor)
        return predictor

    def get_testing_users(self):
        return self.friends_data.keys()

class GlobalReputationEvaluator(Evaluator):
    def __init__(self,training_set, testing_set, friends_data, reputation_data):
        self.reputation_data = reputation_data
        self.friends_data = friends_data
        super(GlobalReputationEvaluator,self).__init__(training_set, testing_set)     
        return


    def build_model(self,train_set):
        i_model = ReputationModel(train_set, self.friends_data, self.reputation_data)
        return i_model

    def build_predictor(self, model):
        similarity = ReputationSimilarity(model)
        ctrbtor = Neighbors_Friends(similarity)
        predictor = BasicBiasPredictor(ctrbtor)
        return predictor

    def get_testing_users(self):
        return self.friends_data.keys()

class FriendStrangerEvaluator(Evaluator):
    def __init__(self,training_set, testing_set, friends_data, f_n, t_n, f_ratio):
        self.friends_data = friends_data
        self.f_n = f_n
        self.t_n = t_n
        self.f_ratio = f_ratio
        super(FriendStrangerEvaluator,self).__init__(training_set,testing_set)
        return

    def build_model(self,train_set):
        i_model = FriendsModel(train_set, self.friends_data)
        return i_model

    def build_predictor(self,model):
        similarity = CosineSimilarity(model)
        ctrbtor = Friends_Strangers(similarity,self.f_n,self.t_n)
        predictor = EsoricsPredictor(ctrbtor,self.f_ratio)
        return predictor

    def get_testing_users(self):
        return self.friends_data.keys()


class JphEvaluator(Evaluator):
    def __init__(self,training_set,testing_set,friends_data=None):
        self.friends_data = friends_data
        super(JphEvaluator,self).__init__(training_set,testing_set)

    def build_model(self,train_set):
        i_model = None
        if self.friends_data:
            i_model = FriendsModel(train_set, self.friends_data)
        else:
            i_model = Model(train_set)
        return i_model

    def build_predictor(self,model):
        similarity = CosineSimilarity(model)
        ctrbtor = None
        if self.friends_data:
            ctrbtor = Friends(similarity)
        else:
            ctrbtor = JphNeighbors(similarity)
        predictor = JphPredictor(ctrbtor)
        return predictor

    #def get_testing_users(self):
    #    return self.friends_data.keys()



        