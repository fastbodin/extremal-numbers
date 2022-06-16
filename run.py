import gurobipy as gp
from gurobipy import GRB


# i_cliques = list of i_cliques
# clique = current clique being constructed
# k_index = kth partition in G
# p_index = vertex being considered in current partition
# c_size = current clique size
# i = we wish to constuct cliques of size i
# K_sizes = sizes of partitions in G
# num_partitions = number of partitions in G
# k_index_to_vertex_id = converts k_index to vertex id
def gen_i_subsets(i_cliques, clique, k_index, p_index, c_size,
                  i, K_sizes, num_partitions, k_index_to_vertex_id):
    # found an i-clique
    if c_size == i:
        i_cliques.append(tuple(clique))
        return
    # considered all partitions
    if k_index == num_partitions:
        return
    # no more vertices to consider in this partition
    if p_index == K_sizes[k_index]:
        return

    # proceed with element corresponding to index + 1 IN i-clique
    clique[k_index_to_vertex_id[k_index] + p_index] = 1
    # proceed to next partition and start at index 0
    gen_i_subsets(i_cliques, clique, k_index + 1, 0, c_size + 1,
                  i, K_sizes, num_partitions, k_index_to_vertex_id)

    # proceed with element corresponding to index + 1 NOT in i-clique
    clique[k_index_to_vertex_id[k_index] + p_index] = 0
    if p_index < K_sizes[k_index] - 1:
        gen_i_subsets(i_cliques, clique, k_index, p_index + 1,
                      c_size, i, K_sizes, num_partitions, k_index_to_vertex_id)

    # if you considered all the vertices in the partition
    elif p_index == K_sizes[k_index] - 1:
        # proceed with no vertex in this partition part of a subset.
        gen_i_subsets(i_cliques, clique, k_index + 1,
                      0, c_size, i, K_sizes, num_partitions,
                      k_index_to_vertex_id)

    # considered all cases
    return


# k_r_cliques = list of subgraphs
# cliques = current subgraph
# k_index = kth partition in G
# p_index = vertex being considered in current partition
# c_num = which clique a vertex is assigned too [1, ..., k]
# r_num = number of vertices in current K_r
# K_sizes = sizes of partitions in G
# num_partitions = number of partitions in G
# k_index_to_vertex_id = convertex k_index to vertex number
# r = desired size of K_r
# k = desired number of disjoint K_r's
# last_k_index = last k_index where corresponds to first vertex
# in a new K_r chosen
# last_p_index = last p_index where corresponds to first vertex
# in a new K_r chosen
def gen_k_r_cliques(k_r_cliques, cliques, k_index, p_index, c_num,
                    r_num, K_sizes, num_partitions, k_index_to_vertex_id,
                    r, k, last_k_index, last_p_index):
    # print("k_index ={}, p_index = {}, c_num = {}, r_num ={}".format(
    #     k_index, p_index, c_num, r_num))
    # print(cliques)
    # found k disjoint K_r's
    if c_num == k + 1:
        # print("\n Added: {}\n".format(cliques))
        k_r_cliques.append(tuple(cliques))
        return
    # considered all partitions
    if k_index == num_partitions:
        return
    # no more vertices to consider in this partition
    if p_index == K_sizes[k_index]:
        return
    # if there are not enough vertices left

    # if the vertex is not already in a clique
    if cliques[k_index_to_vertex_id[k_index] + p_index] == 0:
        # proceed with element corresponding to index + 1 IN current K_r
        cliques[k_index_to_vertex_id[k_index] + p_index] = c_num

        # if we are about to pick the first vertex in a new K_r
        if r_num == 0:
            # there is room in K_r for more vertices
            # proceed to next partition and start at index 0
            # clique number (c_num) remains unchanged
            # number of vertices in K_r (r_num) goes up by one
            # note that last_k_index and last_p_index are updated
            # to current index since this vertex was the first
            # vertex assigned to this clique
            gen_k_r_cliques(k_r_cliques, cliques, k_index + 1, 0, c_num,
                            r_num + 1, K_sizes, num_partitions,
                            k_index_to_vertex_id, r, k, k_index, p_index)
        # if there is room in K_r for more vertices
        elif r_num < r-1:
            # proceed to next partition and start at index 0
            # clique number (c_num) remains unchanged
            # number of vertices in K_r (r_num) goes up by one
            # last_k_index  and last_p_index remains unchanged
            # because this was not the first vertex in the K_r
            gen_k_r_cliques(k_r_cliques, cliques, k_index + 1, 0, c_num,
                            r_num + 1, K_sizes, num_partitions,
                            k_index_to_vertex_id, r, k, last_k_index,
                            last_p_index)

        # cannot add more vertices to K_r
        else:
            # clique number (c_num) goes up by one
            # number of vertices in K_r (r_num) is now 0
            # last_k_index remains unchanged because this was not
            # the first vertex in the K_r
            # however the k_index goes back to the last_k_index
            # since we have to backtrack to start a new K_r
            # and p_index goes back to last_p_index + 1
            # since we have to backtrack to start new K_r
            if last_p_index < K_sizes[last_k_index] - 1:
                gen_k_r_cliques(k_r_cliques, cliques, last_k_index,
                                last_p_index + 1, c_num + 1, 0, K_sizes,
                                num_partitions, k_index_to_vertex_id, r, k,
                                last_k_index, last_p_index)

            # if last_p_index was not a feasible position,
            # move to next parition, i.e. last_k_index + 1,
            # and set p_index = 0
            elif last_p_index == K_sizes[last_k_index] - 1:
                gen_k_r_cliques(k_r_cliques, cliques, last_k_index + 1, 0,
                                c_num + 1, 0, K_sizes, num_partitions,
                                k_index_to_vertex_id, r, k,
                                last_k_index, last_p_index)

        # proceed with element corresponding to index + 1 NOT in
        # current K_r
        cliques[k_index_to_vertex_id[k_index] + p_index] = 0
        if p_index < K_sizes[k_index] - 1:
            gen_k_r_cliques(k_r_cliques, cliques, k_index, p_index + 1, c_num,
                            r_num, K_sizes, num_partitions,
                            k_index_to_vertex_id, r, k,
                            last_k_index, last_p_index)

        # if you considered all the vertices in the partition
        elif p_index == K_sizes[k_index] - 1:
            # proceed with no vertex in this partition part of a K_r
            gen_k_r_cliques(k_r_cliques, cliques, k_index + 1, 0, c_num,
                            r_num, K_sizes, num_partitions,
                            k_index_to_vertex_id, r, k,
                            last_k_index, last_p_index)

        return
    # the vertex is already in a clique
    else:
        # proceed with element corresponding to index + 1 unchanged
        if p_index < K_sizes[k_index] - 1:
            gen_k_r_cliques(k_r_cliques, cliques, k_index, p_index + 1, c_num,
                            r_num, K_sizes, num_partitions,
                            k_index_to_vertex_id, r, k,
                            last_k_index, last_p_index)

        # if you considered all the vertices in the partition
        elif p_index == K_sizes[k_index] - 1:
            # proceed with no vertex in this partition part of a K_r
            gen_k_r_cliques(k_r_cliques, cliques, k_index + 1, 0, c_num,
                            r_num, K_sizes, num_partitions,
                            k_index_to_vertex_id, r, k,
                            last_k_index, last_p_index)

        return


def gen_edges(sub_G_edges, sub_G, edge, k_index, p_index, e_size, K_sizes,
              num_partitions, k_index_to_vertex_id, clique_id):
    # found an edge
    if e_size == 2:
        sub_G_edges.append(tuple(edge))
        return
    # considered all partitions
    if k_index == num_partitions:
        return
    # no more vertices to consider in this partition
    if p_index == K_sizes[k_index]:
        return

    # if vertex is in the correct clique
    if sub_G[k_index_to_vertex_id[k_index] + p_index] == clique_id:
        # proceed with element corresponding to index + 1 IN edge
        edge[k_index_to_vertex_id[k_index] + p_index] = 1
        # move to next partition (k_index + 1)
        # new p_index = 0 in the new partition
        # number of vertices in the edge goes up by one
        gen_edges(sub_G_edges, sub_G, edge, k_index + 1, 0, e_size + 1,
                  K_sizes, num_partitions, k_index_to_vertex_id, clique_id)

        # proceed with element corresponding to index + 1 NOT in edge
        edge[k_index_to_vertex_id[k_index] + p_index] = 0
        if p_index < K_sizes[k_index] - 1:
            gen_edges(sub_G_edges, sub_G, edge, k_index, p_index + 1, e_size,
                      K_sizes, num_partitions, k_index_to_vertex_id, clique_id)

        # if you considered all the vertices in the partition
        elif p_index == K_sizes[k_index] - 1:
            # proceed with no vertex in this partition part of a subset.
            gen_edges(sub_G_edges, sub_G, edge, k_index + 1, 0, e_size,
                      K_sizes, num_partitions, k_index_to_vertex_id, clique_id)

    # vertex is not in correct clique
    else:
        # move on to next vertex in partition
        if p_index < K_sizes[k_index] - 1:
            gen_edges(sub_G_edges, sub_G, edge, k_index, p_index + 1, e_size,
                      K_sizes, num_partitions, k_index_to_vertex_id, clique_id)

        # if you considered all the vertices in the partition
        elif p_index == K_sizes[k_index] - 1:
            # proceed to next partition
            gen_edges(sub_G_edges, sub_G, edge, k_index + 1, 0, e_size,
                      K_sizes, num_partitions, k_index_to_vertex_id, clique_id)

    # considered all cases
    return


class LP:
    def __init__(self, K_sizes, k, r):

        # problem is a maximization problem
        model = gp.Model('')
        model.Params.LogToConsole = 0

        # number of partitions
        num_partitions = len(K_sizes)
        # number of vertices
        num_verts = sum(partition for partition in K_sizes)
        # returns vertex number from k_index
        k_index_to_vertex_id = [sum(partition for partition in K_sizes[0:i])
                                for i in range(num_partitions)]

        # generate the edges of the graph
        edges = []
        gen_i_subsets(edges, [0 for i in range(num_verts)], 0, 0, 0, 2,
                      K_sizes, num_partitions, k_index_to_vertex_id)

        # generate all the possible choices of k disjoint K_r's
        k_dist_r_cliques = []
        gen_k_r_cliques(k_dist_r_cliques, [0 for i in range(num_verts)],
                        0, 0, 1, 0, K_sizes, num_partitions,
                        k_index_to_vertex_id, r, k, 0, 0)

        # generate all the edges of the k disjoint K_r's
        sub_G_edges = []
        index = 0
        # for each subgraph of the multipartie graph
        # which forms k disjoint K_r's
        for sub_G in k_dist_r_cliques:
            # edges corresonding to said subgraph
            sub_G_edges.append([])
            # for each clique
            for clique_id in range(1, k+1):
                # generate edges
                gen_edges(sub_G_edges[index], sub_G,
                          [0 for i in range(num_verts)],
                          0, 0, 0, K_sizes, num_partitions,
                          k_index_to_vertex_id, clique_id)
            # make new index in master list
            index += 1

        # define variables for each edge in the graph
        # variables hold truth value of statement "edge in subgraph"
        variables = model.addVars(edges, name='edges', vtype=GRB.BINARY)

        # from the list of K_r's, generate all possible sets of k dist. K_r's
        num_edge_in_k_dist_K_r = k*r
        max_edges = num_edge_in_k_dist_K_r - 1
        for sub_G in sub_G_edges:
            model.addConstr(sum(variables[edge] for edge in sub_G)
                            <= max_edges)

        # OBJECTIVE FUNCTION
        print("done")
        obj = gp.LinExpr()
        for edge in edges:
            obj += variables[edge]
        model.setObjective(obj, GRB.MAXIMIZE)

        # RUN
        model.optimize()
        formula = 4*3**2 + (k-1)*3

        print('Max number of edges of K_{} which does not contain '
              '{}K_{} is {} = {}'.format(K_sizes, k, r, int(model.objVal), formula))
        print('The elements of this max set are as follows.')
        # final = set([])
        for theset in edges:
            if variables[theset].x == 1:
                # final.add(theset)
                print(theset)


# for LATEX
#        for theedge in edges:
#            if variables[theedge].x == 1:
#                verts = []
#                for vert in range(num_verts):
#                    if theedge[vert] == 1:
#                        verts.append(vert+1)
#                print("(N-{}) edge (N-{})".format(verts[0], verts[1]))


###########################
# input function calls here
###########################
# K_sizes, k, r
LP([4, 4, 4, 4], 2, 3)
