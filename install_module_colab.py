import subprocess
import sys
import tempfile
import os

def install_module_colab():
    packages = [
        "python-dotenv",
        "ipykernel",
        "ipywidgets",
        "requests",
        "numpy",
        "pandas>=2.3.3",
        "scipy",
        "scikit-learn",
        "matplotlib",
        "torch",
        "transformers",
        "tqdm",
        "openai",
        "gradio",
        "langchain",
        "langchain-core",
        "langchain-text-splitters",
        "langchain-openai",
        "langchain-chroma",
        "langchain-community",
        "langchain-ollama",
        "datasets==3.6.0",
        "google-generativeai",
        "anthropic",
        "chromadb",
        "plotly",
        "jupyter-dash",
        "beautifulsoup4",
        "pydub",
        "modal",
        "ollama",
        "psutil",
        "setuptools",
        "speedtest-cli",
        "sentence_transformers",
        "feedparser",
        "protobuf==3.20.2",
        "wandb",
    ]

    subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "uv"])
    subprocess.check_call(["uv", "pip", "install", *packages])

    # langgraph is installed separately with a pandas override because it may
    # request a different pandas version than the one pinned above.
    override_content = "pandas>=2.3.3\n"
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
        f.write(override_content)
        override_file = f.name
    try:
        subprocess.check_call(["uv", "pip", "install", "langgraph", "--override", override_file])
    finally:
        os.unlink(override_file)