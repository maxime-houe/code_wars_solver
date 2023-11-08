FROM --platform=linux/amd64 python:3.11-slim-bullseye AS build-main
RUN apt-get update --fix-missing && \
    apt-get install -y build-essential

ENV POETRY_VERSION=1.6.0
ENV VIRTUAL_ENV=/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# Install poetry and setup venv
RUN pip install "poetry==$POETRY_VERSION"
RUN python -m venv --copies $VIRTUAL_ENV

# Take requirements and install them
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-interaction --no-ansi --only main

FROM --platform=linux/amd64 python:3.11-slim-bullseye AS runtime
COPY --from=build-main /venv /venv
RUN apt-get update --fix-missing && \
    apt-get install -y apt-transport-https wget icu-devtools
ENV VIRTUAL_ENV=/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
SHELL ["/bin/bash", "-c"]
RUN pip install --upgrade setuptools
WORKDIR /code_wars_gpt/app
COPY ./app /code_wars_gpt/app
COPY ./pyproject.toml /code_wars_gpt


FROM runtime AS main
CMD python main.py


FROM build-main AS build-tests
RUN poetry install --no-interaction --no-ansi --with tests


FROM runtime AS tests
COPY --from=build-tests /venv /venv
COPY ./tests /code_wars_gpt/tests
WORKDIR /code_wars_gpt
CMD pytest -v --junitxml=reports/results.xml --cov-report=xml:reports/coverage.xml --cov=.


FROM build-main AS build-local
RUN poetry install --no-interaction --no-ansi --with local,tests


FROM runtime AS local
COPY --from=build-local /venv /venv
CMD python main.py
