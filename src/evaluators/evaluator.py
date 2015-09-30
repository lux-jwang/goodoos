import numpy as np

class Evaluator(object):
    def __init__(self, training_set, testing_set):
        if training_set and testing_set:
            self.training_model = self.build_model(training_set)
            self.testing_model = self.build_model(testing_set)
            self.predictor = self.build_predictor(self.training_model)
        return


    def evaluate(self,metrics):
        est_preferneces = []
        real_preferneces = []

        test_u_ids = self.get_testing_users()

        for u_id in test_u_ids:
            test_item_ids = self.testing_model.get_items(u_id)
            est_prefs = self.predictor.estimate_preference_mul_items(u_id,test_item_ids)
            est_preferneces.extend(est_prefs)
            user_rates = self.testing_model.raw_data[u_id]
            for t_id in test_item_ids:
                rate, __ = user_rates[t_id]
                #rate = self.testing_model.get_rate(u_id,t_id,ts=False)
                real_preferneces.append(float(rate))  

        #a2 = np.subtract(est_preferneces,real_preferneces)
        result = self.calculate_metrics(est_preferneces,real_preferneces,metrics)
        return result

    def calculate_metrics(self,val_arr1, val_arr2, metrics):
        result = {}
        for ky in metrics.keys():
            func = metrics[ky]
            result[ky] = func(val_arr1,val_arr2)
        return result

    def get_testing_users(self):
        return self.testing_model.get_user_ids()


    def build_model(self,train_set):
        raise NotImplementedError("cannot instantiate Abstract Base Class")

    def build_predictor(self, model):
        raise NotImplementedError("cannot instantiate Abstract Base Class")



