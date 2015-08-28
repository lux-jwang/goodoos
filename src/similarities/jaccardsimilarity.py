
from similarity import Similarity 
from distances import jaccard_coefficient

#jaccard coefficient


class JaccardSimilarity(Similarity):
    def __init__(self, model):
        super(JaccardSimilarity,self).__init__(model)
        return

    def calculate_similarity(self,user_id, target_id):
        if user_id == target_id:
            return 1.0
        comm_i_ids = self.model.get_mutual_item_ids(user_id,target_id)
        if not comm_i_ids:
            return 0.0

        u_item_ids = self.model.get_items(user_id)
        t_item_ids = self.model.get_items(target_id)

        sim = jaccard_coefficient([u_item_ids],[t_item_ids]).flatten()[0]
        
        #print user_id, target_id, sim
        #if sim > 0.9999:  
        #	print u_item_ids
        #	print t_item_ids
        #	print "------------------------------------"

        return sim if sim < 1.0 else 1.0