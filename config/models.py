"""
Model Configuration for Agno MLB Agent Team

This file contains all model configurations using FREE tier providers:
- Gemini Direct API (UNLIMITED FREE - Gemini 3.1 Flash)
- OpenRouter FREE models (only models with "free" in name)
- Kilo Gateway (OpenAI-compatible, using user's API key)
"""

import os
from agno.models.google import Gemini
from agno.models.openai import OpenAIChat

# =============================================================================
# API KEYS (loaded from environment)
# =============================================================================

# Gemini Direct API (UNLIMITED FREE!)
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")

# OpenRouter API (free tier models)
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")

# Kilo Gateway API (OpenAI-compatible, user's existing key)
KILO_API_KEY = os.getenv("KILO_API_KEY", "eyJhbGciOiJodHRwOi8vdjIua2lsby5haSIsInR5cCI6IkpXVCJ9.eyJlbnYiOiJwcm9kdWN0aW9uIiwia2lsbFVzZXJJZCI6Im9hdXRoL2dvb2dsZToxMTIyNzU2NTY5ODIzNTA0NTE2MzciLCJhcGlUb2tlblBlcHBlciI6bnVsbCwidmVyc2lvbiI6MywiaWF0IjoxNzc4NTI0MDQ2LCJleHAiOjE5MzYyMDQwNDZ9.AhSlofNM7hwneBtZwVSDdwNJn47bNbVY9Kum0cpacfw")

# =============================================================================
# OPENROUTER FREE MODELS (sorted by usage/tokens - highest to lowest)
# =============================================================================

# From OpenRouter models with "free" in name, sorted by popularity:
# 1. nvidia/nemotron-3-super-120b-a12b:free - 120B total, 12B active params, 1M context
# 2. inclusionai/ring-2.6-1t:free - 63B reasoning model, 262K context
# 3. openai/gpt-oss-120b:free - 120B OSS model
# 4. z-ai/glm-4.5-air:free - GLM model
# 5. minimax/minimax-m2.5:free - MiniMax model

OPENROUTER_FREE_MODELS = {
    "nemotron": "nvidia/nemotron-3-super-120b-a12b:free",
    "ring": "inclusionai/ring-2.6-1t:free",
    "gpt-oss": "openai/gpt-oss-120b:free",
    "glm": "z-ai/glm-4.5-air:free",
    "minimax": "minimax/minimax-m2.5:free",
}

# =============================================================================
# MODEL CONFIGURATIONS
# =============================================================================

# Gemini Direct - UNLIMITED FREE (Gemini 3.1 Flash)
GEMINI_FLASH = Gemini(
    id="gemini-3.1-flash",
    name="Gemini Flash",
    api_key=GOOGLE_API_KEY,
)

# OpenRouter configurations (free tier)
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

# Nemotron - Best overall free model (120B, 1M context)
MODEL_NEMOTRON = OpenAIChat(
    id=OPENROUTER_FREE_MODELS["nemotron"],
    name="Nemotron 120B",
    base_url=OPENROUTER_BASE_URL,
    api_key=OPENROUTER_API_KEY,
)

# Ring - Reasoning model (63B)
MODEL_RING = OpenAIChat(
    id=OPENROUTER_FREE_MODELS["ring"],
    name="Ring Reasoning",
    base_url=OPENROUTER_BASE_URL,
    api_key=OPENROUTER_API_KEY,
)

# GLM - Coding capable
MODEL_GLM = OpenAIChat(
    id=OPENROUTER_FREE_MODELS["glm"],
    name="GLM 4.5",
    base_url=OPENROUTER_BASE_URL,
    api_key=OPENROUTER_API_KEY,
)

# MiniMax - Additional free model
MODEL_MINIMAX = OpenAIChat(
    id=OPENROUTER_FREE_MODELS["minimax"],
    name="MiniMax M2.5",
    base_url=OPENROUTER_BASE_URL,
    api_key=OPENROUTER_API_KEY,
)

# GPT-OSS - OpenAI's open source model
MODEL_GPT_OSS = OpenAIChat(
    id=OPENROUTER_FREE_MODELS["gpt-oss"],
    name="GPT-OSS 120B",
    base_url=OPENROUTER_BASE_URL,
    api_key=OPENROUTER_API_KEY,
)

# Kilo Gateway - OpenAI-compatible, 500+ models
KILO_BASE_URL = "https://api.kilo.ai/api/gateway"

MODEL_KILO = OpenAIChat(
    id="openai/gpt-4o",
    name="Kilo Gateway",
    base_url=KILO_BASE_URL,
    api_key=KILO_API_KEY,
)

# =============================================================================
# AGENT MODEL ASSIGNMENTS
# =============================================================================

# All FREE tier models - no cost!
AGENT_MODELS = {
    # Coordinator - Always FREE (Gemini)
    "coordinator": GEMINI_FLASH,
    
    # AppArchitect - FREE (Nemotron - best overall)
    "app_architect": MODEL_NEMOTRON,
    
    # Coder agents - FREE OpenRouter models
    "coder_1": MODEL_RING,       # Reasoning model
    "coder_2": MODEL_GLM,        # Coding capable
    "coder_3": MODEL_GPT_OSS,    # 120B OSS model
    "coder_4": MODEL_KILO,       # Kilo Gateway (flexible)
    
    # DBSpecialist - FREE (MiniMax for SQL)
    "db_specialist": MODEL_MINIMAX,
    
    # StatsAgent - FREE (Gemini for analysis)
    "stats_agent": GEMINI_FLASH,
    
    # APISpecialist - FREE (Nemotron)
    "api_specialist": MODEL_NEMOTRON,
    
    # CodeReviewer - FREE (Gemini)
    "code_reviewer": GEMINI_FLASH,
    
    # PerformanceOptimizer - FREE (Nemotron)
    "performance_optimizer": MODEL_NEMOTRON,
    
    # DocsWriter - FREE (Gemini)
    "docs_writer": GEMINI_FLASH,
}

# =============================================================================
# MODEL SELECTION HELPERS
# =============================================================================

def get_agent_model(agent_name: str) -> any:
    """Get the configured model for an agent."""
    return AGENT_MODELS.get(agent_name, GEMINI_FLASH)

def get_model_by_id(model_id: str) -> OpenAIChat:
    """Get a model by its ID."""
    for model in AGENT_MODELS.values():
        if hasattr(model, 'id') and model.id == model_id:
            return model
    return GEMINI_FLASH

# =============================================================================
# FALLBACK CHAINS (if one model hits limits)
# =============================================================================

# Fallback order for when primary model is unavailable
FALLBACK_CHAINS = {
    "coder": [MODEL_RING, MODEL_GLM, MODEL_GPT_OSS, MODEL_KILO, GEMINI_FLASH],
    "architect": [MODEL_NEMOTRON, MODEL_RING, GEMINI_FLASH],
    "default": [GEMINI_FLASH, MODEL_NEMOTRON, MODEL_RING],
}

def get_fallback_model(primary_model: any) -> any:
    """Get next available model in fallback chain."""
    # Simple implementation - rotate through models
    return GEMINI_FLASH  # Always fallback to free Gemini
