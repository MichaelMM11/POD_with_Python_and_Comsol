use std::fmt;

fn tra(matrix: Matrix) -> (f32, f32, f32, f32) {
    (matrix.0, matrix.2, matrix.1, matrix.3)
}

fn trax(matrix: Matrix) -> Matrix {
    Matrix(matrix.0, matrix.2, matrix.1, matrix.3)
}

// The following struct is for the activity.
#[derive(Debug)]
struct Matrix(f32, f32, f32, f32);

impl fmt::Display for Matrix {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        // Use `self.number` to refer to each positional data point.
        write!(f, "({}, {})\n({}, {})", self.0, self.1, self.2, self.3)
    }
}



fn main() {
    let matrix = Matrix(1.1, 1.2, 2.1, 2.2);
    println!("{:?}", matrix);
    println!("{}", matrix);
    let a = trax(matrix);
    println!("{}", a);

}
