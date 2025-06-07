#import "@preview/modern-cv:0.8.0": *

#show: resume.with(
  author: (
    firstname: "Will",
    lastname: "Cygan",
    email: "wcygan.io@gmail.com",
    homepage: "https://wcygan.net",
    github: "wcygan",
    linkedin: "wcygan",
    positions: (
      "Software Engineer working on LinkedIn's E-Commerce Platform",
    ),
  ),
  profile-picture: none,
  date: datetime.today().display(),
  language: "en",
  colored-headers: true,
  show-footer: false,
  paper-size: "us-letter",
)

= Work Experience

#resume-entry(
  title: "Senior Software Engineer",
  location: "Chicago, IL",
  date: "March 2024 - Present",
  description: "LinkedIn",
  title-link: "https://www.linkedin.com/in/wcygan/",
)

#resume-item[
  - Architected high-performance alerting system processing 50,000+ QPS using Kafka, Samza, and Venice, enabling real-time invoice tracking and payment failure detection across LinkedIn's commerce platform.
  - Prevented involuntary customer churn by implementing proactive payment failure alerts, recovering \$2M+ in annual revenue and improving subscription retention metrics.
  - Created reusable Oracle-to-MySQL migration framework adopted by 12 teams, saving 1 month of engineering time per team and accelerating organizational MySQL adoption efforts.
  - Executed zero-downtime Oracle-to-MySQL migration for 2 services handling 10K TPS, maintaining 99.99% data consistency using Couchbase-backed entity routing strategy.
  - Migrated 4 critical services from Rest.li to gRPC and standardized service documentation with Docusaurus, accelerating developer onboarding from 2 weeks to 3 days through consistent tooling.
  - Resolved cache bloat issues by implementing daily Airflow job that identifies and removes 30,000 stale records, resulting in 50% less downstream traffic and 10% better reliability
  - Improved JVM health from 30-80% to 99.9%+ across 5 production services through A/B tested optimizations, reducing garbage collection spikes from 700ms to 100ms and resolving daily alerts.
]

#resume-entry(
  title: "Software Engineer",
  location: "San Francisco, CA",
  date: "Feb 2022 - March 2024",
  description: "LinkedIn",
  title-link: "https://www.linkedin.com/in/wcygan/",
)

#resume-item[
  - Scaled LinkedIn Learning's VYMBII recommendation service to 3,000 QPS while maintaining 99.9% availability, increasing video discovery CTR by 25% for personalized learning content.
  - Designed Spark pipelines processing 20+ datasets and 50+TB weekly to classify 10M+ job seekers, enabling targeted Learning Alerts with 5% higher enrollment rates.
  - Built personalized recommendation engine serving 50M+ daily active users, achieving 10% engagement uplift through TikTok-style carousel UX for video course discovery.
]

= Projects

#resume-entry(
  title: "Anton (Kubernetes Homelab)",
  location: [#github-link("wcygan/anton")],
)

#resume-item[
  - Built 3-node Kubernetes cluster on bare metal using Talos Linux, experimenting with fault-tolerant control plane configurations and GitOps deployment patterns with Flux.
  - Deployed and experimented with distributed data systems (TiDB, RedPanda, DragonflyDB, ScyllaDB) to explore modern alternatives to traditional databases and messaging platforms.
  - Secured cluster with zero-trust architecture using Cloudflare Tunnels and Tailscale.
]

#resume-entry(
  title: "tokio-utils Rust Library",
  location: [#github-link("wcygan/tokio-utils")],
)

#resume-item[
  - Published async Rust library implementing rate limiting, object pooling, and graceful shutdown patterns, achieving 2x speedup improvement in object pool benchmarks.
  - Built web crawler processing hundreds of pages per minute with intelligent rate limiting, respecting robots.txt and avoiding IP blacklisting across diverse domains.
]

= Skills

#resume-skill-item(
  "Languages",
  (
    strong("Java"),
    strong("Rust"),
    "Go",
    "SQL",
    "Python",
    "Scala",
    "Typescript",
    "Bash",
  ),
)
#resume-skill-item(
  "Technologies", 
  (
    strong("Temporal"),
    strong("gRPC"),
    "Protocol Buffers",
    "Airflow",
    "Docker",
    "Kubernetes",
    "Talos Linux",
  )
)

#resume-skill-item(
  "Data Systems",
  (
    strong("MySQL"),
    strong("Kafka"),
    "Flink",
    "Beam",
    "Spark",
    "Hadoop",
    "Hive",
    "Trino",
    "Kusto",
    "Redis"
  ),
)

= Education

#resume-entry(
  title: "University of Illinois at Chicago",
  location: "Chicago, IL",
  date: "January 2018 - December 2021",
  description: "B.S. in Computer Science",
  title-link: "https://www.linkedin.com/in/wcygan/",
)
