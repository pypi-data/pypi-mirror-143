# Dockerhub Client

Client library to interact with dockerhub API. Shipped with a CLI that enables high level access to main features.

## Installation

```bash
pip install dockerhub-client
```

## Usage from CLI

Using CLI, dockerhub credentials must be provided as environment variables.

```
export DOCKERHUB_USERNAME=<username>
export DOCKERHUB_PASSWORD=<password or token>
```

## Library reference

Instanciate client with dockerhub credentials...

```python
from dockerhub.client import DockerhubClient

dockerhub = DockerhubClient("<username>", "<password or token>")
```

Get repository information

```python
dockerhub.get_repository("<namespace>/<repo>")
```
