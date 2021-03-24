import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# TODO figure out to way to set precision with matprint
np.set_printoptions(precision=3)

def matprint(mat, fmt="g"):
    """
    USE: This function prints out the matrix in a nice and clean way.
         It also represents the matrix as we view it conceptually not just how its stored in numpy.
    
    If an argument likeTheory is given it'll print out the array like how we conceptualize it in our theory. 
    i.e our sheet is a array of arrays of columns
    """
    msg2 = "Actual data representation"
    print('-'*len(msg2))
    print(msg2)
    print('-'*len(msg2))

    col_maxes = [max([len(("{:"+fmt+"}").format(x)) for x in col]) for col in mat.T]
    for x in mat:
        for i, y in enumerate(x):
            print(("{:"+str(col_maxes[i])+fmt+"}").format(y), end="   ")
        print("")
        print("")
    
    print('-'*len(msg2))

        
def flat(V):
    flat = []
    for row in V:
        for ele in row:
            flat.append(ele)
    return flat

# def get_internal_matrix(V):
#     temp = V
#     temp = temp[1:len(temp)-1]
#     for i, ele in enumerate(temp):
#         temp[i] = temp[i][1:len(temp[i])-1]
#     return temp

# def flat_both(intra, extra):
#     # Make it flat with v = [vi ..... ve] this is the V vector that gets multiplied with L[rows*2, cols*2]
#     flat = []
#     for row in intra:
#         for ele in row:
#             flat.append(ele)
#     for row in extra:
#         for ele in row:
#             flat.append(ele)
#     return flat

def display_heat_map(V):
    sns.set_theme()
    sns.color_palette("rocket", as_cmap=True)
    ax = sns.heatmap(V,  linewidths=1, square=True, annot=True)
    # ax = sns.heatmap(V,  linewidths=1, square=True, cmap='Blues', annot=True)
    plt.show()


def main():
    arr = np.zeros([4,4])
    matprint(arr)


if __name__ == '__main__':
    main()