code_wars_gpt
===========================

## Description
Use chatGPT to solve code katas from code wars

## Specifications
* Python 3.11
* Poetry 1.6.0

## Documentation
The project use Selenium locally to interact with the website and automatically solve the code katas.

**How to run the project:**
* Install [geckodriver](https://github.com/mozilla/geckodriver/releases) to enable Selenium to use Firefox
* Create a `local.env` file at the root of the project with the following content:
```
OPENAI_API_KEY=<INSERT_VALUE_HERE>
EMAIL=<INSERT_VALUE_HERE>
PASSWORD=<INSERT_VALUE_HERE>
PSEUDO=<INSERT_VALUE_HERE>
```
The email, password and pseudo are used to log in the [codewars website](https://www.codewars.com/)

* Run the following command:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```
* Enjoy the swagger on http://localhost:8000/docs. 
The previous command should have opened a new window in your browser and log in to codewars website
