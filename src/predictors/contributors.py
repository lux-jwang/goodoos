from random import shuffle
from models import FriendsModel

class Contributors(object):
    def __init__(self,similarity):
        self.similarity = similarity
        self.model = self.similarity.get_model()
        return
    #0:all
    def get_neighbors(self, user_id, num=0):
        raise NotImplementedError("cannot instantiate Abstract Base Class")

    def get_model(self):
        return self.similarity.get_model()



class Neighbors(Contributors):
    def __init__self(self,similarity):
        super(Neighbors,self).__init__(similarity)
        return

    def get_neighbors(self,user_id,num=0):
        nbs  = self.similarity.get_similarities(user_id)
        if num < 1:
            return nbs
        return nbs[:num]

class JphNeighbors(Contributors):
    def __init__self(self,similarity):
        super(JphNeighbors,self).__init__(similarity)
        return

    def get_neighbors(self,user_id,num=0):
        nbs  = self.similarity.get_similarities(user_id)
        new_nbs = nbs[::2]
        return new_nbs[:num]

#DANGER CODE
class Neighbors_Friends(Contributors):
    def __init__self(self,similarity,):
        super(Neighbors_Friends,self).__init__(similarity)
        #self.check_model_type(self.model)
        return

    def check_model_type(self,model):
        if not type(model) is FriendsModel:
            raise TypeError("model should be an instance of FriendsModel")
        return True


    def get_neighbors(self,user_id,num=0):
    	t_ids = self.model.get_strangers_in_roster(user_id)
        nbs  = self.similarity.get_similarities(user_id,t_ids)
        if num == 0:
            return nbs
        if num < 0:
            num = len(self.model.get_friends(user_id,level=2))
        return nbs[:num]


class Friends(Contributors):
    def __init__(self,similarity):
        super(Friends,self).__init__(similarity)
        #self.check_model_type(self.model)
        return

    def check_model_type(self,model):
        if not type(model) is FriendsModel:
            raise TypeError("model should be an instance of FriendsModel")
        return True


    def get_neighbors(self,user_id,num=0):
        f_ids = self.model.get_friends(user_id,level=2)
        nbs  = self.similarity.get_similarities(user_id,f_ids)
        if num < 1:
            return nbs
        return nbs[:num]

class Friends_Strangers(Contributors):
    def __init__(self,similarity, f_n, t_n):
        super(Friends_Strangers,self).__init__(similarity)
        self.f_n = f_n
        self.t_n = t_n

    # This function is implemented slightly different with the other child classes.
    def get_neighbors(self,user_id,num=0):
        # get friends
        f_ids = self.model.get_friends(user_id,level=1)
        shuffle(f_ids)
        frs = f_ids[:self.f_n]
        fnbs = self.similarity.get_similarities(user_id,frs)

        # get stranger
        t_ids = self.model.get_strangers_in_roster(user_id)
        shuffle(t_ids)
        sts = t_ids[:self.t_n]
        st_sim = [1.0]*len(sts) #specific sim for esorics prefictor
        stnbs = zip(sts,st_sim)

        return (fnbs, stnbs)

    def get_rand_friends(self, user_id):
        f_ids = self.model.get_friends(user_id,level=1)

        shuffle(f_ids)
        frs = f_ids[:self.f_n]
        fnbs = self.similarity.get_similarities(user_id,frs)
        #print "fnbs: ", len(fnbs)
        return fnbs

    def get_rand_strangers(self, user_id):
        t_ids = self.model.get_strangers_in_roster(user_id)
        shuffle(t_ids)
        sts = t_ids[:self.t_n]
        st_sim = [1.0]*len(sts) #specific sim for esorics prefictor
        stnbs = zip(sts,st_sim)
        return stnbs



    


