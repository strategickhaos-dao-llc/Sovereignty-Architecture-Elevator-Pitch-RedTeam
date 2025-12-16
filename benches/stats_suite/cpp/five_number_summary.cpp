// BM-001: Five-Number Summary Implementation (C++)
// Reference implementation for cross-language benchmarking
//
// Computes: min, Q1, median, Q3, max, IQR, and outlier count
// Input: Whitespace-separated numbers from stdin
// Output: Statistical summary to stdout

#include <iostream>
#include <vector>
#include <algorithm>
#include <chrono>
#include <iomanip>
#include <cmath>

using namespace std;
using namespace std::chrono;

// TODO: Implement five-number summary calculation
// This is a placeholder for the actual implementation

struct Statistics {
    double min;
    double q1;
    double median;
    double q3;
    double max;
    double iqr;
    int outlier_count;
    double outlier_percentage;
};

Statistics compute_five_number_summary(vector<double>& data) {
    Statistics stats;
    
    if (data.empty()) {
        cerr << "Error: Empty dataset" << endl;
        exit(1);
    }
    
    // Sort the data (required for quantile calculation)
    sort(data.begin(), data.end());
    
    size_t n = data.size();
    
    // TODO: Implement actual calculation
    // For now, this is a stub that returns placeholder values
    stats.min = data[0];
    stats.max = data[n - 1];
    stats.median = 0.0;  // Placeholder
    stats.q1 = 0.0;      // Placeholder
    stats.q3 = 0.0;      // Placeholder
    stats.iqr = 0.0;     // Placeholder
    stats.outlier_count = 0;
    stats.outlier_percentage = 0.0;
    
    return stats;
}

int main() {
    // Read input data
    vector<double> data;
    double value;
    
    while (cin >> value) {
        data.push_back(value);
    }
    
    if (data.empty()) {
        cerr << "Error: No data read from input" << endl;
        return 1;
    }
    
    cout << "Read " << data.size() << " data points" << endl;
    
    // Start timing (exclude I/O time)
    auto start = high_resolution_clock::now();
    
    Statistics stats = compute_five_number_summary(data);
    
    auto end = high_resolution_clock::now();
    auto duration = duration_cast<microseconds>(end - start);
    
    // Output results
    cout << fixed << setprecision(3);
    cout << "Min: " << stats.min << endl;
    cout << "Q1: " << stats.q1 << endl;
    cout << "Median: " << stats.median << endl;
    cout << "Q3: " << stats.q3 << endl;
    cout << "Max: " << stats.max << endl;
    cout << "IQR: " << stats.iqr << endl;
    cout << "Outliers: " << stats.outlier_count 
         << " (" << setprecision(2) << stats.outlier_percentage << "%)" << endl;
    cout << "\nExecution Time: " << duration.count() << " microseconds" << endl;
    
    return 0;
}
