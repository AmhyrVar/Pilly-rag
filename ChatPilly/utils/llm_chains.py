from sentence_transformers import SentenceTransformer
from neo4j import GraphDatabase
import numpy as np
from scipy.spatial.distance import cosine
from langchain import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

from langchain_community.llms import HuggingFaceEndpoint

"""llm = HuggingFaceEndpoint(
    huggingfacehub_api_token="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",
    repo_id="mistralai/Mistral-7B-Instruct-v0.3",
    task="text-generation",
    max_new_tokens=512,
    top_k=30,
    temperature=0.01,
    repetition_penalty=1.03,
)"""


# Connexion à la base de données Neo4j
url = "bolt://localhost:7687"
username = "neo4j"
password = "781227pAssWord!"
driver = GraphDatabase.driver(url, auth=(username, password))

# Charger le modèle de vecteurs
model = SentenceTransformer('FremyCompany/BioLORD-2023-M')

# Initialisation de l'API OpenAI
llm = OpenAI(base_url="http://localhost:1234/v1", api_key='YOUR_OPENAI_API_KEY', temperature=0.0, max_tokens=4048)

def get_embedding(text):
    """Génère un embedding pour le texte donné."""
    return model.encode(text).tolist()

def get_all_embeddings(tx):
    """Récupère tous les embeddings des nœuds Maladie depuis la base de données Neo4j."""
    result = tx.run("MATCH (m:Maladie) RETURN m.name AS name, m.embeddings AS embeddings")
    return {record["name"]: np.array(record["embeddings"]) for record in result}

def find_closest_maladie(query_embedding, embeddings):
    """Trouve le nœud Maladie le plus proche en utilisant l'embedding."""
    closest_name = None
    min_distance = float('inf')

    for name, embedding in embeddings.items():
        distance = cosine(query_embedding, embedding)
        if distance < min_distance:
            min_distance = distance
            closest_name = name

    return closest_name, min_distance

def get_chunk_texts(tx, maladie_name):
    """Récupère les textes des nœuds chunk en relation avec le nœud Maladie."""
    query = """
    MATCH (m:Maladie {name: $name})-[:CONTAINS]->(c:Chunk)
    RETURN c.texte AS texte
    """
    result = tx.run(query, name=maladie_name)
    return [record["texte"] for record in result]

def generate_answer(query, context):
    """Utilise un modèle de langage pour générer une réponse basée sur le contexte."""
    # Créer le template de prompt
    prompt_template = PromptTemplate(
        input_variables=["context", "query"],
        template="""
        Vous êtes une agent LLM qui exécute des tâches.
        Répondez à la question suivante en utilisant les informations se rapportant à la question fournies dans le contexte et jugées pertinentes.
        Répondez de manière synthétique et concise comlpète sans répétitions.
        
        Contexte : {context}
        
        Question : {query}
        
        Réponse :
        """
    )

    # Initialiser la chaîne LLM avec le prompt template
    chain = LLMChain(llm=llm, prompt=prompt_template)

    # Générer la réponse
    answer = chain.run({"context": context, "query": query})

    return answer

def generate_response_cypher(query):
    query_embedding = get_embedding(query)
    
    with driver.session() as session:
        # Récupérer tous les embeddings des nœuds Maladie
        all_embeddings = session.read_transaction(get_all_embeddings)
        
        # Trouver la maladie la plus proche
        closest_maladie, similarity = find_closest_maladie(query_embedding, all_embeddings)
        
        if closest_maladie:
            print(f"Maladie la plus proche : {closest_maladie}")
            print(f"Distance cosinus : {similarity:.4f}")
            
            # Récupérer les textes des nœuds chunk associés
            chunk_texts = session.read_transaction(get_chunk_texts, closest_maladie)
            context = "\n\n".join(chunk_texts)
            
            # Générer la réponse en utilisant le contexte
            answer = generate_answer(query, context)
            driver.close()
            return answer
        else:
            driver.close()
            return "Aucune maladie trouvée."
    


    