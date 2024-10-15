use pyo3::prelude::*;
use rand::seq::SliceRandom;
use rand::thread_rng;

#[pyfunction]
fn is_sorted(arr: Vec<i32>) -> bool {
    arr.windows(2).all(|w| w[0] <= w[1])
}

#[pyfunction]
fn bogo_sort(mut arr: Vec<i32>) -> Vec<i32> {
    let mut rng = thread_rng();
    while !is_sorted(arr.clone()) {
        arr.shuffle(&mut rng);
    }
    arr
}

/// A Python module implemented in Rust.
#[pymodule]
fn sorting_comparison(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(bogo_sort, m)?)?;
    Ok(())
}
