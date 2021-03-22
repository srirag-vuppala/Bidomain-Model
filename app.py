"""
intracellular initially set to 0
extra initially set to -70
        
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
    the sheet will comprise of arrays of columns.(in theory)
    Here the sheet will comprise of arrays of rows.(in practice)
    """
    # Make the intracellular first with all 0s
    n_rows = 3
    n_columns = 3
    intra = np.zeros([n_rows, n_columns])

    # Make the extracellular first with all -70s
    extra = np.zeros([n_rows, n_columns])
    extra += -70

    # for testing purposes
    intra[1] += -20
    return intra, extra


def create_laplace_matrix(V, c):
    # takes in either intra or extra and makes the respective L
    L = []
    size = len(V)
    L = np.diagflat([c*4 for i in range(size)])

    temp = []
    for i in range(size - 1):
        # The logic here is every third element should be multiplied with 0 and not -1
        if (i+1)%3 == 0:
            temp.append(0)
        else:
            temp.append(c*-1)

    # TODO (Low priority) figure out why this list comprehension isn't working
    # temp = [c*-1 if (i+1)%3 == 0 else 0 for i in range(size - 1)]
    L += np.diagflat(temp, 1)
    L += np.diagflat(temp, -1)

    temp = [c*-1 for i in range(size-3)]
    L += np.diagflat(temp, 3)
    L += np.diagflat(temp, -3)
        
    return L


def main():
    # Create the sheets first
    intra, extra = create_sheets()
    # matprint(intra)
    matprint(intra, True)
    # matprint(extra)

    # Flatten the Transpose array(because transpose of the array is our theoretical representation) then flatten
    intra_flat = flat(intra.T)
    extra_flat = flat(extra.T)
    print("Flattened : ")
    print(intra_flat)

    # Make the constant that multiplies all through the laplacian matrix | sigma/(delta x)^2
    # TODO: Find this constant (Ask prof for values)
    delta_x = 0.01
    const_intra = 1/(delta_x*delta_x)  
    const_extra = 0/(delta_x*delta_x)

    # create our laplacian matrix
    print("The laplacian matrix")
    Li = create_laplace_matrix(intra_flat, const_intra)
    Le = create_laplace_matrix(extra_flat, const_extra)
    matprint(Li)
    # extra_flat = flat_single(extra)
    # print(extra_flat)
    # Le = create_laplace_matrix(extra_flat)

    # V = flat(intra, extra)
    # print(V)


if __name__ == '__main__':
    main()
