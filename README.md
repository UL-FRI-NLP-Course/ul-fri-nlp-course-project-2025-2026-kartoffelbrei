# Natural language processing course: `AI-Assisted Chatbot for Real-Time Information on Finnish Railway Systems`

The chatbot combines **intent detection**, **live API data**, and **LLM-based responses** to answer questions about train connections, delays, and general railway information.

---

## Features

- Intent detection
- Live data via Fintraffic API
- RAG for static railway information
- Local LLMs (e.g. Mistral, TinyLlama)

---

## Setup in Arnes's Cluster

```bash
cd /d/hpc/projects/onj_fri/kartoffelbrei
sbatch run-main.sh
[job-id]
tail -f logs/main-[job-id].out
```
All user queries are stored in:

```bash
src/llm_queries/queries.txt
```