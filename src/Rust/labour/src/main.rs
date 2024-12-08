// https://github.com/rust-ndarray/ndarray-linalg/issues/289
// https://github.com/rust-ndarray/ndarray-linalg/issues/380
// https://stackoverflow.com/questions/76933632/svd-decomposition-of-nalgebra-is-incomprehensible
// https://stackoverflow.com/questions/51476828/how-do-i-fix-the-error-type-annotations-needed-when-creating-a-closure-that-us

// use ndarray_linalg::svd::SVD;
// use std::result::Result::{Err, Ok};
// use std::collections::HashSet;
// use std::collections::HashMap;
// use ndarray_rand::RandomExt;
// use ndarray_rand::rand_distr::Uniform;
// use ndarray::{array, Array, Array2, Array3, ShapeBuilder};
// use ndarray::{rcarr1};
// use ndarray_linalg::convert::flatten;
// use ndarray_linalg::solve::Inverse;
// use ndarray_linalg::Eig;
use ndarray::{Array2, array};
//use rsvd::rsvd;

use nalgebra::dmatrix;
use nalgebra_lapack::SVD;
use std::fs::File;
use std::io::{BufRead, BufReader, Write};

use matrix_operations::csv::{load_matrix_from_csv, write_matrix_to_csv};
use matrix_operations::matrix;
use matrix_operations::operations::transpose_matrix;
use std::io;
use vecstorage::VecStorage;
use std::io::prelude::*;

use csv::ReaderBuilder;
//use ndarray::Array2;
use ndarray_csv::Array2Reader;
use std::error::Error;
use peroxide::fuga::*;

use std::fs;
// fn read_csv(path_to_file: &str) -> Result<Array2<u64>, Box<dyn Error>> {
//     let file = File::open(path_to_file)?;
//     let mut reader = ReaderBuilder::new().has_headers(false).from_reader(file);
//     Ok(reader.deserialize_array2((2, 3))?)
// }

fn main() {
    // let matrix1 = matrix![[1, 2, 3],[4, 5, 6]];
    // write_matrix_to_csv(&matrix1, "output.txt", "\t").unwrap();

    //let matrix2 = load_matrix_from_csv::<u64>("xinput.csv", "\t").unwrap();
    //let abc = read_csv("xinput.csv");
    //println!("{:?}", abc);
    // println!("{}", matrix2);
    // assert_eq!(matrix1, matrix2);

    //let array_read: Array2<u64> = reader.deserialize_array2_dynamic()?;
    //let y = load_matrix_from_csv::<f64>("input.csv", ",").unwrap();
    //let z = y.as_vec();
    let z = VecStorage::<&'static u32>::with_capacity(2);
    //z.push(&y);
    let x = dmatrix![
        //-1.01,  0.86, -4.60;
        //3.98,  0.53, -7.04;
        //3.98,  0.53, -7.04
        // TODO write py-script that converts EACH integer into float, otherwise Rust bitches around
        // (1) \tNUMBER_WITHOUT_DOT\t -> \tNUMBER.0\t
        // (2) add ; at end of line EXCEPT very last
        // cargo run > ouyput.txt  as very poor man'c choice as save/write/... typebitching
        1.,   2.,   3.;
        4.,   5.,   6.;
        1.,   5.,   4.;
        6.,  12.,  13.


        ];
    // 1,   2,   3;
    // 4,   5,   6;
    // 1,   5,   4;
    // 6,  12,  13
    // ];
    //let r = Vec::from(y);
    println!("x: {:?}", x);
    //println!("y: {:?}", y);
    println!("z: {:?}", z);
    //assert_eq!(x,y);
    let svd = SVD::new(x).unwrap();
    //println!("{:?}", svd);

    println!("U: {}", svd.u);
    println!("Σ: {}", svd.singular_values);
    println!("V_t: {}", svd.vt);
    let u = svd.vt;

    let matrix1 = matrix![[1, 2, 3],[4, 5, 6]];

}
