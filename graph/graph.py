from utils import get_group_info

import matplotlib.pyplot as plt
from os import walk
from numba import jit
import sortednp as snp
import networkx
import numpy as np
import time

@jit(forceobj=True)
def make_graph(members):
    matrix = {}
    for i in members:
        for j in members:
            if i != j:
                matrix[i+j] = snp.kway_intersect(members[i], members[j]).shape[0] * 1.0/ min(members[i].shape[0], members[j].shape[0])
    return matrix

def main():

    f = []
    for (dirpath, dirnames, filenames) in walk('groups'):
        f.extend(filenames)
        break

    members = {}
    for g in f:
        members[g.split('_')[1]] = np.loadtxt('groups/' + g, delimiter='\n', unpack=False, dtype=np.int)

    matrix = make_graph(members)

    members_name = []

    for i in members:
        members_name.append(get_group_info(i)['screen_name'])
        time.sleep(0.2)

    s = 0
    with_names = {}
    for i, j in enumerate(members):
        with_names[j] = members_name[i]

    max_matrix = max(matrix.values())
    min_matrix = min(matrix.values())

    for i in matrix:
        matrix[i] = (matrix[i] - min_matrix) / (max_matrix - min_matrix)

    g = networkx.Graph(directed=False)
    for i in with_names:
        for j in with_names:
            if i != j:
                g.add_edge(with_names[i], with_names[j], weight=matrix[str(i)+str(j)])
                
    members_count = {with_names[x]:len(members[x]) for x in members}

    max_value = max(members_count.values()) * 1.0
    size = []
    max_size = 500  
    min_size = 50
    for node in g.nodes():
        size.append(((members_count[node]/max_value)*max_size + min_size)*10)

    pos=networkx.spring_layout(g)
    plt.figure(figsize=(100, 100))
    networkx.draw_networkx(g, pos, node_size=size, width=0.1, font_size=8)
    plt.axis('off')
    plt.savefig('graph.png')

if __name__ == '__main__':
    main()