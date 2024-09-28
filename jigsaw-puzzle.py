import numpy as np
import matplotlib.pyplot as plt
import random
import math
import array
from collections import deque

def load_matrix(file_path):
    matrix = []
    with open(file_path, "r") as f:
        lines = f.readlines()
    matrix_lines = lines[1:]
    for line in matrix_lines:
        line = line.strip()
        if line:
            matrix.append(int(line))
    matrix = np.array(matrix)
    reshaped_matrix = matrix.reshape((512, 512))
    # print(reshaped_matrix)
    # print_image(reshaped_matrix)
    return reshaped_matrix

def create_patch(image):
    patches = []
    state_mat = []
    z = 0
    for i in range(4):
        temp = []
        for j in range(4):
            temp.append(z)
            patch = image[
                i * 128 : (i + 1) * 128,
                j * 128 : (j + 1) * 128,
            ]
            patches.append(patch)
            z = z + 1
        state_mat.append(temp)
    return patches, state_mat

def reconstruct_image(patches, grid):
    patch_height, patch_width = patches[0].shape[:2]
    grid_height = len(grid)
    grid_width = len(grid[0])
    full_image = np.zeros((grid_height * patch_height, grid_width * patch_width), dtype=patches[0].dtype)
    for i in range(4):
        for j in range(4):
            patch = patches[grid[i][j]]
            # print(i,j,grid[i][j])
            # print_image(patch)
            full_image[
                i * patch_height : (i + 1) * patch_height,
                j * patch_width : (j + 1) * patch_width,
            ] = patch
    # print_image(full_image)
    return full_image

def print_image(image):
    plt.imshow(image, cmap="gray")
    plt.title("512x512 Matrix Visualization")
    plt.colorbar()
    plt.show()

def get_successors(state,patches,visited,f):
    succ = []
    i = 0
    for mat in patches:
        if(i in visited):
            i = i + 1
            continue
        val = 0
        if(f):
            for j in range(len(mat)):
                val+=abs(patches[state][len(mat)-1][j]-mat[0][j])
        else:
            for j in range(len(mat)):
                val+=abs(patches[state][j][len(mat)-1]-mat[j][0])
        # val/=len(mat)
        succ.append((val,i))
        i=i+1
    succ.sort()
    c = 0
    for i in range(len(succ)):
        if(succ[0][0]==succ[i][0]):
            c+=1
    # print(c)
    return succ[random.randint(0,c-1)]
    # return succ[0]

def traversal(start,patches):
    visited = []
    queue = deque()
    vis2 = []
    vis2.append(0)
    queue.append((start,0))
    visited.append(start)
    temp = []
    for i in range(16):
        temp.append(0)
    val = 0
    while(queue):
        pos = queue.popleft()
        temp[pos[1]]=pos[0]
        # print(pos[0],pos[1])
        if(pos[1]+4<16):
            if(pos[1]+4 not in vis2):
                next = get_successors(pos[0],patches,visited,True)
                queue.append((next[1],pos[1]+4))
                visited.append(next[1])
                vis2.append(pos[1]+4)
                val+=next[0]
                # print(f"pos: {pos[1]} next: {next[1]} val: {next[0]}")
        if(pos[1]%4!=3):
            if(pos[1]+1 not in vis2):
                next = get_successors(pos[0],patches,visited,False)
                queue.append((next[1],pos[1]+1))
                visited.append(next[1])
                vis2.append(pos[1]+1)
                val+=next[0]
    # print(len(visited))
    # print(temp)
    new_state = [temp[i:i+4] for i in range(0, 16, 4)]
    return (new_state,val)

def rearranged(patches):
    values = []
    v = []
    for i in range(16):
        temp = traversal(i,patches)
        values.append((abs(temp[1]),i))
        v.append((temp[0],i))
    values.sort()

    for i in range(16):
        if(v[i][1]==values[0][1]):
            return v[i][0]

patches,state_mat=create_patch(load_matrix("scrambled_lena.mat").T)

print(state_mat)

# rearranged(patches)
new_state = rearranged(patches)
print(new_state)
new_image = reconstruct_image(patches,new_state)
print(new_image)
print_image(new_image)