# Business Growth Potential 🚀

An interactive web application built with Streamlit for intelligent analysis of company growth potential, based on financial and macroeconomic indicators using Machine Learning.

## 🌟 Features

### 1. Interactive Dashboard 📊
- Elegant interface with dark theme and warm colors
- Premium navigation menu with icons and animations
- Real-time metrics with premium visualizations
- Real-time system status
- Intuitive navigation between sections

### 2. Data Analysis 📈
- General statistics of companies
- Geographic distribution (Top 10 countries)
- Growth potential analysis by category
- Interactive visualizations with Plotly

### 3. Model Information 🤖
- Detailed Random Forest parameters
- Feature importance (most relevant variables)
- Model performance metrics

### 4. Intelligent Predictions 🔮
- **Individual Prediction**: Selection by country and company from dataset
- **Form-Based Prediction (SPA)**: Interactive form for manual data entry
- **Batch Prediction**: CSV upload for bulk analysis
- **Data Template**: Download template for batch predictions
- **Result Interpretation**: Detailed analysis with confidence levels
- **Visualizations**: Probability charts and distribution

### 5. Advanced Insights 💡
- **🌍 Geographic Analysis**: Distribution by countries, heat maps, detailed regional analysis
- **📊 Financial Analysis**: Box plots, violin plots, statistics by growth potential
- **🔍 Correlations**: Complete correlation matrix, specific correlations with potential
- **📈 Trends**: Interactive scatter plots, cluster analysis with K-means
- **🎯 Advanced Insights**: Outlier analysis, data-driven recommendations, executive summary

## 🛠️ Technologies Used

- **Python 3.x**
- **Streamlit**: Interactive web interface
- **Streamlit Option Menu**: Elegant navigation menu
- **Plotly**: Interactive visualizations
- **Pandas**: Data manipulation
- **Scikit-learn**: Machine Learning model (Random Forest)
- **Joblib**: Model serialization

## 📦 Installation

### Method 1: Full Clone (Recommended)
1. Clone the repository:
```bash
git clone https://github.com/sidnei-almeida/potencial_empresarial.git
cd potencial_empresarial
```

2. Create a virtual environment (optional, but recommended):
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Method 2: App Only (Automatic Download)
1. Download only the `app.py` and `requirements.txt` files:
```bash
wget https://raw.githubusercontent.com/sidnei-almeida/potencial_empresarial/main/app.py
wget https://raw.githubusercontent.com/sidnei-almeida/potencial_empresarial/main/requirements.txt
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the app:
```bash
streamlit run app.py
```

> **💡 Note:** With Method 2, data and model are automatically downloaded from GitHub when needed!

## 🚀 How to Use

### Method 1: Automated Script (Recommended)
```bash
./run_app.sh
```

### Method 2: Manual Execution
1. Activate the virtual environment:
```bash
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows
```

2. Run the application:
```bash
streamlit run app.py
```

3. Access the application in your browser (usually at http://localhost:8501)

### Method 3: Direct Execution
```bash
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```

## 📁 File Structure

```
tcc_streamlit/
├── app.py                          # Main Streamlit application
├── run_app.sh                      # Automated execution script
├── requirements.txt                # Python dependencies
├── README.md                       # Documentation
├── .streamlit/
│   └── config.toml                 # Dark theme configuration
├── dados/
│   └── data.csv                   # Main company dataset
├── modelos/
│   ├── Random_Forest_model.joblib # Trained model (Random Forest)
│   └── Random_Forest_model.pkl    # Alternative model format
└── pipeline/
    └── classification_pipeline.py # Classification pipeline
```

## 🔮 Prediction Features

### 🏢 Individual Prediction
- Selection of existing company in dataset
- Analysis based on real data
- Company information visualization
- Results with probability charts

### 📊 Form-Based Prediction (SPA)
- **Single Page Application** with interactive form
- Fields for all financial and macroeconomic indicators
- Real-time input validation
- Personalized analysis with detailed interpretation
- Prediction confidence levels

### 📋 Batch Prediction
- CSV file upload with multiple companies
- Data template available for download
- Automatic validation of required columns
- Bulk processing with consolidated statistics
- Complete results download

## 🔍 Advanced Insights Features

### 🌍 Geographic Analysis
- **Distribution by Countries**: Top 10 countries by number of companies and average potential
- **Detailed Analysis**: Consolidated metrics by country (mean, median, standard deviation)
- **Heat Map**: Visualization of potential distribution by country
- **Smart Filters**: Analysis only for countries with sufficient data

### 📊 Financial Analysis
- **Box Plots**: Distribution of capitalization and revenue by potential
- **Violin Plots**: P/E Ratio and Dividend Yield analysis by category
- **Detailed Statistics**: Consolidated financial metrics by potential
- **Comparisons**: Analysis between different potential levels

### 🔍 Correlation Analysis
- **Complete Matrix**: Correlations between all numeric variables
- **Specific Correlations**: Focus on correlations with growth potential
- **Potential Analysis**: Correlation matrices separated by potential level
- **Interactive Visualizations**: Colorful heatmaps and bar charts

### 📈 Trend Analysis
- **Scatter Plots**: Relationships between financial variables
- **Cluster Analysis**: Identification of company groups using K-means
- **Cluster Characteristics**: Detailed statistics by cluster
- **Data Filters**: Intelligent handling of negative values

### 🎯 Advanced Insights
- **Outlier Analysis**: Identification of companies with atypical characteristics
- **Recommendations**: Companies with upgrade potential based on similarity
- **Executive Summary**: Consolidated metrics and main insights
- **Performance Analysis**: Classification by characteristics (Small/Mid/Large Cap)

## 📊 Data Format

The main dataset (`data.csv`) should contain the following columns:
- `name`: Company name
- `country`: Country of origin
- `dividend_yield_ttm`: Dividend yield
- `earnings_ttm`: Earnings (TTM)
- `marketcap`: Market capitalization
- `pe_ratio_ttm`: P/E Ratio (TTM)
- `revenue_ttm`: Revenue (TTM)
- `price`: Stock price
- `gdp_per_capita_usd`: GDP per capita (USD)
- `gdp_growth_percent`: GDP growth (%)
- `inflation_percent`: Inflation rate (%)
- `interest_rate_percent`: Interest rate (%)
- `unemployment_rate_percent`: Unemployment rate (%)
- `exchange_rate_to_usd`: Exchange rate to USD
- `inflation`: Absolute inflation value (usually negative)
- `interest_rate`: Absolute interest rate value (usually negative)
- `unemployment`: Absolute unemployment rate value (usually negative)
- `pc_class`: Potential class (0=Low, 1=Medium, 2=High)

### 📊 Model Features (15 features)
The Random Forest model was trained with 15 features:
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

## 📊 Machine Learning Model

- **Algorithm**: Random Forest Classifier
- **Prediction Classes**:
  - 0: Low Growth Potential
  - 1: Medium Growth Potential  
  - 2: High Growth Potential
- **Features**: 15+ financial and macroeconomic indicators
- **Preprocessing**: Normalization and class balancing
- **Validation**: Cross-validation for robustness

## 🎨 Design and Interface

- **Theme**: Elegant dark with warm colors (orange, yellow, red)
- **Configuration**: Dark theme configured in `.streamlit/config.toml`
- **Typography**: Inter (Google Fonts) for better readability
- **Components**: Premium cards with smooth animations
- **Visualizations**: Plotly for interactive charts
- **Responsive**: Interface adaptable for different screen sizes

### 🎨 Theme Colors
- **Primary**: #FF6B35 (Hot orange)
- **Background**: #0E1117 (Dark)
- **Secondary Background**: #1E1E1E (Dark gray)
- **Text**: #FAFAFA (Light white)

## 🌐 GitHub Integration

This project is fully integrated with GitHub to facilitate use and distribution:

### 📥 Automatic Download
- **Data and Model**: Are automatically downloaded from GitHub when not available locally
- **Smart Cache**: Files are temporarily stored for 1 hour to avoid repeated downloads
- **Fallback**: If there's no GitHub connection, the app attempts to use local files
- **Real-time Status**: Interface shows data source (Local/GitHub) and connection status

### 🔗 Repository URLs
- **Repository**: https://github.com/sidnei-almeida/potencial_empresarial
- **Data**: https://raw.githubusercontent.com/sidnei-almeida/potencial_empresarial/main/dados/data.csv
- **Model**: https://raw.githubusercontent.com/sidnei-almeida/potencial_empresarial/main/modelos/Random_Forest_model.joblib

### 🚀 Simple Deploy
Now you can share only the `app.py` file and the app will work automatically, downloading all necessary resources from GitHub!

## 📝 Important Notes

- **Local Files**: If `data.csv` and `Random_Forest_model.joblib` files are present locally, they will be used
- **Automatic Download**: If not present, they will be automatically downloaded from GitHub
- **Connection**: Requires internet connection for initial resource download
- **Cache**: Downloaded files are temporarily stored for better performance
- The model was trained with preprocessed and normalized data
- The application automatically checks component availability
- All visualizations are optimized for dark theme

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests.

## 📄 License

This project is licensed under the MIT license - see the [LICENSE](LICENSE) file for details.

## 👥 Author

- Sidnei Almeida - Development