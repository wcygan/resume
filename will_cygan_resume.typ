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
      "Senior Software Engineer",
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
  date: "March 2024 – Present",
  description: "LinkedIn",
  title-link: "https://www.linkedin.com/in/wcygan/",
)

#resume-item[
  - Architected alerting system processing 50,000+ QPS using Kafka/Samza/Venice, enabling real-time payment failure detection that reduced involuntary churn by 15% across LinkedIn's commerce platform.
  - Eliminated involuntary customer churn by implementing proactive payment failure alerts, recovering \$2M+ in annual revenue and improving subscription retention metrics.
  - Pioneered reusable Oracle-to-MySQL migration framework adopted by 12 teams, saving 1 month of engineering time per team and accelerating organizational MySQL adoption efforts.
  - Executed zero-downtime Oracle-to-MySQL migration for 2 services handling 3,000 QPS, maintaining 99.99% data consistency using Couchbase-backed entity routing strategy.
  - Migrated 4 critical services from Rest.li to gRPC and standardized service documentation with Docusaurus, accelerating developer onboarding from 2 weeks to 3 days through consistent tooling.
  - Reduced downstream traffic by 50% and enhanced reliability by 10% through automated Airflow job that purges 30,000 stale cache records daily.
  - Optimized JVM performance across 5 production services from 30-80% to 99.9%+ health, reducing GC spikes by 86% (700ms to 100ms) and eliminating daily alerts.
]

#resume-entry(
  title: "Software Engineer",
  location: "San Francisco, CA",
  date: "Feb 2022 – March 2024",
  description: "LinkedIn",
  title-link: "https://www.linkedin.com/in/wcygan/",
)

#resume-item[
  - Scaled LinkedIn Learning's VYMBII recommendation service to 3,000 QPS while maintaining 99.9% availability, increasing video discovery CTR by 10% for personalized learning content.
  - Designed Spark pipelines processing 20+ datasets and 50+TB weekly to classify 10M+ job seekers, enabling targeted Learning Alerts with 5% higher enrollment rates.
  - Launched personalized recommendation engine serving 50M+ daily active users, achieving 10% engagement uplift through TikTok-style carousel UX for video course discovery.
]

= Projects

#resume-entry(
  title: "Anton (Kubernetes Homelab)",
  location: [#github-link("wcygan/anton")],
)

#resume-item[
  - Engineered fault-tolerant 3-node bare-metal Kubernetes cluster using Talos Linux, achieving 99.9% uptime while implementing GitOps CI/CD patterns with Flux.
  - Benchmarked distributed data systems (TiDB, RedPanda, DragonflyDB, ScyllaDB) to explore modern alternatives to traditional databases and messaging platforms.
  - Fortified cluster with zero-trust architecture using Cloudflare Tunnels and Tailscale.
]

#resume-entry(
  title: "tokio-utils Rust Library",
  location: [#github-link("wcygan/tokio-utils")],
)

#resume-item[
  - Released async Rust library implementing rate limiting, object pooling, and graceful shutdown patterns, achieving 2x speedup improvement in object pool benchmarks.
  - Implemented web crawler processing 300+ pages/minute with adaptive rate limiting, achieving 0% IP blacklist rate across 1,000+ domains while respecting robots.txt.
]

= Skills

#resume-skill-item(
  "Languages",
  (
    "Java",
    "Rust",
    "Go",
    "Python",
    "TypeScript",
    "SQL",
    "Scala",
    "Bash",
  ),
)
#resume-skill-item(
  "Technologies", 
  (
    "Kafka",
    "gRPC",
    "Temporal",
    "Flink",
    "Spark",
    "Airflow",
    "Kubernetes",
    "Docker",
  )
)
#resume-skill-item(
  "Databases",
  (
    "MySQL",
    "Redis",
    "Couchbase",
    "Oracle",
    "ScyllaDB",
    "DragonflyDB",
  ),
)

= Education

#resume-entry(
  title: "University of Illinois at Chicago",
  location: "Chicago, IL",
  date: "2021",
  description: "B.S. in Computer Science",
  title-link: "https://www.linkedin.com/in/wcygan/",
)
