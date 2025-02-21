#Para poder ejecutar el venv para poder usar el api hacer lo siguiente

#envscode en terminal:
#1. Ejecutar el siguiente script: python -m venv venv
#2. Ejecutar el siguiente script: source venv//bin/activate
#3. Ejecutar el siguiente script: pip instal -r requirements.txt
#4. Modificar el archivo .env que se encuentra en la carpeta raíz:
    #a. DATABASE_URL="postgresql://carlos:1234@127.0.0.1:5432/globant"
    #b. CSV_UPLOAD_DIR="./uploads"
#5. Inicializar el servicio: uvicorn app.main:app --reload
#6. Entrar en la siguienmte ruta en el navegador: http://127.0.0.1:8000/docs
#7. En la primera parte estará la interfaz para poder cargar los archivos, en el espacio de file_type escribir "hired, departments o jobs" cualquiera de estas 3 palabras. //
//  Cargar el archivo de formato .csv hired, department o job para ser cargado.
#8. Ejecutar y verificar que se cargó adecuadamente el archivo.
#9. en las siguientes dos pestañas se encontrarán las consultas a base de datos que extraerá la información solicitada en este challenge.

#Muchas gracias