# Senior Software Engineer — LinkedIn (Chicago, IL — Remote)
**March 2024 – Present**

## 1. Scope & Context

- **Org:** LinkedIn Business Platform (LBP — LinkedIn's modern commerce platform, successor to the legacy OMS / Order Management System)
- **Team:** Checkout and Ordering
- **Team size:** 14
- **Systems owned:** Checkout Page, Order Placement System, Payment Failure Alerts (LBP Global Alerts), MySQL/Oracle Delegation Framework
- **Scale:** $3M+ in orders daily, 100,000 QPS alerting system, 12 TB Order Database (~20 billion rows across 6 tables)
- **Key outcomes:** **$2M+ annualized revenue recovered** via LBP Global Alerts; **10 LBP domain teams** onboarded to the Oracle → MySQL Delegation Framework; full Ordering Backend migration off Oracle with zero data loss and zero downtime.
- **Primary tech stack:** Java, MySQL, Temporal, gRPC, Kafka, Flink, Airflow, Spark, Trino, HDFS, Oracle, Couchbase, Venice (distributed KV cache; venicedb.org), OpenHouse, Brooklin (change-data-capture; github.com/linkedin/brooklin), GoldenGate (Oracle replication), Grafana, OpenTelemetry, JooQ (type-safe SQL DSL), Flyway (schema migrations)

Joined LBP's Checkout and Ordering team after the LLS Learner Growth reorg in late 2023 to accelerate the migration from OMS to LBP; the first pre-promotion deliverable was the LBP Global Alerts system described below. **Promoted from Software Engineer to Senior Software Engineer in Mar 2024** on the back of that launch.

The most impactful work in this role has been the LBP Global Alerts system (recovering $2M+ annualized revenue) and the Oracle → MySQL migration of the Ordering Backend. Together they gave me ownership of the online, nearline, and offline surfaces of the commerce stack, plus a reusable database migration framework that 10 LBP domain teams now ride on.

## 3. Projects & Initiatives

### [Oracle → MySQL Migration — Commerce-Ordering]
- **Context:** In FY26 LinkedIn launched a company-wide initiative to migrate off Oracle. LBP used Oracle heavily as a shared monolithic database across 12+ teams, meaning one team's incident degraded availability for every other team. Each team needed an independent MySQL database to scale its domain independently.
- **Role:** Lead engineer; designed and drove the migration end-to-end.
- **Actions:** Catalogued all Oracle tables used by our 2 applications (12 TB dataset, 20B rows, 6 tables). Designed and executed a phased migration while keeping both applications fully running. Coordinated with DBAs to copy data from Oracle to MySQL and stand up GoldenGate replication pipelines to keep the databases in sync. Re-wrote the entire SQL/application stack using JooQ and Flyway, rewriting **30,000+ lines of legacy Oracle SQL across ~75 PRs**. Ran a slow ramp over ~6 weeks with EI / Prod testing and ramp tollgates before 1%, validating **10,000+ real orders at 1% traffic** with zero data inconsistency. Shipped the first successful MySQL production rollout for the Ordering team (Financial Reporting Service). Migrated the offline stack in parallel by creating a full dump plus a Change-Data-Capture stream (Brooklin) to keep the data lake updated.
- **Impact:** Full migration off Oracle (primary OKR), zero data loss, zero downtime. 30,000+ lines migrated across ~75 PRs. 10,000+ validated orders at the 1% tollgate. Developer experience vastly improved: type-safe queries via JooQ, schema-versioned via Flyway, fully documented.
- **Tech:** Java, MySQL, Oracle, JooQ, Flyway, Couchbase, Kafka, Brooklin (CDC), GoldenGate (replication), OpenHouse, HDFS.
- **Status:** Delivered in production since December 2025.

### [MySQL Query Pattern Optimization — N+1 Elimination]
- **Context:** The the Ordering Backend database implementation was ported from Oracle and some code dated back 10+ years to the startup era. An N+1 query pattern was inflating tail latency of database queries, degrading user experience (the dreaded purchase-flow spinner).
- **Role:** Investigator + fixer.
- **Actions:** Catalogued every N+1 occurrence across the read paths, then rewrote them in the MySQL implementation using batched queries.
- **Impact:** **p95 latency 200 ms → 125 ms** (37% reduction); **average latency 50 ms → 30 ms** (40% reduction) across all ordering workflow read paths. Unlocked headroom to scale against higher traffic despite a dataset at 20-billion-row / 12 TB scale.
- **Tech:** Java, MySQL, JooQ.
- **Status:** Delivered in production since December 2025.

### [Oracle → MySQL Delegation Framework]
- **Context:** In FY26 all 12+ LBP domain teams needed to migrate from Oracle to MySQL. Rather than every team re-solving the same consistency and rollback problems, there was a window early in the program to invest in shared migration infrastructure.
- **Role:** Primary designer and owner of the delegation framework.
- **Actions:** Proactively scoped and built the framework as a Java library that each team onboards by providing their Oracle and MySQL implementations. Introduced a Couchbase-backed entity-routing layer so each customer migrates atomically to the new database. The cutover protocol uses an A/B framework to select the next entity cohort for incremental migration, stores the Oracle-vs-MySQL routing decision in Couchbase with a 5-minute TTL for strong read-after-write consistency, and refreshes the TTL on every new write — pinning an entity to whichever database last accepted a write. Once the 5-minute window expires with no writes, GoldenGate replication is guaranteed caught up on both sides, making the flip to the other database safe. Added shadow reads, PIN support, and rollback hooks. Ran KT sessions and built a GitHub Pages wiki so every team could self-serve.
- **Impact:** Standardized migration pattern onboarded by **10 LBP domain teams** — eliminated per-team reinvention of consistency and rollback infrastructure. Directly led to multiple successful FY26 migrations beyond the Ordering Backend.
- **Tech:** Java, Oracle, MySQL, Couchbase, GoldenGate.
- **Status:** Delivered in May 2025; battle-tested through multiple subsequent migrations.

### [Oracle → MySQL Migration Dashboard]
- **Context:** During the Ordering Backend migration we needed a single real-time view of progress, system health, and business metrics to confirm the migration was landing per-plan. No such dashboard existed.
- **Role:** Individual Contributor.
- **Actions:** Catalogued the useful signal across three layers and unified them in a single Grafana dashboard: database metrics (query speed, query count, CPU, connections), server metrics (CPU, memory, API latency, API call count, error rate, connection-pool size/usage), and business metrics (customers migrated, orders placed via MySQL).
- **Impact:** Gave the team a direct measurement surface for the migration. Our hypothesis that the migration would improve performance was confirmed against the dashboard — it's the artifact that backs the 30–40% latency reduction claim.
- **Tech:** Grafana, Kusto, OpenTelemetry.
- **Status:** Delivered in October 2025.

### [Batch Order Cleanup Pipeline]
- **Context:** A prior incident had irreversibly deleted pricing data for a batch of demoted orders, leaving 300,000 corrupted order records orphaned in production. The cleanup was also the mechanism needed to eventually purge billions of legacy OMS orders ahead of downstream migration work.
- **Role:** Individual Contributor.
- **Actions:** Built a batching mechanism to safely clean up old orders from production. Designed the pipeline so the same infrastructure can scale to billions of legacy OMS orders
- **Impact:** **300,000 corrupted order records deleted** in production. Pipeline is now the mechanism that will purge the dormant OMS portion of the Order database.
- **Tech:** Java, Trino, MySQL.
- **Status:** Shipped (H2 2024).

### [MySQL Legacy Data Retention & Cleanup (18 Billion Rows)]
- **Context:** The the Ordering Backend database has run for over a decade and supports both the modern LBP system and the legacy OMS system. It holds ~12 TB across ~20 billion rows in 6 tables, and **more than 95% is unused** — roughly 500,000,000 rows actively serve LBP, while the rest sit dormant from OMS. This dormant mass directly degrades performance via index bloat, makes DDL changes risky, and inflates migration complexity.
- **Role:** Individual Contributor.
- **Actions:** Identified a **33% immediate data reduction opportunity** in Ordering database tables through infrastructure analysis. Scoped the cleanup roadmap for the 10+ year-old Ordering database, piggybacking on the Batch Order Cleanup Pipeline for execution. Remaining Actions/Impact for the full billions-scale purge to be populated as the cleanup ramps.
- **Impact:** **33% immediate reduction opportunity** identified; when executed it reduces MySQL migration complexity and directly reduces infrastructure cost. Full shipped impact TBD.
- **Tech:** Java, MySQL, Trino, Airflow, Kafka, gRPC.
- **Status:** In-flight — reduction opportunity identified H1 2025; execution ongoing, piggybacking on the Batch Order Cleanup Pipeline.

### [LBP Global Alerts — Payment Failure Alerting]
- **Context:** The legacy OMS had payment-failure alerts; LBP, as a newer platform, did not. The new system needed functional parity to avoid members losing access and to recover otherwise-lost subscription revenue. The target was a near-real-time invoice state tracking system that could cope with 100,000 QPS from LinkedIn Feed.
- **Role:** Lead engineer (with 1 IC during the build phase).
- **Actions:** Led design and implementation of the LBP alerting system with 1 IC, originally scoped to subscription products (LinkedIn Premium). Built near-real-time invoice state tracking to detect overdue member payments. Sized the read path for 100,000 QPS against LinkedIn Feed using Venice as the high-scale lookup layer; the write path (Kafka + Flink) processes ~500 invoice-state messages/sec. Two years post-launch, during the design phase of the Usage Billing onboarding effort, rejected a proposal to wire alerts directly to product-specific usage entities and pushed for a generic flexible billing-account entity instead — preventing a fragmented design that would have coupled every future partner-team integration to bespoke plumbing. Guided subsequent feature additions from three partner teams (Winback Promotions, Usage Billing, Mobile Billing) through H1 2025, eliminating the bus factor and enabling Ordering, Payments, and Mobile to develop on the system independently.
- **Impact:** **$2M+ in annualized revenue** recovered — measured via funnel tracking (click on alert → conversion within 2 hours). Venice lookup layer sustains **100,000 QPS reads** from the Feed surface; Flink pipeline processes **~500 messages/sec writes** for invoice-state updates. Three partner teams subsequently shipped features on the platform without my involvement.
- **Tech:** Java, Kafka, Flink, Venice, Airflow.
- **Status:** Delivered in production since Jan 2024; continuously extended through H1 2025.

### [LBP Global Alerts — Venice TTL Automation & Cache Invalidation]
- **Context:** LBP Global Alerts uses Venice as a high-scale lookup (100,000 QPS) to detect when a customer "potentially has an issue" with their invoices — a cheap hint that avoids hammering the downstream billing system. Without a perfect invalidation mechanism, stale hints lingered after customers reconciled their invoices. Each stale hint drove a redundant search-index lookup every time the customer viewed LinkedIn, putting avoidable pressure on Invoice Search API.
- **Role:** Individual Contributor.
- **Actions:** Implemented auto-purging of records older than 35 days from Global Alerts DB (Venice Cache). Contributed Venice TTL + Airflow operational fixes alongside.
- **Impact:** **Global Alerts DB (Venice Cache) size reduced 40%** through automated TTL — measured directly against database record count before/after the Airflow purge job ran. **50% reduction in downstream Invoice Search API QPS** — direct infrastructure-cost saving and improved resilience against cascading failure.
- **Tech:** Venice, Airflow.
- **Status:** Delivered in H1 2025.

### [gRPC Service Modernization — LBP]
- **Context:** Company-wide initiative to converge LBP services on gRPC — unlocking better wire and serialization performance, stronger contract safety, and a single unified RPC standard across the estate.
- **Role:** Individual Contributor; coordinated schema design across teams.
- **Actions:** Completed gRPC migration across four production services — Ordering Backend, Financial Reporting Service, Purchase Orchestrator, end-to-end testing service (10+ PRs). Provided gRPC schema-design guidance to partner teams to avoid naming collisions and ensure smooth rollout.
- **Impact:** Modernized the LBP service architecture across 4 production services; unblocked the migration pattern for adjacent teams.
- **Tech:** gRPC, Java, Protobuf.
- **Status:** Delivered in H1 2025.

### [LBP Availability Investigator (Kusto)]
- **Context:** Engineers and technical support teams were debugging customer issues by re-running the same ad-hoc Kusto queries against application and access logs — reusable queries were scattered, syntax had to be re-memorized per session, and the wrong log database was easy to hit. The opportunity was unlocked by LBP's microservice log tables all living in a single Kusto database, which made a unified dashboard possible.
- **Role:** Individual Contributor; designer and builder.
- **Actions:** Built the LBP Availability Investigator dashboard from scratch after recognizing engineers and support were running the same queries by hand. Unified the most-used triage query patterns across LBP's microservices into a single parameterized Grafana dashboard backed by Kusto, leveraging the fact that all LBP service log tables share one Kusto database. Designed the dashboard to correlate availability dips with their causal errors — finding all 4xx/5xx access-log entries and joining each call tree against the corresponding error-level application logs so the underlying failure is surfaced alongside the availability signal. Iterated on the query library and parameters as engineers and support surfaced new workflows.
- **Impact:** Adopted as a daily oncall tool by LBP engineers for live-site debugging — turned "availability dropped" into "here's the specific error chain that caused it" without manual log-trawling. The technical support team issued a formal commendation for the triage speedup — the dashboard accelerated routing of customer-reported bugs to the right LBP team.
- **Tech:** Kusto, Grafana.
- **Status:** Continuously delivered across H1 2025.

### [LBP Data Quality Jobs — Ordering & Global Alerts]
- **Context:** Two silent-failure incidents motivated the work: (1) **Global Alerts stopped sending** due to a server-code bug — no errors thrown, the pipeline simply produced zero data, so it went undetected until downstream impact surfaced. (2) During an infra-team migration of the order-line offline dataset from a legacy system to Iceberg, row counts on the old and new datasets were not verified — the team was migrated onto a dataset with **only 200M rows versus the original ~18B (≈99% data loss)**. The loss was discovered only after financial reporting flows broke. Both failures proved that error-based monitoring is insufficient for offline datasets; volume itself needs to be a first-class signal.
- **Role:** Individual Contributor.
- **Actions:** Built hourly Airflow + Trino data-quality jobs covering the Ordering and Global Alerts offline datasets. Each run takes a row count via Trino, emits it to a Kafka topic (persisted into an offline measurements table), and on the next run re-asserts the count and compares rate-of-change as a percentage against the prior snapshot. This enables two assertions per dataset: (1) row count stays above a minimum floor, and (2) percentage change between intervals stays within expected bounds — catching both catastrophic loss and anomalous spikes/drops regardless of whether errors are raised upstream.
- **Impact:** Converted two classes of silent failure (zero-data bugs and volume-loss migrations) into auto-detected alerts. Massively improved time-to-detect and reduced exposure time for internal customers of the Ordering and Global Alerts datasets.
- **Tech:** Airflow, Trino, Kafka, HDFS, OpenHouse.
- **Status:** Delivered in H1 2025.

### [Context Repos for Claude Code]
- **Context:** The company adopted agentic coding tools through FY25 and FY26 — Claude Code is the tool I use day-to-day; I was an early adopter and looked for ways to maximize productivity against a sea of literally thousands of internal repositories where a single feature often crosses 30+ microservices.
- **Role:** Individual Contributor.
- **Actions:** Independently designed the "Context Repos" pattern — a git repository that uses git submodules to aggregate the repos relevant to a project, domain, or organization, then augments them with hand-written context so a tool like Claude Code knows where to look and how the codebases interconnect.
- **Impact:** Immediately increased velocity for me and other engineers in my org. For LBP specifically, Context Repos made the ~30+ microservices decomposed from the legacy OMS navigable — developers can launch agents that search across projects, write cross-codebase PRs, and review designs against real implementations. Reduces toil and boosts velocity across the daily loop.
- **Tech:** Claude Code, Git submodules, Markdown context files (Skills, Hooks, Agents).
- **Status:** Piloted May 2025 via org-wide engineering email; a variant was adopted by LinkedIn's Developer Productivity org by Feb 2026.

## 4. Reliability & Multiplier Work

Pre-prod reliability engineering and team-multiplier contributions that underpin the role but don't rise to standalone projects. The reliability work is about catching failure modes *before* they become incidents; the multiplier work is about removing single points of failure on the team and making adjacent engineers faster.

- **Pre-prod reliability — shift-left testing & concurrency safety:**
  - **End-to-end test coverage for usage-based products** — authored E2E tests covering **Flagship Online Job** (standalone usage-based product) and **Recruiter Lite Online Jobs** (usage-based, bundled with the Recruiter subscription) purchase and usage flows. Wired them into the pre-deploy pipeline so every change is smoke-tested against the full checkout/ordering path before promotion, catching integration regressions and pre-empting incident classes they would otherwise cause.
  - **Agentic checkout testing** — built two Claude Code integrations that let agents self-validate checkout changes before PRs reach the E2E suite: (1) a **Playwright-driven UI path** that spins up new test users, drives the browser through the checkout page, enters payment details, and places orders; (2) a **shell-script API path** that mimics the exact API calls the UI makes, so agents can exercise every checkout API without a browser. Coverage spans **all subscription flows** (e.g., LinkedIn Premium) and **all usage-based flows** (e.g., Ads, Jobs) — shifting correctness left and materially raising PR quality by giving agents a fast, automated correctness loop.
  - **Unified optimistic locking for the MySQL Ordering Backend** — designed and shipped a single optimistic-locking mechanism applied to every update-based write path, giving the backend uniform concurrency control and retryability. Critical because writes run inside Temporal workflows whose activity-level retries can re-fire in-flight updates against the same row; the version-based check surfaces conflicts cleanly so Temporal retries converge instead of silently clobbering each other — eliminating a class of conflicting-write pitfalls and making the Ordering Backend materially more reliable.

- **Team leverage & mentorship:**
  - **Eliminated the Global Alerts bus factor** — mentored engineers across 3 teams (Ordering, Payments, Mobile) to independently develop and support features; guided additions of Winback Promotions, Usage Billing, and Mobile Billing alerts without my involvement.
  - **Mentored 2 engineers** — design reviews, pairing, feature guidance (including the billing account → domain-specific-entity redirect before implementation).
  - **Claude Code evangelism** — delivered 5 knowledge-sharing sessions on agentic development (primary tool: Claude Code) reaching 1,000+ engineers (company-wide ICCDW, org- and team-level, plus a Cursor session). Volunteered at the Copilot Agent workshop to help engineers onboard new tooling.
  - **Documentation culture** — 10+ durable docs artifacts (GitHub Pages, READMEs, wikis) across multiproducts, reducing tribal-knowledge dependency.

## Bullet Points

- Designed and built a real-time alerting system — **100,000 QPS reads** (Venice) + **~500 msg/sec writes** (Kafka/Flink) against LinkedIn Feed — recovering **$2M+ annually** in involuntary churn (funnel-tracked: click on alert → conversion within 2 hours) by notifying subscribers of failed payments before cancellations.
- Led the Oracle → MySQL migration of LinkedIn's Ordering Backend — rewrote **30,000+ lines across ~75 PRs** using JooQ and Flyway, launched at 1% with **10,000+ validated orders** and zero data loss, enabling the org's Oracle retirement.
- Eliminated N+1 query patterns in Order Processing, reducing average latency **40% (50 ms → 30 ms)** and **p95 37% (200 ms → 125 ms)** across all ordering workflow read paths on a **12 TB / 20-billion-row dataset**.
- Built a reusable Oracle → MySQL **Delegation Framework** adopted by **10 LBP domain teams**, eliminating per-team reinvention of consistency and rollback infrastructure and directly unblocking the org's Oracle retirement.
- Engineered the framework's cutover protocol: A/B-framework-driven cohort migration + Couchbase entity routing with 5-minute TTL pinning (strong read-after-write consistency) + shadow reads, PIN support, and rollback hooks.
- Automated Venice TTL purging of >35-day data, reducing Global Alerts DB (Venice Cache) size by **40%** and cutting downstream Invoice Search API QPS by **50%**.
- Shipped a distributed deletion pipeline (Spark + Kafka + batch) during oncall urgency, safely removing **300,000 corrupted order records** from production.
- Reused that pipeline to scope a **33% data-reduction opportunity (12 TB → 9 TB)** against billions of dormant legacy OMS rows in the Order database — execution in-flight.
- Completed gRPC migration across 4 production services (Ordering Backend, Financial Reporting Service, Purchase Orchestrator, end-to-end testing service) in 10+ PRs — unlocking better wire/serialization performance, contract safety, and a unified RPC standard across LBP.
- Pioneered **"Context Repos" for Claude Code** — piloted May 2025 via org-wide engineering email; a variant was adopted by LinkedIn's Developer Productivity org by Feb 2026; makes 30+ LBP microservices navigable to agentic tooling.
- Delivered **5 agentic-development knowledge-sharing sessions** on Claude Code reaching **1,000+ engineers** (company-wide ICCDW, org, team, plus a Cursor session), becoming the informal go-to expert on Claude Code workflows at LinkedIn.
- Removed the Global Alerts bus factor by designing for independent extensibility and guiding engineers across **3 teams** (Ordering, Payments, Mobile) to ship Winback Promotions, Usage Billing, and Mobile Billing features without my involvement.
