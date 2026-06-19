# Distributed Large-File Ingestion Pipeline

## Overview

This repository contains an initial Python prototype for a distributed large-file ingestion pipeline.

The prototype focuses on the core state-management concepts behind asynchronous ingestion: parent upload tracking, chunk-level status tracking, queue message modeling, worker-style processing, status aggregation, and retry-aware data structures.

It is intentionally small and uses only the Python standard library, with `pytest` for tests. The goal is to demonstrate clean modeling and testable orchestration patterns, not to present a production-ready ingestion platform.


## Technical Write-Up

For the design thinking behind this prototype, see:

[Designing Reliable Distributed File Ingestion for AI and Analytics Systems](./ARTICLE.md)


## Problem

Large files can be difficult to process reliably through a single synchronous request. Upload size limits, timeouts, partial failures, retry behavior, and long-running backend work all create operational risk.

A distributed ingestion workflow typically needs to:

- Track the overall parent upload lifecycle.
- Split work into independently processed chunks.
- Send chunk work through a queue or queue-like contract.
- Process chunks with background workers.
- Track per-chunk success, failure, and retry state.
- Aggregate chunk statuses back into a parent-level status.
- Preserve enough state to support retries, debugging, and future observability.

## Current Prototype

The current implementation is a local, testable simulation of the core ingestion flow.

It includes:

- `ParentUpload` and `UploadStatus` models for parent-level upload tracking.
- `FileChunk` and `ChunkStatus` models for chunk-level processing state.
- `ChunkProcessingMessage` for queue message modeling.
- `ChunkWorker` for simulated chunk processing.
- `StatusAggregator` for deriving parent upload status from chunk statuses.
- A simple `src.main` script that creates a parent upload, processes three chunks, aggregates final status, and prints the result.
- Pytest coverage for the status aggregation rules.

This prototype does not connect to cloud storage, external queues, databases, or production monitoring systems. Those integrations are intentionally left as future extensions.

## Folder Structure

```text
src/
  __init__.py
  main.py
  models/
    __init__.py
    upload_state.py
    chunk_state.py
    queue_message.py
  worker/
    __init__.py
    chunk_worker.py
  orchestration/
    __init__.py
    status_aggregator.py
tests/
  test_status_aggregation.py
requirements.txt
```

## How to Run

Create a virtual environment:

```bash
python -m venv .venv
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the sample ingestion simulation:

```bash
python -m src.main
```

Expected output shows each processed chunk status followed by the aggregated parent upload status.

## Tests

Run the test suite:

```bash
pytest
```

The tests validate the parent status aggregation rules:

- All successful chunks produce a successful parent upload.
- Mixed successful and failed chunks produce a partially successful parent upload.
- Pending or in-progress chunks produce an in-progress parent upload.
- All failed chunks produce a failed parent upload.

## Future Extensions

Possible next steps include:

- Add local file chunking and manifest generation.
- Simulate retry limits and dead-letter queue behavior.
- Persist parent and chunk state in a lightweight database.
- Add structured logging around worker processing.
- Add failure injection tests for retry and partial completion scenarios.
- Introduce a queue adapter interface for local and cloud-backed implementations.
- Add object storage integration behind a storage abstraction.
- Expand validation and finalization hooks after chunk processing.
- Add basic operational metrics for ingestion progress and failure rates.
