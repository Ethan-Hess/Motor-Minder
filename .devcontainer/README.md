# Dev Container

This folder contains the development container configuration for this repository.

## Purpose

The dev container provides a consistent, reproducible development environment so all contributors can use the same tools and versions.

## Contents

Typical files in this directory:

- `devcontainer.json` – main dev container configuration
- `Dockerfile` _(optional)_ – custom image setup
- `docker-compose.yml` _(optional)_ – multi-service setup
- `README.md` – this documentation

## Requirements

- [Docker](https://www.docker.com/)
- [Visual Studio Code](https://code.visualstudio.com/)
- [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)

## Getting Started

1. Open this repository in VS Code.
2. Run **Dev Containers: Reopen in Container**.
3. Wait for the container to build and start.

## Rebuild the Container

Use **Dev Containers: Rebuild Container** when:

- `devcontainer.json` changes
- `Dockerfile` changes
- dependencies need a clean refresh

## Customization

Update `devcontainer.json` to configure:

- VS Code extensions
- forwarded ports
- post-create commands
- environment variables

## Notes

- Keep tool installation in the container config for reproducibility.
- Prefer committing all dev environment changes in this folder.
