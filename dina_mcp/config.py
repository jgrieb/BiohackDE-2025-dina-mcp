"""Configuration settings for the DINA MCP server."""

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, field_validator


class Config(BaseSettings):
    """Configuration for connecting to a Cordra repository."""

    model_config = SettingsConfigDict(
        env_prefix="DINA_",
        case_sensitive=False,
    )

    base_url: str = Field(
        default="https://dina.senckenberg.de",
        description="Base URL of the Cordra repository",
    )
    host: str = Field(
        default="0.0.0.0",
        description="Hostname under which the server runs",
    )
    log_level: str = Field(
        default="INFO",
        description="Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)",
        validation_alias="LOGLEVEL",
    )

    @field_validator("log_level", mode="before")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        """Validate that log_level is a standard logging level."""
        level_str = str(v).upper().strip()
        valid_levels = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}

        if level_str not in valid_levels:
            raise ValueError(
                f"Invalid log level '{v}'. Must be one of: {', '.join(valid_levels)}"
            )
        return level_str
