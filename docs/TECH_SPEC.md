# Technical Specification – glm‑forge

---

## 1. Overview

**glm‑forge** is a production‑ready, scalable large‑language‑model (LLM) platform inspired by GLM‑5. It is designed for machine‑learning developers and researchers who need a high‑performance, low‑latency inference engine that can be deployed on commodity GPU clusters or on‑prem hardware. The system is built on top of the proven **vLLM** inference engine, with custom extensions for model parallelism, efficient tokenization, and a lightweight API surface.

The project is hosted in the `arkashira/glm-forge` repository and follows the Axentx runbook for CI/CD, observability, and data‑driven improvement loops.

---

## 2. Architecture

```
┌───────────────────────┐
│  Client / SDK          │
│  (REST / gRPC)         │
└────────────┬──────────┘
             │
             ▼
┌───────────────────────┐
│  API Gateway / Load    │
│  Balancer (Envoy)      │
└────────────┬──────────┘
             │
             ▼
┌───────────────────────┐
│  Inference Service     │
│  (vLLM + Custom Layer) │
└───────┬───────┬───────┘
        │       │
        ▼       ▼
┌───────┐ ┌───────┐
│  GPU  │ │  GPU  │   …  (Model Parallelism)
│  Node │ │  Node │
└───────┘ └───────┘
        ▲
        │
        ▼
┌───────────────────────┐
│  Model Store (S3/FS)  │
└───────────────────────┘
        ▲
        │
        ▼
┌───────────────────────┐
│  Training / Fine‑tune  │
│  Pipeline (Optional)   │
└───────────────────────┘
```

### 2.1 Key Components

| Component | Responsibility | Implementation |
|-----------|----------------|----------------|
| **Client SDK** | High‑level API for Python/Node/Go | `sdk/` (Python, Node, Go wrappers) |
| **API Gateway** | Request routing, auth, rate‑limit | Envoy + Istio |
| **Inference Service** | Orchestrates vLLM, tokenization, post‑processing | `service/` (FastAPI + vLLM) |
| **Model Store** | Persistent storage of checkpoints & configs | S3-compatible object store |
| **Monitoring** | Prometheus metrics, OpenTelemetry traces | `monitoring/` |
| **Deployment** | Helm charts, Kustomize manifests | `deploy/` |
| **CI/CD** | Tests, lint, image build, release | GitHub Actions (see `.github/`) |

---

## 3. Data Model

| Entity | Fields | Notes |
|--------|--------|-------|
| **Model** | `id`, `name`, `version`, `architecture`, `tokenizer_path`, `config_path`, `storage_uri` | Stored in DynamoDB (or PostgreSQL) |
| **InferenceRequest** | `model_id`, `prompt`, `max_tokens`, `temperature`, `top_p`, `stop_sequences`, `metadata` | JSON payload |
| **InferenceResponse** | `generated_text`, `usage`, `metadata` | JSON payload |
| **Metrics** | `request_id`, `latency_ms`, `tokens_generated`, `status` | Exported to Prometheus |

---

## 4. Key APIs / Interfaces

### 4.1 REST API (FastAPI)

| Endpoint | Method | Request | Response | Notes |
|----------|--------|---------|----------|-------|
| `/v1/models` | GET | None | List of available models | |
| `/v1/models/{model_id}/generate` | POST | `InferenceRequest` | `InferenceResponse` | Streaming via Server‑Sent Events (SSE) |
| `/v1/models/{model_id}/status` | GET | None | Model status (loading, ready, error) | |

### 4.2 gRPC API

- Service: `InferenceService`
- Methods: `Generate`, `ListModels`, `GetStatus`

### 4.3 SDK

- `glm_forge.client` (Python) – thin wrapper around REST/gRPC
- `glm_forge.node` (Node) – async client
- `glm_forge.go` (Go) – context‑aware client

---

## 5. Tech Stack

| Layer | Technology | Reason |
|-------|------------|--------|
| **Model Engine** | **vLLM** (v1.0.0) | Proven, GPU‑efficient inference |
| **Tokenizer** | SentencePiece | GLM‑5 compatible |
| **Web Framework** | FastAPI | Async, OpenAPI spec |
| **Container Runtime** | Docker + Kubernetes | Scalability, self‑healing |
| **Orchestration** | Helm + Kustomize | Declarative deployments |
| **Observability** | Prometheus + Grafana, OpenTelemetry | Metrics, traces |
| **CI/CD** | GitHub Actions | Automated tests, image build |
| **Storage** | S3 (MinIO) | Model checkpoints |
| **Database** | PostgreSQL (managed) | Metadata, model registry |
| **Auth** | JWT + OAuth2 | Secure access |

---

## 6. Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `vllm` | `>=0.3.0` | Inference engine |
| `sentencepiece` | `>=0.1.99` | Tokenizer |
| `fastapi` | `>=0.109.0` | Web API |
| `uvicorn` | `>=0.27.0` | ASGI server |
| `grpcio` | `>=1.62.0` | gRPC runtime |
| `protobuf` | `>=4.25.0` | Message serialization |
| `psycopg2-binary` | `>=2.9.9` | PostgreSQL driver |
| `boto3` | `>=1.34.0` | S3 client |
| `opentelemetry-sdk` | `>=1.24.0` | Tracing |
| `prometheus-client` | `>=0.20.0` | Metrics |
| `python-dotenv` | `>=1.0.0` | Env var loading |
| `pytest` | `>=8.0.0` | Unit tests |
| `black` | `>=24.0.0` | Code formatting |

All dependencies are pinned in `requirements.txt` and `pyproject.toml`. The Dockerfile uses a multi‑stage build to keep the final image under 1 GB.

---

## 7. Deployment

### 7.1 Helm Chart

- `deploy/helm/glm-forge/`
- Values:
  - `replicaCount`
  - `resources.limits.cpu/memory`
  - `resources.requests.cpu/memory`
  - `modelStore.s3Endpoint`
  - `modelStore.bucket`
  - `auth.jwtSecret`
  - `metrics.enabled`

### 7.2 Kustomize

- `deploy/kustomize/` for environment‑specific overlays (dev, prod).

### 7.3 CI/CD Pipeline

1. **Lint** – `flake8`, `black`, `pre-commit`.
2. **Unit Tests** – `pytest`.
3. **Build Docker** – `docker buildx`.
4. **Push** – to GitHub Container Registry.
5. **Helm Lint** – `helm lint`.
6. **Deploy** – `helm upgrade --install` via ArgoCD.

### 7.4 Scaling Strategy

- **Horizontal Pod Autoscaler** on CPU/Memory usage.
- **GPU Autoscaler** via Kube‑GPU‑Operator.
- **Model Caching** – LRU cache in vLLM for popular checkpoints.

---

## 8. Security & Compliance

- **JWT** for API authentication; scopes: `read`, `write`.
- **TLS** termination at Envoy.
- **Secrets** stored in Vault; mounted as env vars.
- **Audit Logging** – all requests logged to CloudWatch (or Loki).

---

## 9. Observability

| Metric | Description |
|--------|-------------|
| `glm_inference_latency_ms` | Latency per request |
| `glm_tokens_generated_total` | Tokens produced |
| `glm_inference_errors_total` | Error count |
| `glm_gpu_utilization` | GPU usage per node |
| `glm_memory_usage` | Memory consumption |

All metrics are exposed on `/metrics` endpoint. Traces are exported to Jaeger.

---

## 10. Roadmap (Next 3 Months)

1. **Model Parallelism** – Implement 8‑way tensor‑parallel loading.
2. **Fine‑tuning API** – Expose training pipeline via REST.
3. **Auto‑Scaling GPU** – Integrate with Kube‑GPU‑Operator.
4. **Multi‑Tenant Support** – Namespace‑based isolation.

---

## 11. Appendix

### 11.1 Directory Structure

```
glm-forge/
├── api/
│   ├── fastapi/
│   └── grpc/
├── sdk/
│   ├── python/
│   ├── node/
│   └── go/
├── service/
│   ├── inference.py
│   └── tokenizer.py
├── deploy/
│   ├── helm/
│   └── kustomize/
├── tests/
│   ├── unit/
│   └── integration/
├── Dockerfile
├── requirements.txt
├── pyproject.toml
└── README.md
```

### 11.2 Contact

- **Lead Engineer**: Jane Doe (`jane.doe@axentx.com`)
- **Slack**: `#glm-forge`

---
