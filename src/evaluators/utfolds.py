from kfold import KFold
from evaluator import Evaluator
from evaluators.childevaluators import GlobalConsineEvaluator, GlobalJaccardEvaluator
from evaluators.childevaluators import FriendsConsineEvaluator, FriendsJaccardEvaluator
from evaluators.childevaluators import NMFevaluator, FriendsReputationEvaluator,\
                                       GlobalReputationEvaluator, FriendStrangerEvaluator,\
                                       JphEvaluator


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




