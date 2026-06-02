# main.py
import logging
from fastapi import FastAPI, HTTPException, Header, Depends
from models import Server, ServerIn, ServerOut
from health import HealthChecker

# Configuration globale des logs pour le terminal
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s — %(message)s")

app = FastAPI(
    title="DevOps Monitoring API", 
    version="1.0",
    description="Solution de supervision réseau asynchrone avec validation de données"
)

# Stockage local (In-Memory Store)
_store: dict[int, Server] = {}
_counter = 0
checker = HealthChecker()


# ─── SÉCURITÉ (STRETCH GOAL) ──────────────────────────────────────────────────

def require_api_key(x_api_key: str = Header(..., description="Clé d'authentification DevOps")):
    """Middleware de sécurité vérifiant la présence de la clé API secrète."""
    if x_api_key != "ops-secret":
        raise HTTPException(status_code=403, detail="Clé API invalide ou absente.")


# ─── ENDPOINTS (ROUTES CRUD) ─────────────────────────────────────────────────

@app.get("/health", tags=["System Blueprint"])
async def health_check():
    """Vérifie si l'API elle-même répond correctement."""
    return {"status": "ok", "servers_monitored": len(_store)}


@app.post("/servers", response_model=ServerOut, status_code=201, tags=["Servers Core CRUD"])
async def register_server(server: ServerIn, dependencies=Depends(require_api_key)):
    """Enregistre une machine dans le catalogue de surveillance. [Sécurisé]"""
    global _counter
    _counter += 1
    record = Server(
        id=_counter,
        name=server.name,
        host=server.host,
        port=server.port,
        tags=server.tags,
    )
    _store[_counter] = record
    return record


@app.get("/servers", response_model=list[ServerOut], tags=["Servers Core CRUD"])
async def list_servers(status: str | None = None):
    """Affiche toutes les machines enregistrées avec option de filtrage par état (?status=UP)."""
    servers_list = list(_store.values())
    if status:
        servers_list = [s for s in servers_list if s.status.upper() == status.upper()]
    return servers_list


@app.get("/servers/{server_id}", response_model=ServerOut, tags=["Servers Core CRUD"])
async def get_server(server_id: int):
    """Recherche et extrait une machine unique via son identifiant ID."""
    if server_id not in _store:
        raise HTTPException(status_code=404, detail="Machine introuvable.")
    return _store[server_id]


@app.delete("/servers/{server_id}", status_code=204, tags=["Servers Core CRUD"])
async def delete_server(server_id: int, dependencies=Depends(require_api_key)):
    """Supprime définitivement une machine de l'inventaire. [Sécurisé]"""
    if server_id not in _store:
        raise HTTPException(status_code=404, detail="Machine introuvable.")
    del _store[server_id]


@app.post("/servers/{server_id}/check", response_model=ServerOut, tags=["Supervision Network"])
async def trigger_health_check(server_id: int):
    """Déclenche de manière forcée un diagnostic réseau instantané sur une machine ciblée."""
    if server_id not in _store:
        raise HTTPException(status_code=404, detail="Machine introuvable.")
    
    # Exécute la méthode asynchrone du HealthChecker sur l'objet en mémoire
    server_updated = await checker.check(_store[server_id])
    return server_updated
