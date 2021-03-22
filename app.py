"""
intracellular initially set to 0
extra initially set to -70

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
from utilities import matprint, flat
# from scipy.sparse.csgraph import laplacian

# Prints the arrays properly with elements as X.YYY
np.set_printoptions(precision=3)


def create_sheets():
    """
    the sheet will comprise of arrays of columns.
    """
    # Make the intracellular first with all 0s
    n_rows = 5
    n_columns = 5
    intra = np.zeros([n_columns, n_rows ])

    # Make the extracellular first with all -70s
    extra = np.zeros([n_columns, n_rows ])
    extra += -70

    # for testing purposes
    # intra[1] += -20
    return intra, extra


def create_laplace_matrix(V, c):
    # takes in either intra or extra flattens it then and makes the respective L
    flattened = flat(V)
    print("Flattened : ")
    print(flattened)

    L = []
    size = len(flattened)
    # this is the number that changes according to the size of matrix
    buffer_number = len(V[0])
    L = np.diagflat([c*4 for i in range(size)])

    temp = []

    for i in range(size - 1):
        # Here the number is 3 for 3x3 i think 4 for 4x4 
        # I think the trend continues but I haven't verified it.
        # The logic here is every third element should be multiplied with 0 and not -1
        if (i+1)%buffer_number == 0:
            temp.append(0)
        else:
            temp.append(c*-1)

    # TODO (Low priority) figure out why this list comprehension isn't working
    # temp = [c*-1 if (i+1)%3 == 0 else 0 for i in range(size - 1)]
    L += np.diagflat(temp, 1)
    L += np.diagflat(temp, -1)

    # Here the number is 3 for 3x3 i think 4 for 4x4 
    # I think the trend continues but I haven't verified it.
    temp = [c*-1 for i in range(size-buffer_number)]
    L += np.diagflat(temp, buffer_number)
    L += np.diagflat(temp, -1*buffer_number)
        
    return L

def check_laplace_matrix(L):
    # I might be checking this wrong
    tsum = 0
    for arr in L:
        for i in arr:
            tsum += i
    if tsum == 0:
        print("yay it works")    
    else:
        print("Try again")


def main():
    # Create the sheets first
    intra, extra = create_sheets()
    matprint(intra)
    # matprint(intra, True)
    # matprint(extra)


    # Make the constant that multiplies all through the laplacian matrix | sigma/(delta x)^2
    # TODO: Find this constant (Ask prof for values)
    delta_x = 0.01
    const_intra = 1/(delta_x*delta_x)  
    const_extra = 0/(delta_x*delta_x)
    const_intra = 1
    
    # create our laplacian matrix
    L = create_laplace_matrix(intra, const_intra)
    print("The laplacian matrix")
    matprint(L)
    check_laplace_matrix(L)


if __name__ == '__main__':
    main()
