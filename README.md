# Insightful
A productivity tool using ASR and LLM technology to help users inspect recordings with ease.

## Steps
1. Install [Python 3.10](https://www.python.org/downloads/release/python-31010/#:~:text=Full%20Changelog-,Files,-Version), then pipx and pdm:  
    1.1 pipx: `pip install -U pipx`  
    1.2 pdm: `pipx install pdm` (note: use `pipx` to install pdm, not pip)  
2. Install [Node >=18.6](https://nodejs.org/en/), then enable corepack  
    2.1 Change execution policy on Windows (run this powershell command as admin): `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned`  
    2.2 Enable corepack: `corepack enable` (required for Yarn)  
3. Install [Github-CLI](https://cli.github.com/).  
4. Clone the project and install its dependencies:  
    4.1 Clone the repo: `gh repo clone CarlosGTrejo/Insightful`  
    4.2 cd into it: `cd Insightful`  
    4.3 Enable pep582: `pdm --pep582`  
    4.4 Disable Python env: `pdm config python.use_venv false`  
    4.5 Install [Yarn ~=3](https://yarnpkg.com/): `corepack prepare yarn@stable --activate`  
    4.6 Install backend dependencies: `pdm install`  
    4.7 Install frontend dependencies: `yarn install`  

## Run
1. Run the frontend: `yarn dev`
2. Run the backend: `py backend/main.py`


## Recommended IDE Setup

[VS Code](https://code.visualstudio.com/) + [Svelte](https://marketplace.visualstudio.com/items?itemName=svelte.svelte-vscode) + [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python)

**There are VS Code tasks in the project, if you press `ctrl + shift + p` to pull up the command palette then type `Run Task` you can select `Start App` to run the backdend and frontend together, or select `Start Frontend` or `Start Backend` to start them individually.
