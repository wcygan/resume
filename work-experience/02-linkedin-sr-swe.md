# Senior Software Engineer - LinkedIn (Chicago, IL (Remote))
**March 2024 - Present**

## 1. Scope & Context

- **org:** Linkedin Business Platform (LBP)
- **Team:** Checkout and Ordering
- **Team size:** 14
- **Systems owned:** Checkout Page, Order Placement System, Payment Failure Alerts
- **Scale:** 12TB Order Database, $3M+ in orders daily, 100,000 QPS alerting system
- **Primary tech stack:** Java, MySQL, gRPC, Kafka, Flink, Temporal, Airflow, Spark, HDFS

Some of the most impactful work that I've done in this role (current date: April 2026) is the MySQL migration and Global Alerts. These projects gave me exposure to operating large-scale systems across the online, nearline, and offline stack.

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
- **Actions:** I proactively identified the ability to create a framework to perform the migration in a consistent manner. This existed as a Java library that each team could onboard to by providing their Oracle and MySQL implementations. To support each domain's ability to preserve strong consistency, we introduced a couchbase-backed entity-routing solution to allow each customer to migrate to the new database once GoldenGate replication was fully caught up for the user.
- **Impact:** The framework mitigated risk & reduced scope for each team in the organization by eliminating duplicated work and providing a battle-tested way for them to migrate in a reasonable time frame
- **Tech:** Java, Oracle, MySQL, Couchbase
- **Status:** Delivered in May 2026, and directly led to multiple successful migrations in FY26

### [Context Repos for Claude Code]
- **Context:** The company was adopting agentic coding tools throughout FY25 and FY26; I was an early adopter and looking for ways to maximize productivity and to easily find the right documents and code references over a sea of literally thousands of repositories.
- **Role:** Individual Contributor
- **Actions:** I independently came up with the idea of "Context Repos", where you create a git repository which contains git submodules that are relevant to your project, domain, or organization and augment them with context so that a tool like Claude Code knows where to look and how these codebases are interconnected.
- **Impact:** This immediately increased the velocity of myself, and other engineers in my org. For LBP specifically this idea was a boon because we operate a system of ~30+ microservices which were decomposed from our legacy OMS system. Because of the sprawl, it's often difficult for a developer to internalize what parts are connected, and what behavior they have. With context repos, developers can easily launch agents to search through projects, write PRs across codebases, and review designs against the real implementations. Ultimately this helps reduce toil and increase velocity by 
- **Tech:** Claude Code, Git Repositories
- **Status:** Piloted in May 2025, later adopted across the company in February 2026 through the Developer Producitivity organization

### [MySQL Legacy Data Cleanup (18 Billion Rows)]
- **Context:** We've run on the same database tables for over a decade, and they support both the modern system (LBP) and legacy system (OMS). It runs ~12+ TB over 20 Billion records across 6 tables. Worse, more than 95% of this data is unused! There are around 500,000,000 rows actively being used for LBP, while the rest of the rows are sitting dormant from the legacy system OMS. Having so much unused data in the database directly impacts performance and operations through index bloat, difficulty performing DDL changes, and overall query performance. 
- **Role:** Individual Contributor
- **Actions:** TBD
- **Impact:** TBD
- **Tech:** TBD
- **Status:** TBD

### [LBP Global Alerts Cache Invalidation / Stale Data Cleanup]
- **Context:** We use Venice (a caching solution) to detect when a customer "potentially has an issue" with their invoices. This is a useful quick lookup that we can perform at high-scale (100,000 QPS) and avoid putting pressure on the downstream billing system. When this hint is present, we then look in a search index to confirm which invoice is problematic, then fetch it directly from the billing database. The issue is that we don't have a perfect cache invalidation solution, so a small amount of stale data ends up staying in the cache even after the customer has reconciled an issue. This ends up putting more pressure on the search index than needed because every time the customer views linkedin.com, the search index will incur another lookup. We'd like to be good citizens, so avoiding these redundant lookups is beneficial.
- **Role:** Individual Contributor
- **Actions:** TBD
- **Impact:** TBD
- **Tech:** TBD
- **Status:** TBD

### [LBP Availability Investigator (Kusto)]
- **Context:** Engineers and Technical Support teams use application logs and access logs to debug customer issues. We typically apply the same pattern for each product/service we support, and run the same queries over and over. The problem is that every time we do this we need to memorize syntax and connect to the appropriate log databases, which becomes burdensome because we might want to reuse queries and share them with the team.
- **Role:** Individual Contributor
- **Actions:** TBD
- **Impact:** TBD
- **Tech:** TBD
- **Status:** TBD

### [Oracle to MySQL Migration Dashboard]
- **Context:** During the Oracle to MySQL Migration, we wanted to have a realtime view of the system to understand progress, health, and business metrics so that we could have immediate insights into whether things were going according to plan. But we didn't have this!
- **Role:** Individual Contributor
- **Actions:** I catalogued useful information like Database Metrics (Query speed, Query count, CPU utilization, total connections), Server Metrics (CPU, Memory, API Latency, API Call Count, API Error Rate, Connection Pool Size, Connection Pool Usage), and Business Metrics (total customers migrated, number of orders placed using MySQL) to tie the entire loop together in a single Grafana dashboard
- **Impact:** This dashboard gave us the direct capability to measure success during the migration; we had a hunch that the database migration would improve performance, and the dashboard gave us the visibility we needed to ensure that our hypothesis matched reality.
- **Tech:** Grafana, Kusto, OpenTelemetry
- **Status:** Delivered in October 2025

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