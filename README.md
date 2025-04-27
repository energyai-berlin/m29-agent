# m29-agent

Restack AI - Agent with Chat and Web Search

This repository contains an AI agent for Restack that can chat and perform web searches to provide more truthful and up-to-date information, especially useful for fact-checking and gaining more truth in politics.

## Prerequisites

- Docker (for running Restack)
- Python 3.10 or higher

## Start Restack

To start Restack, use the following Docker command:

```bash
docker run -d --pull always --name restack -p 5233:5233 -p 6233:6233 -p 7233:7233 -p 9233:9233 ghcr.io/restackio/restack:main
```

## Start Python Shell

If using uv:

```bash
uv venv && source .venv/bin/activate
```

If using pip:

```bash
python -m venv .venv && source .venv/bin/activate
```

## Install Dependencies

If using uv:

```bash
uv sync
uv run dev
```

If using pip:

```bash
pip install -e .
python -c "from src.services import watch_services; watch_services()"
```

## Run Agent

### From UI

You can run workflows from the UI by clicking the "Run" button.

### From API

You can run workflows from the API using the generated endpoint:

`POST http://localhost:6233/api/agents/AgentChat`

### From Any Client

You can run workflows with any client connected to Restack, for example:

If using uv:

```bash
uv run schedule-seed-workflow
```

If using pip:

```bash
python -c "from src.schedule_workflow import run_schedule_seed_workflow; run_schedule_seed_workflow()"
```

This executes `schedule_agent.py`, which connects to Restack and runs the `AgentChat` agent.

## Send Events to the Agent

### From UI

You can send events like messages or end the conversation from the UI and see the events in the run.

### From API

Send events to the agent using the following endpoint:

`PUT http://localhost:6233/api/agents/AgentChat/:agentId/:runId`

with the payload:

```json
{
  "eventName": "messages",
  "eventInput": {
    "messages": [{"role": "user", "content": "tell me a joke"}]
  }
}
```

to send messages to the agent.

or

```json
{
  "eventName": "end"
}
```

to end the conversation.

### From Any Client

You can send events to the agent workflows with any client connected to Restack. Modify `workflow_id` and `run_id` in `event_workflow.py` and then run:

If using uv:

```bash
uv run event
```

If using pip:

```bash
python -c "from src.event_agent import run_event_agent; run_event_agent()"
```

This will connect to Restack and send events to the agent, such as generating another agent or ending the conversation.

## Deploy on Restack Cloud

To deploy the application on Restack, create an account at [https://console.restack.io](https://console.restack.io).
