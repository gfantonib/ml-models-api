# ML Models API - Pipeline Architecture Plan

## Vision

A microservices pipeline for running ML models, with event-driven communication, persistent storage, and full observability.

---

## Services

### 1. Gateway (REST API) — Go

First point of contact. Receives user input, persists it, and triggers a pipeline run.

- Receives user requests via REST
- Validates input against model protos
- Saves user input to Postgres via **Writer** service (gRPC)
- Writer inserts an outbox row → Debezium publishes the run trigger to Kafka

### 2. Proxy (Kafka Consumer) — Go

Consumes triggers from Gateway. Manages resource allocation and routing.

- Consumes trigger messages from Kafka
- Checks available resources
- Redirects/routes the trigger to the appropriate Model service

### 3. Models (Workers) — Python

The actual ML execution units. Python for access to ML libraries (numpy, scipy, scikit-learn, etc.).

- Consumes trigger from Proxy
- Loads input data from Postgres via **Reader** service (gRPC)
- Runs the model
- Saves output to Postgres via **Writer** service (gRPC)

### 4. Reader (gRPC Service) — Go

Read-only data access layer for Postgres.

### 5. Writer (gRPC Service) — Go

Write-only data access layer for Postgres.

---

## Infrastructure

### Postgres + Outbox Pattern

Two outbox-driven events, both via Debezium CDC:

1. **Run trigger** — When Gateway writes model input via Writer, an outbox row is inserted. Debezium captures it and publishes the run trigger to Kafka. Gateway never produces to Kafka directly.
2. **Run completion** — When a Model writes its output via Writer, another outbox row is inserted. Debezium captures it and publishes a run-completed event to Kafka.

### Kafka

- Topic: run triggers (Gateway -> Proxy -> Models)
- Topic: run completion events (Debezium -> consumers)

### Containers

All services run in containers, orchestrated via Docker Compose.

---

## Data Flow

```
User Request
    |
    v
[Gateway] --gRPC--> [Writer] ---> Postgres (input + outbox)
                                    |
                                    | Outbox table
                                    v
                                [Debezium] ---> Kafka (run trigger)
                                                    |
                                                    v
                                                                                                [Proxy]
                                                    |
                                                    | Kafka (routed trigger)
                                                    v
[Models] --gRPC--> [Reader] ---> Postgres (input)
    |
    | (run model)
    v
[Models] --gRPC--> [Writer] ---> Postgres (output)
                                    |
                                    | Outbox table
                                    v
                                [Debezium] ---> Kafka (run completed event)
```

---

## Observer (Dev Tool - Not Part of the System)

A standalone service for development/debugging only.

- Triggers pipeline runs manually
- Watches Postgres tables (inputs, outputs, outbox)
- Watches Kafka events (triggers, completions)
- Provides visibility into the full pipeline lifecycle

---

## Implementation Order

1. **Postgres schema** - Define tables for inputs, outputs, outbox
2. **Writer** (gRPC) - Write service over Postgres
3. **Reader** (gRPC) - Read service over Postgres
4. **Gateway** (REST) - Receive requests, call Writer, publish to Kafka
5. **Proxy** (Kafka consumer) - Consume triggers, check resources, route
6. **Models** (Python workers) - Consume routed triggers, load data, run model, save output
7. **Debezium + Outbox** - CDC setup for run-completion events
8. **Observer** (dev tool) - Trigger runs, watch DBs and events
9. **Docker Compose** - Wire all services together

---

## Contracts

### Gateway Input (REST)

```json
{
  "user_id": "uuid7",
  "model_name": "ANT_COLONY_MODEL | PYTHAGOREAN_SUPPORT_MACHINE_MODEL",
  "data": "string (JSON-serialized model input)"
}
```

- `data` is a raw JSON string that the Gateway unpacks and validates against the model's proto definition
- Gateway has access to all model protos and rejects invalid payloads before forwarding

### Model Protos (Shared)

Each model defines its own proto for input/output. Lives in a shared `protos/` directory at the repo root — all services reference it.

```
ml-models-api/
├── protos/
│   ├── protos/                    ← .proto source files
│   │   ├── trigger.proto          ← trigger enums and message
│   │   └── models/
│   │       ├── ant_colony.proto
│   │       └── pythagorean.proto
│   ├── protos_go/                 ← generated Go code
│   └── protos_python/             ← generated Python code
├── src/
│   ├── gateway/
│   ├── proxy/
│   ├── models/
│   ├── reader/
│   └── writer/
└── docker-compose.yml
```

Each service's Dockerfile copies `protos/` and runs `protoc` at build time. Go services generate into `protos_go/`, Python workers into `protos_python/`.

Gateway uses the protos to:
1. Deserialize `data` string from the request
2. Validate structure against the proto
3. Reject with error if invalid, forward if valid

**ANT_COLONY_MODEL input:**
```json
{
  "points": [{"x": 1.0, "y": 2.0}, ...]
}
```

**PYTHAGOREAN_SUPPORT_MACHINE_MODEL input:**
```json
{
  "points": [{"coordinates": [1.0, 2.0, ...]}, ...],
  "n_groups": 3
}
```

---

## Section Model

A **section** is the lifecycle unit of a model. It groups everything related to one model usage: fit input, fit output, predict input, predict output.

### Rules

- One section = one fit + N predicts
- Re-fitting creates a new section
- MODEL_PREDICT requires a completed MODEL_FIT on the same section (enforced by the Model worker)
- Each artifact (fit_input, fit_output, predict_input, predict_output) has its own ID, but the `section_id` is the key that ties them together

### Lifecycle

```
User creates section (via Gateway)
    |
    v
MODEL_FIT trigger
    |
    v
Model worker reads fit_input → runs fit → writes state
    |
    v
MODEL_PREDICT trigger (only valid if state exists)
    |
    v
Model worker reads state → runs predict → writes inference
```

---

## Postgres Schema

### sections

| Column     | Type      | Notes                        |
|------------|-----------|------------------------------|
| id         | uuid7     | PK — this is the section_id  |
| user_id    | uuid7     | FK or external reference     |
| model_name | string    | e.g. "ANT_COLONY_MODEL"       |
| created_at | timestamp |                              |

### fit_inputs

| Column     | Type      | Notes                   |
|------------|-----------|-------------------------|
| id         | uuid7     | PK                      |
| section_id | uuid7     | FK → sections.id        |
| data       | jsonb     | model-specific input    |
| created_at | timestamp |                         |

### states

| Column     | Type      | Notes                                          |
|------------|-----------|------------------------------------------------|
| id         | uuid7     | PK                                             |
| section_id | uuid7     | FK → sections.id (unique)                      |
| data       | jsonb     | trained model state — also the predict input   |
| created_at | timestamp |                                                |

### inferences

| Column     | Type      | Notes              |
|------------|-----------|--------------------|
| id         | uuid7     | PK                 |
| section_id | uuid7     | FK → sections.id   |
| data       | jsonb     | predictions        |
| created_at | timestamp |                    |

### outbox

| Column       | Type      | Notes                                    |
|--------------|-----------|------------------------------------------|
| id           | uuid7     | PK                                       |
| trigger_name | string    | "MODEL_FIT" or "MODEL_PREDICT"           |
| section_id   | uuid7     | FK → sections.id                         |
| payload      | jsonb     | full trigger message                     |
| created_at   | timestamp |                                          |
| processed    | boolean   | Debezium marks after capture             |

### Constraints

- `states.section_id` is **unique** — one fit per section
- `inferences` can have many rows per section (N predicts)

---

## Run Trigger Contract (Kafka)

Published via outbox + Debezium after Gateway writes input data.

### MODEL_FIT

```json
{
  "trigger_name": "MODEL_FIT",
  "user_id": "uuid7",
  "model_name": "ANT_COLONY_MODEL",
  "section_id": "uuid7",
  "request_id": "uuid7",
  "fit_input_id": "uuid7"
}
```

### MODEL_PREDICT

```json
{
  "trigger_name": "MODEL_PREDICT",
  "user_id": "uuid7",
  "model_name": "ANT_COLONY_MODEL",
  "section_id": "uuid7",
  "request_id": "uuid7"
}
```

- MODEL_FIT includes `fit_input_id` so the worker knows which row to read
- MODEL_PREDICT only needs `section_id` — the worker reads the `state` from that section

---

## Gateway Flow (detailed)

### POST /fit

1. Validate `data` against model proto
2. Create `section` row (or receive existing section_id — TBD)
3. Write `fit_input` row via Writer
4. Writer inserts outbox row with `MODEL_FIT` trigger
5. Debezium captures outbox → Kafka

### POST /predict

1. Validate `section_id` exists
2. Writer inserts outbox row with `MODEL_PREDICT` trigger
3. Debezium captures outbox → Kafka

### Model Worker Flow (MODEL_FIT)

1. Consume trigger from Kafka (via Proxy)
2. Read `fit_input` via Reader (using `fit_input_id`)
3. Run model `.fit(data)`
4. Write `state` via Writer
5. Writer inserts outbox row with completion event

### Model Worker Flow (MODEL_PREDICT)

1. Consume trigger from Kafka (via Proxy)
2. Read `state` via Reader (using `section_id`) — **fail if not found**
3. Run model `.predict(state)`
4. Write `inference` via Writer
5. Writer inserts outbox row with completion event

---

## Open Questions

- Gateway naming: "Gateway" vs "Router" vs something else?
- Proxy routing strategy: round-robin, model-type-based, resource-aware?
- How many Kafka topics? One per stage or shared?
- Model discovery: static config or dynamic registration?
- Auth/rate-limiting at the Gateway level?
- POST /fit: always creates a new section, or can the user provide an existing section_id?
- How to handle predict requests while fit is still running? Queue or reject?
