import numpy as np

# TODO figure out to way to set precision with matprint
np.set_printoptions(precision=3)

def matprint(mat, likeTheory=False, fmt="g"):
    """
    USE: This function prints out the matrix in a nice and clean way.
         It also represents the matrix as we view it conceptually not just how its stored in numpy.
    
    If an argument likeTheory is given it'll print out the array like how we conceptualize it in our theory. 
    i.e our sheet is a array of arrays of columns
    """
    if likeTheory == True:
        mat = mat.T
        msg1 = "Theory representation"
        print('-'*len(msg1))
        print(msg1)
        print('-'*len(msg1))
    else:
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
    
    if likeTheory== True:
        print('-'*len(msg1))
    else:
        print('-'*len(msg2))

        
def flat(V):
    flat = []
    for row in V:
        for ele in row:
            flat.append(ele)
    return flat

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



def main():
    arr = np.zeros([3,3])
    print(arr)
    matprint(arr)

if __name__ == '__main__':
    main()