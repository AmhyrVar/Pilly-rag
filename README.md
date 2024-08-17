

# Projet RAG avec Neo4j, Langchain, et Mistral Instruct

Ce projet démontre un exemple de Retrieval-Augmented Generation (RAG) utilisant Neo4j pour la gestion des données, Langchain pour le traitement du langage, et Mistral Instruct v0.3 + LM Studio pour la génération de réponses.

## Prérequis

Avant de commencer, assurez-vous d'avoir les éléments suivants installés :

- **Docker** et **Docker Compose**
- **Python 3.x**
- **Streamlit** pour l'interface utilisateur

## Configuration

1. **Cloner le Répertoire**

   Clonez le répertoire contenant les fichiers du projet :

   ```bash
    cd Neo
    docker-compose up -d
    python python pilly_parser.py
    python neo_writer.py
    cd ChatPilly
    streamlit eun Chat_Pilly.py
   ```
