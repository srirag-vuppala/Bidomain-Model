Notes:
------
<img src="https://render.githubusercontent.com/render/math?math=e^{i \pi} = -1">

- https

### Program Flow

1. Initialize the simulation :
   1. Create the internal and external sheets of size (r, c)
      1. Internal sheet : Initialized to -70 mV
      2. External sheet : Initialized to   0 mV
   2. Initializing our <img src="https://render.githubusercontent.com/render/math?math=\Delta x = 0.01"> (CHECK THIS)
   3. Set our constants for the Laplacian:
      1. <img src="https://render.githubusercontent.com/render/math?math=\sigma_{i} = 1/{\Delta x^2}"> 
      2. <img src="https://render.githubusercontent.com/render/math?math=\sigma_{e} = -1/{\Delta x^2}"> 
   4. Create our Complete Laplacian Matrix :
      1. Start by creating the Laplacian for the intracelluar sheet of size (r+c, r+c), <img src="https://render.githubusercontent.com/render/math?math=\nabla_{i}"> passing it to the `create_laplace_matrix`
      2. Now continue by creating the Laplacian for the extracelluar sheet of size (r+c, r+c), <img src="https://render.githubusercontent.com/render/math?math=\nabla_{e}"> passing it to the `create_laplace_matrix`
      3. Finally, use `merge_laplace_matrix` to generate an complete Laplacian of size ((r+c)*2, (r+c)*2) 
         <!-- <img src="https://render.githubusercontent.com/render/math?math=$ \begin{bmatrix}Li & 0\\0 & Le\end{bmatrix} $"> -->
      4. Additionally, we have a `check_laplace_matrix` to verify if the working of our `create_laplace_matrix` is correct.
2. Start Simulation: `simulate()`
   1. Loop for 10 times (Will change it later)
      1. Generate an array of transmembrane potential from <img src="https://render.githubusercontent.com/render/math?math=V_i - V_e"> 
      2. (CHECK THIS:) Add 70 to each element to the transmembrane array.
      3. Create a stimulation:
         1. (CHECK THIS) Add -70 to the first column values and last column values 
         2.  


