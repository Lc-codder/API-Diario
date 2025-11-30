from db import DB, seed_if_empty

db = DB("database.db")
seed_if_empty(db)
db.close()

print("Seed aplicado com sucesso!")