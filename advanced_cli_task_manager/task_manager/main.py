import argparse
import sys
from task_manager.core import add_task, list_tasks, delete_task

def main():
    parser = argparse.ArgumentParser(
        description="🚀 Advanced CLI Task Manager — Système d'administration de tâches"
    )
    subparsers = parser.add_subparsers(dest="command", help="Sous-commandes disponibles")

    # Subcommand : add
    add_parser = subparsers.add_parser("add", help="Ajouter une nouvelle tâche")
    add_parser.add_argument("description", type=str, help="Description/Contenu de la tâche")
    add_parser.add_argument(
        "--priority", 
        type=str, 
        choices=["low", "medium", "high"], 
        default="medium", 
        help="Niveau de priorité de la tâche (default: medium)"
    )

    # Subcommand : list
    subparsers.add_parser("list", help="Afficher l'ensemble des tâches enregistrées")

    # Subcommand : delete
    delete_parser = subparsers.add_parser("delete", help="Supprimer une tâche via son ID")
    delete_parser.add_argument("id", type=int, help="Identifiant numérique (ID) unique de la tâche")

    args = parser.parse_args()

    # Routage des commandes
    if args.command == "add":
        add_task(args.description, args.priority)
        
    elif args.command == "list":
        tasks = list_tasks()
        if not tasks:
            print("\n📭 Aucune tâche en cours. Profitez de votre journée !")
            return
        print("\n📋 LISTE DES TÂCHES ACTIVES :")
        print("-" * 50)
        for t in tasks:
            print(f"[{t['id']}] {t['description']} (Priorité : {t['priority'].upper()})")
        print("-" * 50)
        
    elif args.command == "delete":
        success = delete_task(args.id)
        if not success:
            print(f"❌ Erreur : Impossible de trouver une tâche avec l'ID {args.id}.")
            sys.exit(1)
        else:
            print(f"🗑️ Tâche [{args.id}] supprimée avec succès.")
            
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
