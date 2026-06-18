# REQUIREMENTS.md

## Project Overview
**glm-forge** is an Axentx product that delivers a scalable, efficient large‑language‑model (LLM) comparable to GLM‑5, specifically tuned for machine‑learning developers and researchers. The model will be deployed as a service behind a REST/GRPC API, with optional on‑premise Docker images for privacy‑sensitive workloads. The implementation will leverage the **vLLM** inference engine for high throughput and low latency, and will be built on top of the existing Axentx knowledge base and dataset infrastructure.

---

## Functional Requirements

| ID | Description | Acceptance Criteria |
|----|-------------|---------------------|
| **FR‑1** | **Model Training** | • Train a transformer model with > 10B parameters using the Axentx `auto`, `messages`, `instr‑resp`, and `query‑resp` datasets.<br>• Achieve perplexity ≤ 18 on a held‑out validation split.<br>• Store checkpoints in the shared BRAIN (pgvector) for future fine‑tuning. |
| **FR‑2** | **Inference API** | • Expose a REST endpoint `/v1/chat/completions` and a GRPC service `ChatService`.<br>• Accept JSON payloads with `model`, `messages`, `max_tokens`, `temperature`, `top_p`.<br>• Return streaming responses with token‑level events. |
| **FR‑3** | **Batching & Parallelism** | • Support concurrent requests up to 256 QPS with an average latency < 200 ms for 1‑token requests.<br>• Dynamically batch requests to maximize GPU utilization. |
| **FR‑4** | **Model Serving** | • Use **vLLM** as the inference engine.<br>• Provide a Docker image (`axentx/glm-forge:latest`) that pulls the model weights from S3 and starts the server automatically. |
| **FR‑5** | **Fine‑tuning API** | • Allow users to submit a small dataset (≤ 10 k examples) and trigger a fine‑tune job.<br>• Return a new model ID and a download URL for the checkpoint. |
| **FR‑6** | **Monitoring & Logging** | • Emit Prometheus metrics (`request_latency_seconds`, `request_throughput`, `gpu_utilization`).<br>• Log request/response pairs to a secure audit trail. |
| **FR‑7** | **Security & Access Control** | • Require API key authentication for all endpoints.<br>• Enforce rate limiting (default 1000 requests/min per key). |
| **FR‑8** | **Documentation** | • Generate OpenAPI spec and Swagger UI.<br>• Provide a quick‑start guide in Markdown and a Docker Compose example. |
| **FR‑9** | **Compliance** | • Ensure all data handling complies with GDPR and CCPA for user‑generated content. |
| **FR‑10** | **Extensibility** | • Design the codebase to allow swapping the inference engine (e.g., SGLang) with minimal changes. |

---

## Non‑Functional Requirements

| ID | Category | Requirement | Metrics |
|----|----------|-------------|---------|
| **NFR‑1** | **Performance** | The system must sustain ≥ 200 QPS with < 200 ms average latency for 1‑token requests and < 800 ms for 512‑token requests. | QPS, latency |
| **NFR‑2** | **Scalability** | Horizontal scaling should be achieved via Kubernetes deployments; the service must support up to 32 GPU nodes without code changes. | Node count, throughput |
| **NFR‑3** | **Reliability** | 99.9 % uptime SLA; automatic failover to standby nodes. | MTTR < 5 min |
| **NFR‑4** | **Security** | All traffic encrypted with TLS 1.3; secrets stored in HashiCorp Vault. | Encryption standard |
| **NFR‑5** | **Data Privacy** | No user data is stored beyond the audit trail; all logs are encrypted at rest. | Compliance |
| **NFR‑6** | **Maintainability** | Code coverage ≥ 90 % for core modules; CI pipeline runs tests on every PR. | Coverage |
| **NFR‑7** | **Observability** | Prometheus metrics, Grafana dashboards, and alerting rules for latency spikes and GPU memory usage. | Alert thresholds |
| **NFR‑8** | **Compliance** | All third‑party libraries must be open‑source with permissive licenses (MIT, Apache‑2.0). | License audit |

---

## Constraints

1. **Hardware** – Must run on NVIDIA A100 GPUs; no reliance on proprietary hardware.
2. **Licensing** – All model weights and code must be released under a permissive license (MIT or Apache‑2.0).
3. **Data** – Only use datasets listed in the company context; no external data sources.
4. **Deployment** – The Docker image must be ≤ 5 GB to fit within the existing container registry limits.
5. **Time** – MVP delivery within 12 weeks from project kickoff.

---

## Assumptions

1. The shared BRAIN (pgvector) will provide sufficient storage for model checkpoints and metadata.
2. The vLLM inference engine will support the required batching and streaming features.
3. Users will have access to an API key management system already in place.
4. The Kubernetes cluster will have GPU nodes pre‑configured with NVIDIA drivers and CUDA 12.x.

---

## Deliverables

1. Trained GLM‑5‑like model weights and tokenizer files.  
2. Docker image (`axentx/glm-forge:latest`).  
3. REST/GRPC API implementation with OpenAPI spec.  
4. Fine‑tune job orchestration module.  
5. Prometheus metrics and Grafana dashboards.  
6. Comprehensive documentation (README, API guide, deployment instructions).  
7. CI/CD pipeline configuration (GitHub Actions).  

---

## Acceptance Checklist

- [ ] Model meets perplexity and latency targets.  
- [ ] API passes all functional tests and rate‑limit enforcement.  
- [ ] Docker image builds successfully and starts the server.  
- [ ] Prometheus metrics are exposed and Grafana dashboards render.  
- [ ] Security audit confirms TLS, key auth, and data encryption.  
- [ ] Documentation is complete and passes style checks.  
- [ ] CI pipeline passes all tests with ≥ 90 % coverage.  

---
