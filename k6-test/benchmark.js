import http from 'k6/http';
import { sleep, check } from 'k6';

// Define options for the benchmark test
export const options = {
    // Number of virtual users
    vus: 100000, // 10 concurrent users
    // Duration of the test
    duration: '10s', // Run for 30 seconds
};

// Default function that k6 will run
export default function () {
    // Make an HTTP GET request to the local server
    const res = http.get('http://localhost:8000/');

    // Check if the response status is 200
    check(res, {
        'status is 200': (r) => r.status === 200,
    });

    sleep(0);
}
