from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv(encoding='latin1')  # Cambiar encoding

# Obtener URL de la base de datos
DATABASE_URL = os.getenv("DATABASE_URL")
print("Intentando conectar a la base de datos...")
print(f"URL de conexión: {DATABASE_URL}")

try:
    # Crear el engine
    engine = create_engine(DATABASE_URL, echo=True)
    
    # Intentar conectarse
    with engine.connect() as connection:
        print("\n¡Conexión exitosa!")
        
        # Probar una consulta simple
        result = connection.execute(text("SELECT current_database()"))
        db_name = result.scalar()
        print(f"Base de datos conectada: {db_name}")
        
except Exception as e:
    print("\nError de conexión:")
    print(type(e).__name__, ":", str(e))