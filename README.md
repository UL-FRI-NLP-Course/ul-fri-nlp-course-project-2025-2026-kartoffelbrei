# **AI-Assisted Chatbot for Real-Time Information on Finnish Railway Systems**

The chatbot combines **intent detection**, **live API data**, **live data retrieval with RAG**, and 
**LLM-based responses** to answer questions about train connections, train status, station timetables, 
and general railway information. More information can be found in `report/report.pdf`.

---

## Features

- Intent detection.
- Live data via **Fintraffic API** [1]. 
- RAG for static railway information.
- Local LLMs:
  - *Mistral-7B-Instruct-v0.3* for intent detection.
  - *Qwen2.5-14B* for the answer model.
  - *paraphrase-multilingual-MiniLM-L12-v2* for the embedding model.

---

## Setup in Arnes's Cluster

1. Clone the repository in your home node.
2. Create the directory `containers`.
3. Build a singularity image: `singularity build --sandbox ./containers/container-pytorch-2-5-1 docker://pytorch/pytorch:2.5.1-cuda12.1-cudnn9-runtime`.
4. Install additional libraries: `singularity exec --writable --no-home --no-mount pwd ./containers/container-pytorch-2-5-1 env PYTHONUSERSITE=1 pip install ./ul-fri-nlp-course-project-2025-2026-kartoffelbrei`
5. Create a shell script (e.g. `run-main.sh`) to run the container:
```bash
#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --gres=gpu:1
#SBATCH --partition=gpu
#SBATCH --time=00:30:00
#SBATCH --output=logs/main-%J.out
#SBATCH --error=logs/main-%J.err
#SBATCH --job-name="main test"
#SBATCH --mem=64G

export HF_TOKEN=[your personal huggingface token]
srun singularity exec --nv containers/container-pytorch-2.2.0 python \
    "ul-fri-nlp-course-project-2025-2026-kartoffelbrei/src/main.py"
```
6. Create the directory `logs`: `mkdir logs`
7. To load the models change `MODEL_CACHE_DIR` in `src/llm_engine/config_llm.py` to your shared node.
8. Execute the shell script: `sbatch run-main.sh`

---

## Repository Organization

The repository is organized into the three main directories `report`, `results` and `src`.
- `report` contains the paper describing the scientific contributions of the project.
- `src` contains the projects source code which is divided into the following directories:
  - `analysis` contains code for analyzing the output of the AI assistant.
  - `backend` handles the API requests and scraping of website for RAG based answers.
  - `llm_engine` is the core of the project. Here the intent of a user query is extracted, data is resolved with either API or RAG and an answer is generated with the provided data. The directory also contains all valid intents the assistant can extract.
  - `llm_prompts` contains the used prompts for the intent and the answer model.
  - `llm_queries` provides user queries the pipeline goes through when executed. Users can add or change queries here and label them with the expected intent which can be found in **`src/llm_engine/intents.py`**.
  - `metadata` contains metadata extracted from the **Fintraffic API** that is used for API requests.
  - `util` provides only one class to create the result files.
- `results` contains the generated output of the AI assistant after executing the source code in `src`. Main components are:
  - `confusion_matrix_[current_date].csv`
  - `metrics_[current_date].csv`,
  - and `pipeline_log_[current_date].txt` which contains all the generated answers of the assistant.

All used project dependencies and collaborators can be found in the `pyproject.toml` file.

---

## Sources

[1] https://www.digitraffic.fi/rautatieliikenne/