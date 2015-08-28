from model import Model

class FriendsModel(Model):

    def __init__(self,raw_data,friends_data):
        super(FriendsModel,self).__init__(raw_data)
        self.friends_data = friends_data
        self.friends_cache = {}
        self.strangers_cache = {}

        return

    
    def build_model(self,raw_data,**kargs):
        super(FriendsModel,self).build_model(raw_data)  
        friends_data = kargs.pop('friends_data', None)
        self.friends_data = friends_data
        return

    def get_friends(self,user_id, level=1):
        if not user_id in self.friends_data:
            return None
        if level == 1:
            return self.friends_data[user_id]
        if level == 2:
            scnd_friends = []
            f_ids = self.friends_data[user_id]
            scnd_friends.extend(f_ids)
            for f_id in f_ids:
                if f_id in self.friends_data:
                    sub_friends = self.friends_data[f_id]
                    scnd_friends.extend(sub_friends)

            f_set = set(scnd_friends)
            f_list = list(f_set)

            return f_list

    def get_mutual_friends(self,user_id1,user_id2):
        if not user_id1 in self.friends_data:
            return None
        if not user_id2 in self.friends_data:
            return None
        frds_d1 = self.friends_data[user_id1]
        frds_d2 = self.friends_data[user_id2]
        comm_friends = list(set(frds_d1).intersection(frds_d2))
        return comm_friends

    def get_friends_roster(self):
        return self.friends_data.keys()

    def is_a_friend(self,user_id, f_id,level=1):
        if user_id in self.friends_cache:
            if f_id in self.friends_cache[user_id]:
                if self.friends_cache[user_id][f_id]:
                    return True
                else:
                    return False
        self.friends_cache.setdefault(user_id, {})
        #SHOULD BE THIS?
        if not self.get_friends(user_id,level):
            self.friends_cache[user_id][f_id] = False
            return False

        if f_id in self.get_friends(user_id,level):            
            self.friends_cache[user_id][f_id] = True
            return True
        else:
            self.friends_cache[user_id][f_id] = False
            return False

    def get_strangers_in_roster(self,user_id):
        if user_id in self.strangers_cache:
            return self.strangers_cache[user_id]

        roster = self.get_friends_roster()
        stranger_ids = []
        for u_id in roster:
            if u_id == user_id:
                continue
            if not self.is_a_friend(user_id,u_id):
                stranger_ids.append(u_id)

        self.strangers_cache[user_id] = stranger_ids
        return stranger_ids









