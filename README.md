# \# Fiji Infrastructure Voice-to-GIS Tracker

# 

# A modular, production-ready Streamlit application engineered for tracking regional infrastructure in Fiji, featuring live voice payload ingestion, multimodal Gemini parsing, interactive PyDeck GIS mapping, and Supabase persistence.

# 

# \## Architectural Overview

# \* \*\*Frontend UI (`app.py`, `views/`, `components/`)\*\*: Built using Streamlit for rapid interactive state management, custom PyDeck GIS mapping, and native audio stream capture.

# \* \*\*Service Layer (`services/`)\*\*: Encapsulates external APIs and data backends, including Google GenAI (Gemini 1.5 Pro) for structured voice telemetry extraction and Supabase for spatial record persistence.

# \* \*\*Data Contracts (`models/`)\*\*: Strictly enforced Pydantic schemas validating all incoming voice payloads and database entities.

# 

# \## Local PowerShell Setup \& Execution

# 

# \### 1. Initialize Environment

# Copy the environment template and populate your API credentials:

# ```powershell

# Copy-Item .env.example .env

# notepad .env

