import sys
sys.path.append("./src")
from similarities import CosineSimilarity, JaccardSimilarity
from dataset import get_friends_data, get_user_item_matrix
from models.friendsmodel import FriendsModel
import matplotlib.pyplot as plt
import matplotlib

def get_similarity_matrix(data_set, friend_data):
    i_model = FriendsModel(data_set, friend_data)
    similarity = CosineSimilarity(i_model)

    return similarity

def get_friends_similarity(sim_mat, friend_data):
    sim_dict = {}
    for ky, values in friend_data.iteritems():
        ky_sims = sim_mat.get_similarities(ky,values)
        if not ky_sims:
            continue
        f_id, simz = zip(*ky_sims)
        sim_dict[ky] = simz
        for item in simz:
            if item < 0.1:
                print item

    return sim_dict

def get_strangers_similarity(sim_mat, friend_data):
    sim_dict = {}
    i_model = sim_mat.model
    for ky in friend_data:
        strangers = i_model.get_strangers_in_roster(ky)
        ky_sims = sim_mat.get_similarities(ky,strangers)
        t_id, simz = zip(*ky_sims)
        sim_dict[ky] = simz

    return sim_dict


#plt.scatter(txs, tys, color='k', marker=r'$\bigodot$', alpha=0.9,label="strangers")
#plt.scatter(fxs, fys, color='gray', marker=r'$\bullet$', alpha=0.6,label="friends")
def draw_similarity(friend_sims, stranger_sims):
    #print friend_sims
    matplotlib.rcParams.update({'font.size':28})

    fys, fxs=zip(*((x, k) for k in friend_sims for x in friend_sims[k]))
    tys, txs=zip(*((xt, kt) for kt in stranger_sims for xt in stranger_sims[kt]))

    fig = plt.figure()
    ax = fig.add_subplot(111) 

    #matplotlib.rcParams.update({'font.size':28})

    #plt.plot(txs, tys, 'k>',alpha=0.9,label="strangers")
    #plt.plot(fxs, fys, 'c*',alpha=0.6,label="friends")

    stranger, = plt.plot(txs, tys, ' ', color='lightgrey', marker=r's', alpha=0.9,label="strangers",)
    friend, = plt.plot(fxs, fys, ' ',color='k', marker='>', alpha=0.8,label="friends")

    plt.title('Cosine Similarity')
    plt.axis('tight')
    plt.ylabel("Similarity")
    plt.xlabel("User ID")


    plt.legend(loc='lower right') 
    plt.show()



if __name__ == '__main__':
    raw_data = get_user_item_matrix()
    friend_data = get_friends_data()
    sim_mat = get_similarity_matrix(raw_data,friend_data)
    f_sim = get_friends_similarity(sim_mat,friend_data)
    t_sim = get_strangers_similarity(sim_mat,friend_data)

    idx = 1
    f_sims = {}
    t_sims = {}
    for ky in f_sim:
    	f_sims[idx] = f_sim[ky]
    	t_sims[idx] = t_sim[ky]
    	idx += 1


    draw_similarity(f_sims,t_sims)

    




    

