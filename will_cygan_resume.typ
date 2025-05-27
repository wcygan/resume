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
      "Software Engineer working on Purchase and Payments systems at LinkedIn",
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
  - Architected a high-performance alerting system using Kafka, Samza, and Venice, enabling real-time invoice tracking and alerts at 50,000+ QPS for the LinkedIn Global Alerts feature.
  - Reclaimed \$2M+ in annualized revenue by preventing involuntary churn through the Global Alerts system, contributing to bottom-line growth at LinkedIn and customer retention efforts.
  - Engineered a Kusto-based exception summary dashboard, integrating access and application logs, reducing incident triage time from tens of minutes to seconds and enhancing overall efficiency.
  - Led JVM optimization efforts using A/B testing to improve JVM health from 30-80% to 99.9% across unhealthy production services.
]

#resume-entry(
  title: "Software Engineer",
  location: "San Francisco, CA",
  date: "Feb 2022 - March 2024",
  description: "LinkedIn",
  title-link: "https://www.linkedin.com/in/wcygan/",
)

#resume-item[
  - Contributed to the backend implementation of VYMBII (Videos You Might Be Interested In) for LinkedIn Learning courses on linkedin.com/feed, serving videos at around 3,000 QPS.
  - Leveraged ML models to personalize video recommendations for courses displayed in a carousel format similar to TikTok, resulting in a 10%+ increase in course engagement.
  - Developed the offline flows (Spark+HDFS) for Learning Alerts, a recommendation system that classifies users based on job-seeking preferences and delivers targeted course recommendations to 10M users weekly.
]

#resume-entry(
  title: "Software Engineer Intern", 
  location: "San Francisco, CA",
  date: "Winter 2020, Summer 2021",
  description: "LinkedIn",
  title-link: "https://www.linkedin.com/in/wcygan/",
)

#resume-item[
  - Introduced new learning recommendations into the homepage feed for LinkedIn Learning.
  - Built a course ranker to attract job seekers to LinkedIn Learning.
  - Created a discovery experience on LinkedIn Learning.
  - Leveraged the economic graph to discover relevant skills for job titles.
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
  location: github-link("wcygan/tokio-utils"),
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
    strong("Temporal"),
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
