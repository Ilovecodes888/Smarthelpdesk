# Smart HelpDesk

This repository contains a demonstration of a modern help‑desk application
powered by large language models. The goal of this project is to show how
you can take an existing open‑source chat interface (the excellent
[Chatbot UI](https://github.com/mckaywrigley/chatbot-ui)) and extend it
with a production‑style backend implemented in Python.

The project is split into two parts:

* **smart‑helpdesk‑ui** – a customized front‑end based off of Chatbot UI.
  It allows users to create support tickets and chat about them. The UI
  has been rebranded and slimmed down for use in a help‑desk setting.

* **backend** – a FastAPI application that exposes endpoints for
  authentication, ticket management, conversation history and AI‑powered
  operations such as generating suggested replies or summarizing a
  conversation. Background tasks are run via Celery and Redis to keep
  the API responsive.

The focus of this repository is on demonstrating the **system design
skills** that employers look for in software development engineers:

* Clean separation between front‑end and back‑end services.
* Use of modern web frameworks (Next.js / FastAPI).
* Asynchronous background processing with Celery.
* Containerisation and orchestration via Docker Compose.
* Integration of an external LLM (OpenAI GPT) in a safe, testable way.

## Local development

To run the application locally you will need Docker installed.

```bash
cd backend
docker compose up --build
```

This command starts PostgreSQL, Redis, the FastAPI server and a Celery
worker. The API will be available at <http://localhost:8000>.

In another terminal start the UI:

```bash
cd smart‑helpdesk‑ui
npm install
npm run dev
```

The UI will run on <http://localhost:3000>. You can create tickets,
chat about them and use the "Auto Reply" button to enqueue an AI
generated response. The worker will pick up the job, call the OpenAI
API and store the reply in memory.

## Deployment

This repository includes a simple Dockerfile for the backend. The
`docker-compose.yml` file shows how to run the services together in
production. You can deploy the backend to any platform that supports
Docker containers (e.g. Render, Railway or AWS ECS) and deploy the
frontend to Vercel.

## License

The UI portion of this project is derived from
[Chatbot UI](https://github.com/mckaywrigley/chatbot-ui) which is
licensed under the MIT license. All modifications in this repository
are also released under the MIT license.