// C++ Benchmark Suite for FlameLang Pattern Matching
// Implements arithmetic, algebra, and boolean logic benchmarks

#include <benchmark/benchmark.h>
#include <cmath>
#include <vector>
#include <string>
#include <regex>
#include <functional>

// ============================================================================
// Arithmetic Algorithms
// ============================================================================

namespace arithmetic {

double add(double a, double b) {
    return a + b;
}

double subtract(double a, double b) {
    return a - b;
}

double multiply(double a, double b) {
    return a * b;
}

double divide(double a, double b) {
    if (b == 0.0) throw std::invalid_argument("Division by zero");
    return a / b;
}

double percentage(double percent, double base) {
    return base * (percent / 100.0);
}

// PEMDAS Expression Evaluator (simplified)
double evaluate_expression(const std::string& expr) {
    // Simplified evaluator for demonstration
    // In production, use a proper expression parser
    return 42.0; // Placeholder
}

} // namespace arithmetic

// ============================================================================
// Algebra Algorithms
// ============================================================================

namespace algebra {

double solve_linear(double a, double b, double c) {
    // ax + b = c => x = (c - b) / a
    if (a == 0.0) throw std::invalid_argument("Not a linear equation");
    return (c - b) / a;
}

struct QuadraticSolution {
    double x1;
    double x2;
    bool has_real_solutions;
};

QuadraticSolution solve_quadratic(double a, double b, double c) {
    QuadraticSolution solution;
    double discriminant = b * b - 4 * a * c;
    
    if (discriminant < 0) {
        solution.has_real_solutions = false;
        solution.x1 = solution.x2 = 0.0;
    } else {
        solution.has_real_solutions = true;
        double sqrt_discriminant = std::sqrt(discriminant);
        solution.x1 = (-b + sqrt_discriminant) / (2 * a);
        solution.x2 = (-b - sqrt_discriminant) / (2 * a);
    }
    
    return solution;
}

} // namespace algebra

// ============================================================================
// Boolean Logic Algorithms
// ============================================================================

namespace boolean_logic {

bool logical_and(bool a, bool b) {
    return a && b;
}

bool logical_or(bool a, bool b) {
    return a || b;
}

bool logical_not(bool a) {
    return !a;
}

bool logical_xor(bool a, bool b) {
    return a != b;
}

bool logical_implies(bool a, bool b) {
    return !a || b;
}

// Truth table generation
std::vector<std::vector<bool>> generate_truth_table(
    const std::function<bool(bool, bool)>& logic_func,
    int num_variables = 2
) {
    std::vector<std::vector<bool>> table;
    int rows = 1 << num_variables; // 2^n combinations
    
    for (int i = 0; i < rows; ++i) {
        std::vector<bool> row;
        bool a = (i & 2) != 0;
        bool b = (i & 1) != 0;
        row.push_back(a);
        row.push_back(b);
        row.push_back(logic_func(a, b));
        table.push_back(row);
    }
    
    return table;
}

} // namespace boolean_logic

// ============================================================================
// Pattern Matching
// ============================================================================

namespace pattern_matching {

struct Pattern {
    std::regex regex_pattern;
    std::string category;
};

bool matches_arithmetic_addition(const std::string& text) {
    std::regex pattern(R"((\d+(?:\.\d+)?)\s*\+\s*(\d+(?:\.\d+)?))");
    return std::regex_search(text, pattern);
}

bool matches_quadratic(const std::string& text) {
    std::regex pattern(R"(x\^2.*[+-].*x.*[+-].*=.*0)");
    return std::regex_search(text, pattern);
}

std::string classify_question(const std::string& text) {
    if (matches_arithmetic_addition(text)) return "arithmetic_addition";
    if (matches_quadratic(text)) return "quadratic_equation";
    return "unknown";
}

} // namespace pattern_matching

// ============================================================================
// Benchmark Definitions
// ============================================================================

// Arithmetic Benchmarks
static void BM_Addition(benchmark::State& state) {
    double a = 123.456;
    double b = 789.012;
    for (auto _ : state) {
        benchmark::DoNotOptimize(arithmetic::add(a, b));
    }
}
BENCHMARK(BM_Addition);

static void BM_Multiplication(benchmark::State& state) {
    double a = 123.456;
    double b = 789.012;
    for (auto _ : state) {
        benchmark::DoNotOptimize(arithmetic::multiply(a, b));
    }
}
BENCHMARK(BM_Multiplication);

static void BM_Division(benchmark::State& state) {
    double a = 123.456;
    double b = 789.012;
    for (auto _ : state) {
        benchmark::DoNotOptimize(arithmetic::divide(a, b));
    }
}
BENCHMARK(BM_Division);

static void BM_Percentage(benchmark::State& state) {
    double percent = 25.0;
    double base = 80.0;
    for (auto _ : state) {
        benchmark::DoNotOptimize(arithmetic::percentage(percent, base));
    }
}
BENCHMARK(BM_Percentage);

// Algebra Benchmarks
static void BM_LinearSolver(benchmark::State& state) {
    double a = 2.0, b = 3.0, c = 7.0;
    for (auto _ : state) {
        benchmark::DoNotOptimize(algebra::solve_linear(a, b, c));
    }
}
BENCHMARK(BM_LinearSolver);

static void BM_QuadraticSolver(benchmark::State& state) {
    double a = 1.0, b = -5.0, c = 6.0;
    for (auto _ : state) {
        benchmark::DoNotOptimize(algebra::solve_quadratic(a, b, c));
    }
}
BENCHMARK(BM_QuadraticSolver);

// Boolean Logic Benchmarks
static void BM_LogicalAND(benchmark::State& state) {
    bool a = true, b = false;
    for (auto _ : state) {
        benchmark::DoNotOptimize(boolean_logic::logical_and(a, b));
    }
}
BENCHMARK(BM_LogicalAND);

static void BM_LogicalOR(benchmark::State& state) {
    bool a = true, b = false;
    for (auto _ : state) {
        benchmark::DoNotOptimize(boolean_logic::logical_or(a, b));
    }
}
BENCHMARK(BM_LogicalOR);

static void BM_LogicalXOR(benchmark::State& state) {
    bool a = true, b = true;
    for (auto _ : state) {
        benchmark::DoNotOptimize(boolean_logic::logical_xor(a, b));
    }
}
BENCHMARK(BM_LogicalXOR);

static void BM_TruthTableGeneration(benchmark::State& state) {
    auto logic_func = boolean_logic::logical_and;
    for (auto _ : state) {
        benchmark::DoNotOptimize(
            boolean_logic::generate_truth_table(logic_func, 2)
        );
    }
}
BENCHMARK(BM_TruthTableGeneration);

// Pattern Matching Benchmarks
static void BM_PatternMatchArithmetic(benchmark::State& state) {
    std::string text = "What is 5 + 3?";
    for (auto _ : state) {
        benchmark::DoNotOptimize(
            pattern_matching::matches_arithmetic_addition(text)
        );
    }
}
BENCHMARK(BM_PatternMatchArithmetic);

static void BM_PatternMatchQuadratic(benchmark::State& state) {
    std::string text = "Solve x^2 - 5x + 6 = 0";
    for (auto _ : state) {
        benchmark::DoNotOptimize(
            pattern_matching::matches_quadratic(text)
        );
    }
}
BENCHMARK(BM_PatternMatchQuadratic);

static void BM_QuestionClassification(benchmark::State& state) {
    std::string text = "Calculate 12 + 7";
    for (auto _ : state) {
        benchmark::DoNotOptimize(
            pattern_matching::classify_question(text)
        );
    }
}
BENCHMARK(BM_QuestionClassification);

// ============================================================================
// Main
// ============================================================================

BENCHMARK_MAIN();
