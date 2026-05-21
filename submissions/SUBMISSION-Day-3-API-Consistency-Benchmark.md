# GenLayer Builder Submission — API Consistency Benchmark

Topic: Research & Analysis / Benchmarks

Title: API Consistency Benchmark for GenLayer External Data Relays

Notes / Description:

I added an API consistency benchmark for GenLayer-style external data relays. The benchmark measures repeated relay responses across a window and reports latency, numeric variance, consistency score, and a recommended cache window.

The repo includes an offline sample dataset and a script that can also run against a live relay endpoint through RELAY_URL. The key metrics are temperature/wind/humidity variance, condition stability, and whether responses fit one validator-friendly equivalence window.

The main gotcha is that external-data execution depends on reproducibility, not just speed. Two validators can receive individually valid API responses that disagree enough to break consensus.

Evidence Description: GitHub repository / benchmark report
URL: https://github.com/facrael/genlayer-api-key-relay-demo
