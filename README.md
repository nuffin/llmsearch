# LLM Search

[中文](README.zh.md)

## Summary

Perform efficient semantic search through local or remote LLM backends and ElasticSearch to reduce hardware requirements.

Suitable for personal use with relatively low hardware configurations, and also for organizations with local large model backends deployed.

By uploading documents in various file formats, re-training can be performed according to one's own needs.

## Requirements

- Python 3.x (3.8-3.11, for PyTorch and Tensorflow), for running directly without docker

## How to run

### Run the LLM and ElasticSearch backends

#### With docker

```sh
docker compose -p llmpa -f docker/docker-compose.yml up -d
```

the default docker-compose.yml contains ollama and localai containers, in which the ollama image is built with `scripts/build-ollama-image.sh`

### Run the llmpa engine

#### With docker

There is already llm engine entry in docker/docker-comopose.yml. or you can run it with the following command:

```sh
scripts/build-image.sh
docker run -d -p 58000:58000 --name llmpa llmpa
```

#### Without docker

Assumed you are in the root directory of the project:

```sh
pip install -r requirements.txt --extra-index-url https://download.pytorch.org/whl/cu124
python3 -m llmpa
```

## TODO

- [ ] internal LLM server with pytorch and tensorflow
