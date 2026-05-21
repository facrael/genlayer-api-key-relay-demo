# GenLayer Builder Submission — Studio Debugging UX Spec

Topic: Tools & Infrastructure / Improve Studio and UX

Title: Studio Debugging UX Spec for GenLayer Intelligent Contract Runs

Notes / Description:

I added a Studio debugging UX specification for subjective Intelligent Contract execution. The spec focuses on making external requests, validator observations, model outputs, equivalence checks, and final state transitions easier to inspect.

The proposed UI includes an execution trace panel, external request log, validator disagreement view, prompt/input snapshot export, and a portable run report format that builders can attach to GitHub issues or Builder submissions.

The main gotcha is that builders can confuse contract logic bugs with external-data consistency bugs. Studio should make that distinction visible by showing where leader and validators diverged.

Evidence Description: GitHub repository / UX specification
URL: https://github.com/facrael/genlayer-api-key-relay-demo
