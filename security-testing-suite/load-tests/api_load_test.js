// api_load_test.js - k6 Load Testing Script
// Strategickhaos Sovereign Infrastructure Security Testing Suite
//
// Multi-stage load testing with:
// - Gradual ramp-up (20 → 50 → 100 users)
// - Policy evaluation time tracking
// - P95/P99 latency thresholds
// - Failure rate monitoring
// - Custom metrics for OPA integration
//
// Usage: k6 run api_load_test.js --env TARGET_URL=http://localhost:8000

import http from 'k6/http';
import { check, sleep, group } from 'k6';
import { Rate, Trend, Counter } from 'k6/metrics';

// Custom metrics
const policyEvaluationTime = new Trend('policy_evaluation_time', true);
const authSuccessRate = new Rate('auth_success_rate');
const authFailureRate = new Rate('auth_failure_rate');
const apiErrorRate = new Rate('api_error_rate');
const requestsPerSecond = new Counter('requests_per_second');

// Configuration
const TARGET_URL = __ENV.TARGET_URL || 'http://localhost:8000';
const AUTH_TOKEN = __ENV.AUTH_TOKEN || 'test-token';

// Load test stages
export const options = {
    stages: [
        // Warm-up
        { duration: '30s', target: 10 },
        // Ramp up to 20 users
        { duration: '1m', target: 20 },
        // Hold at 20 users
        { duration: '2m', target: 20 },
        // Ramp up to 50 users
        { duration: '1m', target: 50 },
        // Hold at 50 users
        { duration: '3m', target: 50 },
        // Ramp up to 100 users
        { duration: '1m', target: 100 },
        // Hold at 100 users
        { duration: '3m', target: 100 },
        // Ramp down
        { duration: '1m', target: 0 },
    ],
    thresholds: {
        // Response time thresholds
        http_req_duration: ['p(95)<500', 'p(99)<1000'],
        // Policy evaluation should be fast
        policy_evaluation_time: ['p(95)<100', 'p(99)<200'],
        // Error rates
        http_req_failed: ['rate<0.01'], // Less than 1% failures
        api_error_rate: ['rate<0.05'], // Less than 5% API errors
        auth_failure_rate: ['rate<0.01'], // Less than 1% auth failures
    },
    // Tags for filtering in Grafana
    tags: {
        test_type: 'load',
        environment: __ENV.ENVIRONMENT || 'test',
    },
};

// Request headers
const headers = {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${AUTH_TOKEN}`,
    'X-Request-ID': 'k6-load-test',
};

// Test scenarios
const scenarios = {
    // Health check endpoint
    healthCheck: () => {
        const response = http.get(`${TARGET_URL}/health`, { headers });
        
        check(response, {
            'health check status is 200': (r) => r.status === 200,
            'health check response time < 100ms': (r) => r.timings.duration < 100,
        });
        
        return response;
    },
    
    // List resources (read operation)
    listResources: () => {
        const response = http.get(`${TARGET_URL}/api/v1/resources`, { headers });
        
        const success = check(response, {
            'list resources status is 200': (r) => r.status === 200,
            'list resources has data': (r) => {
                try {
                    const body = JSON.parse(r.body);
                    return Array.isArray(body) || body.items !== undefined;
                } catch (e) {
                    return false;
                }
            },
        });
        
        apiErrorRate.add(!success);
        requestsPerSecond.add(1);
        
        return response;
    },
    
    // Get single resource (read with ID)
    getResource: () => {
        const resourceId = Math.floor(Math.random() * 1000) + 1;
        const response = http.get(`${TARGET_URL}/api/v1/resources/${resourceId}`, { headers });
        
        check(response, {
            'get resource status is 200 or 404': (r) => r.status === 200 || r.status === 404,
        });
        
        return response;
    },
    
    // Create resource (write operation)
    createResource: () => {
        const payload = JSON.stringify({
            name: `test-resource-${Date.now()}`,
            description: 'Load test resource',
            type: 'test',
        });
        
        const response = http.post(`${TARGET_URL}/api/v1/resources`, payload, { headers });
        
        const success = check(response, {
            'create resource status is 201 or 200': (r) => r.status === 201 || r.status === 200,
            'create resource response time < 500ms': (r) => r.timings.duration < 500,
        });
        
        apiErrorRate.add(!success);
        requestsPerSecond.add(1);
        
        return response;
    },
    
    // Authentication test
    authenticate: () => {
        const payload = JSON.stringify({
            username: 'testuser',
            password: 'testpassword',
        });
        
        const response = http.post(`${TARGET_URL}/api/v1/auth/login`, payload, {
            headers: { 'Content-Type': 'application/json' },
        });
        
        const success = response.status === 200;
        authSuccessRate.add(success);
        authFailureRate.add(!success && response.status !== 401);
        
        return response;
    },
    
    // OPA policy evaluation test
    evaluatePolicy: () => {
        const payload = JSON.stringify({
            input: {
                user: {
                    id: `user-${Math.floor(Math.random() * 100)}`,
                    role: ['admin', 'user', 'moderator', 'guest'][Math.floor(Math.random() * 4)],
                },
                action: ['read', 'write', 'delete'][Math.floor(Math.random() * 3)],
                resource: {
                    type: 'document',
                    id: `${Math.floor(Math.random() * 1000)}`,
                },
            },
        });
        
        const startTime = Date.now();
        const response = http.post(`${TARGET_URL}/api/v1/authorize`, payload, { headers });
        const evalTime = Date.now() - startTime;
        
        policyEvaluationTime.add(evalTime);
        
        check(response, {
            'policy evaluation status is 200': (r) => r.status === 200,
            'policy evaluation time < 100ms': () => evalTime < 100,
            'policy returns decision': (r) => {
                try {
                    const body = JSON.parse(r.body);
                    return body.allow !== undefined || body.result !== undefined;
                } catch (e) {
                    return false;
                }
            },
        });
        
        return response;
    },
    
    // Search operation (potentially expensive)
    searchResources: () => {
        const queries = ['test', 'resource', 'data', 'user', ''];
        const query = queries[Math.floor(Math.random() * queries.length)];
        
        const response = http.get(`${TARGET_URL}/api/v1/search?q=${encodeURIComponent(query)}`, { headers });
        
        check(response, {
            'search status is 200': (r) => r.status === 200,
            'search response time < 1000ms': (r) => r.timings.duration < 1000,
        });
        
        return response;
    },
    
    // Admin endpoint (should require elevated permissions)
    adminOperation: () => {
        const response = http.get(`${TARGET_URL}/api/v1/admin/users`, { headers });
        
        check(response, {
            'admin endpoint returns expected status': (r) => 
                r.status === 200 || r.status === 403 || r.status === 401,
        });
        
        return response;
    },
};

// Main test function
export default function () {
    // Distribute load across different scenarios
    const rand = Math.random();
    
    group('API Load Test', () => {
        if (rand < 0.05) {
            // 5% health checks
            group('Health Check', () => {
                scenarios.healthCheck();
            });
        } else if (rand < 0.30) {
            // 25% list operations
            group('List Resources', () => {
                scenarios.listResources();
            });
        } else if (rand < 0.50) {
            // 20% get single resource
            group('Get Resource', () => {
                scenarios.getResource();
            });
        } else if (rand < 0.60) {
            // 10% create operations
            group('Create Resource', () => {
                scenarios.createResource();
            });
        } else if (rand < 0.75) {
            // 15% policy evaluation
            group('Policy Evaluation', () => {
                scenarios.evaluatePolicy();
            });
        } else if (rand < 0.85) {
            // 10% search
            group('Search', () => {
                scenarios.searchResources();
            });
        } else if (rand < 0.90) {
            // 5% authentication
            group('Authentication', () => {
                scenarios.authenticate();
            });
        } else {
            // 10% admin operations
            group('Admin', () => {
                scenarios.adminOperation();
            });
        }
    });
    
    // Think time between requests
    sleep(Math.random() * 2 + 0.5);
}

// Setup function - runs once before test
export function setup() {
    console.log(`Starting load test against ${TARGET_URL}`);
    
    // Verify target is reachable
    const response = http.get(`${TARGET_URL}/health`);
    
    if (response.status !== 200) {
        console.warn(`Health check returned status ${response.status}`);
    }
    
    return {
        startTime: Date.now(),
        targetUrl: TARGET_URL,
    };
}

// Teardown function - runs once after test
export function teardown(data) {
    const duration = (Date.now() - data.startTime) / 1000;
    console.log(`Load test completed in ${duration.toFixed(2)} seconds`);
}

// Handle test summary
export function handleSummary(data) {
    const summary = {
        timestamp: new Date().toISOString(),
        target: TARGET_URL,
        duration: data.state.testRunDurationMs,
        iterations: data.metrics.iterations.values.count,
        vus_max: data.metrics.vus_max.values.max,
        http_reqs: data.metrics.http_reqs.values.count,
        http_req_duration: {
            avg: data.metrics.http_req_duration.values.avg,
            p95: data.metrics.http_req_duration.values['p(95)'],
            p99: data.metrics.http_req_duration.values['p(99)'],
        },
        policy_evaluation_time: data.metrics.policy_evaluation_time ? {
            avg: data.metrics.policy_evaluation_time.values.avg,
            p95: data.metrics.policy_evaluation_time.values['p(95)'],
            p99: data.metrics.policy_evaluation_time.values['p(99)'],
        } : null,
        error_rate: data.metrics.http_req_failed.values.rate,
        checks_passed: data.metrics.checks.values.passes,
        checks_failed: data.metrics.checks.values.fails,
    };
    
    return {
        'stdout': textSummary(data, { indent: ' ', enableColors: true }),
        'reports/k6_summary.json': JSON.stringify(summary, null, 2),
    };
}

// Text summary helper
function textSummary(data, options) {
    const lines = [];
    
    lines.push('');
    lines.push('═══════════════════════════════════════════════════════════');
    lines.push('                    K6 LOAD TEST SUMMARY                    ');
    lines.push('═══════════════════════════════════════════════════════════');
    lines.push('');
    lines.push(`Target URL: ${TARGET_URL}`);
    lines.push(`Duration: ${(data.state.testRunDurationMs / 1000).toFixed(2)}s`);
    lines.push(`Max VUs: ${data.metrics.vus_max.values.max}`);
    lines.push(`Total Requests: ${data.metrics.http_reqs.values.count}`);
    lines.push('');
    lines.push('Response Times:');
    lines.push(`  Average: ${data.metrics.http_req_duration.values.avg.toFixed(2)}ms`);
    lines.push(`  P95: ${data.metrics.http_req_duration.values['p(95)'].toFixed(2)}ms`);
    lines.push(`  P99: ${data.metrics.http_req_duration.values['p(99)'].toFixed(2)}ms`);
    lines.push('');
    lines.push(`Error Rate: ${(data.metrics.http_req_failed.values.rate * 100).toFixed(2)}%`);
    lines.push(`Checks Passed: ${data.metrics.checks.values.passes}/${data.metrics.checks.values.passes + data.metrics.checks.values.fails}`);
    lines.push('');
    lines.push('═══════════════════════════════════════════════════════════');
    
    return lines.join('\n');
}
