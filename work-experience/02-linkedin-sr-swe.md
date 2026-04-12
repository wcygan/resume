# Senior Software Engineer - LinkedIn (Chicago, IL (Remote))
**March 2024 - Present**

## 1. Scope & Context

- **org:** Linkedin Business Platform (LBP)
- **Team:** Checkout and Ordering
- **Team size:** 14
- **Systems owned:** Checkout Page, Order Placement System, Payment Failure Alerts
- **Scale:** 12TB Order Database, $3M+ in orders daily, 100,000 QPS alerting system
- **Primary tech stack:** Java, MySQL, gRPC, Kafka, Flink, Temporal, Airflow, Spark, HDFS

## 2. Projects & Initiatives

### [Global Alerts for LBP]
- **Context:** OMS (the legacy system) has payment failure alerts, but LBP did not since it was a new platform, and we needed the new system to be at functional parity with the old system since it avoided members losing access and drove dollars. So we set out to build the next evolution of the system for LBP.
- **Role:** Lead Engineer of a 3-person team
- **Actions:** I led the design & implementation of the alerting system for LBP. The old system was built on legacy technology, so we built a near-realtime invoice state tracking system to detect when member payments are overdue. We needed to design the system so it could cope with the scale of 100,000 QPS from LinkedIn Feed.
- **Impact:** $2M+ in annualized revenue, measured based on conversion after clicking the alerts
- **Tech:** Java, Kafka, Flink, Venice, Airflow
- **Status:** Delivered in production since Jan 2024

### [MySQL Query Pattern Optimization: Removing N+1 Queries]
- **Context:** Our database implementation was ported from Oracle, and some of the code existed since we were a startup 10+ years ago. Unfortunately, we were affected by the [N+1 Query Problem](https://planetscale.com/blog/what-is-n-1-query-problem-and-how-to-solve-it) and it was impacting the tail latency of our database queries. We needed to fix it to improve the user experience, so they weren't left waiting with a spinner
- **Role:** Investigator + Fixer
- **Actions:** Catalogued all occurrences of N+1, fixed them in the new MySQL implementation by batching the queries
- **Impact:** We saw tail latencies (~p95) drop from 200ms to 125ms, and average latency drop from 50ms to 30ms. This effort improved our ability to scale to higher amounts of traffic against our system, even while our dataset was massive (20 billion rows in the database)
- **Tech:** Java, MySQL
- **Status:** Delivered in production since December 2025

### [MySQL Migration of Ordering System]
- **Context:** In FY26, we launched a company-wide initiative to migrate away from the Oracle database. Our teams in LBP used it heavily in a monolithic way where 12+ teams shared the same database. Our organization's ability to scale was impacted by this because an issue for one team could be a problem for every other team, impacting org-wide availability given the shared nature of the database and replication infrastructure. So each team would be responsible for creating their own database which is separate from the other teams to avoid the noisy neighbor issue and allow each domain to scale independently.
- **Role:** Lead Engineer of 2 person team to design & execute on the migration
- **Actions:** Our team owns 2 applications powered by Oracle, so I catalogued all tables being used by our teams and designed the plan for us to migrate off of Oracle and onto our own MySQL databases while keeping the applications fully running. We worked with DBAs to copy the data from Oracle to MySQL, create GoldenGate replication pipelines to keep the databases in sync, and re-write the entire SQL/Application code stack using JooQ and Flyway to make the codebase cleaner and easier to integrate with. The developer experience of working with our databases became vastly better well-documented. The migration itself was a slow ramp over ~6 weeks of incremental progress to ensure that customers were migrated with 0% data loss and full compatibility with the ordering system's logic. In addition to this, we migrated to a new offline data source by creating a full-dump of the database and attaching a Change-Data-Capture stream to keep the data lake updated with new data.
- **Impact:** Full migration off of Oracle (primary OKR), improved developer experience, added documentation to all database code, achieved a phased migration with zero data loss and zero downtime.
- **Tech:** Java, MySQL, Oracle, Couchbase, Kafka, Brooklin (CDC), GoldenGate (Replication), OpenHouse, HDFS
- **Status:** Delivered in production since December 2025

### [Oracle to MySQL Delegation Framework]
- **Context:** In FY26, the 12+ domain teams in LBP needed a path to migrate from Oracle to MySQL. Given we all had an urgent need to migrate, it was a good time to invest time investigating in migration infrastructure rather than trying to actively migrate our codebases. Given this was early in the development cycle of the MySQL migration, we set aside time to invest in shared infrastructure to accelerate all teams in our organization.
- **Role:** Individual Contributor, primary designer of the delegation framework.
- **Actions:** I proactively identified the ability to create a framework to perform the migration in a consistent manner. This existed as a Java library that each team could onboard to by providing their Oracle and MySQL implementations 
- **Impact:** The framework mitigated risk & reduced scope for each team in the organization by eliminating duplicated work and providing a battle-tested way for them to migrate in a reasonable time frame
- **Tech:** Java, Oracle, MySQL, Couchbase
- **Status:** Delivered in May 2026, and directly led to multiple successful migrations in FY26

### [MySQL Legacy Data Cleanup (18 Billion Rows)]
- **Context:** TBD
- **Role:** Individual Contributor
- **Actions:** TBD
- **Impact:** TBD
- **Tech:** TBD
- **Status:** TBD

### [LBP Global Alerts Cache Invalidation / Stale Data Cleanup]
- **Context:** TBD
- **Role:** Individual Contributor
- **Actions:** TBD
- **Impact:** TBD
- **Tech:** TBD
- **Status:** TBD

### [LBP Availability Investigator (Kusto)]
- **Context:** TBD
- **Role:** Individual Contributor
- **Actions:** TBD
- **Impact:** TBD
- **Tech:** TBD
- **Status:** TBD

### [Oracle to MySQL Migration Dashboard]
- **Context:** TBD
- **Role:** Individual Contributor
- **Actions:** TBD
- **Impact:** TBD
- **Tech:** TBD
- **Status:** TBD

### [LBP Data Quality jobs for Ordering & Global Alerts data]
- **Context:** TBD
- **Role:** Individual Contributor
- **Actions:** TBD
- **Impact:** TBD
- **Tech:** Airflow, Trino, HDFS, OpenHouse
- **Status:** TBD

## Bullet Points
- Architected real-time alerting system processing 100,000+ QPS using Kafka/Flink/Venice, recovering $2M+ annually in involuntary churn by notifying subscribers of failed payments before subscription cancellations.
- Eliminated N+1 query problem in Order Processing system, reducing average query latency by 40% (50ms→30ms) and p95 by 37% (200ms→125ms) across all ordering workflow read paths.
- Built reusable Oracle-to-MySQL migration framework adopted by 12 teams, saving 12+ months of cumulative engineering time and standardizing migration patterns across the organization.
- Executed zero-downtime Oracle-to-MySQL migration for 2 databases handling 3,000 QPS, maintaining strong consistency through Couchbase-backed sticky sessions and GoldenGate replication.
- Created Airflow cache invalidation job purging 30,000 stale records daily, preventing unnecessary gRPC calls to downstream services and reducing cross-team service load.
- Reduced Order database size by 33% (12TB→9TB) by implementing distributed deletion pipeline using Spark, Kafka, and batch processing to safely remove 3TB of obsolete records.
- Optimized JVM performance across 5 production services, improving health scores from 30-80% to 99.9%+ by reducing GC pause times by 86% (700ms→100ms) and eliminating daily alerts.