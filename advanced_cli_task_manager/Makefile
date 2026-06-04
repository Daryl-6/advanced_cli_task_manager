# ─── CONFIGURATION ───────────────────────────────────────────────────────────
VENV = .venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip

.PHONY: help init run-add run-list test clean

# Target par défaut : Menu d'aide
help:
	@echo "Commandes disponibles pour l'exercice 2 :"
	@echo "  make init      - Initialise l'environnement virtuel et les dépendances"
	@echo "  make run-list  - Affiche la liste des tâches actives"
	@echo "  make test      - Exécute les tests unitaires avec couverture de code"
	@echo "  make clean     - Supprime les résidus de caches, logs et fichiers json"

# Initialisation de l'environnement virtuel
init:
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	@echo "✅ Environnement prêt. Lancez 'source .venv/bin/activate' pour l'activer."

# Raccourci pour lister les tâches locales
run-list:
	PYTHONPATH=. $(PYTHON) task_manager/main.py list

# Exécution des tests avec génération du rapport de couverture (Target >= 75%)
test:
	PYTHONPATH=. $(VENV)/bin/pytest -v --cov=task_manager tests/

# Nettoyage de l'espace de travail
clean:
	rm -rf .pytest_cache .coverage logs/ tasks.json test_tasks.json
	find . -type d -name "__pycache__" -exec rm -rf {} +
	@echo "🧹 Espace de travail nettoyé."
