# Software Engineer — LinkedIn (San Francisco, CA)
**Feb 2022 – Mar 2024**

## 1. Scope & Context

Two sub-periods across this role — started on LinkedIn Learning's Learner Growth pillar, transitioned to LinkedIn Business Platform (LBP) toward the end.

### Sub-period A: LinkedIn Learning — Learner Growth (LLS) *(Feb 2022 – ~mid/late 2023)*

- **Org:** LinkedIn Learning Solutions (LLS)
- **Team:** Learner Growth
- **Systems owned:** Learning Alerts platform, VYMBII Slideshows (feed-mixer integration), Urn Resolver, Feed Backend, Ads Ranking Backend, Learning GraphQL Frontend
- **Scale:** 50M+ DAU surface (Flagship Feed), 22M members ramped on Learning Alerts V2, 3,000 QPS on VYMBII Slideshows recommendation service, 50+ TB/week Spark pipelines over 20+ datasets
- **Primary tech stack:** Java, Spark, Airflow, Kafka, Samza (distributed stream processing; samza.apache.org), HDFS, Pegasus + Rest.li APIs, LiX (LinkedIn's A/B experimentation & feature-flag framework), HDFS, Trino, 

### Sub-period B: LinkedIn Business Platform (LBP) — Checkout and Ordering *(~mid/late 2023 – Mar 2024)*

Joined LBP's Checkout and Ordering team after the LLS Learner Growth reorg; this sub-period sets up the Global Alerts, Token Unification, and LBP tooling work that continues into the Senior Software Engineer role.

- **Org:** LinkedIn Business Platform (LBP — modern LinkedIn commerce platform, successor to the legacy OMS / Order Management System)
- **Team:** Checkout and Ordering
- **Systems owned:** Global Alerts (new LBP system replacing legacy OMS alerts), Token Creation flows, LBP Internal Tooling, New LBP Purchase Tool
- **Scale:** Payment failure alerting system spec'd for 100,000 QPS from LinkedIn Feed (design/build period; launched Jan 2024 as pre-promotion deliverable)
- **Primary tech stack:** Java, Temporal, Oracle, Kafka, Samza (distributed stream processing), Venice (distributed KV cache; venicedb.org), Airflow, LiX (A/B experimentation & feature-flag framework), RFC/tracking-spec workflow

## 3. Projects & Initiatives

### [VYMBII Slideshows — Learner Growth]
- **Context:** Learning Solutions needed a way to surface course video content inside LinkedIn's Flagship Feed to drive learner engagement at scale. The feature started as CYMBII (a single recommended-course video in-feed) and evolved into VYMBII Slideshows, presenting all videos in a recommended nano-course as a swipeable slideshow.
- **Role:** Primary infra contributor across the end-to-end feature.
- **Actions:** Drove the discovery research that evolved the feature from single-video CYMBII into nano-course VYMBII Slideshows. Built the Urn Resolver infrastructure that resolves videos from courses for slideshow display (and later migrated it off deprecated Lynda course URNs to native Linkedin Learning Course URNs). Built the feed-mixer integration that stitched the slideshow content into LinkedIn's Flagship Feed. Migrated consumers to a batch finder pattern, reducing QPS to Learning Backend. Scaled the feature from nano courses to the full VYMBII catalog across 3 successive experiments.
- **Impact:** **+2.5% WSL** (LinkedIn Learning's north-star Weekly Skilled Learners metric) across 3 experiments and **+0.57% SWI** for Skill Credits. Delivered cross-pillar QPS reduction to Learning Backend via the batch finder migration. Reached LinkedIn's 50M+ DAU feed surface.
- **Tech:** Java, feed-mixer, Pegasus, LiX experimentation, Learning Backend.
- **Status:** Shipped.
- **Relevance:** 4/5 — +2.5% WSL across 3 experiments + 0.57% SWI + 3K QPS shipped to LinkedIn's 50M+ DAU Flagship Feed; moved Learning's north-star metric.

### [Learning Alerts V2 — Member Targeting Framework]
- **Context:** Learning Alerts needed a targeting layer that could segment members by their position in the career-change funnel and deliver a relevant notification. Cohorts were behavioral — members who clicked Save on a job, members who applied for a job, members who recently changed their title, members marked Open to Work. Members landing in multiple cohorts were routed to the one furthest along the funnel of changing jobs, so each member received the single most relevant nudge. Segmentation ran in Spark at massive scale. No offline-targeting precedent existed on Learner Growth.
- **Role:** Designed and built the targeting framework from scratch with zero prior offline-development experience on the team.
- **Actions:** Designed the member/stage targeting system and the Spark pipelines behind it (20+ datasets, ~50 TB of historical data processed per run, classifying 10M+ job seekers). Launched Professional Certificates email, the Phase 3 job-applicant cohort, and the non-subscriber cohort extension. Delivered the Interview Guidance feature in coordination with the Jobs team (7 PRs). Built impression discounting — an HDFS-backed history table that tracked recommendations already served per user so the same nudge wasn't delivered twice across runs. Took over the LAv2 ramp to 22M members, fixed critical bugs mid-ramp, and owned the experiment design. Proactively validated capacity for Learning GraphQL Frontend with SRE before launch.
- **Impact:** **+1.09% WSL** from the targeting framework overall, **+0.1% WSL** from Professional Certificates emails, targeted delivery across **22M members**. 5% higher enrollment rates on Spark-pipeline-classified cohorts.
- **Tech:** Java, Spark, Kafka, LiX, Learning GraphQL Frontend.
- **Status:** Shipped.
- **Relevance:** 4/5 — +1.09% WSL + 22M members ramped + built-from-scratch targeting framework on 50 TB/week Spark across 20+ datasets classifying 10M+ job seekers.

### [Audio-Only Content Filter — Flagship Feed]
- **Context:** VYMBII Slideshows was surfacing audio-only course content inside LinkedIn's Flagship Feed, where it performed poorly relative to visual content. Quality was a drag on feed engagement at scale.
- **Role:** Investigator + owner of the short-term experiment and the long-term RFC.
- **Actions:** Scoped and ran the short-term filter experiment to remove audio-only content from VYMBII output in the Flagship Feed, then authored the long-term RFC for the durable fix.
- **Impact:** **+0.2% feed engagement lift** — statistically significant at the scale of hundreds of millions of daily feed impressions. Most feed experiments at this scale target 0.1–0.5% lifts; this was a strong win.
- **Tech:** Java, feed-mixer, LiX.
- **Status:** Shipped.
- **Relevance:** 3/5 — +0.2% Flagship Feed engagement lift at hundreds-of-millions-of-impressions scale; single-experiment scope but statistically significant on a tier-1 surface.

### [JVM / GC Tuning — Core Java Services]
- **Context:** Feed Backend (a mobile/web API pillar serving LinkedIn's clients) and Ads Ranking Backend were flagged by the JVM Performance working group with poor GC Health Scores — regular GC pauses were degrading user-facing latency.
- **Role:** Individual contributor; primary driver of both services' GC recovery. Migrated configuration to G1GC as part of the work.
- **Actions:** Profiled heap behavior, tuned G1GC parameters, and iterated on production settings. Wrote the JVM Tuning runbook capturing the methodology and shared it with the JVM Performance working group.
- **Impact:** Feed Backend **GC Health Score 78% → 99%**. Ads Ranking Backend **GC Health Score 5% → 99%**. Runbook adopted by the JVM Performance working group and reused across the org.
- **Tech:** Java, JVM, G1GC, LinkedIn JVM performance tooling.
- **Status:** Shipped.
- **Relevance:** 2/5 — 78%→99% and 5%→99% GC Health Scores on two core services + runbook adopted by the JVM Performance working group; internal-infra impact without a top-line metric.

### [Token Creation Unification — LBP]
- **Context:** The legacy token system was built on OMS but was still serving LBP's checkout flow — a cross-platform dependency that tied LBP's correctness and oncall to a system LBP did not own. LBP had multiple divergent paths for token creation across products. An FY24 unification effort was launched to migrate checkout onto a fully LBP-native token flow and converge products on a single canonical path.
- **Role:** Led implementation with 2 other engineers (did not author the RFC).
- **Actions:** Executed the migration against the existing RFC across 13+ PRs. Developed comms, the release plan, and coordinated a bug bash.
- **Impact:** Checkout became fully LBP-native — removed the residual OMS dependency from the purchase flow and converged LBP products on a single canonical token-creation path. Rolled out behind a LiX.
- **Tech:** Java, LiX, LBP platform.
- **Status:** Shipped.
- **Relevance:** 2/5 — Led implementation with 2 ICs across 13+ PRs + removed cross-platform OMS dependency; inherited the RFC and narrower in scope than the later LBP migration framework.

### [LBP Internal Tooling — Card Override & Alternative Payment Methods]
- **Context:** Engineers and technical support teams needed ways to test purchase flows across alternative payment methods without depending on real customer data. The existing LBP Internal Tooling didn't cover card override or alternative payment methods.
- **Role:** Individual Contributor.
- **Actions:** Added credit card override functionality to the New LBP Purchase Tool (5+ PRs). Enhanced LBP Internal Tooling with an extensible API model so future alternative payment methods could be plugged in without re-plumbing the tool.
- **Impact:** Ease-of-testing for LBP engineers and TS; unlocked reliable purchase-flow debugging against a broader range of payment methods.
- **Tech:** Java, LBP platform.
- **Status:** Shipped.
- **Relevance:** 2/5 — Shipped card-override and extensible payment-method support across 5+ PRs; impact is internal-tooling convenience, hard to quantify compellingly.

### [Jobs in Learning (Jobs on LiL)]
- **Context:** Cross-team initiative to surface LinkedIn Jobs inside LinkedIn Learning — required backend integration across the Jobs and Learning stacks.
- **Role:** Backend contributor representing Learner Growth.
- **Actions:** Contributed PRD feedback, co-authored the RFC and tracking spec, wrote the runbook, and shipped 8 PRs across the integration. Migrated JDP (Job Details Page) Learning Recommendations onto Jobs Feed Backend as part of the Right Rail GraphQL migration (3 PRs). Represented Learner Growth in the learning GraphQL migration
- **Impact:** Launched Jobs-on-LiL backend integration; extended Learning Right Rail recommendations onto the Jobs page
- **Tech:** Java, GraphQL, Jobs Feed Backend, Pegasus.
- **Status:** Shipped.
- **Relevance:** 2/5 — 8 PRs + PRD + RFC + runbook for the Jobs-on-LiL backend integration; cross-team delivery but impact reads as "launched integration" — interview material more than resume material.

## 4. Performance, Reliability & Cost

On-call, incident response, cross-team operational contributions that don't rise to project level but form the operational backbone of the role.

- **Incidents led / resolved:**
  - Identified root cause on a production incident and led the postmortem.
  - **Affiliate offline reporting fix** — resolved a 6-month-old broken flow across 10 PRs, unblocking marketing's ability to pay third-party affiliate program members.
  - **Sample-ratio-mismatch fix during LAv2 Phase 2** — corrected a statistical SRM issue mid-experiment ramp.

- **Reliability, monitoring & oncall:**
  - Proactively validated Learning GraphQL Frontend capacity with SRE before the LAv2 ramp; earned "Honorary SRE" acknowledgment.
  - **Monitoring & Alerting Champion (Learner Growth)** — created alerting runbooks and dashboards for critical services.
  - Mentored peers through oncall rotations on availability dips, metric dashboards, deployments, and tuning.

