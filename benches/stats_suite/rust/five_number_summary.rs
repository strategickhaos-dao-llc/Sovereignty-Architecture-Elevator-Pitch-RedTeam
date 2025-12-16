// BM-001: Five-Number Summary Implementation (Rust)
// Cross-language benchmark comparison with C++ and FlameLang
//
// Computes: min, Q1, median, Q3, max, IQR, and outlier count
// Input: Whitespace-separated numbers from stdin
// Output: Statistical summary to stdout

use std::io::{self, BufRead};
use std::time::Instant;

#[derive(Debug)]
struct Statistics {
    min: f64,
    q1: f64,
    median: f64,
    q3: f64,
    max: f64,
    iqr: f64,
    outlier_count: usize,
    outlier_percentage: f64,
}

// TODO: Implement five-number summary calculation
// This is a placeholder for the actual implementation
fn compute_five_number_summary(data: &mut Vec<f64>) -> Statistics {
    if data.is_empty() {
        eprintln!("Error: Empty dataset");
        std::process::exit(1);
    }
    
    // Sort the data (required for quantile calculation)
    data.sort_by(|a, b| a.partial_cmp(b).unwrap());
    
    let n = data.len();
    
    // TODO: Implement actual calculation
    // For now, this is a stub that returns placeholder values
    Statistics {
        min: data[0],
        max: data[n - 1],
        median: 0.0,  // Placeholder
        q1: 0.0,      // Placeholder
        q3: 0.0,      // Placeholder
        iqr: 0.0,     // Placeholder
        outlier_count: 0,
        outlier_percentage: 0.0,
    }
}

fn main() {
    // Read input data
    let stdin = io::stdin();
    let mut data = Vec::new();
    
    for line in stdin.lock().lines() {
        if let Ok(line) = line {
            for token in line.split_whitespace() {
                if let Ok(value) = token.parse::<f64>() {
                    data.push(value);
                }
            }
        }
    }
    
    if data.is_empty() {
        eprintln!("Error: No data read from input");
        std::process::exit(1);
    }
    
    println!("Read {} data points", data.len());
    
    // Start timing (exclude I/O time)
    let start = Instant::now();
    
    let stats = compute_five_number_summary(&mut data);
    
    let duration = start.elapsed();
    
    // Output results
    println!("Min: {:.3}", stats.min);
    println!("Q1: {:.3}", stats.q1);
    println!("Median: {:.3}", stats.median);
    println!("Q3: {:.3}", stats.q3);
    println!("Max: {:.3}", stats.max);
    println!("IQR: {:.3}", stats.iqr);
    println!("Outliers: {} ({:.2}%)", stats.outlier_count, stats.outlier_percentage);
    println!("\nExecution Time: {} microseconds", duration.as_micros());
}
