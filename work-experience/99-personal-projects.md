# Personal Projects

### [Anton (Kubernetes Homelab)]
- **Context:** Self-hosted, production-style Kubernetes cluster ("data center in the basement") built from bare-metal mini PCs to run personal services, host public-facing apps, and serve as a testbed for distributed-systems experimentation. Repo: https://github.com/wcygan/anton; write-up: https://wcygan.net/anton.
- **Role:** Individual Contributor
- **Actions:**
  - Provisioned a 3-node HA control-plane cluster on MS-01 mini PCs (Intel N100, 16 GB RAM each; 6× 1 TB NVMe) using Talos Linux for immutable, API-driven, SSH-less nodes.
  - Implemented full GitOps with Flux CD against a GitHub repo, SOPS-encrypted secrets, and Renovate-driven dependency PRs so every cluster change is a reviewed commit.
  - Exposed public workloads via Cloudflare Tunnel (zero open inbound ports) and private workloads over Tailscale VPN across a second domain.
- **Impact:**
  - I had fun while doing it.
  - Replaced several paid SaaS subscriptions with self-hosted equivalents while keeping a public, HTTPS-terminated footprint reachable worldwide.
  - Gave hands-on, end-to-end exposure to what it means to run a kubernetes cluster / data center.
- **Tech:** Talos Linux, Kubernetes, Cilium, Flux CD, SOPS, Envoy Gateway, cert-manager, external-dns, Cloudflare Tunnel, Tailscale, Harbor, Prometheus.
- **Status:** Active — cluster is live and continuously updated

### [Betty (Personal)]

- **Context:** TBD
- **Role:** Individual Contributor
- **Actions:** TBD
- **Impact:** TBD
- **Tech:** TBD
- **Status:** TBD

### [Dotfiles (Claude Code Skills)]

- **Context:** TBD
- **Role:** Individual Contributor
- **Actions:** TBD
- **Impact:** TBD
- **Tech:** TBD
- **Status:** TBD

