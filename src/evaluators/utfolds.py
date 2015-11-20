
import numpy as np
from multiprocessing import Pool
from kfold import KFold
from evaluator import Evaluator
from evaluators.childevaluators import GlobalConsineEvaluator, GlobalJaccardEvaluator
from evaluators.childevaluators import FriendsConsineEvaluator, FriendsJaccardEvaluator
from evaluators.childevaluators import NMFevaluator, FriendsReputationEvaluator,\
                                       GlobalReputationEvaluator, FriendStrangerEvaluator,\
                                       JphEvaluator, EsoricsSingleUserInfluenceEvaluator


class GlobalCosineKfold(KFold):
    def __init__(self,k,data_set,friends_data,metrics):
        self.metrics = metrics
        self.friends_data = friends_data
        super(GlobalCosineKfold,self).__init__(k,data_set)     
        return

    def validate(self,train_set,test_set):
        valuator = GlobalConsineEvaluator(train_set,test_set,self.friends_data)
        return valuator.evaluate(self.metrics)
        

class FriendsCosineKfold(KFold):
    def __init__(self,k,data_set,friends_data,metrics):
        super(FriendsCosineKfold,self).__init__(k,data_set)
        self.metrics = metrics
        self.friends_data = friends_data
        return

    def validate(self,train_set,test_set):
        valuator = FriendsConsineEvaluator(train_set,test_set,self.friends_data)
        return valuator.evaluate(self.metrics)
        


class GlobalJaccardKfold(KFold):
    def __init__(self,k,data_set,friends_data,metrics):
        super(GlobalJaccardKfold,self).__init__(k,data_set)
        self.metrics = metrics
        self.friends_data = friends_data
        return

    def validate(self,train_set,test_set):
        valuator = GlobalJaccardEvaluator(train_set,test_set,self.friends_data)
        return valuator.evaluate(self.metrics)
        

class FriendsJaccardKfold(KFold):
    def __init__(self,k,data_set,friends_data,metrics):
        super(FriendsJaccardKfold,self).__init__(k,data_set)
        self.metrics = metrics
        self.friends_data = friends_data
        return

    def validate(self,train_set,test_set):
        valuator = FriendsJaccardEvaluator(train_set,test_set,self.friends_data)
        return valuator.evaluate(self.metrics)

class NMFKfold(KFold):
    def __init__(self,k,data_set,metrics):
        super(NMFKfold,self).__init__(k,data_set)
        self.metrics = metrics
        return

    def validate(self,train_set,test_set):
        valuator = NMFevaluator(train_set,test_set)
        return valuator.evaluate(self.metrics)

class FriendsReputationKfold(KFold):
    def __init__(self,k,data_set,friends_data,reputation_data,metrics):
        super(FriendsReputationKfold,self).__init__(k,data_set)
        self.metrics = metrics
        self.reputation_data = reputation_data
        self.friends_data = friends_data
        return

    def validate(self,train_set,test_set):
        valuator = FriendsReputationEvaluator(train_set, test_set, self.friends_data, self.reputation_data)
        return valuator.evaluate(self.metrics)


class GlobalReputationKfold(KFold):
    def __init__(self,k,data_set,friends_data,reputation_data,metrics):
        super(GlobalReputationKfold,self).__init__(k,data_set)
        self.metrics = metrics
        self.reputation_data = reputation_data
        self.friends_data = friends_data
        return

    def validate(self,train_set,test_set):
        valuator = GlobalReputationEvaluator(train_set, test_set, self.friends_data, self.reputation_data)
        return valuator.evaluate(self.metrics)

class FriendStrangerKfold(KFold):
    def __init__(self,k,data_set,friends_data,metrics, f_n, t_n, f_ratio):
        super(FriendStrangerKfold,self).__init__(k,data_set)
        self.metrics = metrics
        self.friends_data = friends_data
        self.f_n = f_n
        self.t_n = t_n
        self.f_ratio = f_ratio
        return

    def validate(self,train_set,test_set):
        valuator = FriendStrangerEvaluator(train_set, test_set, self.friends_data, self.f_n, self.t_n, self.f_ratio)
        return valuator.evaluate(self.metrics)


class JphKfold(KFold):
    def __init__(self,k,data_set,metrics, friends_data=None): 
        super(JphKfold,self).__init__(k,data_set)
        self.metrics = metrics
        self.friends_data = friends_data
        return

    def validate(self,train_set,test_set):
        valuator = JphEvaluator(train_set, test_set, self.friends_data)
        return valuator.evaluate(self.metrics)


class EsoricsSingleUserValidation(KFold):
    def __init__(self,k,data_set,friends_data, f_n, t_n, f_ratio):
        super(EsoricsSingleUserValidation,self).__init__(k,data_set)
        self.friends_data = friends_data
        self.f_n = f_n
        self.t_n = t_n
        self.f_ratio = f_ratio

        return

    def cross_validate(self):
        xresults = []
        tt_idx = 0
        ss_idx = 0
        ssum_idx = 0

        for oth in range(0,50):  #spcial test trick
            print "start: ", oth, "/50 run..."
            for ith in range(0,self.K):               
                train_set, test_set = self.constuct_data_set(ith)
                result, t_idx, s_idx, sum_idx = self.validate(train_set,test_set)
                xresults.extend(result)
                tt_idx += t_idx
                ss_idx += s_idx
                ssum_idx += sum_idx
            valuator = EsoricsSingleUserInfluenceEvaluator(None, None, None, 0, 0, 0)
            valuator.reset_predictor_cache()
        print ":=> ", tt_idx, " ", ss_idx, " ", ssum_idx
        return xresults


    def validate(self,train_set,test_set):
        valuator = EsoricsSingleUserInfluenceEvaluator(train_set, test_set, self.friends_data, self.f_n, self.t_n, self.f_ratio)
        res1, t_idx, s_idx, sum_idx = valuator.evaluate()
        return res1, t_idx, s_idx, sum_idx



