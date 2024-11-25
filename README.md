* install ollama with `curl -fsSL https://ollama.com/install.sh | sh`
* run ollama `ollama serve`
* pull model: `ollama pull qwen2:0.5b`

* install uv: `curl -LsSf https://astral.sh/uv/install.sh | sh`

* clone this repo
* optional: add your private data into info.txt
* RAG_MODEL=qwen2:0.5b uv run main.py
* input your questions