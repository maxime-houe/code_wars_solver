FROM amd64/ubuntu:latest

# Install essential packages
RUN apt-get update && \
    apt-get install -y \
    software-properties-common \
    curl unzip wget \
    build-essential \
    libgtk-3-0 \
    libdbus-glib-1-2 \
    libxt6 \
    libx11-xcb1 \
    libxrender1 \
    libx11-6 \
    libcairo2 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libasound2

# install geckodriver and firefox
#TODO: retrieve the latest version automatically (next commented line does not work)
# RUN GECKODRIVER_VERSION=`curl https://github.com/mozilla/geckodriver/releases/latest | grep -Po 'v[0-9]+.[0-9]+.[0-9]+'`
ENV GECKODRIVER_VERSION="v0.33.0"
RUN echo $GECKODRIVER_VERSION
RUN wget https://github.com/mozilla/geckodriver/releases/download/$GECKODRIVER_VERSION/geckodriver-$GECKODRIVER_VERSION-linux64.tar.gz && \
    tar -zxf geckodriver-$GECKODRIVER_VERSION-linux64.tar.gz -C /usr/local/bin && \
    chmod +x /usr/local/bin/geckodriver && \
    rm geckodriver-$GECKODRIVER_VERSION-linux64.tar.gz

RUN FIREFOX_SETUP=firefox-setup.tar.bz2 && \
    apt-get purge firefox && \
    wget -O $FIREFOX_SETUP "https://download.mozilla.org/?product=firefox-latest&os=linux64" && \
    tar xjf $FIREFOX_SETUP -C /opt/ && \
    ln -s /opt/firefox/firefox /usr/bin/firefox && \
    rm $FIREFOX_SETUP


ENV PYTHON_VERSION=3.11
ENV POETRY_VERSION=1.6.0
ENV VIRTUAL_ENV=/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install Python 3.11
RUN apt-get update && \
    apt-get install -y \
    python$PYTHON_VERSION \
    python3-pip \
    python$PYTHON_VERSION-venv

# Set the default Python version
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.11 1

# Update pip to the latest version
RUN python -m pip install --upgrade pip


# Install poetry and setup venv
RUN pip install "poetry==$POETRY_VERSION"
RUN python -m venv --copies $VIRTUAL_ENV

# Take requirements and install them
COPY pyproject.toml ./
COPY poetry.lock ./
RUN poetry install --no-interaction --no-ansi


SHELL ["/bin/bash", "-c"]
RUN pip install --upgrade setuptools
COPY ./app /code_wars_solver/app
COPY ./pyproject.toml /code_wars_solver
COPY ./tests /code_wars_solver/tests
WORKDIR /code_wars_solver/app

RUN pytest --version
CMD uvicorn main:app --host 0.0.0.0 --port 8000 --reload
