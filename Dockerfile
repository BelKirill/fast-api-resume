FROM python:3.11 AS poetry-base
RUN pip install poetry && poetry config virtualenvs.create false

FROM poetry-base AS poetry-install
WORKDIR /app
COPY pyproject.toml .
RUN poetry install --no-root

FROM poetry-install AS dev
WORKDIR /app
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
