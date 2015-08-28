import glob
from os import path
import pickle
import numpy as np
import matplotlib.pyplot as plt




def get_files():
    return glob.glob("ff_svd_result_friends_*")


def get_tidy(all_rs):
    maes = {}
    rmses = {}
    for ky in all_rs.keys():
        rs = all_rs[ky]
        maes[ky] = []
        rmses[ky] = []        
        for mae, rmse in rs:
            maes[ky].append(mae)
            rmses[ky].append(rmse)

    dst_filename = "./svd_result_mae.mat"
    pickle.dump(maes,open(dst_filename, "w"),protocol=2)

    dst_filename = "./svd_result_rmse.mat"
    pickle.dump(rmses,open(dst_filename, "w"),protocol=2)

    return maes, rmses

def ana_data():
    filenames = get_files()
    all_rs = {}
    for fn in filenames:
        mat = pickle.load(open(fn,"rb"))
        for ky in mat.keys():
            results = mat[ky]
            for rs in results:
                mae = rs["MAE"]
                rmse = rs["RMSE"]
                if not ky in all_rs:
                    all_rs[ky] = [(mae, rmse)]
                else:
                    all_rs[ky].append((mae,rmse))

    return get_tidy(all_rs)

def get_mae_rmse():
    
    mae_filename = "./ff_svd_result_mae.mat"
    rmse_filename = "./ff_svd_result_rmse.mat"

    if (not path.isfile(rmse_filename)) or (not path.isfile(mae_filename)):
        return ana_data()

    maes = pickle.load(open(mae_filename,"rb"))
    rmse = pickle.load(open(rmse_filename,"rb"))

    return maes, rmse

def draw_result(r_max, r_min,r_mean):
    xx = range(len(r_max))

    fig = plt.figure(figsize=(16,8))
    #plt.xlim(0,830)
    #plt.ylim(0.1,1.3)
    #plt.xlabel("Users")
    #plt.ylabel("MAE")
    #plt.axis("tight")
    imean = round(np.mean(r_mean),4)

    ax=fig.add_subplot(1,1,0)
    ax.tick_params(axis="both",which="major",labelsize=20)
    #fig.xlim(0,830)
    ax.set_xlabel("Users",fontsize=14)
    ax.set_ylabel("MAE",fontsize=14)
    ax.set_xlim(0,830)
    ax.plot(xx,r_mean,"og",label="MAE per user")
    ax.axhline(y=imean,color="r",linewidth = 2, label="mean MAE of all users: "+str(imean))
    #plt.plot(xx,r_max,"or",label="max mae per user")
    #plt.plot(xx,r_min,"ob",label="min mae per user")
    #plt.plot(xx,r_mean,"og",label="mean mae per user")
    #plt.axhline(y=imean,color="r",linewidth = 2, label="mean mae of all users: "+str(imean))

    #for tick in ax.xaxis.get_major_ticks():
    #    tick.label.set_font_size(14)

    plt.legend()
    plt.show()


if __name__ == '__main__':

    maes, rmses = get_mae_rmse()
    r_min = []
    r_max = []
    r_mean = []
    for ky in rmses:
        r_min.append(np.min(maes[ky]))
        r_mean.append(np.mean(maes[ky]))
        r_max.append(np.max(maes[ky]))

    draw_result(r_max,r_min,r_mean)




    
