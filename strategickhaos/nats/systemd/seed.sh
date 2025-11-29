#!/usr/bin/env bash
set -e
# Streams
nats --server nats://127.0.0.1:4222 stream add TELEMETRY --subjects "telemetry.>" --retention limits --storage file --replicas 1 --maxMsgs=-1 --maxBytes=-1 --discard old
nats stream add CMD --subjects "cmd.>" --retention workqueue --storage file --replicas 1
nats stream add AUDIT --subjects "audit.>" --retention limits --storage file --replicas 1
nats consumer add TELEMETRY AUDIT_SINK --pull --filter "telemetry.>" --ack explicit
