# Usa uma imagem oficial do Python como base
FROM python:3.10-slim

# Define a pasta de trabalho dentro do container
WORKDIR /app

# Copia o arquivo de dependências para o container
COPY requirements.txt .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o código da sua aplicação para o container
COPY . .

# Expõe a porta que o Django vai usar
EXPOSE 8000

# Comando para iniciar o servidor do Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]