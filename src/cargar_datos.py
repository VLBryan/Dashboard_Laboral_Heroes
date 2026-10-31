import os
from typing import List, Dict, Optional
import pandas as pd
from datetime import timedelta, datetime
from pymongo import MongoClient

# Intentamos importar ObjectId para detectar y convertirlo
try:
    from bson import ObjectId
except Exception:
    ObjectId = None

# -------------------------
# Configuración / Conexión
# -------------------------
def get_mongo_client(uri: Optional[str] = None) -> MongoClient:
    uri = uri or os.getenv("MONGO_URI", "mongodb://localhost:27017")
    return MongoClient(uri)

def get_collection_df(client: MongoClient, db_name: str, coll_name: str) -> pd.DataFrame:
    db = client[db_name]
    cursor = db[coll_name].find()
    df = pd.DataFrame(list(cursor))
    return df

# -------------------------
# Cargas
# -------------------------
def load_collections(client: MongoClient, db_name: str, collections: List[str]) -> Dict[str, pd.DataFrame]:
    out = {}
    for c in collections:
        try:
            out[c] = get_collection_df(client, db_name, c)
        except Exception as e:
            print(f"Warning: no se pudo cargar {c}: {e}")
            out[c] = pd.DataFrame()
    return out

# -------------------------
# Cache / persistencia simple
# -------------------------
def save_df_cache(df: pd.DataFrame, path: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, index=False)

def load_df_cache(path: str, con_fecha=True) -> pd.DataFrame:
    df = pd.read_csv(path, index_col=False)
    if con_fecha:
        df["fecha"] = pd.to_datetime(df["fecha"])
    return df


# -------------------------
# Construimos build_all
# -------------------------
def build_all(db_name: str, mongo_uri: Optional[str] = None, cache_dir: str = "./cache") -> Dict[str, pd.DataFrame]:
    client = get_mongo_client(mongo_uri)
    db = client[db_name]

    # -------------------------
    # df de Métricas generales
    # -------------------------
    Usuarios = pd.DataFrame(list(db.users.find({"isActive": True,"invitationCode": {"$exists": True,"$nin": [None, ""]}}, {"user": 1, "firstName": 1, "lastName": 1, "disponibilidad": 1, "modalidad": 1, "location": 1, "rubros": 1})))
    Cvs = pd.DataFrame(list(db.cvs.find({}, {"user": 1, "profession": 1})))
    #Idioma = pd.DataFrame(list(db.languages.find({}, {"user": 1, "language": 1, "level": 1})))

    Usuarios_Master = Usuarios.merge(Cvs, on="user", how="left")


    # -------------------------
    # Guardar en cache
    # -------------------------
    os.makedirs(cache_dir, exist_ok=True)
    save_df_cache(Usuarios_Master, os.path.join(cache_dir, "Usuarios_Master.csv"))
    
    return {
        "df_metricas": Usuarios_Master
    }
