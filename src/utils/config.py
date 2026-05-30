"""Configuration management"""
from typing import Any, Dict, Optional
from pathlib import Path
import json

class Config:
    """Global configuration"""
    
    _defaults = {
        'device_id': 0,
        'debug': False,
        'log_level': 'info',
        'memory_pool_size': 256 * 1024 * 1024,  # 256MB
        'max_streams': 8,
        'compile_cache_dir': '~/.phoenix/cache',
    }
    
    _instance: Optional['Config'] = None
    
    def __init__(self):
        self._values = self._defaults.copy()
        self._load_from_env()
    
    @classmethod
    def get(cls) -> 'Config':
        """Get global config instance"""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def _load_from_env(self):
        """Load config from environment variables"""
        import os
        for key in self._defaults:
            env_key = f'PHOENIX_{key.upper()}'
            if env_key in os.environ:
                self._values[key] = os.environ[env_key]
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get config value"""
        return self._values.get(key, default)
    
    def set(self, key: str, value: Any):
        """Set config value"""
        self._values[key] = value
    
    def load_file(self, path: str):
        """Load config from JSON file"""
        with open(path) as f:
            data = json.load(f)
            self._values.update(data)
    
    def save(self, path: str):
        """Save config to file"""
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w') as f:
            json.dump(self._values, f, indent=2)
