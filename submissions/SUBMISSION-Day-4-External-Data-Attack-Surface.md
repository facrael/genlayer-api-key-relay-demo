# GenLayer Builder Submission — External Data Attack Surface

Topic: Research & Analysis / Security audits

Title: External Data Attack Surface for GenLayer Intelligent Contracts

Notes / Description:

I added a security report for Intelligent Contracts that consume external API data through relays. The report documents vulnerable and patched patterns for external-data use.

The attack surface includes input injection, schema drift, stale data, validator disagreement, malicious HTML/API content, retry manipulation, and relay tampering. The repo ties these risks back to the relay implementation, signed responses, and benchmark/cache-window recommendations.

The main gotcha is that external data is part of the contract attack surface. A contract can be logically correct and still fail because live inputs are unstable, malicious, or observed differently by validators.

Evidence Description: GitHub repository / security review
URL: https://github.com/facrael/genlayer-api-key-relay-demo
