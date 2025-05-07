# 📈 Análise Preditiva do Potencial de Crescimento de Empresas

Este repositório apresenta uma solução de *machine learning* que combina **agrupamento não supervisionado (KMeans)** e **classificação supervisionada (XGBoost)** para prever o *potencial de crescimento (PC)* de empresas do continente americano, com base em dados financeiros e macroeconômicos. O projeto inclui uma **API pronta para deploy** em websites ou aplicações interativas.

🔗 [Acesse o repositório](https://github.com/sidnei-almeida/potencial_empresarial)

---

## 🧠 Objetivo do Projeto

O objetivo é construir um modelo que classifique empresas em diferentes classes de **potencial de crescimento**, utilizando dados estruturados. Para isso:

- Foi feita uma análise exploratória dos dados.
- As empresas foram agrupadas usando **KMeans**, criando uma variável-alvo (`pc_class`).
- Essa variável foi utilizada em modelos de classificação supervisionada.
- O **XGBoost** foi o algoritmo com melhor desempenho.

---

## 🧰 Tecnologias e Ferramentas

- **Python 3.10+**
- `pandas`, `numpy`, `matplotlib`, `seaborn`
- `scikit-learn`, `xgboost`
- `FastAPI`
- `uvicorn`

---

## 🗃️ Estrutura do Repositório

📦 potencial_empresarial/
┣ 📂 data/ # Datasets utilizados (financeiros e macroeconômicos)
┣ 📂 notebooks/ # Jupyter Notebooks com EDA, modelagem e validação
┣ 📂 models/ # Modelos treinados e salvos (.pkl)
┣ 📂 api/ # API com Streamlit ou Flask
┣ 📄 requirements.txt # Dependências do projeto
┣ 📄 README.md # Este arquivo
┗ 📄 .gitignore

---

## 📊 Pipeline do Projeto

1. **Coleta de Dados**
   - Dados financeiros de empresas: dividend yield, revenue, P/E ratio, market cap, earnings.
   - Dados macroeconômicos via APIs: PIB per capita, taxa de crescimento, juros, câmbio, desemprego, inflação.

2. **Análise Exploratória (EDA)**
   - Verificação de distribuições, outliers, correlações.
   - Visualização com `seaborn` e `matplotlib`.

3. **Pré-processamento**
   - Normalização e preenchimento de valores nulos.
   - Criação de novas variáveis derivadas (feature engineering).

4. **Clusterização com KMeans**
   - Agrupamento das empresas em 4 clusters (0 a 3) com base em características financeiras.
   - Essa variável foi renomeada como `pc_class` e usada como *target* para os classificadores.

5. **Modelagem Supervisionada**
   - Algoritmos testados: Decision Tree, Logistic Regression, KNN, SVM, Random Forest e XGBoost.
   - Melhor desempenho: **XGBoost** com alta acurácia e F1-Score.
   - Avaliação com matriz de confusão e curva ROC.

6. **Deploy da API**
   - Aplicação web com **Streamlit**, permitindo ao usuário inserir dados e obter a previsão do potencial de crescimento.
   - Endpoint da API para integração com outros sistemas.

---

## 📈 Principais Resultados

- **XGBoost** teve os melhores resultados entre os modelos supervisionados.
- A clusterização inicial com **KMeans** ajudou a reduzir ruído e criar rótulos coerentes.
- O modelo foi encapsulado em uma API leve e responsiva.

---

## 🌐 Como Executar

### 1. Clone o repositório

```bash
git clone https://github.com/sidnei-almeida/potencial_empresarial.git
cd potencial_empresarial
