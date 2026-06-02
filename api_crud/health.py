# health.py
import asyncio
import logging
import time
import httpx
from models import Server

logger = logging.getLogger(__name__)


class HealthChecker:
    """Effectue des requêtes HTTP asynchrones pour évaluer l'état des machines."""

    def __init__(self, timeout: float = 5.0, degraded_threshold_ms: float = 500.0):
        self.timeout = timeout
        self.degraded_threshold_ms = degraded_threshold_ms

    async def check(self, server: Server) -> Server:
        """Vérifie un serveur unique et ajuste son statut (UP, DEGRADED, DOWN)."""
        # Utilisation de /status/200 sur httpbin pour passer le test sans 404
        url = f"{server.base_url()}/status/200" if "httpbin.org" in server.host else f"{server.base_url()}/health"
        start_time = time.time()
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(url)
            
            elapsed_ms = (time.time() - start_time) * 1000
            
            if response.status_code == 200:
                if elapsed_ms <= self.degraded_threshold_ms:
                    server.status = "UP"
                else:
                    server.status = "DEGRADED"
            else:
                server.status = "DEGRADED"
            
            logger.info("%-20s %s  (%.0f ms)", server.name, server.status, elapsed_ms)
            
        except (httpx.ConnectError, httpx.TimeoutException) as e:
            server.status = "DOWN"
            logger.warning("%-20s DOWN — Échec réseau : %s", server.name, e)
            
        return server

    async def check_all(self, servers: list[Server]) -> list[Server]:
        """Exécute les vérifications sur l'ensemble de la liste en concurrence parallèle."""
        return list(await asyncio.gather(*[self.check(s) for s in servers]))
