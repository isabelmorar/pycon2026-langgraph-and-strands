# LangGraph and Strands Agents: Core Concepts, Patterns, and Tradeoffs

Hands-on workshop for PyCon Colombia 2026 where participants build the same **Loka Research Agent** in LangGraph and Strands Agents, 
comparing how each framework handles tools, memory, and multi-step reasoning.

## Prerequisites

- [uv](https://docs.astral.sh/uv/) (it will install the right Python for you)
- An **Anthropic API key**

## Setup (do this before the workshop)

```bash
# 1. Clone this repo
git clone https://github.com/isabelmorar/pycon2026-langgraph-and-strands.git

# 2. From the repo root use uv to install dependencies and create a virtual environment:
uv sync                     

# 3. Add your API key
cp .env.example .env        # then paste your key into ANTHROPIC_API_KEY
```

Verify it worked (no API key needed — this just checks the shared code loads):

```bash
uv run python shared/knowledge_base.py
```

## Running the notebooks

The hands-on part of the workshop is in Jupyter notebooks. Run them either with `uv run jupyter lab` or in VS Code / PyCharm with the `.venv` interpreter.

Open the two notebooks in `notebooks/` (one for each framework) and complete the exercises as indicated throughout the workshop.

Answers will be published to **`solutions/`** after each exercise has had some experiment time. Run `git pull` to get them.

## Layout

```
shared/            # given code both frameworks reuse (knowledge base + website search)
notebooks/         # your working notebooks (fill in the blanks here)
  strands.ipynb
  langgraph.ipynb
solutions/         # answers, published as exercises pass
  strands.ipynb
  langgraph.ipynb
```