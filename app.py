"""
API REST para previsão do potencial de crescimento de empresas.

Esta API substitui a aplicação Streamlit original e expõe o modelo
`Random_Forest_model.joblib` como serviço de previsão, com suporte a:
- Previsão individual (um registro por vez, via JSON)
- Previsão em batch (lista de registros via JSON)
"""

from __future__ import annotations

from pathlib import Path
import os
import tempfile
import time
from typing import List, Literal, Optional

import joblib
import numpy as np
import pandas as pd
import requests
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field


# ---------------------------------------------------------
# Configuração de caminhos e GitHub (mantida da versão Streamlit)
# ---------------------------------------------------------

GITHUB_USERNAME = "sidnei-almeida"
GITHUB_REPO = "potencial_empresarial"
GITHUB_BRANCH = "main"
GITHUB_BASE_URL = f"https://raw.githubusercontent.com/{GITHUB_USERNAME}/{GITHUB_REPO}/{GITHUB_BRANCH}"

DATA_URL = f"{GITHUB_BASE_URL}/dados/data.csv"
MODEL_URL = f"{GITHUB_BASE_URL}/modelos/Random_Forest_model.joblib"


def download_file_from_github(url: str, filename: str, ttl_seconds: int = 7200) -> Optional[str]:
    """
    Faz download de um arquivo do GitHub para um diretório temporário e
    retorna o caminho local. Usa cache simples baseado em mtime.
    """
    try:
        temp_dir = Path(tempfile.gettempdir()) / "potencial_empresarial"
        temp_dir.mkdir(exist_ok=True)

        file_path = temp_dir / filename

        # Cache baseado em mtime
        if file_path.exists():
            file_age = time.time() - os.path.getmtime(file_path)
            if file_age < ttl_seconds:
                print(f"[download_file_from_github] Using cached file: {filename}")
                return str(file_path)

        print(f"[download_file_from_github] Downloading {filename} from GitHub...")
        headers = {
            "User-Agent": "Business-Growth-Potential-API/1.0",
            "Accept": "application/vnd.github.v3.raw",
        }
        response = requests.get(url, timeout=60, headers=headers)
        if response.status_code in (403, 429):
            # Problema de rate limiting ou permissão — tenta usar arquivo antigo
            if file_path.exists():
                print(
                    f"[download_file_from_github] GitHub returned {response.status_code}, "
                    f"using cached file for {filename}"
                )
                return str(file_path)
            return None

        response.raise_for_status()

        with open(file_path, "wb") as f:
            f.write(response.content)

        print(f"[download_file_from_github] Successfully downloaded {filename}")
        return str(file_path)
    except Exception as e:
        print(f"[download_file_from_github] Error downloading {filename}: {e}")
        if "file_path" in locals() and file_path.exists():
            print(f"[download_file_from_github] Using cached file due to error: {filename}")
            return str(file_path)
        return None


def load_model() -> Optional[object]:
    """
    Carrega o modelo Random Forest treinado.
    Prioriza o arquivo local `modelos/Random_Forest_model.joblib`.
    Se não existir, tenta baixar do GitHub.
    """
    try:
        local_path = Path("modelos") / "Random_Forest_model.joblib"
        if local_path.exists():
            print(f"[load_model] Loading model from local path: {local_path}")
            return joblib.load(local_path)

        # Fallback: baixar do GitHub
        model_path = download_file_from_github(MODEL_URL, "Random_Forest_model.joblib")
        if model_path:
            print(f"[load_model] Loading model from GitHub cache: {model_path}")
            return joblib.load(model_path)

        print("[load_model] Could not load model from local or GitHub")
        return None
    except Exception as e:
        print(f"[load_model] Error loading model: {e}")
        return None


def load_example_data() -> Optional[pd.DataFrame]:
    """
    Carrega o dataset de exemplo para fins de documentação / sanity check.
    Não é obrigatório para a API funcionar.
    """
    try:
        local_path = Path("dados") / "data.csv"
        if local_path.exists():
            print(f"[load_example_data] Loading data from local path: {local_path}")
            return pd.read_csv(local_path)

        data_path = download_file_from_github(DATA_URL, "data.csv")
        if data_path:
            print(f"[load_example_data] Loading data from GitHub cache: {data_path}")
            return pd.read_csv(data_path)

        print("[load_example_data] Could not load data from local or GitHub")
        return None
    except Exception as e:
        print(f"[load_example_data] Error loading data: {e}")
        return None


# ---------------------------------------------------------
# Definição da API (FastAPI)
# ---------------------------------------------------------

app = FastAPI(
    title="Business Growth Potential API",
    description=(
        "API REST para previsão do potencial de crescimento de empresas "
        "nos países do continente americano, utilizando Random Forest."
    ),
    version="1.0.0",
)

# ---------------------------------------------------------
# CORS
# ---------------------------------------------------------

# Ajuste esta lista para os domínios reais do front-end em produção
origins = [
    "*",  # para desenvolvimento; em produção, preferir domínios específicos
    # "https://seu-frontend.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Modelo carregado em memória na inicialização
MODEL = load_model()
EXAMPLE_DF = load_example_data()


PotentialLabel = Literal["Low", "Medium", "High"]


class Features(BaseModel):
    """
    Mesma ordem e significado de features usados na interface Streamlit
    (`show_manual_prediction`), compatível com o modelo treinado.
    """

    dividend_yield_ttm: float = Field(..., description="Dividend Yield (%)")
    earnings_ttm: float = Field(..., description="Earnings TTM (USD)")
    marketcap: float = Field(..., description="Market Cap (USD)")
    pe_ratio_ttm: float = Field(..., description="P/E Ratio (TTM)")
    revenue_ttm: float = Field(..., description="Revenue TTM (USD)")
    price: float = Field(..., description="Stock price (USD)")
    gdp_per_capita_usd: float = Field(..., description="GDP per capita (USD)")
    gdp_growth_percent: float = Field(..., description="GDP growth (%)")
    inflation_percent: float = Field(..., description="Inflation rate (%)")
    interest_rate_percent: float = Field(..., description="Interest rate (%)")
    unemployment_rate_percent: float = Field(..., description="Unemployment rate (%)")
    exchange_rate_to_usd: float = Field(..., description="Exchange rate to USD")
    inflation: float = Field(..., description="Absolute inflation value (usually negative)")
    interest_rate: float = Field(..., description="Absolute interest rate value (usually negative)")
    unemployment: float = Field(..., description="Absolute unemployment value (usually negative)")


class PredictionResult(BaseModel):
    predicted_class: int = Field(..., description="Classe prevista: 0=Low, 1=Medium, 2=High")
    predicted_potential: PotentialLabel = Field(..., description="Rótulo textual da classe prevista")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Probabilidade da classe prevista (0-1)")
    prob_low: float = Field(..., ge=0.0, le=1.0)
    prob_medium: float = Field(..., ge=0.0, le=1.0)
    prob_high: float = Field(..., ge=0.0, le=1.0)


class BatchRequest(BaseModel):
    instances: List[Features]


class BatchPredictionResult(BaseModel):
    predictions: List[PredictionResult]


class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    n_example_rows: Optional[int] = None


class ModelInfoResponse(BaseModel):
    model_type: str
    params: dict
    feature_order: List[str]


POTENTIAL_LABELS = {0: "Low", 1: "Medium", 2: "High"}


def _features_to_array(features: Features) -> np.ndarray:
    """
    Converte o modelo pydantic `Features` para o vetor numpy na ordem
    esperada pelo modelo, exatamente como no Streamlit.
    """
    return np.array(
        [
            [
                features.dividend_yield_ttm,
                features.earnings_ttm,
                features.marketcap,
                features.pe_ratio_ttm,
                features.revenue_ttm,
                features.price,
                features.gdp_per_capita_usd,
                features.gdp_growth_percent,
                features.inflation_percent,
                features.interest_rate_percent,
                features.unemployment_rate_percent,
                features.exchange_rate_to_usd,
                features.inflation,
                features.interest_rate,
                features.unemployment,
            ]
        ]
    )


def _proba_to_result(pred_class: int, proba: np.ndarray) -> PredictionResult:
    return PredictionResult(
        predicted_class=int(pred_class),
        predicted_potential=POTENTIAL_LABELS.get(int(pred_class), "Low"),  # fallback
        confidence=float(proba[int(pred_class)]),
        prob_low=float(proba[0]),
        prob_medium=float(proba[1]),
        prob_high=float(proba[2]),
    )


@app.get("/health", response_model=HealthResponse, tags=["system"])
def health_check() -> HealthResponse:
    """
    Verificação simples de saúde da API.
    """
    n_rows = int(EXAMPLE_DF.shape[0]) if EXAMPLE_DF is not None else None
    return HealthResponse(status="ok", model_loaded=MODEL is not None, n_example_rows=n_rows)


@app.get("/model-info", response_model=ModelInfoResponse, tags=["model"])
def model_info() -> ModelInfoResponse:
    """
    Retorna informações básicas sobre o modelo e a ordem das features.
    """
    if MODEL is None:
        raise HTTPException(status_code=503, detail="Modelo não carregado.")

    feature_order = [
        "dividend_yield_ttm",
        "earnings_ttm",
        "marketcap",
        "pe_ratio_ttm",
        "revenue_ttm",
        "price",
        "gdp_per_capita_usd",
        "gdp_growth_percent",
        "inflation_percent",
        "interest_rate_percent",
        "unemployment_rate_percent",
        "exchange_rate_to_usd",
        "inflation",
        "interest_rate",
        "unemployment",
    ]

    params = MODEL.get_params() if hasattr(MODEL, "get_params") else {}

    return ModelInfoResponse(
        model_type=MODEL.__class__.__name__,
        params=params,
        feature_order=feature_order,
    )


@app.post("/predict", response_model=PredictionResult, tags=["prediction"])
def predict(features: Features) -> PredictionResult:
    """
    Previsão individual (um registro por vez).
    """
    if MODEL is None:
        raise HTTPException(status_code=503, detail="Modelo não carregado.")

    try:
        X = _features_to_array(features)
        pred = MODEL.predict(X)[0]
        if hasattr(MODEL, "predict_proba"):
            proba = MODEL.predict_proba(X)[0]
        else:
            # Se o modelo não suportar probabilidades, cria distribuição dummy
            proba = np.zeros(3, dtype=float)
            proba[int(pred)] = 1.0

        return _proba_to_result(int(pred), proba)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao realizar previsão: {e}")


@app.post("/predict-batch", response_model=BatchPredictionResult, tags=["prediction"])
def predict_batch(request: BatchRequest) -> BatchPredictionResult:
    """
    Previsão em batch.

    Envie uma lista de instâncias no campo `instances`, cada uma com as mesmas
    features usadas no endpoint `/predict`.
    """
    if MODEL is None:
        raise HTTPException(status_code=503, detail="Modelo não carregado.")

    if not request.instances:
        raise HTTPException(status_code=400, detail="Lista de instâncias vazia.")

    try:
        X_list = [_features_to_array(instance)[0] for instance in request.instances]
        X = np.vstack(X_list)

        preds = MODEL.predict(X)
        if hasattr(MODEL, "predict_proba"):
            probas = MODEL.predict_proba(X)
        else:
            probas = np.zeros((len(preds), 3), dtype=float)
            for i, c in enumerate(preds):
                probas[i, int(c)] = 1.0

        results = [_proba_to_result(int(c), probas[i]) for i, c in enumerate(preds)]
        return BatchPredictionResult(predictions=results)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao realizar previsões em batch: {e}")


@app.get("/", tags=["system"])
def root():
    """
    Endpoint raiz simples com link para documentação.
    """
    return {
        "message": "Business Growth Potential API",
        "docs": "/docs",
        "redoc": "/redoc",
    }


if __name__ == "__main__":
    # Execução local (desenvolvimento):
    # uvicorn app:app --reload
    import uvicorn

    uvicorn.run("app:app", host="0.0.0.0", port=int(os.environ.get("PORT", 8000)), reload=True)


