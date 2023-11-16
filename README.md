code_wars_gpt
===========================

_Use chatGPT to solve code katas from code\_wars_

## Description
The project uses Selenium locally to interact with the website and automatically solve the code katas. The browser used is Mozilla Firefox.

## How to run the project

You can run the project with or without Docker.
It is mandatory to run the project in headless mode if you use Docker.
1. Clone the project [code_wars_gpt](https://github.com/maxime-houe/code_wars_gpt)
2. Create a `local.env` file at the root of the project with the following content:
```
OPENAI_API_KEY=<INSERT_VALUE_HERE>
EMAIL=<INSERT_VALUE_HERE>
PASSWORD=<INSERT_VALUE_HERE>
PSEUDO=<INSERT_VALUE_HERE>
```
The email, password and pseudo are used to log in the [codewars website](https://www.codewars.com/)


### Without Docker
3. Install [geckodriver](https://github.com/mozilla/geckodriver/releases) to enable Selenium to use Firefox

4. Run the following command:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```
If you are using Jetbrains, you can instead run the command in the configuration panel.
The command should have opened a new window in your browser and log in to codewars website

5. Enjoy the [swagger](http://localhost:8000/docs).

### With Docker
3. Run the following command:
```bash
docker-compose up main
```
If you are using Jetbrains, you can instead run the command in the configuration panel.

4. Enjoy the [swagger](http://localhost:8000/docs).