# Potencial de Crescimento Empresarial 🚀

Uma aplicação web interativa construída com Streamlit para análise inteligente do potencial de crescimento de empresas, baseada em indicadores financeiros e macroeconômicos usando Machine Learning.

## 🌟 Funcionalidades

### 1. Dashboard Interativo 📊
- Interface elegante com tema escuro e cores quentes
- Menu de navegação premium com ícones e animações
- Métricas em tempo real com visualizações premium
- Status do sistema em tempo real
- Navegação intuitiva entre seções

### 2. Análise de Dados 📈
- Estatísticas gerais das empresas
- Distribuição geográfica (Top 10 países)
- Análise de potencial de crescimento por categoria
- Visualizações interativas com Plotly

### 3. Informações do Modelo 🤖
- Parâmetros detalhados do Random Forest
- Importância das features (variáveis mais relevantes)
- Métricas de performance do modelo

### 4. Predições Inteligentes 🔮
- **Predição Individual**: Seleção por país e empresa do dataset
- **Predição por Campos (SPA)**: Formulário interativo para entrada manual de dados
- **Predição em Lote**: Upload de CSV para análise em massa
- **Template de Dados**: Download de template para predições em lote
- **Interpretação de Resultados**: Análise detalhada com níveis de confiança
- **Visualizações**: Gráficos de probabilidades e distribuição

### 5. Insights Avançados 💡
- **🌍 Análise Geográfica**: Distribuição por países, mapas de calor, análise regional detalhada
- **📊 Análise Financeira**: Box plots, violin plots, estatísticas por potencial de crescimento
- **🔍 Correlações**: Matriz de correlação completa, correlações específicas com potencial
- **📈 Tendências**: Scatter plots interativos, análise de clusters com K-means
- **🎯 Insights Avançados**: Análise de outliers, recomendações baseadas em dados, resumo executivo

## 🛠️ Tecnologias Utilizadas

- **Python 3.x**
- **Streamlit**: Interface web interativa
- **Streamlit Option Menu**: Menu de navegação elegante
- **Plotly**: Visualizações interativas
- **Pandas**: Manipulação de dados
- **Scikit-learn**: Modelo de Machine Learning (Random Forest)
- **Joblib**: Serialização do modelo

## 📦 Instalação

### Método 1: Clone Completo (Recomendado)
1. Clone o repositório:
```bash
git clone https://github.com/sidnei-almeida/potencial_empresarial.git
cd potencial_empresarial
```

2. Crie um ambiente virtual (opcional, mas recomendado):
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

### Método 2: Apenas o App (Download Automático)
1. Baixe apenas o arquivo `app.py` e `requirements.txt`:
```bash
wget https://raw.githubusercontent.com/sidnei-almeida/potencial_empresarial/main/app.py
wget https://raw.githubusercontent.com/sidnei-almeida/potencial_empresarial/main/requirements.txt
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Execute o app:
```bash
streamlit run app.py
```

> **💡 Nota:** Com o Método 2, os dados e modelo são baixados automaticamente do GitHub quando necessário!

## 🚀 Como Usar

### Método 1: Script Automatizado (Recomendado)
```bash
./run_app.sh
```

### Método 2: Execução Manual
1. Ative o ambiente virtual:
```bash
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
```

2. Execute a aplicação:
```bash
streamlit run app.py
```

3. Acesse a aplicação no navegador (geralmente em http://localhost:8501)

### Método 3: Execução Direta
```bash
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```

## 📁 Estrutura de Arquivos

```
tcc_streamlit/
├── app.py                          # Aplicação principal Streamlit
├── run_app.sh                      # Script de execução automatizado
├── requirements.txt                # Dependências Python
├── README.md                       # Documentação
├── .streamlit/
│   └── config.toml                 # Configuração do tema escuro
├── dados/
│   └── data.csv                   # Dataset principal das empresas
├── modelos/
│   ├── Random_Forest_model.joblib # Modelo treinado (Random Forest)
│   └── Random_Forest_model.pkl    # Modelo em formato alternativo
└── pipeline/
    └── classification_pipeline.py # Pipeline de classificação
```

## 🔮 Funcionalidades de Predição

### 🏢 Predição Individual
- Seleção de empresa existente no dataset
- Análise baseada em dados reais
- Visualização de informações da empresa
- Resultados com gráficos de probabilidades

### 📊 Predição por Campos (SPA)
- **Single Page Application** com formulário interativo
- Campos para todos os indicadores financeiros e macroeconômicos
- Validação de entrada em tempo real
- Análise personalizada com interpretação detalhada
- Níveis de confiança da predição

### 📋 Predição em Lote
- Upload de arquivo CSV com múltiplas empresas
- Template de dados disponível para download
- Validação automática de colunas obrigatórias
- Processamento em massa com estatísticas consolidadas
- Download dos resultados completos

## 🔍 Funcionalidades de Insights Avançados

### 🌍 Análise Geográfica
- **Distribuição por Países**: Top 10 países por número de empresas e potencial médio
- **Análise Detalhada**: Métricas consolidadas por país (média, mediana, desvio padrão)
- **Mapa de Calor**: Visualização da distribuição de potencial por país
- **Filtros Inteligentes**: Análise apenas para países com dados suficientes

### 📊 Análise Financeira
- **Box Plots**: Distribuição de capitalização e receita por potencial
- **Violin Plots**: Análise de P/E Ratio e Dividend Yield por categoria
- **Estatísticas Detalhadas**: Métricas financeiras consolidadas por potencial
- **Comparações**: Análise entre diferentes níveis de potencial

### 🔍 Análise de Correlações
- **Matriz Completa**: Correlações entre todas as variáveis numéricas
- **Correlações Específicas**: Foco nas correlações com potencial de crescimento
- **Análise por Potencial**: Matrizes de correlação separadas por nível de potencial
- **Visualizações Interativas**: Heatmaps coloridos e gráficos de barras

### 📈 Análise de Tendências
- **Scatter Plots**: Relações entre variáveis financeiras
- **Análise de Clusters**: Identificação de grupos de empresas usando K-means
- **Características dos Clusters**: Estatísticas detalhadas por cluster
- **Filtros de Dados**: Tratamento inteligente de valores negativos

### 🎯 Insights Avançados
- **Análise de Outliers**: Identificação de empresas com características atípicas
- **Recomendações**: Empresas com potencial de upgrade baseado em similaridade
- **Resumo Executivo**: Métricas consolidadas e insights principais
- **Análise de Performance**: Classificação por características (Small/Mid/Large Cap)

## 📊 Formato dos Dados

O dataset principal (`data.csv`) deve conter as seguintes colunas:
- `name`: Nome da empresa
- `country`: País de origem
- `dividend_yield_ttm`: Rendimento de dividendos
- `earnings_ttm`: Lucros (TTM)
- `marketcap`: Capitalização de mercado
- `pe_ratio_ttm`: Índice P/L (TTM)
- `revenue_ttm`: Receita (TTM)
- `price`: Preço da ação
- `gdp_per_capita_usd`: PIB per capita (USD)
- `gdp_growth_percent`: Crescimento do PIB (%)
- `inflation_percent`: Taxa de inflação (%)
- `interest_rate_percent`: Taxa de juros (%)
- `unemployment_rate_percent`: Taxa de desemprego (%)
- `exchange_rate_to_usd`: Taxa de câmbio para USD
- `inflation`: Valor absoluto da inflação (geralmente negativo)
- `interest_rate`: Valor absoluto da taxa de juros (geralmente negativo)
- `unemployment`: Valor absoluto da taxa de desemprego (geralmente negativo)
- `pc_class`: Classe de potencial (0=Baixo, 1=Médio, 2=Alto)

### 📊 Features do Modelo (15 features)
O modelo Random Forest foi treinado com 15 features:
1. `dividend_yield_ttm`
2. `earnings_ttm`
3. `marketcap`
4. `pe_ratio_ttm`
5. `revenue_ttm`
6. `price`
7. `gdp_per_capita_usd`
8. `gdp_growth_percent`
9. `inflation_percent`
10. `interest_rate_percent`
11. `unemployment_rate_percent`
12. `exchange_rate_to_usd`
13. `inflation`
14. `interest_rate`
15. `unemployment`

## 📊 Modelo de Machine Learning

- **Algoritmo**: Random Forest Classifier
- **Classes de Previsão**:
  - 0: Baixo Potencial de Crescimento
  - 1: Médio Potencial de Crescimento  
  - 2: Alto Potencial de Crescimento
- **Features**: 15+ indicadores financeiros e macroeconômicos
- **Preprocessamento**: Normalização e balanceamento de classes
- **Validação**: Cross-validation para robustez

## 🎨 Design e Interface

- **Tema**: Escuro elegante com cores quentes (laranja, amarelo, vermelho)
- **Configuração**: Tema escuro configurado no `.streamlit/config.toml`
- **Tipografia**: Inter (Google Fonts) para melhor legibilidade
- **Componentes**: Cards premium com animações suaves
- **Visualizações**: Plotly para gráficos interativos
- **Responsivo**: Interface adaptável para diferentes tamanhos de tela

### 🎨 Cores do Tema
- **Primária**: #FF6B35 (Laranja quente)
- **Fundo**: #0E1117 (Escuro)
- **Fundo Secundário**: #1E1E1E (Cinza escuro)
- **Texto**: #FAFAFA (Branco claro)

## 🌐 Integração com GitHub

Este projeto está totalmente integrado com o GitHub para facilitar o uso e distribuição:

### 📥 Download Automático
- **Dados e Modelo**: São baixados automaticamente do GitHub quando não estão disponíveis localmente
- **Cache Inteligente**: Arquivos são armazenados temporariamente por 1 hora para evitar downloads repetidos
- **Fallback**: Se não houver conexão com o GitHub, o app tenta usar arquivos locais
- **Status em Tempo Real**: Interface mostra a fonte dos dados (Local/GitHub) e status da conexão

### 🔗 URLs do Repositório
- **Repositório**: https://github.com/sidnei-almeida/potencial_empresarial
- **Dados**: https://raw.githubusercontent.com/sidnei-almeida/potencial_empresarial/main/dados/data.csv
- **Modelo**: https://raw.githubusercontent.com/sidnei-almeida/potencial_empresarial/main/modelos/Random_Forest_model.joblib

### 🚀 Deploy Simples
Agora você pode compartilhar apenas o arquivo `app.py` e o app funcionará automaticamente, baixando todos os recursos necessários do GitHub!

## 📝 Notas Importantes

- **Arquivos Locais**: Se os arquivos `data.csv` e `Random_Forest_model.joblib` estão presentes localmente, eles serão usados
- **Download Automático**: Se não estiverem presentes, serão baixados automaticamente do GitHub
- **Conexão**: Requer conexão com a internet para download inicial dos recursos
- **Cache**: Arquivos baixados são armazenados temporariamente para melhor performance
- O modelo foi treinado com dados pré-processados e normalizados
- A aplicação verifica automaticamente a disponibilidade dos componentes
- Todas as visualizações são otimizadas para o tema escuro

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor, sinta-se à vontade para submeter pull requests.

## 📄 Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 👥 Autor

- Sidnei Almeida - Desenvolvimento 