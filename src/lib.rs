use rand::seq::SliceRandom;
use std::io;

pub fn is_sorted(arr: &[i32]) -> bool {
    arr.windows(2).all(|w| w[0] <= w[1])
}

pub fn bogo_sort(arr: &mut [i32]) {
    let mut rng = rand::thread_rng();
    while !is_sorted(arr) {
        arr.shuffle(&mut rng);
    }
}

#[warn(dead_code)]
fn main() {
    let mut input = String::new();
    io::stdin().read_line(&mut input).unwrap();
    let mut numbers: Vec<i32> = input
        .split_whitespace()
        .map(|s| s.parse().unwrap())
        .collect();

    bogo_sort(&mut numbers);

    for num in numbers {
        print!("{} ", num);
    }
    println!();
}
