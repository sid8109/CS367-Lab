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

def calc(state,patches):
    ans = 0
    for i in range(4):
        for j in range(4):
            val=0
            if(j+1<4):
                for k in range(len(patches[state[i][j]])):
                    for l in range(len(patches[state[i][j+1]])):
                        val+=abs(patches[state[i][j]][k][127]-patches[state[i][j+1]][l][0])
            if(i+1<4):
                for k in range(len(patches[state[i][j]])):
                    for l in range(len(patches[state[i+1][j]])):
                        val+=abs(patches[state[i][j]][127][k]-patches[state[i+1][j]][0][l])
            ans+=val
    return ans

def rearranged(patches,state_mat):
    i,j=random.randint(0,3),random.randint(0,3)
    new_state = state_mat
    new_state[i][j],new_state[j][i]=state_mat[j][i],state_mat[i][j]
    val = calc(new_state,patches)
    return val,new_state

patches,state_mat=create_patch(load_matrix("scrambled_lena.mat").T)
# print(state_mat)

val = calc(state_mat,patches)
state = state_mat

Tm=1000
for i in range(1000):
    print(i)
    T = Tm//(i+1)
    new_val,new_state=rearranged(patches,state_mat)
    if new_val<val:
        state = new_state
        val = new_val
    else:
        random_val = random.uniform(0,1)
        prob = 1/(1+math.exp((val-new_val)/T))
        if random_val<prob:
            state = new_state
            val = new_val

mew_image = reconstruct_image(patches,state)
print_image(mew_image)
