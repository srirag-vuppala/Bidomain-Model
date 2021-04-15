import numpy as np
import seaborn as sns
import pandas as pd
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
    mat = np.asarray(mat)
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
    if(V.ndim == 1):
        return V
    flat = []
    for row in V:
        for ele in row:
            flat.append(ele)
    return np.asarray(flat)

def unflat(V, rows, cols):
    size = len(V)
    final = []
    i, r, = 0, 0
    while i < size and r < rows:
        temp = []
        c=0
        while c < cols:
            temp.append(V[i])
            c+=1
            i += 1
        final.append(temp)
        r += 1
    # print(final)
    return np.asarray(final)

def check_laplace_matrix(L):
    # Each row's elements sum should be = 0
    # Each column's elements sum should be = 0
    # Thus total sum of all elements should be 0 too 
    tsum = 0
    for arr in L:
        for i in arr:
            tsum += i
    if tsum == 0:
        print("yay it works")    
    else:
        print("Try again")

def display_heat_map(V, c):
    df = pd.DataFrame(V, columns=[str(i)+'cols' for i in range(len(V[0]))], index=[str(i)+'rows' for i in range(len(V))]) 
    sns.set_theme()
    sns.color_palette("rocket", as_cmap=True)
    ax = sns.heatmap(df,  linewidths=1, square=True, annot=True)
    ax.invert_yaxis()
    # ax = sns.heatmap(V,  linewidths=1, square=True, cmap='Blues', annot=True)
    plt.savefig('foo'+str(c+1).zfill(3)+'.jpg')
    plt.clf()
    # plt.show()

def split_list(a_list):
    half = len(a_list)//2
    return a_list[:half], a_list[half:]

def flat_join(A, B):
    # Will probably used to flatten the intra and extra then attach to make a single arr of all the V's
    return np.concatenate((flat(A), flat(B)), axis=0)

def unflat_join(V, rows, cols):
    # Will probably used to unflatten the intra and extra then attach to make a single arr of all the V's
    A,B = split_list(V)
    A = unflat(A, rows, cols)
    B = unflat(B, rows, cols)
    return A, B

def create_block_diag_matrix(Li, Le):
    # block diagonal form 
    # Create the big laplace matrix with Vi's L and Ve's L
    final = []
    zero = np.zeros(len(Li))
    for ele in Li:
        final.append(np.concatenate((ele, zero), axis=0))
    for ele in Le:
        final.append(np.concatenate((zero, ele), axis=0))
    return np.asarray(final)

def main():
    arr = np.zeros([4,4])
    matprint(unflat(flat(arr), 4, 4))


if __name__ == '__main__':
    main()