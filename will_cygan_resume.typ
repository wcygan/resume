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
  - Architected real-time alerting system processing 100,000+ QPS through linkedin.com using Kafka/Flink/Venice, enabling payment failure detection that claws back \$2M+ in involuntary churn from subscribers each year.
  - Eliminated N+1 query problem in LinkedIn's Order Processing system, reducing average query latency by 40% (50ms→30ms) and p95 by 37% (200ms→125ms) in the core read paths for ordering workflows
  - Built reusable Oracle-to-MySQL migration framework adopted by 12 teams, accelerating adoption of MySQL by saving 1 month of engineering time per team and providing consistent migration logic throughout the organization
  - Completed zero-downtime Oracle-to-MySQL migration for 2 databases handling 3,000 QPS, maintaining strong consistency using Couchbase-backed "sticky session" strategy with GoldenGate replication.
  - Created a cache invalidation job in Airflow which purges 30,000 stale cache records daily, reducing pressure on neighboring team's gRPC services (additional RPCs occur if records exist in the cache, so it's better to clean them up)
  - Identified an opportunity to reduce the Order database size by 33% (12TB→9TB) and implemented a traffic distribution pattern to delete records (Spark query to find all records, push them into Kafka, process them on the server in batches)
  - Optimized JVM performance across 5 production services from 30-80% to 99.9%+ health score, reducing GC spikes by 86% (700ms to 100ms) and eliminating daily alerts.
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
  - Built fault-tolerant 3-node bare-metal Kubernetes cluster using Talos Linux, achieving 99.9% uptime while implementing GitOps CI/CD patterns with Flux.
  - Built https://kneadybynaturebakery.com/ for my sister & hosting it in the cluster in my basement (for fun & profit)  
  - Deployed distributed data systems (TiDB, RedPanda, DragonflyDB, ScyllaDB, ClickHouse) to explore modern alternatives to traditional databases and messaging platforms. It's a good way to explore systems you wouldn't otherwise see at work.

]

#resume-entry(
  title: "tokio-utils Rust Library",
  location: [#github-link("wcygan/tokio-utils")],
)

#resume-item[
  - Published async Rust library implementing rate limiting, object pooling, and graceful shutdown patterns, achieving 2x speedup improvement in object pool benchmarks.
  - Implemented web crawler processing 300+ pages/minute with adaptive rate limiting, achieving 0% IP blacklist rate across 1,000+ domains while building an index of internet graph data (similar to the inputs of PageRank).
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
