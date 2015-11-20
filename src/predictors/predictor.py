

class Predictor(object):
    def __init__(self):
        self.preferences = {}
        return

    def estimate_preference(self,user_id,item_id):        
        if self.is_calculated(user_id,item_id):
            return self.preferences[user_id][item_id]

        pref = self.predict(user_id,item_id)
        self.update_cache(user_id,item_id,pref)

        return pref

    def predict(self,user_id,item_id):
        raise NotImplementedError("cannot instantiate Abstract Base Class")
        return

    def estimate_preference_mul_items(self,user_id,item_ids):
        prefs = []
        for i_id in item_ids:
            pref = self.estimate_preference(user_id,i_id)
            prefs.append(pref)

        return prefs

    def estimate_preference_mul_users(self,user_ids, item_id):
        prefs = []
        for u_id in user_ids:
            pref = self.estimate_preference(u_id,item_id)
            prefs.append(pref)
        return prefs

    def is_calculated(self,user_id, item_id):
        return False
        if not user_id in self.preferences:
            return False
        if not item_id in self.preferences[user_id]:
            return False

        return True

    def update_cache(self,user_id,item_id,pref_value):
        return
        self.preferences.setdefault(user_id,{})
        self.preferences[user_id][item_id] = pref_value

