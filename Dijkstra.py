import numpy as np
import csv
from queue import PriorityQueue
import matplotlib.pyplot as plt

def read_surf2plot(name):
    with open(f'{name}.csv', 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=' ')
        z = []
        for idx, row in enumerate(reader):
            if idx == 0:
                l, step = map(int, row)
                continue
            if idx == 1:
                A = tuple(map(int, row))
                continue
            if idx == 2:
                B = tuple(map(int, row))
                continue
            z.append(list(map(float, row)))
    lim = ((l - 1) // 2) * step

    x = [[- lim + i * step for j in range(l)] for i in range(l)]
    y = [[- lim + j * step for j in range(l)] for i in range(l)]

    return np.array(x), np.array(y), np.array(z), lim, A, B, step

def plot(x, y, z, lim, path=None, opacity=0.5):
    fig = plt.figure()
    ax = plt.axes(projection='3d')

    ax.plot_surface(x, y, z, cmap="viridis", edgecolor='none', alpha=opacity)
    ax.set_title('Surface plot')
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)
    
    ax.set_zlim(-lim, lim)

    if path:
        path_x = []
        path_y = []
        path_z = []
        for i, j in path:
            path_x.append(x[i][j])
            path_y.append(y[i][j]) 
            path_z.append(z[i][j] + 1000)

        ax.plot(path_x, path_y, path_z, c='k')

    plt.show()

def left(inds, a):
    if inds[1]==0:
        return False
    return (inds[0], inds[1]-1)
def right(inds, max_l):
    if inds[1]==max_l[1]-1:
        return False
    return (inds[0], inds[1]+1)
def up(inds, a):
    if inds[0]==0:
        return False
    return (inds[0]-1, inds[1])
def down(inds, max_l):
    if inds[0]==max_l[0]-1:
        return False
    return (inds[0]+1, inds[1])

def way(matrix, hlong, vlong, finish):
    max_l = matrix.shape
    way = [finish]
    ind = finish
    while matrix[ind]!=0:
        if up(ind, max_l):
            if np.round(matrix[ind] - vlong[ind[0]-1, ind[1]], 4) == np.round(matrix[ind[0]-1, ind[1]], 4):
                ind = ind[0]-1, ind[1]
                way.append(ind)
                
        if down(ind, max_l):
            if np.round(matrix[ind] - vlong[ind], 4) == np.round(matrix[ind[0]+1, ind[1]], 4):
                ind = ind[0]+1, ind[1]
                way.append(ind)
                
        if left(ind, max_l):
            if np.round(matrix[ind]- hlong[ind[0], ind[1]-1], 4)== np.round(matrix[ind[0], ind[1]-1], 4):
                ind = ind[0], ind[1]-1
                way.append(ind)
                
        if right(ind, max_l):
            if np.round(matrix[ind]- hlong[ind], 4) == np.round(matrix[ind[0], ind[1]+1], 4):
                ind = ind[0], ind[1]+1
                way.append(ind)
                
    return way

def dijkstra(z, step, A, B):
    vertical = np.sqrt(abs(np.diff(z, axis=0))**2 + step**2)
    horizontal = np.sqrt(abs(np.diff(z, axis=1))**2 + step**2)
    
    start = A
    
    result = np.ones(z.shape) * np.inf
    result[start] = 0 
    
    counted = PriorityQueue() 

    counted.put((result[start], start)) 
    hor_or_ver = {right:horizontal, down:vertical, left:horizontal, up:vertical}
    max_l = z.shape
    labeled = set() 
    while not counted.empty():
        start = counted.get()[1] 
        while start in labeled: 
            if counted.empty():
                break
            start = counted.get()[1] 
        labeled.add(start) 
        indices = {right:start, down:start, left:(start[0], start[1]-1), up:(start[0]-1, start[1])} 

        for change in [up, right, down, left]: 
            new_start = change(start, max_l) 
            if new_start and new_start not in labeled: 
                new_el = np.minimum(hor_or_ver[change][indices[change]] + result[start], result[new_start]) 
                if not np.equal(new_el, result[new_start]): 
                    result[new_start] = new_el 
                    counted.put((result[new_start], new_start))
    
    path = way(result, horizontal, vertical, B)
    return path
    
def main():
    filepath = input("Enter path to csv filem that conatains matrix. \nIf you just whant to see an examplem enter None or just use our function\n:")
    if filepath=="None":
        filepath="example1"
    x, y, z, lim, A, B, step = read_surf2plot(filepath)
    path = dijkstra(z, step, A, B)
    plot(x, y, z, lim, path)
    
if __name__ == "__main__":
    main()
