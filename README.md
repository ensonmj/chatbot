* install ollama with `curl -fsSL https://ollama.com/install.sh | sh`
* run ollama `ollama serve`
* pull model: `ollama pull qwen2:0.5b`

* install uv: `curl -LsSf https://astral.sh/uv/install.sh | sh`

* clone this repo
* optional: add your private data into info.txt
* uv run main.py
* try this [http://localhost:8080/ask?query=what's your name?](http://localhost:8080/ask?query=what's your name?)