import psycopg2

try:
    # Parámetros de conexión a la base de datos globant y schema test_globant
    conn = psycopg2.connect(
        database="globant",
        user="postgres",
        password="CeacZick129661.2025",
        host="127.0.0.1",
        port="5432"
    )

    print("¡Conexión exitosa a la base de datos!")

    # Crear un cursor
    cursor = conn.cursor()
    
    # Establecer el schema test_globant
    cursor.execute('SET search_path TO test_globant')
    
    # Verificar en qué base de datos y schema estamos
    cursor.execute('SELECT current_database(), current_schema()')
    db_info = cursor.fetchone()
    print(f"\nBase de datos conectada: {db_info[0]}")
    print(f"Schema actual: {db_info[1]}")
    
    # Listar todas las tablas en el schema test_globant
    cursor.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'test_globant'
        AND table_type = 'BASE TABLE'
    """)
    
    tables = cursor.fetchall()
    print("\nTablas encontradas en el schema test_globant:")
    for table in tables:
        # Mostrar estructura de cada tabla
        cursor.execute(f"""
            SELECT column_name, data_type, character_maximum_length
            FROM information_schema.columns
            WHERE table_schema = 'test_globant'
            AND table_name = '{table[0]}'
        """)
        columns = cursor.fetchall()
        
        print(f"\nEstructura de la tabla {table[0]}:")
        for col in columns:
            length = f"({col[2]})" if col[2] else ""
            print(f"- {col[0]}: {col[1]}{length}")

except Exception as e:
    print("Error de conexión:")
    print(e)

finally:
    # Cerrar cursor y conexión
    if 'cursor' in locals():
        cursor.close()
    if 'conn' in locals():
        conn.close()
    print("\nConexión cerrada.")