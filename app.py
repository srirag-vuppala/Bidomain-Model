"""
**IF THERE IS A FUNCTION YOU CAN'T FIND THE FUNCTION ITS PROBABLY PLACED IN THE UTILITIES**
"""
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.animation as animation 
import pandas as pd
from utilities import *
import os
import hh

# Prints the arrays properly with elements as X.YYY
np.set_printoptions(precision=3)


def create_sheets():
    # the sheet will comprise of arrays of columns.
    n_rows = 6 
    n_columns = 6
    intra = np.zeros([n_columns, n_rows ])
    intra += -70
    extra = np.zeros([n_columns, n_rows ])
    return intra, extra
     
def create_laplace_matrix(V, c):
    # takes in either intra or extra flattens it then and makes the respective L
    flattened= flat(V)
    L = []
    size = len(flattened)
    # this is the number that changes according to the size of matrix (the m value of matrix)
    buffer_number = len(V[0])
    temp = []

    # The main diagonal
    for i in range(len(V)):
        for j in range(len(V[i])):
            # Three point stencil
            if (i==0 and j==0) or (i==len(V)-1 and j==0) or (i==0 and j==len(V)-1) or (i==len(V)-1 and j==len(V)-1):
                temp.append(c*-2)
            # Four point stencil
            elif (0<i<len(V[i])-1 and j==0) or (0<i<len(V[i]) and j== len(V)-1) or (i==0 and 0<j<len(V)) or (i==len(V)-1 and 0<j<len(V)):
                temp.append(c*-3)
            # Five point stencil
            else:
                temp.append(c*-4)
    L = np.diagflat(temp)

    # The diagonals right beside the main diagonal
    temp = []
    for i in range(size - 1):
        # Here the number is 3 for 3x3 i think 4 for 4x4 
        # I think the trend continues but I haven't verified it.
        if (i+1)%buffer_number == 0:
            temp.append(0)
        else:
            temp.append(c*1)
    # TODO (Low priority) figure out why this list comprehension isn't working
    # temp = [c*-1 if (i+1)%3 == 0 else 0 for i in range(size - 1)]
    L += np.diagflat(temp, 1)
    L += np.diagflat(temp, -1)

    #The diagonals that are spaced our depending on the size of the matrix
    temp = [c*1 for i in range(size-buffer_number)]
    L += np.diagflat(temp, buffer_number)
    L += np.diagflat(temp, -1*buffer_number)
    return L

def generate_ionic_current(V, A, delta_t):
    V_send = np.matmul(A, V)
    V_send = np.add(V_send, 70)
    I_ion = hh.HodgkinHuxley().main(flat(V_send))
    # delta_t rearrangement
    return delta_t*np.asarray(I_ion) 

def find_A(trans_V):
    # The pattern is the length of the trans_V is going to be the identity matrix which is going to be like [I -I | I -I]
    size_I_matrix = len(trans_V)

    I_pos = np.identity(size_I_matrix)
    I_neg = -1*I_pos

    final = np.zeros((size_I_matrix*2, size_I_matrix*2))
    #merging horizontally
    temp = np.concatenate((I_pos, I_neg), axis=1)

    #merging vertically
    final = np.concatenate((temp, temp), axis=0);

    # To remove the negative zero i.e a weird kink with numpy
    final = np.where(final==-0, 0, final)
    
    # matprint(final)
    return final 

def find_coeff_V(type, A, C_m, delta_t, L):
    # term1 = C_m/delta_t
    term1 = C_m
    term1 = term1*A 
    
    term2 = delta_t/2
    term2 = term2*L

    if type == 'new':
        return term1 - term2
    elif type == 'now':
        return term1 + term2

def simulate(intra, extra, L):
    orig_intra, orig_extra = intra, extra
    # constants 
    stepper = 0
    C_m = 1
    delta_t = 0.01
    trans_V = flat(intra)-flat(extra)
    A_matrix = find_A(trans_V)
    V_now_coeff = find_coeff_V("now", A_matrix, C_m, delta_t, L)
    V_new_coeff = find_coeff_V("new", A_matrix, C_m, delta_t, L)
    # Adding modification for constant potentials 
    # Make last row all 1s to make the equation of the sum of all variables.
    V_new_coeff[-1] = 1
    #look a few lines below for the constant it gets equated to

    # print("Laplacian")
    # matprint(L)
    matprint(V_new_coeff)
    print("Determinant of V_new_coeff")
    print(np.linalg.det(V_new_coeff))

    # Counter for storing plots
    c = 0
    V_now = flat_join(intra, extra)

    # Finding the T variable that should be equated to our modification for constant potentials 
    T = V_now.sum()
    # T = 10 
    while stepper < 100:
        #1
        #display stuff existing right now 
        display_heat_map(intra - extra, c)

        #2
        if stepper < 5:
            extra[0] = -40
            extra[-1] = 40
        #2
        trans_V = flat(intra)-flat(extra)

        # I can't think of a better name aahhhhhh
        left_term = np.matmul(V_now_coeff, V_now)
        right_term = generate_ionic_current(V_now, A_matrix, delta_t)
        soln_term = left_term - right_term
        soln_term[-1] = T

        #3 
        # solve doesn't work unfortunatly
        # V_new = np.linalg.lstsq(V_new_coeff, soln_term, rcond=1)
        V_new = np.linalg.solve(V_new_coeff, soln_term)
        
        print("V_new")
        print(V_new)

        #overwrite the intra and extra to new intra and extra 
        intra, extra = unflat_join(V_new, len(orig_intra), len(orig_extra[0]))
        print("intra")
        print(intra)
        print("extra")
        print(extra)
        # T = V_now.sum()
        
        V_now = V_new
        stepper += 1
        c += 1

def main():
    # Create the sheets first
    intra, extra = create_sheets()
    # matprint(intra)

    # Make the constant that multiplies all through the laplacian matrix | sigma/(delta x)^2
    # Divide this constant with chi (membrane surface-to-volume ratio)   
    # TODO: Find this constant (Ask prof for values)
    delta_x = 0.01
    chi = 1
    sigma_i = 1
    sigma_e = 1
    const_intra = sigma_i/(delta_x*delta_x*chi)  
    const_extra = -1*sigma_e/(delta_x*delta_x*chi)
    
    # create our laplacian matrix
    Li = create_laplace_matrix(intra, const_intra)
    Le = create_laplace_matrix(extra, const_extra)
    # print("The laplacian matrix")
    # matprint(Li)
    # check_laplace_matrix(Li)

    # Merge the Laplacian matrices 
    L = create_block_diag_matrix(Li, Le)
    # matprint(L)
    # check_laplace_matrix(L)

    simulate(intra, extra, L)

os.system("ffmpeg -y -i 'foo%03d.jpg' bidomain.m4v")
# os.system("ffmpeg -i bidomain.m4v -map 0:v -c:v copy -bsf:v h264_mp4toannexb raw.h264")
# os.system("ffmpeg -i bidomain.mkv -filter:v \"setpts=2.0*PTS\" bidomain2.mkv")



if __name__ == '__main__':
    main()
    # os.system("rm -f *.jpg")