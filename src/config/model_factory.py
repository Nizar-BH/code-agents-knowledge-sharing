"""
Model Factory for creating Agno model instances based on configuration.

Supports:
- Ollama (local and cloud)
- OpenAI

Configuration via environment variables:
- MODEL_PROVIDER: "ollama" or "openai" (default: "ollama")
- For Ollama: OLLAMA_MODEL_ID, OLLAMA_TEMPERATURE
- For OpenAI: OPENAI_MODEL_ID, OPENAI_TEMPERATURE, OPENAI_API_KEY
"""
import os
from typing import Literal, Optional
from agno.models.ollama import Ollama
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

# Conditional OpenAI import - only import if needed
try:
    from agno.models.openai.chat import OpenAIChat
    OPENAI_AVAILABLE = True
except ImportError:
    OpenAIChat = None
    OPENAI_AVAILABLE = False

ModelProvider = Literal["ollama", "openai"]


class ModelFactory:
    """Factory class for creating Agno model instances."""

    @staticmethod
    def get_provider() -> ModelProvider:
        """Get the model provider from environment variable."""
        provider = os.getenv("MODEL_PROVIDER", "ollama").lower()
        if provider not in ["ollama", "openai"]:
            raise ValueError(
                f"MODEL_PROVIDER must be 'ollama' or 'openai', got '{provider}'"
            )
        return provider

    @staticmethod
    def create_model(
        model_id: Optional[str] = None,
        temperature: Optional[float] = None,
    ):
        """
        Create a model instance based on configuration.

        Args:
            model_id: Override model ID (optional, uses env var if not provided)
            temperature: Override temperature (optional, uses env var if not provided)

        Returns:
            Model instance (Ollama or OpenAIChat)
        """
        provider = ModelFactory.get_provider()

        if provider == "ollama":
            return ModelFactory._create_ollama_model(
                model_id=model_id,
                temperature=temperature,
            )
        elif provider == "openai":
            if not OPENAI_AVAILABLE:
                raise ImportError(
                    "OpenAI support not available. Install with: pip install openai"
                )
            return ModelFactory._create_openai_model(
                model_id=model_id,
                temperature=temperature,
            )
        else:
            raise ValueError(f"Unsupported provider: {provider}")

    @staticmethod
    def _create_ollama_model(
        model_id: Optional[str] = None,
        temperature: Optional[float] = None,
    ) -> Ollama:
        """Create an Ollama model instance."""
        # Determine model ID
        if model_id:
            final_model_id = model_id
        else:
            final_model_id = os.getenv("OLLAMA_MODEL_ID")
            if not final_model_id:
                raise ValueError(
                    "OLLAMA_MODEL_ID environment variable is required"
                )

        # Determine temperature
        if temperature is not None:
            final_temperature = temperature
        else:
            temp_env = os.getenv("OLLAMA_TEMPERATURE")
            if not temp_env:
                raise ValueError(
                    "OLLAMA_TEMPERATURE environment variable is required"
                )
            final_temperature = float(temp_env)

        return Ollama(
            id=final_model_id,
            options={"temperature": final_temperature}
        )

    @staticmethod
    def _create_openai_model(
        model_id: Optional[str] = None,
        temperature: Optional[float] = None,
    ) -> OpenAIChat:
        """Create an OpenAI model instance."""
        # Determine model ID
        if model_id:
            final_model_id = model_id
        else:
            final_model_id = os.getenv("OPENAI_MODEL_ID")
            if not final_model_id:
                raise ValueError(
                    "OPENAI_MODEL_ID environment variable is required"
                )

        # Get API key
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError(
                "OPENAI_API_KEY environment variable is required"
            )

        # Determine temperature
        if temperature is not None:
            final_temperature = temperature
        else:
            temp_env = os.getenv("OPENAI_TEMPERATURE")
            if temp_env:
                final_temperature = float(temp_env)
            else:
                # Default temperature for OpenAI if not specified
                final_temperature = 0.7

        return OpenAIChat(
            id=final_model_id,
            api_key=api_key,
            temperature=final_temperature,
        )

