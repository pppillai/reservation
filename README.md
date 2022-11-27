# reservation
- create reservation system
  - use fast api/flask? or use click to create cmdline python program and sql lite for db
- add user interface
- add test
  - use pytest

## Setup
  - create a virtual environment
    - python -m venv .venv
  - activate the virtual environment
    - source .venv/bin/activate
  - install pip-tools
    - pip install pip-tools
  - create a new requirements.in file and add the library you want to use without version
    - eg: pytest
  - create a requirement.txt file by running the following command.
    - pip-comiple requirements.in --output-file requirements.txt
  - install the packages by running 
    - pip install -r requirements.txt

## Run the Server
    - cd to the api_server folder
    - type the following command
        uvicorn main:app --reload