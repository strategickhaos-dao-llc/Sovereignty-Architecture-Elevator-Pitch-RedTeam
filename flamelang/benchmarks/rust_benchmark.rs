// Rust Benchmark Suite for FlameLang Pattern Matching
// Implements arithmetic, algebra, and boolean logic benchmarks with Criterion

use criterion::{black_box, criterion_group, criterion_main, Criterion};
use regex::Regex;
use std::collections::HashMap;

// ============================================================================
// Arithmetic Module
// ============================================================================

mod arithmetic {
    pub fn add(a: f64, b: f64) -> f64 {
        a + b
    }

    pub fn subtract(a: f64, b: f64) -> f64 {
        a - b
    }

    pub fn multiply(a: f64, b: f64) -> f64 {
        a * b
    }

    pub fn divide(a: f64, b: f64) -> Result<f64, String> {
        if b == 0.0 {
            Err("Division by zero".to_string())
        } else {
            Ok(a / b)
        }
    }

    pub fn percentage(percent: f64, base: f64) -> f64 {
        base * (percent / 100.0)
    }
}

// ============================================================================
// Algebra Module
// ============================================================================

mod algebra {
    pub fn solve_linear(a: f64, b: f64, c: f64) -> Result<f64, String> {
        // ax + b = c => x = (c - b) / a
        if a == 0.0 {
            Err("Not a linear equation".to_string())
        } else {
            Ok((c - b) / a)
        }
    }

    #[derive(Debug, Clone)]
    pub struct QuadraticSolution {
        pub x1: f64,
        pub x2: f64,
        pub has_real_solutions: bool,
    }

    pub fn solve_quadratic(a: f64, b: f64, c: f64) -> QuadraticSolution {
        let discriminant = b * b - 4.0 * a * c;

        if discriminant < 0.0 {
            QuadraticSolution {
                x1: 0.0,
                x2: 0.0,
                has_real_solutions: false,
            }
        } else {
            let sqrt_discriminant = discriminant.sqrt();
            QuadraticSolution {
                x1: (-b + sqrt_discriminant) / (2.0 * a),
                x2: (-b - sqrt_discriminant) / (2.0 * a),
                has_real_solutions: true,
            }
        }
    }
}

// ============================================================================
// Boolean Logic Module
// ============================================================================

mod boolean_logic {
    pub fn logical_and(a: bool, b: bool) -> bool {
        a && b
    }

    pub fn logical_or(a: bool, b: bool) -> bool {
        a || b
    }

    pub fn logical_not(a: bool) -> bool {
        !a
    }

    pub fn logical_xor(a: bool, b: bool) -> bool {
        a != b
    }

    pub fn logical_implies(a: bool, b: bool) -> bool {
        !a || b
    }

    #[derive(Debug, Clone)]
    pub struct TruthTableRow {
        pub inputs: Vec<bool>,
        pub output: bool,
    }

    pub fn generate_truth_table<F>(logic_func: F, num_vars: usize) -> Vec<TruthTableRow>
    where
        F: Fn(bool, bool) -> bool,
    {
        let rows = 1 << num_vars; // 2^n combinations
        let mut table = Vec::new();

        for i in 0..rows {
            let a = (i & 2) != 0;
            let b = (i & 1) != 0;
            let output = logic_func(a, b);

            table.push(TruthTableRow {
                inputs: vec![a, b],
                output,
            });
        }

        table
    }
}

// ============================================================================
// Pattern Matching Module
// ============================================================================

mod pattern_matching {
    use regex::Regex;

    pub fn matches_arithmetic_addition(text: &str) -> bool {
        let pattern = Regex::new(r"(\d+(?:\.\d+)?)\s*\+\s*(\d+(?:\.\d+)?)").unwrap();
        pattern.is_match(text)
    }

    pub fn matches_quadratic(text: &str) -> bool {
        let pattern = Regex::new(r"x\^2.*[+-].*x.*[+-].*=.*0").unwrap();
        pattern.is_match(text)
    }

    pub fn classify_question(text: &str) -> &'static str {
        if matches_arithmetic_addition(text) {
            "arithmetic_addition"
        } else if matches_quadratic(text) {
            "quadratic_equation"
        } else {
            "unknown"
        }
    }
}

// ============================================================================
// Benchmark Definitions
// ============================================================================

fn bench_arithmetic_addition(c: &mut Criterion) {
    c.bench_function("arithmetic::add", |b| {
        b.iter(|| arithmetic::add(black_box(123.456), black_box(789.012)))
    });
}

fn bench_arithmetic_multiplication(c: &mut Criterion) {
    c.bench_function("arithmetic::multiply", |b| {
        b.iter(|| arithmetic::multiply(black_box(123.456), black_box(789.012)))
    });
}

fn bench_arithmetic_division(c: &mut Criterion) {
    c.bench_function("arithmetic::divide", |b| {
        b.iter(|| arithmetic::divide(black_box(123.456), black_box(789.012)))
    });
}

fn bench_arithmetic_percentage(c: &mut Criterion) {
    c.bench_function("arithmetic::percentage", |b| {
        b.iter(|| arithmetic::percentage(black_box(25.0), black_box(80.0)))
    });
}

fn bench_linear_solver(c: &mut Criterion) {
    c.bench_function("algebra::solve_linear", |b| {
        b.iter(|| algebra::solve_linear(black_box(2.0), black_box(3.0), black_box(7.0)))
    });
}

fn bench_quadratic_solver(c: &mut Criterion) {
    c.bench_function("algebra::solve_quadratic", |b| {
        b.iter(|| algebra::solve_quadratic(black_box(1.0), black_box(-5.0), black_box(6.0)))
    });
}

fn bench_logical_and(c: &mut Criterion) {
    c.bench_function("boolean_logic::logical_and", |b| {
        b.iter(|| boolean_logic::logical_and(black_box(true), black_box(false)))
    });
}

fn bench_logical_or(c: &mut Criterion) {
    c.bench_function("boolean_logic::logical_or", |b| {
        b.iter(|| boolean_logic::logical_or(black_box(true), black_box(false)))
    });
}

fn bench_logical_xor(c: &mut Criterion) {
    c.bench_function("boolean_logic::logical_xor", |b| {
        b.iter(|| boolean_logic::logical_xor(black_box(true), black_box(true)))
    });
}

fn bench_truth_table_generation(c: &mut Criterion) {
    c.bench_function("boolean_logic::generate_truth_table", |b| {
        b.iter(|| {
            boolean_logic::generate_truth_table(
                |a, b| boolean_logic::logical_and(a, b),
                black_box(2),
            )
        })
    });
}

fn bench_pattern_match_arithmetic(c: &mut Criterion) {
    c.bench_function("pattern_matching::matches_arithmetic_addition", |b| {
        b.iter(|| pattern_matching::matches_arithmetic_addition(black_box("What is 5 + 3?")))
    });
}

fn bench_pattern_match_quadratic(c: &mut Criterion) {
    c.bench_function("pattern_matching::matches_quadratic", |b| {
        b.iter(|| pattern_matching::matches_quadratic(black_box("Solve x^2 - 5x + 6 = 0")))
    });
}

fn bench_question_classification(c: &mut Criterion) {
    c.bench_function("pattern_matching::classify_question", |b| {
        b.iter(|| pattern_matching::classify_question(black_box("Calculate 12 + 7")))
    });
}

// ============================================================================
// Criterion Groups and Main
// ============================================================================

criterion_group!(
    arithmetic_benches,
    bench_arithmetic_addition,
    bench_arithmetic_multiplication,
    bench_arithmetic_division,
    bench_arithmetic_percentage
);

criterion_group!(
    algebra_benches,
    bench_linear_solver,
    bench_quadratic_solver
);

criterion_group!(
    boolean_logic_benches,
    bench_logical_and,
    bench_logical_or,
    bench_logical_xor,
    bench_truth_table_generation
);

criterion_group!(
    pattern_matching_benches,
    bench_pattern_match_arithmetic,
    bench_pattern_match_quadratic,
    bench_question_classification
);

criterion_main!(
    arithmetic_benches,
    algebra_benches,
    boolean_logic_benches,
    pattern_matching_benches
);
