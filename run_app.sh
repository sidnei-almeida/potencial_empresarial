#!/bin/bash

# Script para executar o app Streamlit de Potencial de Crescimento Empresarial

echo "🚀 Iniciando o app de Potencial de Crescimento Empresarial..."

# Verificar se o ambiente virtual existe
if [ -d "venv" ]; then
    echo "📦 Ativando ambiente virtual..."
    source venv/bin/activate
else
    echo "⚠️  Ambiente virtual não encontrado. Criando um novo..."
    python -m venv venv
    source venv/bin/activate
    
    echo "📥 Instalando dependências..."
    pip install -r requirements.txt
fi

# Verificar se os arquivos necessários existem
echo "🔍 Verificando arquivos necessários..."

if [ ! -f "dados/data.csv" ]; then
    echo "❌ Arquivo dados/data.csv não encontrado!"
    exit 1
fi

if [ ! -f "modelos/Random_Forest_model.joblib" ]; then
    echo "❌ Modelo Random_Forest_model.joblib não encontrado!"
    exit 1
fi

echo "✅ Todos os arquivos necessários encontrados!"

# Executar o app
echo "🌟 Executando o app Streamlit..."
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
