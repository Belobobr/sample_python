from typing import TypeVar, Generic, List, Optional
from pydantic.dataclasses import dataclass

@dataclass
class Config():
   aiven_domain: str = "api.aiven.io"

# config should load daata from file, env, configuration server, secrets manager, etc.
def get_config() -> Config:
   return Config()