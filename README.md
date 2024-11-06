# POD_with_Python_and_Comsol
The goal of this repo is to trade accuracy for computation speed, meaning instead of running time-consuming (Comsol) transient simulations, just go for the snapshot matrix and get the main modes (= eigenvalues that weight most).
The main idea of that lies in the fact that physical insight into the model's behaviour is more enlightning than values correct to the 4th digit after the period. That means the more parameters of the model can be changed and yet still reliable results be generated the more useful such a reduction can be considered. Such a parameter-study can answer questions like "if we exchange the material here and there, how much will it have an influence on the heat distribution?", or "how will the magnetic field be changed when we use a different geometry, in particular how sensitive is it to the radius?". So instead to have time-consuming simulations provide an answer after noticeable time, an exact answer won't yield much insight. Here the reduced model of the system comes into the game.


# Main steps

1. get snapshot matrix from Comsol (by simple export after parameter and time study)
2. use POD (proper orthogonal decomposition)

    2.1. calculate covariance matrix C

    2.2. calculate and sort the eigenvectors and eigenvalues of the matrix C

    2.3. construct diagonal matrix S with singular values on the diagonal

    2.4. calculate new matrix based on the sorted eigenvectors and S

    2.5. multiply the snapshot matrix with the eigenvector to get matrix A

    2.6. depending on the settings get the reduced modes


# order of file execution
1. generate_mesh_snapshot_form_file.sh
2. POD_with_solution_matrix.py
3. make_diff_matrix.py
4. make_vtu_data.py
5. make_paraview_animation_files.py


# What is done/achieved/available
1. from snapshot matrix the *n*th highest modes can be calculated for 2d

    1.1. despite the fact that 
2. the difference of "reduced" and "unreduced (=original)" system can be visualized

    2.1. the difference matrix can be calculated
    2.2. a comparison in paraview is possible where the time evolution of 1, 2, 3,...modes can be done (and see that the more modes are used the higher the agreement with the unreduced system is)
    2.3. a time series (gif) can be done based on the number of modes

3. the most time-consuming part is the computation starting from the snapshot matrix (covariance matrix, eigenvectors, eigenvalues...)

    3.1. Python is acceptable fast for this job but the bigger the snapshot matrix is, the more likely the computer is running out of RAM (and therefore no MOR possible)

    3.2. to circumvent this problem (speed, memory) it makes sense to outsource the heavy numerics into more suitable languages like Fortran, Rust)

    3.2.1. for Rust the SVD can be computated incredibly fast (compared to Python) but there is some cleaning of the input data needed (all numbers HAVE to be floats, implicit integer->float conversion not possible); matrix has to be passed by hand; writing to file not possible as well as many other pecularities of Rust (the available crates for numeric are not compatible, i.e. matrix multiplication is possible in crate A but saving matrix to file in crate B and there is no convenient way to change the type of matrix from crate A to matrix from crate B => overhead of complication); in theory best approach but Rust seems not be made for numerics, at least not for acceptable prototyping effort without learning a whole great bunch of the language

    3.2.2. Fortran might be promising in anything that affects number crunching, the code is not written (yet); another issue is the interaction of different submodules with LAPACK and EIGEN, should be not too complicated but no MWE at hand


# What is not done
- as soon as geometry is moving/rotating there is no way to match the data from the modes to the geometry (in the static case one can see by timeframe to timeframe the similarity between mode and full-simulation, in the rotating case this is not the case anymore)
- any little parser that prepares the data for Rust (like converting ALL numbers to floats as required and add a ";" at the end of each line except the last one)
- MWE of Fortran for matrix computation (this include proper reading from file [actually done] and doing eigenvalue/eigenvector computation) [doesn't sound all in all too challenging]


# major goals/next steps
- any simulation that combines temperature T and magnetic field B (or torque M) or material parameter change (and therefore no snapshot matrix)
- to construct the full field of quantity when certain points are measured


# problems (so far) and overcoming
- computational speed => less matrix, other "faster" languages
- display of results:
  - bunch of data and modes, which one is the one with greatest insight
  - paraview is doing great, with some data polishing even gifs can be generated (as well as results compared to each other)
