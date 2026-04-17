# Acronyms & Internal Terms — Reference

Glossary for internal LinkedIn tech and proprietary platforms referenced in `01-linkedin-swe.md` and `02-linkedin-sr-swe.md`. Inline expansions in the writeups are first-mention only; this file is the authoritative reference.

## Platforms

- **LBP** — LinkedIn Business Platform. The modern LinkedIn commerce platform (post-2022 era).
- **OMS** — Order Management System. The legacy LinkedIn commerce platform that LBP is replacing.
- **LLS** — LinkedIn Learning Solutions (the Learning org).
- **LiL** — LinkedIn Learning (the consumer product).
- **LiX** — LinkedIn's A/B experimentation and feature-flag framework.

## Open-source / published tech

- **Venice** — distributed key-value store / feature store. https://venicedb.org/ (open-sourced by LinkedIn).
- **Brooklin** — change-data-capture (CDC) pipeline with bootstrap. https://github.com/linkedin/brooklin (open-sourced by LinkedIn).
- **Samza** — Apache distributed stream-processing framework (originally built at LinkedIn). https://samza.apache.org/. *Note: LinkedIn migrated much of its stream processing from Samza to Apache Flink (https://flink.apache.org/) during the FY24–FY26 window.*
- **JooQ** — Java API for type-safe SQL. https://www.jooq.org/.
- **Flyway** — database-migration framework. https://github.com/flyway/flyway.
- **GoldenGate** — Oracle's log-based replication product (used for Oracle → MySQL sync during the migration).

## Product / experiment metrics

- **WSL** — Weekly Skilled Learners. LinkedIn Learning's north-star metric.
- **SWI** — Site Wide Impact. A LinkedIn A/B-testing metric describing how meaningful / realistic an experiment's measured change is across the site as a whole.
- **VYMBII** — "Videos You Might Be Interested In" (Slideshows feature in Flagship Feed).
- **CYMBII** — "Courses You Might Be Interested In" (the single-video version of VYMBII).
- **SSRM** — Sample Size Ratio Mismatch (experimentation statistical diagnostic, unbalanced groups).

## Internal infra / operations

- **ICCDW** — company-wide LinkedIn engineering event (Internal Community / Cross-Discipline Week).
- **SRE** — Site Reliability Engineering (generic industry term; used within LinkedIn teams).
- **SLO** — Service Level Objective (generic industry term).
