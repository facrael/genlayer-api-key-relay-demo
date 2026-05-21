# GenLayer Builder Submission — External Data Relay Kit MVP

Topic: Projects & Milestones

Title: GenLayer External Data Relay Kit MVP Milestone

Notes / Description:

I packaged the relay work as an MVP milestone for a GenLayer external-data relay kit. The repo now includes private API-key relay logic, signed responses, benchmark tooling, a security report, a price-feed variant, and a Studio debugging UX spec.

The milestone report summarizes what works, how it was verified, known limitations, and the next technical roadmap. Tests cover validation, secret stripping, signed response verification, replay/expiry rejection, price normalization, and benchmark report generation.

The main gotcha is that this is not a decentralized oracle. It is a practical builder-side relay kit that makes trust boundaries explicit and gives future work a concrete path: public-key signatures, multi-provider checks, cache windows, and Studio run reports.

Evidence Description: GitHub repository / project milestone
URL: https://github.com/facrael/genlayer-api-key-relay-demo
