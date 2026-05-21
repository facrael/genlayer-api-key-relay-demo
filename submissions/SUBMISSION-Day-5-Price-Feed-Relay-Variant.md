# GenLayer Builder Submission — Price Feed Relay Variant

Topic: Tools & Infrastructure

Title: Price Feed Relay Variant for GenLayer Intelligent Contracts

Notes / Description:

I extended the relay pattern from weather data to price feeds with a normalized price.v1 schema. The new module validates symbols, normalizes price values, strips unsafe fields, and wraps responses with schema metadata.

The repo includes a price relay module, tests for symbol validation and secret stripping, and a GenLayer-style PriceVolatilityGuardContract sketch that rejects execution when relay price drift exceeds a configured basis-point threshold.

The main gotcha is that price feeds need tighter cache windows and explicit drift tolerance than weather-like data. A schema-first relay helps builders make those assumptions visible before validators rely on the data.

Evidence Description: GitHub repository / price relay implementation
URL: https://github.com/facrael/genlayer-api-key-relay-demo
