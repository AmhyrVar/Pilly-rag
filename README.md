Ceci est un exemple de RAG utilisant Neo4J, Langchain, et Mistral Instruct v0.3 + LM Studio 


Cd Neo
docker-compose up -d
python python pilly_parser.py
python neo_writer.py
cd ChatPilly
streamlit eun Chat_Pilly.py
