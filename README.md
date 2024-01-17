code_wars_solver
===========================

_Use LLM to solve code katas from code\_wars_

## Description
The project uses Selenium locally to interact with the website and automatically solve the code katas. The browser used is Mozilla Firefox.
This only supports OpenAI API key for now.

## How to run the project

You can run the project with or without Docker.
It is mandatory to run the project in headless mode if you use Docker.
1. Create a `local.env` file at the root of the project with the following content:
```
OPENAI_API_KEY=<INSERT_VALUE_HERE>
EMAIL=<INSERT_VALUE_HERE>
PASSWORD=<INSERT_VALUE_HERE>
PSEUDO=<INSERT_VALUE_HERE>
```
The email, password and pseudo are used to log in the [codewars website](https://www.codewars.com/)


### Without Docker
2. Install [geckodriver](https://github.com/mozilla/geckodriver/releases) to enable Selenium to use Firefox

3. Run the following command:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```
If you are using Jetbrains, you can instead run the command in the configuration panel.
The command should have opened a new window in your browser and log in to codewars website

4. Enjoy the [swagger](http://localhost:8000/docs).

### With Docker
2. Run the following command:
```bash
docker-compose up main
```
If you are using Jetbrains, you can instead run the command in the configuration panel.

3. Enjoy the [swagger](http://localhost:8000/docs).

## Contributors
Run the following command to link the git hooks to your local git repository:
```bash
ln -s ../../hooks/pre-commit .git/hooks/pre-commit
ln -s ../../hooks/pre-push .git/hooks/pre-push
chmod +x .git/hooks/pre-commit
chmod +x .git/hooks/pre-push
```
You also should install dev dependencies with the following command:
```bash
poetry install --with dev --no-root
```
Then, before each commit, you should run 
```bash
black .
```
This will format the python files accordingly. If not done, the hook will fail.
