"""
**IF THERE IS A FUNCTION YOU CAN'T FIND THE FUNCTION ITS PROBABLY PLACED IN THE UTILITIES**
"""
# Imports 
import numpy as np
from utilities import *
import os
import hh

# Prints the arrays properly with elements as X.YYY
np.set_printoptions(precision=3)


def create_sheets():
    # A key observation from the cable equation implementation is that we have two sheets to represent the intracellular and extracellular space
    # The sheet will comprise of arrays of columns. Thus to get the actual sheet just call transpose on the sheet.
    n_rows = 10
    n_columns = 15
    # The intracellular space is initally at a potential of -70 mV
    intra = np.zeros([n_columns, n_rows ])
    intra += -70
    # The extracellular space is initally at a potential of 0 mV
    extra = np.zeros([n_columns, n_rows ])
    return intra, extra
     
def create_laplace_matrix(V, c):
    # Takes in either intra or extra flattens it then and makes the respective Laplacian
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
            if (i==0 and j==0) or (i==(len(V)-1) and j==0) or (i==0 and j==(len(V[i])-1)) or (i==len(V)-1 and j==len(V[i])-1):
                temp.append(c*-2)
            # Four point stencil
            elif (0<i<len(V)-1 and j==0) or (0<i<len(V) and j== len(V[i])-1) or (i==0 and 0<j<len(V[i])) or (i==len(V)-1 and 0<j<len(V[i])):
                temp.append(c*-3)
            # Five point stencil
            else:
                temp.append(c*-4)
    L = np.diagflat(temp)

    # The diagonals right beside the main diagonal
    temp = [0 if (i+1)%buffer_number == 0 else c*1 for i in range(size - 1)]
    L += np.diagflat(temp, 1)
    L += np.diagflat(temp, -1)

    #The diagonals that are spaced our depending on the size of the matrix
    temp = [c*1 for _ in range(size-buffer_number)]
    L += np.diagflat(temp, buffer_number)
    L += np.diagflat(temp, -1*buffer_number)
    return L

def generate_ionic_current(V, A, delta_t):
    V_send = np.matmul(A, V)
    V_send = np.add(V_send, 70)
    I_ion = hh.HodgkinHuxley().main(flat(V_send))
    return 1000*delta_t*np.asarray(I_ion) 

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
    
    return final 

def find_coeff_V(type, A, C_m, delta_t, L):
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
    delta_t = 1.47*10**(-7) 
    trans_V = flat(intra)-flat(extra)

    A_matrix = find_A(trans_V)

    V_now_coeff = find_coeff_V("now", A_matrix, C_m, delta_t, L)
    V_new_coeff = find_coeff_V("new", A_matrix, C_m, delta_t, L)

    # Adding modification for constant potentials 
    # Make last row all 1s to make the equation of the sum of all variables.
    V_new_coeff[-1] = 1

    extra[0] = -40
    extra[-1] = 40

    # Counter for storing plots
    c = 0
    V_now = flat_join(intra, extra)
    display_heat_map(intra - extra, c)

    while stepper < 60000:
        #1
        #display stuff existing stuff every 600 time steps right now 
        if stepper%600 == 0:
            display_heat_map((intra - extra).T, c)
            c += 1

        #2
        # Holding ends of the sheet at a high potential difference so as to induce an current to initiate action potential
        if stepper < 4:
            extra[0] = -40
            extra[-1] = 40
        #2
        trans_V = flat(intra)-flat(extra)

        left_term = np.matmul(V_now_coeff, V_now)
        right_term = generate_ionic_current(V_now, A_matrix, delta_t)
        soln_term = left_term - right_term

        #3 
        V_new = np.linalg.solve(V_new_coeff, soln_term)

        #overwrite the intra and extra to new intra and extra 
        intra, extra = unflat_join(V_new, len(orig_intra), len(orig_extra[0]))
        
        V_now = V_new
        stepper += 1

def main():
    # Create the sheets first
    intra, extra = create_sheets()


    # delta_x is the seperating distance between two nodes
    delta_x = 0.014

    # Divide this constant with chi (membrane surface-to-volume ratio)  | We do this just for ease 
    chi = 1
    
    # sigma_i and e are the conductivity tensors for the intracellular and extracellular spaces
    sigma_i = 1
    sigma_e = 1

    # Similar to the D_v like constant that existed in the cable equation
    # Make the constant that multiplies all through the laplacian matrix | sigma/(delta x)^2
    # Since we have two laplacians for each space, we have sign changed constants that we multiply our Laplacians 
    const_intra = sigma_i/(delta_x*delta_x*chi)  
    const_extra = -1*sigma_e/(delta_x*delta_x*chi) # chi is also sent here just to reduce variables 
    
    # create our laplacian matrices
    Li = create_laplace_matrix(intra, const_intra)
    Le = create_laplace_matrix(extra, const_extra)

    # Merge the Laplacian matrices 
    # We do this to to unify all of our variables to make it easy to keep track off of 
    # This isn't required if you'd rather just continue to do things twice (once for intra and once for extra)
    L = create_block_diag_matrix(Li, Le)

    simulate(intra, extra, L)


    os.system("ffmpeg -y -i 'foo%03d.jpg' bidomain.mp4")
    os.system("rm -f *.jpg")

if __name__ == '__main__':
    main()