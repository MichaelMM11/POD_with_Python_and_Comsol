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
// The left singular vectors are:
//  [[-0.3167331446091065, -0.948514688924756, 0.0],
//  [-0.6707011685937435, 0.22396415437963857, -0.7071067811865476],
//  [-0.6707011685937436, 0.2239641543796386, 0.7071067811865475]], shape=[3, 3], strides=[3, 1], layout=Cc (0x5), const ndim=2

// The right singular vectors are:
//  [[-0.4168301381758514, -0.0816682352525302, 0.9053081990455173],
//  [0.8982609360852509, -0.18954008048752713, 0.39648688325344433],
//  [0.13921180485702067, 0.9784706726517249, 0.1523654033858462]], shape=[3, 3], strides=[3, 1], layout=Cc (0x5), const ndim=2

// The sigma vector:
//  [12.040590078046721, 3.051178554664221, 9.490164740574465e-18], shape=[3], strides=[1], layout=CFcf (0xf), const ndim=1



    // let array_d2 = array![
    //     [1, 2, 3],
    //     [4, 5, 6],
    //     [1, 5, 4],
    //     [6, 12, 13],
    // ];
// M=
//  1   2   3
//  4   5   6
//  1   5   4
//  6  12  13

// U = (0.168877 |  0.0564768 |  0.84752  | -0.5
//      0.397136 |  0.646701  | -0.417206 | -0.5
//      0.288648 | -0.758626  | -0.301941 | -0.5
//      0.854661 | -0.0554484 |  0.128373 |  0.5)

// Σ = (21.8578 | 0      | 0          # 477.7634
//            0 | 1.9318 | 0          # 3.73185
//            0 | 0      | 0.71048    # 0.50478
//            0 | 0      | 0)

// V = (0.328214 | 0.803375  | -0.496854
//      0.641538 | -0.575655 | -0.507001
//      0.693329 | 0.152346  | 0.704334)
