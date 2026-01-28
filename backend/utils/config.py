"""
Configuration management module
"""
import os
from pathlib import Path
import yaml


class Config:
    """Configuration manager for loading and accessing config values"""
    
    _instance = None
    _config = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._config is None:
            self.load_config()
    
    def load_config(self, config_path: str = None):
        """Load configuration from YAML file"""
        if config_path is None:
            # Default config path
            base_dir = Path(__file__).parent.parent.parent
            env = os.getenv("APP_ENV", "development")
            config_path = base_dir / "config" / f"config.yaml"
            
            # Try environment-specific config first
            env_config_path = base_dir / "config" / f"config.{env}.yaml"
            if env_config_path.exists():
                config_path = env_config_path
        
        with open(config_path, "r", encoding="utf-8") as f:
            self._config = yaml.safe_load(f)
        
        # Apply environment variable overrides
        self._apply_env_overrides()
    
    def _apply_env_overrides(self):
        """Apply environment variable overrides"""
        env_mappings = {
            "APP_DEBUG": ("app", "debug"),
            "APP_SECRET_KEY": ("app", "secret_key"),
            "SERVER_HOST": ("server", "host"),
            "SERVER_PORT": ("server", "port"),
            "DB_TYPE": ("database", "type"),
            "DB_PATH": ("database", "path"),
            "DB_HOST": ("database", "host"),
            "DB_PORT": ("database", "port"),
            "DB_USER": ("database", "username"),
            "DB_PASSWORD": ("database", "password"),
            "DB_NAME": ("database", "database"),
            "LOG_LEVEL": ("logging", "level"),
            "LOG_DIR": ("logging", "output_dir"),
        }
        
        for env_key, config_path in env_mappings.items():
            value = os.getenv(env_key)
            if value is not None:
                self._set_nested(config_path, value)
    
    def _set_nested(self, path: tuple, value):
        """Set a nested config value"""
        current = self._config
        for key in path[:-1]:
            if key not in current:
                current[key] = {}
            current = current[key]
        
        # Type conversion
        if isinstance(current.get(path[-1]), bool):
            value = value.lower() in ("true", "1", "yes")
        elif isinstance(current.get(path[-1]), int):
            value = int(value)
        
        current[path[-1]] = value
    
    def get(self, *keys, default=None):
        """Get a config value by nested keys"""
        current = self._config
        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return default
        return current
    
    @property
    def app(self):
        return self._config.get("app", {})
    
    @property
    def server(self):
        return self._config.get("server", {})
    
    @property
    def database(self):
        return self._config.get("database", {})
    
    @property
    def logging(self):
        return self._config.get("logging", {})
    
    @property
    def cors(self):
        return self._config.get("cors", {})


# Global config instance
config = Config()
