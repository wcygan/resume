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
  - Architected a high-performance alerting system using Kafka, Samza, and Venice, processing 50,000+ QPS to provide real-time invoice tracking and critical financial alerts for LinkedIn's Global Alerts platform.
  - Reclaimed \$2M+ in annualized revenue by preventing involuntary churn through the Global Alerts system, directly impacting LinkedIn's bottom-line and enhancing customer retention.
  - Pioneered a scalable Oracle-to-MySQL migration framework, empowering a dozen engineering teams to seamlessly onboard to MySQL, significantly accelerating organizational database modernization efforts.
  - Orchestrated the design and execution of a zero-downtime migration for 2 key services from Oracle to MySQL; ensured strong data consistency throughout the transition by leveraging a Couchbase-backed pinning strategy for entity routing.
  - Spearheaded the migration of 4 critical services from Rest.li to gRPC, enhancing system interoperability and boosting developer productivity through standardized tooling and comprehensive documentation.
  - Optimized the Global Alerts system by implementing an Airflow-based offline workflow to proactively identify and purge stale cache records, successfully cutting downstream service traffic by 50%.
  - Led JVM optimization initiatives, employing A/B testing methodologies to elevate JVM health from a baseline of 30-80% to a consistent 99.9%+ across critical, underperforming production services.
]

#resume-entry(
  title: "Software Engineer",
  location: "San Francisco, CA",
  date: "Feb 2022 - March 2024",
  description: "LinkedIn",
  title-link: "https://www.linkedin.com/in/wcygan/",
)

#resume-item[
  - Developed and scaled backend microservices for "Videos You Might Be Interested In" (VYMBII), a LinkedIn Learning discovery feature on the main feed, handling ~3,000 QPS.
  - Engineered the backend data infrastructure powering personalized video course recommendations within a TikTok-style carousel, achieving a 10%+ uplift in member engagement with learning content.
  - Engineered robust offline data pipelines using Spark and HDFS for "Learning Alerts," a system classifying 10M+ users weekly to deliver targeted course recommendations based on job-seeking signals.
]

= Projects

#resume-entry(
  title: "Anton (Kubernetes Homelab)",
  location: [#github-link("wcygan/anton")],
  date: "December 2024 - Present",
  description: "Cluster Operator / Technician",
)

#resume-item[
  - Constructed a 3-node Kubernetes control plane on Talos Linux, achieving a fault-tolerant, highly available cluster.
  - Implemented zero-trust remote access via Cloudflare Tunnels and Tailscale, streamlining remote cluster management
  - Deployed data infrastructure like TiDB, RedPanda, DragonflyDB, and ScyllaDB for experimentation & learning
]

#resume-entry(
  title: "tokio-utils Rust Library",
  location: [#github-link("wcygan/tokio-utils")],
  date: "March 2023 - Present",
  description: "Maintainer",
)

#resume-item[
  - Crafted a library for Asynchronous Rust which supports patterns like Rate Limiting, Object Pooling, and Graceful Shutdown
  - Engineered a web crawler atop this library with rate limiting to ensure continuous data capture of internet graph data (similar to Google's PageRank) without triggering rate limits or IP blacklisting
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
    strong("Temporal Workflows"),
    strong("gRPC"),
    "Protocol Buffers",
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
