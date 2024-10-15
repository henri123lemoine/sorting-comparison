use rand::seq::SliceRandom;
use std::io::{self, BufRead};

pub fn is_sorted(arr: &[i32]) -> bool {
    arr.windows(2).all(|w| w[0] <= w[1])
}

pub fn bogo_sort(arr: &mut [i32]) {
    let mut rng = rand::thread_rng();
    while !is_sorted(arr) {
        arr.shuffle(&mut rng);
    }
}

#[cfg(feature = "python")]
use pyo3::prelude::*;

#[cfg(feature = "python")]
#[pyfunction]
fn rust_bogo_sort(py: Python, arr: Vec<i32>) -> PyResult<Vec<i32>> {
    let mut arr = arr;
    py.allow_threads(|| bogo_sort(&mut arr));
    Ok(arr)
}

#[cfg(feature = "python")]
#[pymodule]
fn sorting_comparison(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(rust_bogo_sort, m)?)?;
    Ok(())
}

#[cfg(not(feature = "python"))]
fn main() {
    let stdin = io::stdin();
    let mut line = String::new();
    stdin.lock().read_line(&mut line).unwrap();

    let mut numbers: Vec<i32> = line
        .split_whitespace()
        .map(|s| s.parse().unwrap())
        .collect();

    bogo_sort(&mut numbers);

    for num in numbers {
        print!("{} ", num);
    }
    println!();
}
