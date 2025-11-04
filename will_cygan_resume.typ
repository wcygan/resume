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
      "Senior Software Engineer, Linkedin Business Platform",
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
  - Architected real-time alerting system processing 100,000+ QPS using Kafka/Flink/Venice, recovering \$2M+ annually in involuntary churn by notifying subscribers of failed payments before subscription cancellations.
  - Eliminated N+1 query problem in Order Processing system, reducing average query latency by 40% (50ms→30ms) and p95 by 37% (200ms→125ms) across all ordering workflow read paths.
  - Built reusable Oracle-to-MySQL migration framework adopted by 12 teams, saving 12+ months of cumulative engineering time and standardizing migration patterns across the organization.
  - Executed zero-downtime Oracle-to-MySQL migration for 2 databases handling 3,000 QPS, maintaining strong consistency through Couchbase-backed sticky sessions and GoldenGate replication.
  - Created Airflow cache invalidation job purging 30,000 stale records daily, preventing unnecessary gRPC calls to downstream services and reducing cross-team service load.
  - Reduced Order database size by 33% (12TB→9TB) by implementing distributed deletion pipeline using Spark, Kafka, and batch processing to safely remove 3TB of obsolete records.
  - Optimized JVM performance across 5 production services, improving health scores from 30-80% to 99.9%+ by reducing GC pause times by 86% (700ms→100ms) and eliminating daily alerts.
]

#resume-entry(
  title: "Software Engineer",
  location: "San Francisco, CA",
  date: "Feb 2022 – March 2024",
  description: "LinkedIn",
  title-link: "https://www.linkedin.com/in/wcygan/",
)

#resume-item[
  - Scaled Videos You Might Be Interested In recommendation to 3,000 QPS on LinkedIn Feed, increasing course discovery CTR by 10% through TikTok-style video carousel.
  - Built Learning Alerts Spark pipeline analyzing 50TB+ weekly to match 10M+ job seekers with learning courses aligned to their career goals, increasing notification conversion rates by 5%.
  - Developed deterministic bucketing algorithm for Learning Alerts Spark pipeline, enabling clean A/B test readouts by segmenting 10M+ users into isolated experiment groups.
]

= Projects

#resume-entry(
  title: "Anton (Kubernetes Homelab)",
  location: [#github-link("wcygan/anton")],
)

#resume-item[
  - Built fault-tolerant 3-node bare-metal Kubernetes cluster using Talos Linux with GitOps CI/CD automation, achieving 99.9% uptime over 12+ months.
  - Built and deployed e-commerce site (kneadybynaturebakery.com) on homelab cluster so my sister can sell online
  - Deployed distributed data systems (TiDB, RedPanda, DragonflyDB, ScyllaDB, ClickHouse) to evaluate performance characteristics and operational trade-offs of modern database alternatives.

]

#resume-entry(
  title: "tokio-utils Rust Library",
  location: [#github-link("wcygan/tokio-utils")],
)

#resume-item[
  - Published async Rust library implementing rate limiting, object pooling, and graceful shutdown patterns, achieving 2x performance improvement in object pool benchmarks.
  - Implemented web crawler processing 300+ pages/minute with adaptive rate limiting, achieving 0% IP blacklist rate across 1,000+ domains while building internet graph index for PageRank analysis.
]

= Skills

#resume-skill-item(
  "Languages",
  (
    "Java",
    "Rust",
    "Python",
    "SQL",
    "Bash",
    "Go",
    "TypeScript",
    "Scala",
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
    "Trino",
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
    "DragonflyDB",
    "Venice",
    "HDFS",
    "S3"
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
