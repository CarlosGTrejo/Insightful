# Insightful
A productivity tool using ASR and LLM technology to help users inspect recordings with ease.

## Requirements
1. [Python 3.10](https://www.python.org/downloads/release/python-31010/#:~:text=Full%20Changelog-,Files,-Version)
    1.1 pipx: optional, but encouraged `pip install -U pipx`
    1.2 pdm: **required**, encouraged to be installed using pipx (`pipx install -U pdm`)
2. [Node >=18.6 <=18.14.1](https://nodejs.org/en/)
    2.1 Enable corepack: `corepack enable` (required for Yarn)
3. [Yarn ~=3](https://yarnpkg.com/) `corepack prepare yarn@stable --activate`

## Setup
1. Enable pep582: `pdm --pep582`
2. `cd Insightful`
3. Install project dependencies (Backend): `pdm install`
4. Install project dependencies (Frontend): `yarn install`

## Run
1. Run the frontend: `yarn dev`
2. Run the backend: `py backend/main.py`


## Recommended IDE Setup

[VS Code](https://code.visualstudio.com/) + [Svelte](https://marketplace.visualstudio.com/items?itemName=svelte.svelte-vscode) + [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
