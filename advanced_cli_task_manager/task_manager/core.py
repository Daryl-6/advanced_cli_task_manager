import json
import os
from task_manager.logger import setup_logger

# Récupération du chemin du fichier JSON via la variable d'environnement (avec valeur par défaut)
TASKS_FILE = os.getenv("TASKS_FILE_PATH", "tasks.json")
logger = setup_logger()

def load_tasks() -> list:
    """Charge les tâches depuis le fichier JSON persistant."""
    if not os.path.exists(TASKS_FILE):
        return []
    try:
        with open(TASKS_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError:
        logger.error(f"Le fichier {TASKS_FILE} est corrompu ou illisible.")
        return []

def save_tasks(tasks: list) -> None:
    """Sauvegarde la liste des tâches dans le fichier JSON."""
    try:
        with open(TASKS_FILE, "w", encoding="utf-8") as file:
            json.dump(tasks, file, indent=4, ensure_ascii=False)
    except Exception as e:
        logger.error(f"Erreur lors de la sauvegarde dans {TASKS_FILE}: {e}")

def add_task(description: str, priority: str = "medium") -> dict:
    """Ajoute une nouvelle tâche et la sauvegarde."""
    tasks = load_tasks()
    
    # Génération d'un ID incrémental unique
    task_id = max([t["id"] for t in tasks], default=0) + 1
    
    new_task = {
        "id": task_id,
        "description": description,
        "priority": priority.lower()
    }
    tasks.append(new_task)
    save_tasks(tasks)
    logger.info(f"Tâche ajoutée avec succès - ID: {task_id} | Priorité: {priority}")
    return new_task

def list_tasks() -> list:
    """Retourne la liste complète des tâches actives."""
    tasks = load_tasks()
    logger.info(f"Consultation de l'inventaire des tâches. Nombre trouvé : {len(tasks)}")
    return tasks

def delete_task(task_id: int) -> bool:
    """Supprime une tâche spécifique par son ID. Retourne True si supprimée, False sinon."""
    tasks = load_tasks()
    initial_length = len(tasks)
    
    # Filtrage pour enlever la tâche cible
    tasks = [t for t in tasks if t["id"] != task_id]
    
    if len(tasks) == initial_length:
        logger.warning(f"Échec de la suppression - ID introuvable : {task_id}")
        return False
        
    save_tasks(tasks)
    logger.info(f"Tâche avec l'ID {task_id} supprimée définitivement.")
    return True
