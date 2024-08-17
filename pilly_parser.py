import os
from pdfminer.high_level import extract_text
import re



# Fonction pour extraire le titre du document
def extract_title(text):
    text = text.strip()
    lines = text.split("\n")
    lines = [line.strip() for line in lines if line.strip()]
    if len(lines) >= 3:
        if re.match(r"^\d+$", lines[0]):  # Vérifie que la première ligne est un numéro
            if lines[1].strip().lower() in ["maladies", "syndromes"]:
                title = f"{lines[1].strip().capitalize()} {lines[2].strip()} : "
                return title
    return "Titre non détecté"

# Fonction pour chunker le texte en sections basées sur le format "numéro point espace"
def chunk_all_sections(text, title):
    pattern = r"(\d+\.\s.*?)(?=\n\d+\.\s|\Z)"
    sections = re.findall(pattern, text, re.DOTALL)
    chunks = [title + " " + section.strip() for section in sections]
    return chunks



# Liste pour stocker tous les embeddings

all_chunks = []

# Parcourir tous les fichiers PDF dans le répertoire "minirag-pdf"
for filename in os.listdir("pdfs"):
    if filename.endswith(".pdf"):
        filepath = os.path.join("pdfs", filename)
        print(filepath)
        # Extraire le texte du PDF
        text = extract_text(filepath)
        # Extraire le titre
        title = extract_title(text)
        # Chunker le texte en sections
        chunks = chunk_all_sections(text, title)
        all_chunks.extend(chunks)
        # Générer les embeddings pour chaque chunk


# Initialisation de la liste pour stocker les dictionnaires
result = []

# Boucle sur chaque élément de all_chunks
for chunk in all_chunks:
    # Regex pour extraire la maladie
    maladie_match = re.search(r"Maladies\s+([\w\s]+)\s*:", chunk)
    maladie = maladie_match.group(1).strip() if maladie_match else None

    # Regex pour extraire le chapitre
    chapitre_match = re.search(r"\s+(\d+)\.\s+([\w\s.]+?)(?=\s|\n)", chunk)
    chapitre = chapitre_match.group(2).strip() if chapitre_match else None

    # Extrait le texte restant après le titre et le chapitre
    texte = chunk.split(chapitre_match.group(0))[-1].strip() if chapitre_match else None

    # Vérification que tous les éléments sont présents
    if maladie and chapitre and texte:
        # Créer un dictionnaire pour cet élément
        entry = {
            "Maladie": maladie,
            "Chapitre": chapitre,
            "Texte": texte
        }

        # Ajouter le dictionnaire à la liste résultat
        result.append(entry)

import json
with open("result.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=4)

print("Les résultats ont été écrits dans 'result.json'.")



        