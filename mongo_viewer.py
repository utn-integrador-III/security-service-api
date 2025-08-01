from pymongo import MongoClient

# Cadena de conexión proporcionada
MONGO_URI = "mongodb+srv://utnuser:utnus3r24@cluster0.d9lhmxd.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(MONGO_URI)

# Listar bases de datos
print("Bases de datos disponibles:")
for db_name in client.list_database_names():
    print(f"- {db_name}")
    db = client[db_name]
    # Listar colecciones en cada base de datos
    collections = db.list_collection_names()
    print(f"  Colecciones: {collections}")
    # Mostrar hasta 3 documentos de cada colección
    for coll_name in collections:
        print(f"    Documentos en {coll_name} (máx 3):")
        collection = db[coll_name]
        for doc in collection.find().limit(3):
            print(f"      {doc}") 