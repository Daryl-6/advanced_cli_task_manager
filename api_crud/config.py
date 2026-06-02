# config.py
import json
import logging
import pathlib
from models import Server

logger = logging.getLogger(__name__)


class ConfigError(ValueError):
    """Exception personnalisée levée en cas d'erreur de configuration."""
    pass


class ConfigLoader:
    """Gère le chargement et le parsing des serveurs depuis un fichier JSON."""

    def __init__(self, path: str):
        self.path = pathlib.Path(path)

    def load(self) -> list[Server]:
        """Charge le JSON et convertit chaque entrée en instance de Dataclass Server."""
        logger.info("Tentative de chargement du fichier : %s", self.path)
        try:
            raw_data = self.path.read_text(encoding="utf-8")
            parsed_json = json.loads(raw_data)
        except FileNotFoundError:
            logger.error("Fichier de configuration introuvable : %s", self.path)
            raise ConfigError(f"Fichier manquant : {self.path}")
        except json.JSONDecodeError as e:
            logger.error("Le format JSON du fichier est invalide : %s", e)
            raise ConfigError(f"JSON Invalide : {e}") from e

        servers = []
        for index, entry in enumerate(parsed_json, start=1):
            servers.append(Server(
                id=index,
                name=entry.get("name"),
                host=entry.get("host"),
                port=entry.get("port"),
                tags=entry.get("tags", [])
            ))
        logger.info("%d serveurs importés avec succès depuis la configuration.", len(servers))
        return servers
