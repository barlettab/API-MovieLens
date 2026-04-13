# Usa exatamente a sua versão do Python (slim é mais leve)
FROM python:3.12.4-slim

# Define o diretório de trabalho
WORKDIR /app

# Copia primeiro apenas o requirements para aproveitar o cache do Docker
COPY requirements.txt .

# Instala as dependências exatas
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante dos arquivos (seu código e o modelo .sav)
COPY . .

# Expõe a porta 8000
EXPOSE 8000

# Comando para rodar a API (sem o reload para ser mais leve no Docker)
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]