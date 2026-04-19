#import "template/modern-cv.typ": *

// Disable automatic hyphenation so soft hyphens (U+00AD) don't leak into
// ATS extractor output (Tika breaks hyphenated words across paragraphs).
#set text(hyphenate: false)
// Disable smart-quote substitution so straight ' and " survive extraction —
// U+2019 (curly apostrophe) is flagged as mojibake by the extraction gate.
#set smartquote(enabled: false)
// Disable paragraph justification so body text wraps left-aligned —
// justified text causes river-spacing in the dense bullets below.
#set par(justify: false)

#show: resume.with(
  author: (
    firstname: "Will",
    lastname: "Cygan",
    email: "wcygan.io@gmail.com",
    homepage: "https://wcygan.net",
    github: "wcygan",
    linkedin: "wcygan",
    positions: (
      "Senior Software Engineer, LinkedIn Business Platform",
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
  date: "Mar 2024 – Present",
  description: "LinkedIn",
)

#resume-item[
  - Led design of churn-recovery alerting platform driving \$2M+ annually by notifying subscribers of failed payments before cancellation; extended by 3 partner teams for Winback Offers, Usage Billing, and Mobile Billing (Venice KV read path sustaining 100K QPS peak from Feed; Kafka+Flink write path at \~500 msg/s on invoice-state changes).
  - Designed Oracle-to-MySQL Delegation Framework (shadow reads, query perf comparison, phased migration, rollback) onboarded by all 10 LBP domain teams as the org-wide migration pattern; novel Couchbase-TTL entity-routing cutover ensured strong consistency with GoldenGate-caught-up safety guarantees.
  - Led zero-downtime Oracle-to-MySQL migration of LinkedIn's Ordering Database (12TB / 20B rows / 6 tables) in partnership with DBAs running GoldenGate replication; rewrote 30,000+ lines of SQL/Java across \~75 PRs with JooQ/Flyway; zero data loss through 6-week phased ramp.
  - Built distributed deletion pipeline (Airflow, Trino, Kafka, gRPC) that purged 300,000 corrupted order records in production with rate-limited writes; pipeline repurposed to target \~33% of the 10+ year-old Ordering database (\~6B dormant OMS rows).
  - Automated Venice TTL purging of 35+ day records on the Global Alerts cache, cutting cache size 40% and downstream Invoice Search API QPS 50%.
  - Eliminated N+1 query problem in Order Processing system, reducing average query latency by 40% (50ms→30ms) and p95 by 37% (200ms→125ms) across all ordering workflow read paths.
  - Designed Unified Optimistic Locking mechanism for the MySQL Ordering Database, eliminating a class of silent conflicting-write failures under Temporal activity retries via version-based concurrency control across every update-based write path.
  - Delivered 5 agentic-development KT sessions reaching 1,000+ engineers using Claude Code; mentored 2 engineers on Global Alerts and MySQL Migration through design reviews and feature guidance, upleveling them and expanding team capability.
]

#resume-entry(
  title: "Software Engineer",
  location: "San Francisco, CA",
  date: "Feb 2022 – Mar 2024",
  description: "LinkedIn",
)

#resume-item[
  - Scaled Videos You Might Be Interested In recommendation to 3,000 QPS on LinkedIn's 50M+ DAU Flagship Feed, driving +2.5% Weekly Skilled Learners (LinkedIn Learning's north-star metric) and +0.57% SWI on Skill Credits across 3 experiments.
  - Built Learning Alerts V2 member/stage targeting framework from scratch, driving +1.09% WSL via Spark pipelines over 20+ datasets (\~50TB/run) classifying 10M+ job seekers into career-change-funnel cohorts with deterministic bucketing for clean A/B readouts; ramped safely to 22M members.
  - Improved LinkedIn Flagship Feed engagement +0.2% by filtering audio-only content from video course recommendations, a statistically significant lift at hundreds of millions of daily impressions.
]

= Projects

#resume-entry(
  title: "Anton (Kubernetes Homelab)",
  location: [#github-link("wcygan/anton")],
)

#resume-item[
  - Built fault-tolerant 3-node bare-metal Kubernetes cluster using Talos Linux with GitOps CI/CD automation, achieving 99.9% uptime over 12+ months.
  - Deployed distributed data systems (TiDB, RedPanda, DragonflyDB, ScyllaDB, ClickHouse) to evaluate performance characteristics and operational trade-offs of modern database alternatives.
]

= Skills

#resume-skill-item(
  "Tools",
  (
    "Claude Code",
    "Codex",
    "Java",
    "Rust",
    "Python",
    "SQL",
    "Bash",
    "TypeScript",
  ),
)
#resume-skill-item(
  "Infrastructure", 
  (
    "Kafka",
    "Flink",
    "Temporal",
    "gRPC",
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

// Force a paragraph break + vertical gap so ATS extractors (especially
// pdftotext -layout) emit a blank line between Skills and Education.
#parbreak()
#v(12pt, weak: false)

= Education

#resume-entry(
  title: "University of Illinois at Chicago",
  location: "Chicago, IL",
  date: "2021",
  description: "B.S. in Computer Science",
)
