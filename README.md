# Network Monitoring and Alerting System

A containerized network monitoring lab built with Docker, Prometheus, Blackbox Exporter, Alertmanager, and Grafana. The project monitors an HTTP endpoint, detects failures, generates alerts, and sends alert notifications to a local webhook receiver.

## Project Objectives

- Monitor HTTP endpoint availability.
- Collect probe metrics using Prometheus and Blackbox Exporter.
- Detect endpoint failures with Prometheus alert rules.
- Route firing and resolved notifications through Alertmanager.
- Visualize endpoint health and response time in Grafana.
- Test failure and recovery scenarios locally.

## Architecture

```text
Demo HTTP Endpoint
       |
       v
Blackbox Exporter
       |
       v
   Prometheus
       |
       v
  Alertmanager
       |
       v
 Local Webhook Receiver

Prometheus Metrics
       |
       v
     Grafana
```

## Technology Stack

- Docker and Docker Compose
- Prometheus
- Prometheus Blackbox Exporter
- Alertmanager
- Grafana
- Python / Flask for the demo endpoint and local alert receiver
- PromQL

## Monitoring and Alerting

The Blackbox Exporter probes the demo endpoint:

`http://demo-target:5000/health`

Prometheus collects probe metrics, including `probe_success` and `probe_duration_seconds`.

Configured alert rules include:

- **NetworkEndpointDown:** triggers when the monitored endpoint fails.
- **NetworkEndpointSlow:** detects slow probes when the configured threshold is exceeded.

Alertmanager routes notifications to a local webhook receiver. Both firing and resolved notification payloads were observed during testing.

## Failure and Recovery Testing

The demo application exposes endpoints for simulating failure and recovery:

- `POST /simulate/down`
- `POST /simulate/up`
- `GET /health`

Example commands:

```cmd
curl -X POST http://localhost:8082/simulate/down
curl http://localhost:8082/health
curl http://localhost:8090/alerts
curl -X POST http://localhost:8082/simulate/up
```

Prometheus verification:

```cmd
curl http://localhost:9090/api/v1/targets
curl "http://localhost:9090/api/v1/query?query=probe_success"
curl http://localhost:9090/api/v1/alerts
```

## Local Access

| Component | Local URL |
|---|---|
| Demo endpoint | http://localhost:8082/health |
| Prometheus | http://localhost:9090 |
| Alertmanager | http://localhost:9094 |
| Grafana | http://localhost:3001 |
| Alert receiver | http://localhost:8090/alerts |

Ports are mapped for this local development environment and may differ in other setups.

## Verification Results

- Prometheus targets reported healthy scraping status.
- The endpoint probe returned `probe_success = 1` during recovery.
- The `NetworkEndpointDown` alert was observed in firing and resolved states.
- The local webhook receiver recorded firing and resolved notification payloads.
- Grafana dashboard panels were created for endpoint status, response time, and recent probe availability.

## Scope and Limitations

This is a local Docker-based monitoring lab. It does not represent a production deployment or a real cloud-hosted monitoring environment. The availability percentage panel reflects recent probe results, not a long-term SLA.

## Skills Demonstrated

- Containerized service deployment
- HTTP endpoint monitoring
- Prometheus scraping and PromQL queries
- Alert rule configuration
- Alertmanager notification routing
- Webhook-based alert inspection
- Grafana dashboard creation
- Failure simulation and recovery verification
- Troubleshooting port conflicts in a multi-container environment
