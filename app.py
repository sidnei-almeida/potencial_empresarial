import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import joblib
from streamlit_option_menu import option_menu
import warnings
import requests
import os
from pathlib import Path
import tempfile
warnings.filterwarnings('ignore')

# Configurações do GitHub
GITHUB_USERNAME = "sidnei-almeida"
GITHUB_REPO = "potencial_empresarial"
GITHUB_BRANCH = "main"
GITHUB_BASE_URL = f"https://raw.githubusercontent.com/{GITHUB_USERNAME}/{GITHUB_REPO}/{GITHUB_BRANCH}"

# URLs dos arquivos no GitHub
DATA_URL = f"{GITHUB_BASE_URL}/dados/data.csv"
MODEL_URL = f"{GITHUB_BASE_URL}/modelos/Random_Forest_model.joblib"

@st.cache_data
def download_file_from_github(url: str, filename: str) -> str:
    """
    Baixa um arquivo do GitHub e retorna o caminho local
    """
    try:
        # Criar diretório temporário se não existir
        temp_dir = Path(tempfile.gettempdir()) / "potencial_empresarial"
        temp_dir.mkdir(exist_ok=True)
        
        file_path = temp_dir / filename
        
        # Verificar se o arquivo já existe e é recente (cache de 1 hora)
        if file_path.exists():
            file_age = os.path.getmtime(file_path)
            current_time = os.path.getmtime(file_path)
            if (current_time - file_age) < 3600:  # 1 hora em segundos
                return str(file_path)
        
        # Baixar arquivo do GitHub
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        # Salvar arquivo
        with open(file_path, 'wb') as f:
            f.write(response.content)
        
        return str(file_path)
        
    except Exception as e:
        st.error(f"Erro ao baixar {filename} do GitHub: {str(e)}")
        return None

@st.cache_data
def check_github_connection():
    """Verifica se a conexão com o GitHub está funcionando"""
    try:
        response = requests.get(f"https://github.com/{GITHUB_USERNAME}/{GITHUB_REPO}", timeout=10)
        return response.status_code == 200
    except:
        return False

# Configuração da página
st.set_page_config(
    page_title="Potencial de Crescimento Empresarial",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado para tema escuro elegante com cores quentes
st.markdown("""
<style>
    /* Importar fontes elegantes */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Variáveis de cores premium - PALETA QUENTE */
    :root {
        --primary-color: #FF6B35;
        --secondary-color: #F7931E;
        --accent-color: #FFD23F;
        --success-color: #FF8C42;
        --warning-color: #FF6B6B;
        --dark-bg: #0E1117;
        --card-bg: #1E1E1E;
        --text-primary: #FAFAFA;
        --text-secondary: #B0B0B0;
        --gradient-primary: linear-gradient(135deg, #FF6B35 0%, #F7931E 100%);
        --gradient-secondary: linear-gradient(135deg, #FFD23F 0%, #FF8C42 100%);
        --gradient-dark: linear-gradient(135deg, #1E1E1E 0%, #2D2D2D 100%);
        --shadow-soft: 0 8px 32px rgba(255, 107, 53, 0.3);
        --shadow-hover: 0 12px 40px rgba(255, 107, 53, 0.4);
    }
    
    /* Estilo global */
    .stApp {
        background: var(--dark-bg);
        color: var(--text-primary);
    }
    
    /* Ajustar o container principal para usar toda a largura */
    .main .block-container {
        max-width: none !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }
    
    /* Header principal */
    .main-header {
        font-family: 'Inter', sans-serif;
        font-size: 2.5rem;
        font-weight: 700;
        background: var(--gradient-primary);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin-bottom: 1.5rem;
        text-shadow: 0 4px 8px rgba(255, 107, 53, 0.3);
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
    }
    
    /* Cards de métricas premium */
    .metric-card {
        background: var(--gradient-dark);
        padding: 1rem;
        border-radius: 12px;
        color: var(--text-primary);
        text-align: center;
        margin: 0.3rem 0;
        border: 1px solid rgba(255, 107, 53, 0.2);
        box-shadow: var(--shadow-soft);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: var(--gradient-primary);
    }
    
    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: var(--shadow-hover);
        border-color: var(--primary-color);
    }
    
    /* Cards de informação */
    .info-box {
        background: var(--card-bg);
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid var(--primary-color);
        margin: 1rem 0;
        box-shadow: var(--shadow-soft);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .success-box {
        background: linear-gradient(135deg, rgba(255, 107, 53, 0.1) 0%, rgba(247, 147, 30, 0.1) 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid var(--primary-color);
        margin: 1rem 0;
        box-shadow: var(--shadow-soft);
        border: 1px solid rgba(255, 107, 53, 0.3);
    }
    
    .warning-box {
        background: linear-gradient(135deg, rgba(255, 139, 66, 0.1) 0%, rgba(255, 107, 107, 0.1) 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid var(--warning-color);
        margin: 1rem 0;
        box-shadow: var(--shadow-soft);
        border: 1px solid rgba(255, 107, 107, 0.3);
    }
    
    /* Botões premium */
    .stButton > button {
        background: var(--gradient-primary);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: var(--shadow-soft);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-hover);
    }
    
    /* Sidebar elegante */
    .css-1d391kg {
        background: var(--card-bg);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Títulos elegantes */
    h1, h2, h3, h4, h5, h6 {
        color: var(--text-primary);
        font-family: 'Inter', sans-serif;
        font-weight: 600;
    }
    
    /* Texto secundário */
    .text-secondary {
        color: var(--text-secondary);
    }
    
    /* Cards de dados */
    .data-card {
        background: var(--card-bg);
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        box-shadow: var(--shadow-soft);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Animações suaves */
    .fade-in {
        animation: fadeIn 0.6s ease-in;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Scrollbar personalizada */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--dark-bg);
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--primary-color);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--secondary-color);
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Carrega os dados das empresas do GitHub ou localmente"""
    try:
        df = None
        
        # Tentar carregar localmente primeiro
        try:
            if os.path.exists('dados/data.csv'):
                df = pd.read_csv('dados/data.csv')
                st.info("📁 Dados carregados localmente")
            else:
                # Baixar do GitHub
                st.info("🌐 Baixando dados do GitHub...")
                data_path = download_file_from_github(DATA_URL, "data.csv")
                if data_path:
                    df = pd.read_csv(data_path)
                    st.success("✅ Dados baixados com sucesso do GitHub")
                else:
                    st.error("❌ Erro ao baixar dados do GitHub")
                    return None, None
        except Exception as e:
            st.error(f"Erro ao carregar dados: {e}")
            return None, None
        
        return df, None  # Sempre retorna None para df_potencial pois não é mais usado
        
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        return None, None

@st.cache_resource
def load_model():
    """Carrega o modelo treinado do GitHub ou localmente"""
    try:
        model = None
        
        # Tentar carregar localmente primeiro
        if os.path.exists('modelos/Random_Forest_model.joblib'):
            model = joblib.load('modelos/Random_Forest_model.joblib')
            st.info("📁 Modelo carregado localmente")
        else:
            # Baixar do GitHub
            st.info("🌐 Baixando modelo do GitHub...")
            model_path = download_file_from_github(MODEL_URL, "Random_Forest_model.joblib")
            if model_path:
                model = joblib.load(model_path)
                st.success("✅ Modelo baixado com sucesso do GitHub")
            else:
                st.error("❌ Erro ao baixar modelo do GitHub")
                return None
        
        return model
        
    except Exception as e:
        st.error(f"Erro ao carregar modelo: {e}")
        return None

def show_system_status(model, df):
    """Mostra o status dos componentes do sistema"""
    
    # Status do Modelo
    model_status = "✅ Carregado" if model is not None else "❌ Erro"
    model_color = "#FF6B35" if model is not None else "#FF6B6B"
    model_source = "Local" if os.path.exists('modelos/Random_Forest_model.joblib') else "GitHub"
    
    st.markdown(f"""
    <div style="background: rgba(255, 107, 53, 0.1); padding: 0.8rem; border-radius: 8px; margin-bottom: 0.5rem; border-left: 3px solid {model_color};">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <span style="color: #FAFAFA; font-weight: 600;">🤖 Modelo Random Forest ({model_source})</span>
            <span style="color: {model_color}; font-weight: 700;">{model_status}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Status dos Dados
    data_status = "✅ Carregado" if df is not None else "❌ Erro"
    data_color = "#FF6B35" if df is not None else "#FF6B6B"
    data_source = "Local" if os.path.exists('dados/data.csv') else "GitHub"
    
    st.markdown(f"""
    <div style="background: rgba(255, 107, 53, 0.1); padding: 0.8rem; border-radius: 8px; margin-bottom: 0.5rem; border-left: 3px solid {data_color};">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <span style="color: #FAFAFA; font-weight: 600;">📊 Dataset Empresas ({data_source})</span>
            <span style="color: {data_color}; font-weight: 700;">{data_status}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Status da Conexão GitHub
    github_status = "✅ Conectado" if check_github_connection() else "⚠️ Sem conexão"
    github_color = "#FF6B35" if check_github_connection() else "#FFD23F"
    
    st.markdown(f"""
    <div style="background: rgba(255, 107, 53, 0.1); padding: 0.8rem; border-radius: 8px; margin-bottom: 0.5rem; border-left: 3px solid {github_color};">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <span style="color: #FAFAFA; font-weight: 600;">🌐 GitHub Connection</span>
            <span style="color: {github_color}; font-weight: 700;">{github_status}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

def show_project_info(df):
    """Mostra informações do projeto"""
    
    if df is not None:
        # Total de empresas
        st.markdown(f"""
        <div style="background: rgba(255, 107, 53, 0.1); padding: 0.8rem; border-radius: 8px; margin-bottom: 0.5rem; border-left: 3px solid #FF6B35;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="color: #FAFAFA; font-weight: 600;">🏢 Total de Empresas</span>
                <span style="color: #FF6B35; font-weight: 700;">{len(df):,}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Países únicos
        st.markdown(f"""
        <div style="background: rgba(255, 107, 53, 0.1); padding: 0.8rem; border-radius: 8px; margin-bottom: 0.5rem; border-left: 3px solid #FF6B35;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="color: #FAFAFA; font-weight: 600;">🌍 Países</span>
                <span style="color: #FF6B35; font-weight: 700;">{df['country'].nunique()}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

def main():
    # Título principal com design premium
    st.markdown('<h1 class="main-header fade-in">🚀 Potencial de Crescimento Empresarial</h1>', unsafe_allow_html=True)
    st.markdown('<p class="text-secondary" style="text-align: center; font-size: 1.2rem; margin-bottom: 3rem;">Análise Inteligente de Potencial de Crescimento usando Machine Learning</p>', unsafe_allow_html=True)
    
    # Carregar dados e modelo
    df, df_potencial = load_data()
    model = load_model()
    
    if df is None:
        st.error("Não foi possível carregar os dados. Verifique se os arquivos estão no local correto.")
        return
    
    # Menu de navegação premium com streamlit-option-menu
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; margin-bottom: 2rem;">
            <h2 style="color: #FF6B35; font-family: 'Inter', sans-serif; font-weight: 700;">🎯 Navegação</h2>
        </div>
        """, unsafe_allow_html=True)
        
        selected = option_menu(
            menu_title=None,
            options=["Início", "Análise de Dados", "Modelo", "Predições", "Insights"],
            icons=["house", "bar-chart", "cpu", "magic", "lightbulb"],
            menu_icon="cast",
            default_index=0,
            styles={
                "container": {"padding": "0!important", "background-color": "transparent"},
                "icon": {"color": "#FF6B35", "font-size": "20px"},
                "nav-link": {
                    "font-size": "16px",
                    "text-align": "left",
                    "margin": "0px",
                    "--hover-color": "#1E1E1E",
                    "color": "#B0B0B0",
                    "font-family": "'Inter', sans-serif",
                    "font-weight": "500",
                },
                "nav-link-selected": {
                    "background-color": "rgba(255, 107, 53, 0.1)",
                    "color": "#FF6B35",
                    "border-left": "4px solid #FF6B35",
                    "border-radius": "8px",
                },
            }
        )
        
        # Separador
        st.markdown("---")
        
        # Status do Sistema
        st.markdown("""
        <div style="margin-bottom: 1.5rem;">
            <h3 style="color: #FF6B35; font-family: 'Inter', sans-serif; font-weight: 600; margin-bottom: 1rem;">📊 Status do Sistema</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Status dos Componentes
        show_system_status(model, df)
        
        # Separador
        st.markdown("---")
        
        # Informações do Projeto
        st.markdown("""
        <div style="margin-bottom: 1.5rem;">
            <h3 style="color: #FF6B35; font-family: 'Inter', sans-serif; font-weight: 600; margin-bottom: 1rem;">ℹ️ Informações</h3>
        </div>
        """, unsafe_allow_html=True)
        
        show_project_info(df)
    
    # Navegação baseada na seleção
    if selected == "Início":
        show_home_page(df, df_potencial, model)
    elif selected == "Análise de Dados":
        show_data_analysis(df)
    elif selected == "Modelo":
        show_model_info(model)
    elif selected == "Predições":
        show_predictions_interface(df, model)
    elif selected == "Insights":
        show_insights(df, df_potencial)

def show_home_page(df, df_potencial, model):
    """Página inicial com visão geral premium"""
    st.markdown('<h2 style="color: #FF6B35; font-family: \'Inter\', sans-serif; font-weight: 600; margin-bottom: 2rem;">🎯 Visão Geral do Projeto</h2>', unsafe_allow_html=True)
    
    # Cards de métricas premium
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Distribuição por potencial de crescimento
        if 'pc_class' in df.columns:
            high_potential = len(df[df['pc_class'] == 2])
            total_companies = len(df)
            high_potential_pct = (high_potential / total_companies) * 100
            
            st.markdown(f'''
            <div class="fade-in" style="background: linear-gradient(90deg, #FF6B35 {high_potential_pct}%, rgba(255, 107, 53, 0.1) {high_potential_pct}%); border-radius: 6px; padding: 0.6rem; margin: 0.3rem 0; border: 1px solid rgba(255, 107, 53, 0.3); box-shadow: 0 3px 12px rgba(0, 0, 0, 0.3);">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.25rem;">
                    <span style="color: #FFFFFF; font-weight: 600; font-size: 0.75rem; text-shadow: 0 1px 3px rgba(0,0,0,0.8);">🚀 Alto Potencial</span>
                    <span style="color: #FFFFFF; font-weight: 700; font-size: 0.8rem; text-shadow: 0 1px 3px rgba(0,0,0,0.8);">{high_potential:,}</span>
                </div>
                <div style="background: rgba(255, 255, 255, 0.3); border-radius: 3px; height: 2px; margin: 0.25rem 0;">
                    <div style="background: rgba(255, 255, 255, 0.6); height: 100%; width: 100%; border-radius: 3px;"></div>
                </div>
                <p style="color: #FFFFFF; margin-top: 0.25rem; font-size: 0.65rem; margin: 0; text-shadow: 0 1px 3px rgba(0,0,0,0.8);">Empresas com alto potencial de crescimento</p>
            </div>
            ''', unsafe_allow_html=True)
    
    with col2:
        # Média de capitalização de mercado
        avg_market_cap = df['marketcap'].mean() / 1e9  # Em bilhões
        avg_market_cap_pct = min(avg_market_cap / 10, 100)  # Normalizar para 0-100%
        
        st.markdown(f'''
        <div class="fade-in" style="background: linear-gradient(90deg, #F7931E {avg_market_cap_pct}%, rgba(247, 147, 30, 0.1) {avg_market_cap_pct}%); border-radius: 6px; padding: 0.6rem; margin: 0.3rem 0; border: 1px solid rgba(247, 147, 30, 0.3); box-shadow: 0 3px 12px rgba(0, 0, 0, 0.3);">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.25rem;">
                <span style="color: #FFFFFF; font-weight: 600; font-size: 0.75rem; text-shadow: 0 1px 3px rgba(0,0,0,0.8);">💰 Cap. Média</span>
                <span style="color: #FFFFFF; font-weight: 700; font-size: 0.8rem; text-shadow: 0 1px 3px rgba(0,0,0,0.8);">${avg_market_cap:.1f}B</span>
            </div>
            <div style="background: rgba(255, 255, 255, 0.3); border-radius: 3px; height: 2px; margin: 0.25rem 0;">
                <div style="background: rgba(255, 255, 255, 0.6); height: 100%; width: 100%; border-radius: 3px;"></div>
            </div>
            <p style="color: #FFFFFF; margin-top: 0.25rem; font-size: 0.65rem; margin: 0; text-shadow: 0 1px 3px rgba(0,0,0,0.8);">Capitalização média de mercado</p>
        </div>
        ''', unsafe_allow_html=True)
    
    with col3:
        # Diversidade geográfica
        countries_count = df['country'].nunique()
        countries_pct = min((countries_count / 50) * 100, 100)  # Normalizar para 0-100%
        
        st.markdown(f'''
        <div class="fade-in" style="background: linear-gradient(90deg, #FFD23F {countries_pct}%, rgba(255, 210, 63, 0.1) {countries_pct}%); border-radius: 6px; padding: 0.6rem; margin: 0.3rem 0; border: 1px solid rgba(255, 210, 63, 0.3); box-shadow: 0 3px 12px rgba(0, 0, 0, 0.3);">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.25rem;">
                <span style="color: #FFFFFF; font-weight: 600; font-size: 0.75rem; text-shadow: 0 1px 3px rgba(0,0,0,0.8);">🌍 Países</span>
                <span style="color: #FFFFFF; font-weight: 700; font-size: 0.8rem; text-shadow: 0 1px 3px rgba(0,0,0,0.8);">{countries_count}</span>
            </div>
            <div style="background: rgba(255, 255, 255, 0.3); border-radius: 3px; height: 2px; margin: 0.25rem 0;">
                <div style="background: rgba(255, 255, 255, 0.6); height: 100%; width: 100%; border-radius: 3px;"></div>
            </div>
            <p style="color: #FFFFFF; margin-top: 0.25rem; font-size: 0.65rem; margin: 0; text-shadow: 0 1px 3px rgba(0,0,0,0.8);">Diversidade geográfica</p>
        </div>
        ''', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Descrição do projeto com design premium
    st.markdown('<h2 style="color: #FF6B35; font-family: \'Inter\', sans-serif; font-weight: 600; margin-bottom: 0.8rem; font-size: 1.1rem;">📝 Sobre o Projeto</h2>', unsafe_allow_html=True)
    st.markdown("""
    <div class="info-box">
        <p style="font-size: 0.75rem; line-height: 1.4; margin: 0;">
            Este projeto implementa um <strong>sistema de análise de potencial de crescimento empresarial</strong> utilizando 
            <strong>Machine Learning</strong> com Random Forest. O objetivo é classificar empresas em diferentes níveis de 
            potencial de crescimento baseado em indicadores financeiros e econômicos.
        </p>
        <p style="font-size: 0.7rem; line-height: 1.4; margin: 0.5rem 0 0 0; color: #B0B0B0;">
            <strong>🌐 Fonte dos Dados:</strong> Os dados e modelo são carregados automaticamente do GitHub 
            (<a href="https://github.com/sidnei-almeida/potencial_empresarial" target="_blank" style="color: #FF6B35;">sidnei-almeida/potencial_empresarial</a>) 
            quando não estão disponíveis localmente.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Características principais com cards premium
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="data-card">
            <h3 style="color: #FF6B35; font-family: 'Inter', sans-serif; font-weight: 600; margin-bottom: 0.6rem; font-size: 0.95rem;">🔧 Características Técnicas</h3>
            <ul style="color: #FAFAFA; line-height: 1.4; margin: 0; font-size: 0.75rem;">
                <li><strong>Algoritmo</strong>: Random Forest</li>
                <li><strong>Features</strong>: 15+ indicadores financeiros</li>
                <li><strong>Classes</strong>: Baixo, Médio, Alto Potencial</li>
                <li><strong>Países</strong>: Análise internacional</li>
                <li><strong>Preprocessamento</strong>: Normalização e balanceamento</li>
                <li><strong>Validação</strong>: Cross-validation</li>
                <li><strong>Métricas</strong>: Accuracy, Precision, Recall</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="data-card">
            <h3 style="color: #FF6B35; font-family: 'Inter', sans-serif; font-weight: 600; margin-bottom: 0.6rem; font-size: 0.95rem;">📊 Indicadores Analisados</h3>
            <ul style="color: #FAFAFA; line-height: 1.4; margin: 0; font-size: 0.75rem;">
                <li><strong>Financeiros</strong>: Receita, Lucros, P/E Ratio</li>
                <li><strong>Mercado</strong>: Capitalização, Dividend Yield</li>
                <li><strong>Macroeconômicos</strong>: PIB, Inflação, Taxa de Juros</li>
                <li><strong>Social</strong>: Taxa de Desemprego</li>
                <li><strong>Cambial</strong>: Taxa de Câmbio</li>
                <li><strong>Geográfico</strong>: País de origem</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

def show_data_analysis(df):
    """Análise detalhada dos dados"""
    st.markdown('<h2 style="color: #FF6B35; font-family: \'Inter\', sans-serif; font-weight: 600; margin-bottom: 2rem;">📊 Análise dos Dados</h2>', unsafe_allow_html=True)
    
    # Estatísticas gerais
    st.markdown("### 📈 Estatísticas Gerais")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total de Empresas", f"{len(df):,}")
    with col2:
        st.metric("Países Diferentes", f"{df['country'].nunique()}")
    with col3:
        st.metric("Capitalização Média", f"${df['marketcap'].mean()/1e9:.1f}B")
    with col4:
        if 'pc_class' in df.columns:
            st.metric("Alto Potencial", f"{len(df[df['pc_class'] == 2]):,}")
    
    # Distribuição por país
    st.markdown("### 🌍 Distribuição por País")
    
    country_counts = df['country'].value_counts().head(10)
    
    fig = px.bar(
        x=country_counts.values,
        y=country_counts.index,
        orientation='h',
        title="Top 10 Países por Número de Empresas",
        color=country_counts.values,
        color_continuous_scale='Oranges'
    )
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#FAFAFA',
        yaxis=dict(autorange="reversed")
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Distribuição de potencial se disponível
    if 'pc_class' in df.columns:
        st.markdown("### 🎯 Distribuição de Potencial de Crescimento")
        
        potential_counts = df['pc_class'].value_counts().sort_index()
        potential_labels = {0: 'Baixo', 1: 'Médio', 2: 'Alto'}
        potential_names = [potential_labels[i] for i in potential_counts.index]
        
        fig = px.pie(
            values=potential_counts.values,
            names=potential_names,
            title="Distribuição de Potencial de Crescimento",
            color_discrete_sequence=['#FF6B35', '#F7931E', '#FFD23F']
        )
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#FAFAFA'
        )
        
        st.plotly_chart(fig, use_container_width=True)

def show_model_info(model):
    """Informações sobre o modelo"""
    st.markdown('<h2 style="color: #FF6B35; font-family: \'Inter\', sans-serif; font-weight: 600; margin-bottom: 2rem;">🤖 Informações do Modelo</h2>', unsafe_allow_html=True)
    
    if model is not None:
        st.markdown("### 🔧 Parâmetros do Modelo")
        
        params = model.get_params()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🌳 Random Forest")
            st.json({
                "Número de Árvores": params.get('n_estimators', 'N/A'),
                "Profundidade Máxima": params.get('max_depth', 'N/A'),
                "Amostras Mínimas por Folha": params.get('min_samples_leaf', 'N/A'),
                "Amostras Mínimas para Divisão": params.get('min_samples_split', 'N/A'),
                "Bootstrap": params.get('bootstrap', 'N/A'),
                "Random State": params.get('random_state', 'N/A')
            })
        
        with col2:
            st.markdown("#### 📊 Importância das Features")
            if hasattr(model, 'feature_importances_'):
                # Carregar dados para obter nomes das features
                df, _ = load_data()
                if df is not None:
                    feature_names = [col for col in df.columns if col not in ['name', 'country', 'pc_class']]
                    
                    if len(feature_names) == len(model.feature_importances_):
                        importance_df = pd.DataFrame({
                            'Feature': feature_names,
                            'Importance': model.feature_importances_
                        }).sort_values('Importance', ascending=False)
                        
                        st.dataframe(importance_df.head(10), use_container_width=True)
    else:
        st.error("Modelo não carregado. Verifique se o arquivo do modelo existe.")

def show_predictions_interface(df, model):
    """Interface para predições - SPA com abas para predição individual e batch"""
    st.markdown('<h2 style="color: #FF6B35; font-family: \'Inter\', sans-serif; font-weight: 600; margin-bottom: 2rem;">🔮 Interface de Predições</h2>', unsafe_allow_html=True)
    
    if model is None:
        st.error("Modelo não carregado. Não é possível fazer predições.")
        return
    
    # Criar abas para diferentes tipos de predição
    tab1, tab2, tab3 = st.tabs(["🏢 Predição Individual", "📊 Predição por Campos", "📋 Predição em Lote"])
    
    with tab1:
        show_company_prediction(df, model)
    
    with tab2:
        show_manual_prediction(model)
    
    with tab3:
        show_batch_prediction(df, model)

def show_company_prediction(df, model):
    """Predição baseada em empresa existente no dataset"""
    st.markdown("### 🏢 Selecionar Empresa para Análise")
    
    # Filtrar por país
    countries = df['country'].unique()
    selected_country = st.selectbox("Selecionar País:", countries, key="country_select")
    
    # Filtrar empresas por país
    df_filtered = df[df['country'] == selected_country]
    
    if len(df_filtered) > 0:
        # Selecionar empresa
        company_names = df_filtered['name'].tolist()
        selected_company = st.selectbox("Selecionar Empresa:", company_names, key="company_select")
        
        if selected_company:
            # Obter dados da empresa selecionada
            company_data = df_filtered[df_filtered['name'] == selected_company].iloc[0]
            
            # Mostrar informações da empresa
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 📊 Informações da Empresa")
                st.markdown(f"""
                <div class="info-box">
                    <p><strong>Nome:</strong> {selected_company}</p>
                    <p><strong>País:</strong> {selected_country}</p>
                    <p><strong>Capitalização:</strong> ${company_data['marketcap']/1e9:.2f}B</p>
                    <p><strong>Receita TTM:</strong> ${company_data['revenue_ttm']/1e6:.2f}M</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                # Preparar features para predição
                feature_cols = [col for col in df.columns if col not in ['name', 'country', 'pc_class']]
                X_company = company_data[feature_cols].values.reshape(1, -1)
                
                # Fazer predição
                if st.button("🔍 Analisar Potencial", type="primary", key="analyze_company"):
                    with st.spinner("Analisando..."):
                        prediction = model.predict(X_company)[0]
                        probabilities = model.predict_proba(X_company)[0]
                        
                        # Mapear predição para rótulo
                        potential_labels = {0: 'Baixo', 1: 'Médio', 2: 'Alto'}
                        predicted_label = potential_labels[prediction]
                        
                        # Cores baseadas na predição
                        colors = {'Baixo': '#FF6B6B', 'Médio': '#F7931E', 'Alto': '#FFD23F'}
                        color = colors[predicted_label]
                        
                        # Mostrar resultado
                        st.markdown(f'''
                        <h3 style="color: {color}; font-family: 'Inter', sans-serif; font-weight: 600; margin-bottom: 0.6rem;">🎯 Potencial: {predicted_label}</h3>
                        <div style="background: {color}; border-radius: 8px; padding: 0.6rem; margin: 0.3rem 0; border: 1px solid {color};">
                            <p style="color: #FFFFFF; font-size: 0.75rem; margin: 0; text-shadow: 0 1px 3px rgba(0,0,0,0.8);">
                                Confiança: {probabilities[prediction]:.1%}<br>
                                Empresa: {selected_company}
                            </p>
                        </div>
                        ''', unsafe_allow_html=True)
                        
                        # Gráfico de probabilidades
                        prob_df = pd.DataFrame({
                            'Potencial': ['Baixo', 'Médio', 'Alto'],
                            'Probabilidade': probabilities
                        })
                        
                        fig = px.bar(
                            prob_df,
                            x='Potencial',
                            y='Probabilidade',
                            title='Probabilidades de Classificação',
                            color='Probabilidade',
                            color_continuous_scale='Oranges'
                        )
                        
                        fig.update_layout(
                            plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(0,0,0,0)',
                            font_color='#FAFAFA'
                        )
                        
                        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning(f"Nenhuma empresa encontrada para o país {selected_country}")

def show_manual_prediction(model):
    """Predição manual baseada em campos de entrada (SPA)"""
    st.markdown("### 📊 Análise Personalizada")
    st.markdown("Digite os valores dos indicadores financeiros e macroeconômicos para análise:")
    
    # Criar formulário com campos de entrada
    with st.form("prediction_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 💰 Indicadores Financeiros")
            dividend_yield = st.number_input(
                "Dividend Yield (%)",
                min_value=0.0,
                max_value=50.0,
                value=2.5,
                step=0.1,
                help="Rendimento de dividendos em porcentagem"
            )
            
            earnings_ttm = st.number_input(
                "Earnings TTM (USD)",
                min_value=-1e12,
                max_value=1e12,
                value=1000000.0,
                step=100000.0,
                format="%.0f",
                help="Lucros dos últimos 12 meses"
            )
            
            marketcap = st.number_input(
                "Market Cap (USD)",
                min_value=1000.0,
                max_value=5e12,
                value=1000000000.0,
                step=10000000.0,
                format="%.0f",
                help="Capitalização de mercado"
            )
            
            pe_ratio = st.number_input(
                "P/E Ratio",
                min_value=-100.0,
                max_value=1000.0,
                value=15.0,
                step=0.1,
                help="Relação Preço/Lucro"
            )
            
            revenue_ttm = st.number_input(
                "Revenue TTM (USD)",
                min_value=0.0,
                max_value=1e13,
                value=5000000000.0,
                step=100000000.0,
                format="%.0f",
                help="Receita dos últimos 12 meses"
            )
            
            price = st.number_input(
                "Stock Price (USD)",
                min_value=0.01,
                max_value=10000.0,
                value=50.0,
                step=0.01,
                help="Preço da ação"
            )
        
        with col2:
            st.markdown("#### 🌍 Indicadores Macroeconômicos")
            gdp_per_capita = st.number_input(
                "GDP per Capita (USD)",
                min_value=100.0,
                max_value=200000.0,
                value=50000.0,
                step=100.0,
                help="PIB per capita"
            )
            
            gdp_growth = st.number_input(
                "GDP Growth (%)",
                min_value=-20.0,
                max_value=20.0,
                value=2.5,
                step=0.1,
                help="Crescimento do PIB"
            )
            
            inflation_percent = st.number_input(
                "Inflation (%)",
                min_value=-10.0,
                max_value=100.0,
                value=2.5,
                step=0.1,
                help="Taxa de inflação"
            )
            
            interest_rate_percent = st.number_input(
                "Interest Rate (%)",
                min_value=-10.0,
                max_value=50.0,
                value=4.875,
                step=0.1,
                help="Taxa de juros"
            )
            
            unemployment_rate_percent = st.number_input(
                "Unemployment Rate (%)",
                min_value=0.0,
                max_value=50.0,
                value=3.7,
                step=0.1,
                help="Taxa de desemprego"
            )
            
            exchange_rate = st.number_input(
                "Exchange Rate to USD",
                min_value=0.001,
                max_value=10000.0,
                value=1.0,
                step=0.01,
                help="Taxa de câmbio para USD"
            )
            
            # Features adicionais necessárias para o modelo
            st.markdown("#### 📊 Indicadores Adicionais")
            inflation = st.number_input(
                "Inflation (Valor Absoluto)",
                min_value=-10.0,
                max_value=100.0,
                value=-2.5,
                step=0.1,
                help="Valor absoluto da inflação (geralmente negativo)"
            )
            
            interest_rate = st.number_input(
                "Interest Rate (Valor Absoluto)",
                min_value=-50.0,
                max_value=50.0,
                value=-4.875,
                step=0.1,
                help="Valor absoluto da taxa de juros (geralmente negativo)"
            )
            
            unemployment = st.number_input(
                "Unemployment (Valor Absoluto)",
                min_value=-50.0,
                max_value=50.0,
                value=-3.7,
                step=0.1,
                help="Valor absoluto da taxa de desemprego (geralmente negativo)"
            )
        
        # Botão de submissão
        submitted = st.form_submit_button("🔍 Analisar Potencial", type="primary")
        
        if submitted:
            # Preparar dados para predição (15 features na ordem correta)
            input_data = np.array([[
                dividend_yield, earnings_ttm, marketcap, pe_ratio, revenue_ttm, price,
                gdp_per_capita, gdp_growth, inflation_percent, interest_rate_percent, 
                unemployment_rate_percent, exchange_rate, inflation, interest_rate, unemployment
            ]])
            
            with st.spinner("Analisando..."):
                prediction = model.predict(input_data)[0]
                probabilities = model.predict_proba(input_data)[0]
                
                # Mapear predição para rótulo
                potential_labels = {0: 'Baixo', 1: 'Médio', 2: 'Alto'}
                predicted_label = potential_labels[prediction]
                
                # Cores baseadas na predição
                colors = {'Baixo': '#FF6B6B', 'Médio': '#F7931E', 'Alto': '#FFD23F'}
                color = colors[predicted_label]
                
                # Mostrar resultado
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f'''
                    <h3 style="color: {color}; font-family: 'Inter', sans-serif; font-weight: 600; margin-bottom: 0.6rem;">🎯 Potencial: {predicted_label}</h3>
                    <div style="background: {color}; border-radius: 8px; padding: 0.6rem; margin: 0.3rem 0; border: 1px solid {color};">
                        <p style="color: #FFFFFF; font-size: 0.75rem; margin: 0; text-shadow: 0 1px 3px rgba(0,0,0,0.8);">
                            Confiança: {probabilities[prediction]:.1%}<br>
                            Análise Personalizada
                        </p>
                    </div>
                    ''', unsafe_allow_html=True)
                
                with col2:
                    # Gráfico de probabilidades
                    prob_df = pd.DataFrame({
                        'Potencial': ['Baixo', 'Médio', 'Alto'],
                        'Probabilidade': probabilities
                    })
                    
                    fig = px.bar(
                        prob_df,
                        x='Potencial',
                        y='Probabilidade',
                        title='Probabilidades de Classificação',
                        color='Probabilidade',
                        color_continuous_scale='Oranges'
                    )
                    
                    fig.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font_color='#FAFAFA'
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                
                # Mostrar interpretação dos resultados
                show_prediction_interpretation(predicted_label, probabilities[prediction])

def show_batch_prediction(df, model):
    """Predição em lote via upload de arquivo CSV"""
    st.markdown("### 📋 Predição em Lote")
    st.markdown("Faça upload de um arquivo CSV com dados de empresas para análise em massa:")
    
    # Template para download
    st.markdown("#### 📄 Template de Dados")
    st.markdown("Baixe o template abaixo para ver o formato esperado dos dados:")
    
    # Criar template
    template_data = {
        'name': ['Empresa Exemplo 1', 'Empresa Exemplo 2'],
        'country': ['United States', 'Brazil'],
        'dividend_yield_ttm': [2.5, 3.0],
        'earnings_ttm': [1000000.0, 2000000.0],
        'marketcap': [1000000000.0, 2000000000.0],
        'pe_ratio_ttm': [15.0, 12.0],
        'revenue_ttm': [5000000000.0, 8000000000.0],
        'price': [50.0, 75.0],
        'gdp_per_capita_usd': [50000.0, 10000.0],
        'gdp_growth_percent': [2.5, 1.7],
        'inflation_percent': [2.5, 4.83],
        'interest_rate_percent': [4.875, 12.25],
        'unemployment_rate_percent': [3.7, 6.2],
        'exchange_rate_to_usd': [1.0, 6.18],
        'inflation': [-2.5, -4.83],
        'interest_rate': [-4.875, -12.25],
        'unemployment': [-3.7, -6.2]
    }
    
    template_df = pd.DataFrame(template_data)
    
    # Botão para download do template
    csv_template = template_df.to_csv(index=False)
    st.download_button(
        label="📥 Baixar Template CSV",
        data=csv_template,
        file_name="template_empresas.csv",
        mime="text/csv"
    )
    
    # Upload de arquivo
    uploaded_file = st.file_uploader(
        "Escolha um arquivo CSV:",
        type="csv",
        help="Upload um arquivo CSV com dados das empresas seguindo o template"
    )
    
    if uploaded_file is not None:
        try:
            # Ler arquivo
            batch_df = pd.read_csv(uploaded_file)
            
            # Validar colunas necessárias (15 features)
            required_cols = [
                'dividend_yield_ttm', 'earnings_ttm', 'marketcap', 'pe_ratio_ttm',
                'revenue_ttm', 'price', 'gdp_per_capita_usd', 'gdp_growth_percent',
                'inflation_percent', 'interest_rate_percent', 'unemployment_rate_percent',
                'exchange_rate_to_usd', 'inflation', 'interest_rate', 'unemployment'
            ]
            
            missing_cols = [col for col in required_cols if col not in batch_df.columns]
            
            if missing_cols:
                st.error(f"Colunas obrigatórias ausentes: {', '.join(missing_cols)}")
            else:
                st.success(f"✅ Arquivo carregado com sucesso! {len(batch_df)} empresas encontradas.")
                
                # Mostrar preview dos dados
                st.markdown("#### 👀 Preview dos Dados")
                st.dataframe(batch_df.head(), use_container_width=True)
                
                # Botão para processar
                if st.button("🚀 Processar Predições", type="primary"):
                    with st.spinner("Processando predições..."):
                        # Preparar dados para predição
                        feature_cols = required_cols
                        X_batch = batch_df[feature_cols].values
                        
                        # Fazer predições
                        predictions = model.predict(X_batch)
                        probabilities = model.predict_proba(X_batch)
                        
                        # Mapear predições
                        potential_labels = {0: 'Baixo', 1: 'Médio', 2: 'Alto'}
                        predicted_labels = [potential_labels[p] for p in predictions]
                        
                        # Criar DataFrame com resultados
                        results_df = batch_df.copy()
                        results_df['predicted_class'] = predictions
                        results_df['predicted_potential'] = predicted_labels
                        results_df['confidence'] = [probabilities[i][predictions[i]] for i in range(len(predictions))]
                        
                        # Adicionar probabilidades individuais
                        results_df['prob_baixo'] = probabilities[:, 0]
                        results_df['prob_medio'] = probabilities[:, 1]
                        results_df['prob_alto'] = probabilities[:, 2]
                        
                        # Mostrar resultados
                        st.markdown("#### 📊 Resultados das Predições")
                        
                        # Estatísticas gerais
                        col1, col2, col3, col4 = st.columns(4)
                        
                        with col1:
                            st.metric("Total de Empresas", len(results_df))
                        
                        with col2:
                            high_potential = len(results_df[results_df['predicted_potential'] == 'Alto'])
                            st.metric("Alto Potencial", high_potential)
                        
                        with col3:
                            medium_potential = len(results_df[results_df['predicted_potential'] == 'Médio'])
                            st.metric("Médio Potencial", medium_potential)
                        
                        with col4:
                            low_potential = len(results_df[results_df['predicted_potential'] == 'Baixo'])
                            st.metric("Baixo Potencial", low_potential)
                        
                        # Gráfico de distribuição
                        fig = px.pie(
                            values=results_df['predicted_potential'].value_counts().values,
                            names=results_df['predicted_potential'].value_counts().index,
                            title="Distribuição de Potencial de Crescimento",
                            color_discrete_sequence=['#FF6B6B', '#F7931E', '#FFD23F']
                        )
                        
                        fig.update_layout(
                            plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(0,0,0,0)',
                            font_color='#FAFAFA'
                        )
                        
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Tabela de resultados
                        st.markdown("#### 📋 Tabela de Resultados")
                        st.dataframe(results_df, use_container_width=True)
                        
                        # Botão para download dos resultados
                        csv_results = results_df.to_csv(index=False)
                        st.download_button(
                            label="📥 Baixar Resultados CSV",
                            data=csv_results,
                            file_name="resultados_predicoes.csv",
                            mime="text/csv"
                        )
        
        except Exception as e:
            st.error(f"Erro ao processar arquivo: {str(e)}")

def show_prediction_interpretation(potential, confidence):
    """Mostra interpretação dos resultados da predição"""
    st.markdown("#### 💡 Interpretação dos Resultados")
    
    if potential == 'Alto':
        st.markdown("""
        <div class="success-box">
            <h4 style="color: #FFD23F; margin-bottom: 0.5rem;">🚀 Alto Potencial de Crescimento</h4>
            <p>Esta empresa apresenta indicadores que sugerem um <strong>alto potencial de crescimento</strong>. 
            Os fatores analisados indicam oportunidades favoráveis para investimento e expansão.</p>
        </div>
        """, unsafe_allow_html=True)
    elif potential == 'Médio':
        st.markdown("""
        <div class="info-box">
            <h4 style="color: #F7931E; margin-bottom: 0.5rem;">⚖️ Médio Potencial de Crescimento</h4>
            <p>Esta empresa apresenta um <strong>potencial de crescimento moderado</strong>. 
            Existem oportunidades, mas também alguns desafios que devem ser considerados na tomada de decisão.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="warning-box">
            <h4 style="color: #FF6B6B; margin-bottom: 0.5rem;">⚠️ Baixo Potencial de Crescimento</h4>
            <p>Esta empresa apresenta indicadores que sugerem um <strong>baixo potencial de crescimento</strong>. 
            Recomenda-se uma análise mais detalhada antes de investimentos significativos.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Indicador de confiança
    if confidence > 0.8:
        confidence_level = "Alta"
        confidence_color = "#FFD23F"
    elif confidence > 0.6:
        confidence_level = "Média"
        confidence_color = "#F7931E"
    else:
        confidence_level = "Baixa"
        confidence_color = "#FF6B6B"
    
    st.markdown(f"""
    <div style="background: rgba(255, 255, 255, 0.1); padding: 1rem; border-radius: 8px; margin-top: 1rem;">
        <h4 style="color: {confidence_color}; margin-bottom: 0.5rem;">🎯 Nível de Confiança: {confidence_level}</h4>
        <p>O modelo apresenta <strong>{confidence:.1%}</strong> de confiança nesta predição.</p>
    </div>
    """, unsafe_allow_html=True)

def show_insights(df, df_potencial):
    """Mostra insights e análises avançadas"""
    st.markdown('<h2 style="color: #FF6B35; font-family: \'Inter\', sans-serif; font-weight: 600; margin-bottom: 2rem;">💡 Insights e Análises Avançadas</h2>', unsafe_allow_html=True)
    
    if 'pc_class' not in df.columns:
        st.info("Dados de classificação não disponíveis. Execute o pipeline de classificação primeiro.")
        return
    
    # Criar abas para diferentes tipos de insights
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["🌍 Análise Geográfica", "📊 Análise Financeira", "🔍 Correlações", "📈 Tendências", "🎯 Insights Avançados"])
    
    with tab1:
        show_geographic_insights(df)
    
    with tab2:
        show_financial_insights(df)
    
    with tab3:
        show_correlation_insights(df)
    
    with tab4:
        show_trend_insights(df)
    
    with tab5:
        show_advanced_insights(df)

def show_geographic_insights(df):
    """Insights geográficos avançados"""
    st.markdown("### 🌍 Análise Geográfica Detalhada")
    
    # Top países por potencial
    col1, col2 = st.columns(2)
    
    with col1:
        # Distribuição por país
        country_counts = df['country'].value_counts().head(10)
        
        fig = px.bar(
            x=country_counts.values,
            y=country_counts.index,
            orientation='h',
            title="Top 10 Países por Número de Empresas",
            color=country_counts.values,
            color_continuous_scale='Oranges'
        )
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#FAFAFA',
            yaxis=dict(autorange="reversed")
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Potencial médio por país
        country_potential = df.groupby('country')['pc_class'].mean().sort_values(ascending=False).head(10)
        
        fig = px.bar(
            x=country_potential.values,
            y=country_potential.index,
            orientation='h',
            title="Top 10 Países por Potencial Médio",
            color=country_potential.values,
            color_continuous_scale='Viridis'
        )
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#FAFAFA',
            yaxis=dict(autorange="reversed")
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Análise detalhada por país
    st.markdown("#### 📋 Análise Detalhada por País")
    
    country_analysis = df.groupby('country').agg({
        'pc_class': ['count', 'mean', 'std'],
        'marketcap': ['mean', 'median'],
        'revenue_ttm': ['mean', 'median'],
        'pe_ratio_ttm': 'mean'
    }).round(2)
    
    country_analysis.columns = [
        'Total_Empresas', 'Potencial_Medio', 'Potencial_Desvio',
        'Cap_Mercado_Media', 'Cap_Mercado_Mediana',
        'Receita_Media', 'Receita_Mediana', 'PE_Ratio_Medio'
    ]
    country_analysis = country_analysis.sort_values('Total_Empresas', ascending=False)
    
    # Filtrar países com pelo menos 5 empresas
    country_analysis_filtered = country_analysis[country_analysis['Total_Empresas'] >= 5]
    
    st.dataframe(country_analysis_filtered.head(15), use_container_width=True)
    
    # Mapa de calor por país e potencial
    st.markdown("#### 🗺️ Mapa de Calor: País vs Potencial")
    
    # Criar pivot table para mapa de calor
    pivot_data = df.groupby(['country', 'pc_class']).size().unstack(fill_value=0)
    pivot_data = pivot_data[pivot_data.sum(axis=1) >= 5]  # Filtrar países com pelo menos 5 empresas
    
    fig = px.imshow(
        pivot_data.values,
        labels=dict(x="Potencial", y="País", color="Número de Empresas"),
        x=['Baixo', 'Médio', 'Alto'],
        y=pivot_data.index,
        title="Distribuição de Potencial por País",
        color_continuous_scale='Oranges'
    )
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#FAFAFA'
    )
    
    st.plotly_chart(fig, use_container_width=True)

def show_financial_insights(df):
    """Insights financeiros avançados"""
    st.markdown("### 💰 Análise Financeira Detalhada")
    
    # Métricas financeiras por potencial
    col1, col2 = st.columns(2)
    
    with col1:
        # Box plot de capitalização por potencial
        fig = px.box(
            df, 
            x='pc_class', 
            y='marketcap',
            title="Distribuição de Capitalização por Potencial",
            labels={'pc_class': 'Potencial', 'marketcap': 'Capitalização (USD)'}
        )
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#FAFAFA'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Box plot de receita por potencial
        fig = px.box(
            df, 
            x='pc_class', 
            y='revenue_ttm',
            title="Distribuição de Receita por Potencial",
            labels={'pc_class': 'Potencial', 'revenue_ttm': 'Receita TTM (USD)'}
        )
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#FAFAFA'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Análise de múltiplos por potencial
    st.markdown("#### 📊 Análise de Múltiplos Financeiros")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # P/E Ratio por potencial
        fig = px.violin(
            df[df['pe_ratio_ttm'] > 0],  # Filtrar P/E positivos
            x='pc_class', 
            y='pe_ratio_ttm',
            title="P/E Ratio por Potencial de Crescimento",
            labels={'pc_class': 'Potencial', 'pe_ratio_ttm': 'P/E Ratio'}
        )
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#FAFAFA'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Dividend Yield por potencial
        fig = px.violin(
            df[df['dividend_yield_ttm'] > 0],  # Filtrar dividend yields positivos
            x='pc_class', 
            y='dividend_yield_ttm',
            title="Dividend Yield por Potencial de Crescimento",
            labels={'pc_class': 'Potencial', 'dividend_yield_ttm': 'Dividend Yield (%)'}
        )
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#FAFAFA'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Estatísticas financeiras por potencial
    st.markdown("#### 📈 Estatísticas Financeiras por Potencial")
    
    financial_stats = df.groupby('pc_class').agg({
        'marketcap': ['count', 'mean', 'median', 'std'],
        'revenue_ttm': ['mean', 'median'],
        'pe_ratio_ttm': ['mean', 'median'],
        'dividend_yield_ttm': ['mean', 'median']
    }).round(2)
    
    financial_stats.columns = [
        'N_Empresas', 'Cap_Media', 'Cap_Mediana', 'Cap_Desvio',
        'Receita_Media', 'Receita_Mediana',
        'PE_Media', 'PE_Mediana',
        'Dividend_Media', 'Dividend_Mediana'
    ]
    
    # Renomear índices
    financial_stats.index = ['Baixo Potencial', 'Médio Potencial', 'Alto Potencial']
    
    st.dataframe(financial_stats, use_container_width=True)

def show_correlation_insights(df):
    """Insights de correlação avançados"""
    st.markdown("### 🔍 Análise de Correlações Avançada")
    
    # Matriz de correlação principal
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    correlation_matrix = df[numeric_cols].corr()
    
    fig = px.imshow(
        correlation_matrix,
        title="Matriz de Correlação Completa",
        color_continuous_scale='RdBu_r',
        aspect="auto"
    )
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#FAFAFA'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Correlações com potencial de crescimento
    st.markdown("#### 🎯 Correlações com Potencial de Crescimento")
    
    # Calcular correlações com pc_class
    correlations_with_potential = df[numeric_cols].corrwith(df['pc_class']).sort_values(ascending=False)
    correlations_with_potential = correlations_with_potential.drop('pc_class')  # Remover auto-correlação
    
    fig = px.bar(
        x=correlations_with_potential.values,
        y=correlations_with_potential.index,
        orientation='h',
        title="Correlação com Potencial de Crescimento",
        color=correlations_with_potential.values,
        color_continuous_scale='RdBu_r'
    )
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#FAFAFA',
        yaxis=dict(autorange="reversed")
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Análise de correlações por potencial
    st.markdown("#### 📊 Matriz de Correlação por Potencial")
    
    potential_levels = ['Baixo', 'Médio', 'Alto']
    
    for i, level in enumerate(potential_levels):
        st.markdown(f"**{level} Potencial:**")
        
        # Filtrar dados por potencial
        df_filtered = df[df['pc_class'] == i]
        
        if len(df_filtered) > 10:  # Só mostrar se houver dados suficientes
            corr_matrix_level = df_filtered[numeric_cols].corr()
            
            fig = px.imshow(
                corr_matrix_level,
                title=f"Correlações - {level} Potencial",
                color_continuous_scale='RdBu_r',
                aspect="auto"
            )
            
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='#FAFAFA',
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info(f"Dados insuficientes para análise de {level} Potencial")

def show_trend_insights(df):
    """Insights de tendências"""
    st.markdown("### 📈 Análise de Tendências")
    
    # Scatter plots com tendências
    col1, col2 = st.columns(2)
    
    with col1:
        # Market Cap vs Revenue
        # Filtrar dados com P/E positivo para usar como size
        df_positive_pe = df[df['pe_ratio_ttm'] > 0]
        
        if len(df_positive_pe) > 0:
            fig = px.scatter(
                df_positive_pe, 
                x='revenue_ttm', 
                y='marketcap',
                color='pc_class',
                size='pe_ratio_ttm',
                title="Capitalização vs Receita (P/E > 0)",
                labels={'revenue_ttm': 'Receita TTM (USD)', 'marketcap': 'Capitalização (USD)', 'pc_class': 'Potencial'},
                color_discrete_sequence=['#FF6B6B', '#F7931E', '#FFD23F']
            )
        else:
            # Se não houver P/E positivo, usar scatter sem size
            fig = px.scatter(
                df, 
                x='revenue_ttm', 
                y='marketcap',
                color='pc_class',
                title="Capitalização vs Receita",
                labels={'revenue_ttm': 'Receita TTM (USD)', 'marketcap': 'Capitalização (USD)', 'pc_class': 'Potencial'},
                color_discrete_sequence=['#FF6B6B', '#F7931E', '#FFD23F']
            )
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#FAFAFA'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # P/E vs Dividend Yield
        # Filtrar dados com P/E positivo
        df_positive_pe_2 = df[(df['pe_ratio_ttm'] > 0) & (df['dividend_yield_ttm'] >= 0)]
        
        if len(df_positive_pe_2) > 0:
            fig = px.scatter(
                df_positive_pe_2, 
                x='dividend_yield_ttm', 
                y='pe_ratio_ttm',
                color='pc_class',
                size='marketcap',
                title="Dividend Yield vs P/E Ratio (Valores Positivos)",
                labels={'dividend_yield_ttm': 'Dividend Yield (%)', 'pe_ratio_ttm': 'P/E Ratio', 'pc_class': 'Potencial'},
                color_discrete_sequence=['#FF6B6B', '#F7931E', '#FFD23F']
            )
        else:
            # Se não houver dados positivos, usar scatter sem size
            fig = px.scatter(
                df, 
                x='dividend_yield_ttm', 
                y='pe_ratio_ttm',
                color='pc_class',
                title="Dividend Yield vs P/E Ratio",
                labels={'dividend_yield_ttm': 'Dividend Yield (%)', 'pe_ratio_ttm': 'P/E Ratio', 'pc_class': 'Potencial'},
                color_discrete_sequence=['#FF6B6B', '#F7931E', '#FFD23F']
            )
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#FAFAFA'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Análise de clusters
    st.markdown("#### 🎯 Análise de Clusters")
    
    # Usar K-means para identificar clusters
    from sklearn.cluster import KMeans
    from sklearn.preprocessing import StandardScaler
    
    # Selecionar features numéricas para clustering
    clustering_features = ['marketcap', 'revenue_ttm', 'pe_ratio_ttm', 'dividend_yield_ttm']
    df_cluster = df[clustering_features].dropna()
    
    if len(df_cluster) > 50:  # Só fazer clustering se houver dados suficientes
        # Normalizar dados
        scaler = StandardScaler()
        df_scaled = scaler.fit_transform(df_cluster)
        
        # Aplicar K-means
        kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
        clusters = kmeans.fit_predict(df_scaled)
        
        # Adicionar clusters ao dataframe
        df_cluster = df_cluster.copy()
        df_cluster['cluster'] = clusters
        
        # Visualizar clusters
        # Filtrar P/E positivo para usar como size
        df_cluster_positive = df_cluster[df_cluster['pe_ratio_ttm'] > 0]
        
        if len(df_cluster_positive) > 0:
            fig = px.scatter(
                df_cluster_positive, 
                x='marketcap', 
                y='revenue_ttm',
                color='cluster',
                size='pe_ratio_ttm',
                title="Clusters de Empresas (Market Cap vs Revenue)",
                labels={'marketcap': 'Capitalização (USD)', 'revenue_ttm': 'Receita TTM (USD)', 'cluster': 'Cluster'},
                color_discrete_sequence=['#FF6B6B', '#F7931E', '#FFD23F']
            )
        else:
            # Se não houver P/E positivo, usar scatter sem size
            fig = px.scatter(
                df_cluster, 
                x='marketcap', 
                y='revenue_ttm',
                color='cluster',
                title="Clusters de Empresas (Market Cap vs Revenue)",
                labels={'marketcap': 'Capitalização (USD)', 'revenue_ttm': 'Receita TTM (USD)', 'cluster': 'Cluster'},
                color_discrete_sequence=['#FF6B6B', '#F7931E', '#FFD23F']
            )
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#FAFAFA'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Estatísticas dos clusters
        st.markdown("#### 📊 Características dos Clusters")
        cluster_stats = df_cluster.groupby('cluster')[clustering_features].mean().round(2)
        cluster_stats.index = ['Cluster 1', 'Cluster 2', 'Cluster 3']
        st.dataframe(cluster_stats, use_container_width=True)
    else:
        st.info("Dados insuficientes para análise de clusters")

def show_advanced_insights(df):
    """Insights avançados e recomendações"""
    st.markdown("### 🎯 Insights Avançados e Recomendações")
    
    # Análise de outliers
    st.markdown("#### 🔍 Análise de Outliers")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Outliers em Market Cap
        Q1 = df['marketcap'].quantile(0.25)
        Q3 = df['marketcap'].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        outliers_marketcap = df[(df['marketcap'] < lower_bound) | (df['marketcap'] > upper_bound)]
        
        st.metric("Outliers em Capitalização", len(outliers_marketcap))
        
        if len(outliers_marketcap) > 0:
            st.markdown("**Top 5 Outliers:**")
            top_outliers = outliers_marketcap.nlargest(5, 'marketcap')[['name', 'country', 'marketcap', 'pc_class']]
            st.dataframe(top_outliers, use_container_width=True)
    
    with col2:
        # Outliers em P/E Ratio
        Q1_pe = df[df['pe_ratio_ttm'] > 0]['pe_ratio_ttm'].quantile(0.25)
        Q3_pe = df[df['pe_ratio_ttm'] > 0]['pe_ratio_ttm'].quantile(0.75)
        IQR_pe = Q3_pe - Q1_pe
        upper_bound_pe = Q3_pe + 1.5 * IQR_pe
        
        outliers_pe = df[(df['pe_ratio_ttm'] > 0) & (df['pe_ratio_ttm'] > upper_bound_pe)]
        
        st.metric("Outliers em P/E Ratio", len(outliers_pe))
        
        if len(outliers_pe) > 0:
            st.markdown("**Top 5 Outliers:**")
            top_outliers_pe = outliers_pe.nlargest(5, 'pe_ratio_ttm')[['name', 'country', 'pe_ratio_ttm', 'pc_class']]
            st.dataframe(top_outliers_pe, use_container_width=True)
    
    # Análise de performance por setor (simulado)
    st.markdown("#### 🏭 Análise de Performance por Características")
    
    # Simular setores baseado em características
    df['sector'] = pd.cut(df['marketcap'], 
                         bins=[0, 1e9, 10e9, float('inf')], 
                         labels=['Small Cap', 'Mid Cap', 'Large Cap'])
    
    sector_performance = df.groupby('sector')['pc_class'].agg(['count', 'mean', 'std']).round(2)
    sector_performance.columns = ['N_Empresas', 'Potencial_Medio', 'Potencial_Desvio']
    
    st.dataframe(sector_performance, use_container_width=True)
    
    # Recomendações baseadas em dados
    st.markdown("#### 💡 Recomendações Baseadas em Dados")
    
    # Calcular métricas para recomendações
    high_potential = df[df['pc_class'] == 2]
    
    if len(high_potential) > 0:
        avg_market_cap_high = high_potential['marketcap'].mean()
        avg_revenue_high = high_potential['revenue_ttm'].mean()
        avg_pe_high = high_potential[high_potential['pe_ratio_ttm'] > 0]['pe_ratio_ttm'].mean()
        
        # Empresas com características similares
        similar_companies = df[
            (df['marketcap'] >= avg_market_cap_high * 0.5) & 
            (df['marketcap'] <= avg_market_cap_high * 2.0) &
            (df['revenue_ttm'] >= avg_revenue_high * 0.5) & 
            (df['revenue_ttm'] <= avg_revenue_high * 2.0) &
            (df['pc_class'] != 2)  # Excluir as que já são alto potencial
        ]
        
        if len(similar_companies) > 0:
            st.markdown("**🚀 Empresas com Potencial de Upgrade:**")
            st.markdown(f"Encontradas {len(similar_companies)} empresas com características similares às de alto potencial:")
            
            # Mostrar top 10 empresas similares
            top_similar = similar_companies.nlargest(10, 'marketcap')[
                ['name', 'country', 'marketcap', 'revenue_ttm', 'pe_ratio_ttm', 'pc_class']
            ]
            st.dataframe(top_similar, use_container_width=True)
            
            st.markdown("""
            <div class="success-box">
                <h4 style="color: #FFD23F; margin-bottom: 0.5rem;">💡 Insight</h4>
                <p>Estas empresas apresentam características financeiras similares às empresas de alto potencial 
                e podem ser candidatas a upgrade na classificação com melhorias operacionais.</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Resumo executivo
    st.markdown("#### 📋 Resumo Executivo")
    
    total_companies = len(df)
    high_potential_pct = len(df[df['pc_class'] == 2]) / total_companies * 100
    avg_market_cap = df['marketcap'].mean() / 1e9
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total de Empresas", f"{total_companies:,}")
    
    with col2:
        st.metric("Alto Potencial", f"{high_potential_pct:.1f}%")
    
    with col3:
        st.metric("Cap. Média", f"${avg_market_cap:.1f}B")
    
    # Insights finais
    st.markdown("""
    <div class="info-box">
        <h4 style="color: #FF6B35; margin-bottom: 0.5rem;">🎯 Principais Insights</h4>
        <ul>
            <li><strong>Diversificação Geográfica:</strong> O dataset apresenta empresas de múltiplos países com diferentes perfis de potencial.</li>
            <li><strong>Correlações Financeiras:</strong> Existem correlações significativas entre indicadores financeiros e potencial de crescimento.</li>
            <li><strong>Oportunidades de Investimento:</strong> Empresas com características similares às de alto potencial podem representar oportunidades.</li>
            <li><strong>Análise de Risco:</strong> A identificação de outliers ajuda na avaliação de riscos e oportunidades.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
