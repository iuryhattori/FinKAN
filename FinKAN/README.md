# FinKAN

![Status](https://img.shields.io/badge/status-em%20desenvolvimento-yellow)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey)

FinKAN is a real-time prediction platform for stock market assets. The application collects data from MetaTrader 5, organizes time series, performs inference using a Machine Learning model exported to ONNX, and delivers continuous predictions through a modular, responsibility-oriented architecture designed to evolve.

The project was built to explore how software engineering, Machine Learning, and MLOps can be applied to the financial market domain, reducing friction between data collection, training, model export, and production consumption.

---

## Table of Contents

- [Overview](#overview)
- [Objective](#objective)
- [Highlights](#highlights)
- [System Design](#system-design)
- [Key Features](#key-features)
- [Technologies Used](#technologies-used)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Execution](#execution)
- [Training Flow](#training-flow)
- [Project Entry Points](#project-entry-points)
- [Folder Structure](#folder-structure)
- [Future Improvements](#future-improvements)

---

## Overview

FinKAN implements a complete Machine Learning pipeline for financial time series. The application can collect historical and real-time data, prepare temporal windows, run inference with an ONNX model, and support training, evaluation, and artifact export workflows.

When `main.py` is executed, the system initializes the application lifecycle, loads the configuration, connects to MetaTrader 5, starts asynchronous candle collection for the monitored assets, maintains a temporal buffer with the most recent observations, and triggers inference as soon as the input window is complete.

---

## Highlights

- Real-time financial inference using MetaTrader 5 data
- Asynchronous data ingestion and prediction pipeline
- ONNX Runtime inference for low-latency serving
- Modular architecture inspired by Clean Architecture and DDD
- Production-oriented ML workflow with artifact versioning
- Continuous prediction pipeline for market data (PETR4)

---

## Objective

The project aims to demonstrate how Machine Learning models can be operationalized in production-oriented financial scenarios by using real-time market data and a decoupled software architecture.

Instead of concentrating the logic in notebooks or isolated scripts, FinKAN organizes the full flow of ingestion, processing, inference, training, and model export, bringing ML experimentation closer to a production-oriented environment.

---

## System Design

FinKAN was structured as a modular, event-oriented pipeline to support continuous financial data ingestion and real-time inference.

Main architectural characteristics:

- asynchronous data ingestion
- temporal buffering for inference windows
- decoupled prediction pipeline
- ONNX-based model serving
- lifecycle management with FastAPI lifespan
- fault-tolerant collection with automatic retries
- separation between domain, application, and infrastructure layers

---

## Key Features

- Historical and real-time data collection through MetaTrader 5
- Time series preprocessing and consolidation
- Model training for financial forecasting
- Result evaluation and visualization
- ONNX model export
- Continuous inference in production
- Asynchronous execution of data collection and prediction
- Modular organization inspired by Clean Architecture and DDD

---

## Technologies Used

- Python
- FastAPI
- MetaTrader 5
- ONNX Runtime
- PyTorch
- Pandas
- Polars
- NumPy
- Matplotlib
- PyYAML
- python-dotenv

---

## Architecture

The project was structured with a clear separation between domain, application, infrastructure, and the ML pipeline.

- `src/domain`: entities, value objects, and system contracts
- `src/application`: use cases and application orchestration
- `src/infrastructure`: concrete implementations for collection, configuration, buffering, and inference
- `src/pipeline`: training, experiments, dataloaders, model layers, and utilities

This organization promotes decoupling, testability, and clear responsibility boundaries.

---

### Production Flow

1. `main.py` initializes the FastAPI application.
2. During the `lifespan`, the main application context is assembled.
3. `AppFactory` instantiates the core system components.
4. `CollectorManager` runs the asynchronous ingestion pipeline.
5. `DataCollectorAdapter` consumes real-time candles from MetaTrader 5.
6. The data is transformed into domain entities.
7. `PredictorManager` maintains a temporal buffer until the input window is complete.
8. After the buffer is filled, the input data is organized for inference.
9. `Predictor` performs inference using ONNX Runtime.
10. The system remains continuously active, with failure handling, automatic retries, and resilient shutdown behavior.

### Training Flow

1. The training script loads `config/config.yaml`.
2. The dataset is built from preprocessed data.
3. The model is trained and evaluated in `src/pipeline/exp`.
4. Checkpoints are saved to `artifacts/checkpoints/`.
5. The final model is exported to `onnx/prediction_1h/prediction_1h.onnx`.

---

## Prerequisites

Before running the project, make sure you have:

- Windows
- Python 3.10 or higher
- GPU
- MetaTrader 5 installed and configured
- Access to a valid MT5 account or broker
- A Python virtual environment
- Dependencies installed via `requirements.txt` or manually

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/iuryhattori/FinKAN.git
cd FinKAN
```

### 2. Create and activate the virtual environment

On Windows with PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

Or manually:

```bash
pip install fastapi uvicorn MetaTrader5 onnxruntime torch pandas polars numpy matplotlib pyyaml python-dotenv
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
LOGIN=your_login
PASSWORD=your_password
SERVER=your_server
APP_CONFIG_PATH=config/config.yaml
```

### 5. Review the application configuration

The `config/config.yaml` file centralizes parameters such as:

- monitored symbols
- MetaTrader 5 execution mode
- ONNX model path
- buffer size
- time frequency
- training hyperparameters

---

## Execution

### Run the real-time prediction application

```bash
uvicorn main:app --reload
```

When the application starts, it:

1. loads the configuration;
2. connects to MetaTrader 5;
3. starts data collection;
4. fills the temporal buffer;
5. runs inference when the input window is complete.

### Main endpoints

- `GET /health`: checks whether the application was initialized correctly
- `GET /stop`: requests the shutdown of collection and execution

---

## Training Flow

### Train the model and export it to ONNX

```bash
python entrypoint/run_model.py
```

This script runs training, performs evaluation, and exports the model to:

```text
onnx/prediction_1h/prediction_1h.onnx
```

### Generate plots and validate results

```bash
python entrypoint/run_plot.py
```

This flow loads the saved checkpoint, generates visualizations comparing real and predicted values, and stores the plots in `imgs/`.

---

## Project Entry Points

The main files to understand how the system works are:

- [main.py](main.py)
- [config/config.yaml](config/config.yaml)
- [src/infrastructure/factory/app_factory.py](src/infrastructure/factory/app_factory.py)
- [src/application/use_cases/data_ingestion_manager.py](src/application/use_cases/data_ingestion_manager.py)
- [src/application/use_cases/prediction_manager.py](src/application/use_cases/prediction_manager.py)
- [src/infrastructure/Predictor/Predictor.py](src/infrastructure/Predictor/Predictor.py)
- [entrypoint/run_model.py](entrypoint/run_model.py)
- [entrypoint/run_plot.py](entrypoint/run_plot.py)

These files represent, respectively, the application entry point, the central configuration, dependency composition, the continuous ingestion flow, inference, and the training and evaluation scripts.

---

## Folder Structure

```text
FinKAN/
├── artifacts/
├── config/
├── data/
├── entrypoint/
├── imgs/
├── onnx/
├── src/
│   ├── application/
│   ├── domain/
│   ├── infrastructure/
│   └── pipeline/
└── README.md
```

## Future Improvements

- Docker containerization
- Kafka integration for streaming
- WebSocket endpoints for real-time predictions
- Monitoring and observability
- Automatic model retraining
- Model registry and experiment tracking
- Distributed inference workers
- CI/CD integration