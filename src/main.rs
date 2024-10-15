use rand::seq::SliceRandom;
use std::io::{self, BufRead};

fn is_sorted(arr: &[i32]) -> bool {
    arr.windows(2).all(|w| w[0] <= w[1])
}

fn bogo_sort(arr: &mut [i32]) {
    let mut rng = rand::thread_rng();
    while !is_sorted(arr) {
        arr.shuffle(&mut rng);
    }
}

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
