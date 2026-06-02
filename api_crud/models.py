# models.py
from dataclasses import dataclass, field
from pydantic import BaseModel, Field


@dataclass
class Server:
    """Représentation interne d'un serveur dans l'application."""
    id: int
    name: str
    host: str
    port: int
    status: str = "unknown"
    tags: list[str] = field(default_factory=list)

    def base_url(self) -> str:
        """Génère le protocole de base HTTP/HTTPS automatiquement."""
        protocol = "https" if self.port == 443 else "http"
        return f"{protocol}://{self.host}:{self.port}"


class ServerIn(BaseModel):
    """Schéma Pydantic pour valider l'enregistrement d'un nouveau serveur (Requêtes POST)."""
    name: str
    host: str
    port: int = Field(default=8080, ge=1, le=65535)
    tags: list[str] = []


class ServerOut(BaseModel):
    """Schéma Pydantic filtrant les données renvoyées aux clients (Réponses API)."""
    id: int
    name: str
    host: str
    port: int
    status: str
    tags: list[str] = []

    model_config = {"from_attributes": True}
