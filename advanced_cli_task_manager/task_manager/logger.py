import logging
import os

def setup_logger(log_file="task_manager.log") -> logging.Logger:
    """Configure et renvoie un logger qui écrit dans la console et dans un fichier."""
    log_directory = "logs"
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)
        
    log_path = os.path.join(log_directory, log_file)
    logger = logging.getLogger("TaskManagerLogger")
    
    # Évite de dupliquer les handlers si setup_logger est appelé plusieurs fois
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
        
        # Handler Fichier
        file_handler = logging.FileHandler(log_path, encoding="utf-8")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
        # Handler Console
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
    return logger
