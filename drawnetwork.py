#! /usr/bin/env python

# We probably will need some things from several places
import sys
# We need to import the graph_tool module itself
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from graph_tool.all import *
sys.path.append("./src")
from dataset import get_friends_data_index

def draw_edges(gx, src, dsts):
    for dst in dsts:
        gx.add_edge(dst,src)

def map_indx_to_vertex(gx, indxs):
    vers = []
    for indx in indxs:
        vers.append(gx.vertex(indx))
    return vers


def construct_graphic():
    ui_mat, roster = get_friends_data_index()
    total_num = len(roster.keys())

    gx = Graph()
    gx.set_directed(True)
    vlist = gx.add_vertex(total_num)

    print len(ui_mat.keys())

    for ky, val in ui_mat.iteritems():
        src_v = gx.vertex(ky)
        dsts_v = map_indx_to_vertex(gx,val)
        draw_edges(gx,src_v,dsts_v)
        
    return gx, ui_mat

def get_shortest_distance(gx,srcs):
    valid_distance = []
    for src in srcs:
        dist = shortest_distance(gx,source=gx.vertex(src))
        for item in dist.a:
            if item < 2000:
                valid_distance.append(item)
    print " "

    print "average degree: ", np.mean(valid_distance)
    #hist
    matplotlib.rcParams.update({'font.size':28})
    title = "Six Degrees of Separation ( Avg: "+str(round(np.mean(valid_distance),4))+" )"
    plt.hist(valid_distance, bins=10, facecolor='grey')
    plt.title(title)
    plt.xlabel("Degrees")
    plt.ylabel("Frequency")
    plt.axis('tight')
    plt.show()


def get_shortest_distance_uni(gx):
    valid_distance = []
    dist = shortest_distance(gx)

    for item in dist.a:
    	if item < 2000:
            valid_distance.append(item)

    print "average degree: ", np.mean(valid_distance)
    #hist
    title = "Six Degrees of Separation ( Avg: "+str(round(np.mean(valid_distance),4))+" )"
    plt.hist(valid_distance)
    plt.title(title)
    plt.xlabel("Degrees")
    plt.ylabel("Frequency")
    plt.axis('tight')
    plt.show()


def show_graphic(gx):
    pos = sfdp_layout(gx)
    graph_draw(gx, pos=pos, vertex_text=gx.vertex_index, vertex_font_size=11,output_size=(4800,4800),output="friends_relation_1010_3.png")

if __name__ == '__main__':

    g, ui_mat = construct_graphic()
    srcs = ui_mat.keys()
    get_shortest_distance(g,srcs)
    #get_shortest_distance_uni(g)
    #show_graphic(g)






