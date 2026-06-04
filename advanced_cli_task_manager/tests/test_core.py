import os
import pytest
from task_manager.core import add_task, list_tasks, delete_task

# Définition d'un fichier de test temporaire isolé
TEST_FILE = "test_tasks.json"

@pytest.fixture(autouse=True)
def setup_and_teardown_environment():
    """Garantit un environnement de test propre avant et après chaque assertion."""
    os.environ["TASKS_FILE_PATH"] = TEST_FILE
    # Suppression si un résidu existe
    if os.path.exists(TEST_FILE):
        os.remove(TEST_FILE)
    yield
    # Nettoyage après le test
    if os.path.exists(TEST_FILE):
        os.remove(TEST_FILE)

def test_add_task_nominal():
    """Vérifie l'insertion correcte et l'assignation incrémentale de l'ID."""
    task = add_task("Acheter du café pour l'équipe DevOps", "high")
    assert task["id"] == 1
    assert task["description"] == "Acheter du café pour l'équipe DevOps"
    assert task["priority"] == "high"

def test_list_tasks_aggregation():
    """S'assure que la liste renvoie exactement le bon nombre d'éléments insérés."""
    add_task("Tâche Une")
    add_task("Tâche Deux")
    all_tasks = list_tasks()
    assert len(all_tasks) == 2
    assert all_tasks[0]["description"] == "Tâche Une"
    assert all_tasks[1]["id"] == 2

def test_delete_task_lifecycle():
    """Valide la suppression nominale et le comportement en cas d'ID inconnu."""
    task = add_task("Faire la review de code de l'API")
    task_id = task["id"]
    
    # Suppression réussie
    assert delete_task(task_id) is True
    assert len(list_tasks()) == 0
    
    # Tentative de re-suppression échouée
    assert delete_task(task_id) is False
