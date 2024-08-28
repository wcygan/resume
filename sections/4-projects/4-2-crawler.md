Concurrent Web Crawler 
Technologies: Rust, Tokio

Developed a high-performance, asynchronous web crawler using Rust and Tokio. The application efficiently crawls web pages to collect and index data while respecting rate limits for each domain.

Key contributions:

• Implemented a concurrent architecture using connection and parser pools for optimal performance

• Designed a domain-specific rate limiter to prevent overloading target servers

• Implemented graceful shutdown mechanism for clean termination of the crawler

• Incorporated efficient data structures (DashMap) for concurrent access to shared state

GitHub: https://github.com/wcygan/crawler