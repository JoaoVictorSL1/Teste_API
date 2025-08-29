# Usa imagem oficial do Python slim
FROM python:3.11-slim

# Variáveis de ambiente
ENV PORT=8080
ENV LOG_FILE=requests_log.txt

# Define diretório de trabalho
WORKDIR /TESTES_API

# Copia dependências e instala
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código da aplicação
COPY Teste_api.py .

# Expõe a porta do container
EXPOSE $PORT

# Comando para iniciar o servidor com Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "Teste_api:app"]