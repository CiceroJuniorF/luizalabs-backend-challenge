# Use uma imagem base com Python
FROM python:3.12-slim

# Instala dependências do sistema (se precisar)
RUN apt-get update && apt-get install -y build-essential

# Instala Poetry
RUN pip install poetry

# Copia arquivos do projeto
WORKDIR /app
COPY pyproject.toml poetry.lock /app/

# Instala as dependências com Poetry
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-root

COPY ./src /app/src

COPY .env /app/

# Expõe porta padrão do FastAPI / Uvicorn
EXPOSE 8000

# Comando para rodar FastAPI (sem reload no container)
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
