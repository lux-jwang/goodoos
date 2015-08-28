from friendsmodel import FriendsModel

class ReputationModel(FriendsModel):
    def __init__(self,raw_data,friends_data, reputation_data):
        super(ReputationModel,self).__init__(raw_data,friends_data)
        self.reputation_data = reputation_data
        return

    def get_reputation(self,user_id):
        if not user_id in self.reputation_data:
            return None
        return self.reputation_data[user_id]