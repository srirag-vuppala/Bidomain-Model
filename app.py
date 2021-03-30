"""
intracellular initially set to -70
extra initially set to 0 

Questions for Dr. Lin:
    1. Would it be possible for us to generate the laplacian matrix for the intra then extra and -> form the complete laplacian matrix?
    2. This is a bit conceptual but would the pattern of the laplacian descrete 
        
Important notes:
    1. We want to find the speed of the action potential so having a reference to time is necessary.
    2. An action potential is initiated when V(intra) - V(extra) > 0 i.e delta V > 0
    3. We are only involving ourselves with 2-D in this model that's why sheet.

Strategy:
    1. Create two sheets each representing the intracellular and extra cellular layer for potentials.
        a. The sheets are going to arrays of columns, here each cell represents a single point in space not the ACTUAL cell.
        
    2. Initiate the action potential by setting the ends of the 
        a. extra cellular -30 and -110
        Do this for a while and use the same hodgkin and huxley from cable eqn
        
Checkpoints:
    1. The sum of all columns and rows = 0.
    2. Check if you hit the correct points manually. 

"""
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.animation as animation 
import pandas as pd
# from ipywidgets import interactive
from utilities import matprint, flat, display_heat_map, split_list, unflatten, check_laplace_matrix
import hh

# Prints the arrays properly with elements as X.YYY
np.set_printoptions(precision=3)


def create_sheets():
    # the sheet will comprise of arrays of columns.
    n_rows = 4 
    n_columns = 4 
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
        # The logic here is every third element should be multiplied with 0 and not 1
        if (i+1)%buffer_number == 0:
            temp.append(0)
        else:
            temp.append(c*1)
    # TODO (Low priority) figure out why this list comprehension isn't working
    # temp = [c*-1 if (i+1)%3 == 0 else 0 for i in range(size - 1)]
    L += np.diagflat(temp, 1)
    L += np.diagflat(temp, -1)

    #The diagonals that are spaced our depending on the size of the matrix
    # Here the number is 3 for 3x3 i think 4 for 4x4 
    # I think the trend continues but I haven't verified it.
    temp = [c*1 for i in range(size-buffer_number)]
    L += np.diagflat(temp, buffer_number)
    L += np.diagflat(temp, -1*buffer_number)
    return L

def merge_laplace_matrix(Li, Le):
    # Create the big laplace matrix with Vi's L and Ve's L
    final = []
    zero = np.zeros(len(Li))
    for ele in Li:
        final.append(np.concatenate((ele, zero), axis=0))
    for ele in Le:
        final.append(np.concatenate((zero, ele), axis=0))
    return np.asarray(final)
        



def generate_ionic_current(V):
    #TODO figure this out
    # Membrane surface to volume ratio
    #look in cable
    chi = 1
    I_ion = hh.HodgkinHuxley().main(V)
    # this doesn't work for some reason
    # final = chi*(np.concatenate((I_ion, -1*I_ion), axis=0))
    temp = []
    for i in I_ion:
        temp.append(i)
    for i in I_ion:
        temp.append(-1*i)
    return temp 

# def simulate(intra, extra, L):
#     # we might need to convert trans_V is not a sheet 
#     orig_intra, orig_extra = intra, extra
#     stepper = 0
#     while stepper < 10:
#         #TODO check if + or - for the shift
#         trans_V = np.add(flat(intra)-flat(extra), 70.0)
#         # trans_V = (flat(intra)- flat(extra)) + 70
#         val = 30.0
#         if stepper < 5:
#             trans_V[0] = -70+val
#             trans_V[1] = -70+val
#             # trans_V[2] = -70+val
#             trans_V[-1] = -70+val
#             trans_V[-2] = -70+val
#             # trans_V[-3] = -70+val
#         # print(generate_ionic_current(trans_V))
#         new_V = np.linalg.solve(L, generate_ionic_current(trans_V))
#         intra, extra = split_list(new_V)
#         intra = unflatten(intra, len(orig_intra), len(orig_intra[0]))
#         extra = unflatten(extra, len(orig_extra), len(orig_extra[0]))
#         #display stuff
#         display_heat_map(intra - extra)
        
#         # trans_V = np.add(intra - extra, 70.0) 
#         stepper += 1

def simulate(intra, extra, L):
    # we might need to convert trans_V to a sheet 
    orig_intra, orig_extra = intra, extra
    stepper = 0
    while stepper < 1:
        #TODO check if + or - for the shift
        trans_V = np.add(flat(intra)-flat(extra), 70.0)
        trans_V = unflatten(trans_V, len(orig_intra), len(orig_intra[0]))
        matprint(trans_V)
        val = 30.0
        if stepper < 5:
            trans_V[0] = -70+val
            trans_V[-1] = -70+val
        # print(generate_ionic_current(trans_V))
        new_V = np.linalg.solve(L, generate_ionic_current(flat(trans_V)))
        intra, extra = split_list(new_V)
        intra = unflatten(intra, len(orig_intra), len(orig_intra[0]))
        extra = unflatten(extra, len(orig_extra), len(orig_extra[0]))

        #display stuff
        # display_heat_map(intra - extra)
        
        # trans_V = np.add(intra - extra, 70.0) 
        stepper += 1

def main():
    # Create the sheets first
    intra, extra = create_sheets()
    # matprint(intra)

    # Make the constant that multiplies all through the laplacian matrix | sigma/(delta x)^2
    # Divide this constant with chi (membrane surface-to-volume ratio)   
    # TODO: Find this constant (Ask prof for values)
    delta_x = 0.01
    chi = 1
    const_intra = 1/(delta_x*delta_x*chi)  
    const_extra = -1/(delta_x*delta_x*chi)
    # const_intra = 1
    # const_extra = -1
    
    # create our laplacian matrix
    Li = create_laplace_matrix(intra, const_intra)
    Le = create_laplace_matrix(extra, const_extra)
    print("The laplacian matrix")
    # matprint(Li)
    check_laplace_matrix(Li)

    # Merge the Laplacian matrices and flat(Vi)+flat(Ve) = V (Variables) ; so we have a single L and V
    L = merge_laplace_matrix(Li, Le)
    matprint(L)
    check_laplace_matrix(L)
    # The shape of our total V variables
    V = np.concatenate((flat(intra), flat(extra)), axis=0)

    # simulate(intra, extra, L)
    print(V)
    matprint(unflatten(flat(intra)-flat(extra) , 3, 3))

    # Display heat map of intra-cellular and extra-cellular matrices
    # display_heat_map(L)

if __name__ == '__main__':
    main()
    # generate_ionic_current([4]*5)
