import json
from neo4j import GraphDatabase

# Connexion à la base de données Neo4j
uri = "bolt://localhost:7687"
username = "neo4j"
password = "781227pAssWord!"
driver = GraphDatabase.driver(uri, auth=(username, password))

def create_maladie_and_chunks(tx, maladie, chapitre, texte):
    # Vérifier si le nœud Maladie existe déjà
    query = (
        "MERGE (m:Maladie {name: $name}) "
        "ON CREATE SET m.created_at = datetime() "
        "RETURN m"
    )
    tx.run(query, name=maladie)

    # Créer un nœud Chunk pour chaque chapitre et texte
    query = (
        "MERGE (m:Maladie {name: $maladie}) "
        "MERGE (c:Chunk {chapitre: $chapitre, texte: $texte}) "
        "MERGE (m)-[:CONTAINS]->(c)"
    )
    tx.run(query, maladie=maladie, chapitre=chapitre, texte=texte)

def main(json_file):
    with open(json_file, 'r', encoding='utf-8') as file:
        data = json.load(file)

    with driver.session() as session:
        for entry in data:
            maladie = entry.get('Maladie')
            chapitre = entry.get('Chapitre', '')
            texte = entry.get('Texte', '')

            if maladie:
                # Assurer que le texte est correctement encodé en UTF-8
                # Note: En général, vous ne devriez pas avoir besoin de cette ligne si les fichiers sont déjà en UTF-8.
                texte = texte.encode('utf-8').decode('utf-8')

                session.write_transaction(create_maladie_and_chunks, maladie, chapitre, texte)

if __name__ == "__main__":
    main("result.json")
    driver.close()