FROM python:3.11-buster


COPY src /src
copy ./pyproject.toml /

RUN pip install poetry
RUN poetry install
run sed -i 's/7576/7575/g' /src/main/python/fws-square/main-fastwsgi.py

ENTRYPOINT ["poetry", "run", "python", "/src/main/python/fws-square/main-fastwsgi.py"]