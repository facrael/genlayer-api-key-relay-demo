# Building a Private API Key Relay for GenLayer Intelligent Contracts

I built a small relay pattern for GenLayer Intelligent Contracts that need external APIs without exposing API keys. The first demo uses weather data, but the pattern is meant for any API-backed contract: price feeds, social media checks, compliance lookups, routing data, or project-specific private APIs.

The relay keeps `WEATHER_API_KEY` server-side, validates the requested city, calls the upstream API, and returns only a normalized `weather.v1` JSON object. The Intelligent Contract sketch consumes that sanitized response and makes a simple weather-risk decision. The key point is the boundary: the contract sees useful external data, while the upstream secret never appears in contract code, calldata, validator prompts, or returned JSON.

The main gotcha is that hiding the API key does not magically remove trust. The relay can still lie, fail, censor, or return data at a different time to different validators. That is why the repo includes a threat model covering API-key leakage, input injection, schema drift, validator disagreement, stale data, and relay tampering.

The next step is to make the relay responses signed and cache them by time window, so validators can compare the same payload instead of racing a live API. For GenLayer builders, this kind of service layer feels like common infrastructure: not a full oracle network, but a practical pattern for safely connecting Intelligent Contracts to private-key APIs.
