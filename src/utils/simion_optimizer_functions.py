
def insert_shared_potentials(X,number_of_particles,leader,disciples):
    try:
        for j in disciples:
            for k in range(number_of_particles):
                X[k][int(j)] = X[k][leader]
    except:
        pass
    return X

def limit_geometry(g_min,g_max,G):
    for i in range(shape(G)[0]):
        for j in range(shape(G)[1]):
            if G[i][j] < g_min[j]:
                G[i][j] = g_min[j]
            elif G[i][j] > g_max[j]:
                G[i][j] = g_max[j]
    return G

