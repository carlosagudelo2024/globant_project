import psycopg2

# Define las credenciales directamente en el código
db_username = 'carlos'
db_password = '1234'  # Aquí incluye tu contraseña real

# Establece la conexión con la base de datos
conn = psycopg2.connect(
    dbname='test_globant',
    user=db_username,
    password=db_password,
    host='127.0.0.1@5432'
)
print("Conexión exitosa")
conn.close()