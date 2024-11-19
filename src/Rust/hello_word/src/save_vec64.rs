use std::error::Error;
use std::fs::File;
use std::io::BufReader;
use std::io::BufWriter;
use std::io::Write;
use std::io::BufRead;
use std::path::Path;

fn read_vec_from_file(path: impl AsRef<Path>) -> Result<Vec<f64>, Box<dyn Error>> {
    // Open the file in read-only mode with buffer.
    let file = File::open(path.as_ref())?;
    let mut reader = BufReader::new(file);

    let mut v = vec![];

    let mut buf = String::new();

    while reader.read_line(&mut buf)? != 0 {
        v.push(buf.trim_end().parse()?);
        buf.clear();
    }

    Ok(v)
}

fn write_vec_to_new_file(path: impl AsRef<Path>, value: &[f64]) -> Result<(), Box<dyn Error>> {
    let file = File::create(path.as_ref())?;
    let mut writer = BufWriter::new(file);

    for x in value {
        write!(writer, "{x}\n")?;
    }

    writer.flush()?;
    Ok(())
}

fn main() {
    let v1 = vec![1.0, 1.5, 2.0, 2.5];
    println!("v1: {v1:?}");
    write_vec_to_new_file("test.json", &v1).unwrap();

    // for demonstration purposes let's look at the file, too
    println!("Here's what the file looks like:");
    println!("========================================");
    println!("{}", std::fs::read_to_string("test.json").unwrap());
    println!("========================================");

    // get back the vector
    let v2 = read_vec_from_file("test.json").unwrap();
    assert!(v1 == v2);
    println!("v2: {v2:?}");
}
