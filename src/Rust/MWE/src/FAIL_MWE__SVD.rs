// https://github.com/Axect/Peroxide/blob/master/examples/svd.rs
// https://medium.com/gaussian-machine/implementing-svd-algorithm-in-rust-ac1489eb7ca4
// https://stackoverflow.com/questions/76933632/svd-decomposition-of-nalgebra-is-incomprehensible
// https://towardsdatascience.com/the-ultimate-ndarray-handbook-mastering-the-art-of-scientific-computing-with-rust-ef5ab767212a -> Singular Value Decomposition (SVD):


//use ndarray::array;
//use nalgebra::dmatrix;
//use nalgebra_lapack::SVD;
use ndarray::array;
use ndarray_linalg::svd::SVD;
use std::result::Result::{Err, Ok};



    let array_d2 = array![
        [-1.01,  0.86, -4.60],
        [ 3.98,  0.53, -7.04],
        [ 3.98,  0.53, -7.04],
    ];
    // let array_d2 = array![
    //     [1, 2, 3],
    //     [4, 5, 6],
    //     [1, 5, 4],
    //     [6, 12, 13],
    // ]
    println!("all's fine");
    match array_d2.svd(true, true) {
        Ok((u, sigma, v)) => {
            println!("The left singular vectors are: {:?}", u.unwrap());
            println!("The right singular vectors are: {:?}", v.unwrap());
            println!("The sigma vector: {:?}", sigma);
        }
        Err(err) => {
            println!("{err}");
        }
    }
