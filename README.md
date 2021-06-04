Bidomain-Model
---
A bidomain model of the heart where we simulate the progression of an action potential within cells of the heart.

Description
---
To read more about the bidomain model and our implementation, click here - https://www.srirag.dev/article/bidomain-model

## Getting Started

### Installing
* Clone the repository  
    ```
    git clone https://github.com/srirag-vuppala/Bidomain-Model.git
    ```

### Executing program

* To start
    ```
    python3 app.py
    ```

Help
---

A list of helpful notes 

* If you want to contribute to this script and make it better open a pull request with your suggestion. :rocket:
* If anything doesn't work go ahead and open an issue. :rotating_light:

Version History
---

* 0.1
    * Initial Release

<!-- License -->
<!-- --- -->

<!-- This project is licensed under the [LICENSE] - see the LICENSE.md file for details -->
* * *


Program Flow
---

1. **Initialize the simulation** :
   1. Create the internal and external sheets of size (r, c) using `create_sheets()`
      1. Internal sheet : Initialized to -70 mV
      2. External sheet : Initialized to   0 mV
   2. Initializing our <img src="https://render.githubusercontent.com/render/math?math=\Delta x = 0.01"> (CHECK THIS)
   3. Set our constants for the Laplacian:
      1. Now, <img src="https://render.githubusercontent.com/render/math?math=\sigma_{i} = 1/{\Delta x^2}"> 
		  - Also dividing it with <img src="https://render.githubusercontent.com/render/math?math=\chi"> just to make it easier. 
		  	- 	So, <img src="https://render.githubusercontent.com/render/math?math=\sigma_{i} = \sigma_{i}/\chi">

      2. Now, <img src="https://render.githubusercontent.com/render/math?math=\sigma_{e} = -1/{\Delta x^2}"> 
			- Also dividing it with <img src="https://render.githubusercontent.com/render/math?math=\chi"> just to make it easier. 
				- 	So, <img src="https://render.githubusercontent.com/render/math?math=\sigma_{e} = \sigma_{e}/\chi">
   4. Create our Complete Laplacian Matrix :
      1. Start by creating the Laplacian for the intracelluar sheet of size (r+c, r+c), <img src="https://render.githubusercontent.com/render/math?math=\nabla_{i}"> passing it to the `create_laplace_matrix()`
      2. Now continue by creating the Laplacian for the extracelluar sheet of size (r+c, r+c), <img src="https://render.githubusercontent.com/render/math?math=\nabla_{e}"> passing it to the `create_laplace_matrix`
      3. Finally, use `create_block_diag_matrix()` to generate an complete Laplacian of size ((r+c)*2, (r+c)*2) 
      4. Additionally, we have a `check_laplace_matrix()` to verify if the working of our `create_laplace_matrix()` is correct.

2. **Start Simulation**: `simulate()`
 	1. Loop for 10 times (Will change it later) (use do while?)
		1. Display the heat-map of present timestep using `display_heat_map()`
		2. Stimulate for `n` times
			1. Hold <img src="https://render.githubusercontent.com/render/math?math=V_e"> 's:
				1. Starting to `-40mV` 
				2. Ending to `40mV`
		3. Prep work:
			1. Generate an 1-D array of transmembrane potential from <img src="https://render.githubusercontent.com/render/math?math=V_{Trans} = V_{intra} - V_{extra}"> 
			2.  Find the <img src="https://render.githubusercontent.com/render/math?math=A"> coefficient from <img src="https://render.githubusercontent.com/render/math?math=V_T = A[V_i V_e]"> using `find_A()`
				<!-- 1.  **NOTE** I have no clue how to actually find this...look in code for why. -->
			4. Set the <img src="https://render.githubusercontent.com/render/math?math=C_m , \Delta{t}"> [could be done earlier]
			5. Now find the **coefficient** for the <img src="https://render.githubusercontent.com/render/math?math=V^{n plus 1}"> time step [To be rendered] using `find_coeff_V()`
			6. Solve the first term (i.e the term containing <img src="https://render.githubusercontent.com/render/math?math=V^{n}">) using `find_coeff_V()` and <img src="https://render.githubusercontent.com/render/math?math=V^{n}">
			7. Find the Ionic current using `generate_ionic_current()`
			8. Now substract 5th step - 6th step
		4. Solve for <img src="https://render.githubusercontent.com/render/math?math=V^{nplus1}">
		5. Clean up for next iteration:
			1. Set <img src="https://render.githubusercontent.com/render/math?math=V_{intra}^{n} = V_{intra}^{nplus1}">
			2. Set <img src="https://render.githubusercontent.com/render/math?math=V_{extra}^{n} = V_{extra}^{nplus1}">
			3. Set <img src="https://render.githubusercontent.com/render/math?math=V^{n} = V^{nplus1}">

    2. Finish the simulation.
---
