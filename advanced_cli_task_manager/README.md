# 🚀 Advanced CLI Task Manager 

Ce projet implémente un gestionnaire de tâches robuste utilisable en ligne de commande (CLI). Il met en application la gestion de sous-commandes complexes
 via `argparse`, la persistance de données locales au format JSON, la configuration fine de journaux d'événements (Logging),
 ainsi qu'une isolation d'environnement basée sur des variables d'infrastructure.

## ✨ Fonctionnalités Implémentées

- **CLI à Sous-commandes** : Support des commandes explicites `add`, `list`, et `delete`.
- **Persistance Découplée** : Enregistrement de l'état dans un fichier JSON contrôlé par la variable d'environnement `TASKS_FILE_PATH`.
- **Système de Traçabilité (Logging)** : Journalisation double (Console + Fichier `logs/task_manager.log`) pour un audit post-exécution.
- **Conformité DevOps** : Pilotage complet du projet à l'aide d'un `Makefile` standardisé.

---

## 🛠️ Installation et Prérequis

Déployez l'environnement virtuel et installez les paquets de test en une seule commande grâce au Makefile :

```bash
make init
 
Dans mon ENV à perso mon (.venv) se trouve dans le repertoire ou j'ai cloné le repo complet
pour experimenter dans le cas précis nous allons :
 1-activation de l'env
source .venv/bin/activate
2- ajouts des taches de la CLI
python task_manager/main.py add "Finaliser l'image Docker du projet" --priority high
python task_manager/main.py add "Relire le sujet du TP" --priority low
3- lister les taches
python task_manager/main.py list
4- supprimer les taches 
python task_manager/main.py delete 1
5-suites de validations 
make test
