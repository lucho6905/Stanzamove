import os
import stanza
import shutil
import concurrent.futures
from tqdm import tqdm

# Configuración de Stanza para etiquetado de entidades
stanza.download("en")  # Descarga el modelo de idioma en inglés
nlp = stanza.Pipeline("en", processors="tokenize,ner")

# Función para verificar si hay entidades específicas en un texto
def tiene_entidades(texto, entidades):
    # Procesar el texto para etiquetar entidades
    doc = nlp(texto)

    # Verificar si hay entidades específicas
    for entity in doc.ents:
        if entity.type in entidades:
            return True

    return False

# Ruta de la carpeta de entrada y salida
input_folder = "CARPETA DE ENTRADA"
output_folder = "CARPETA DE SALIDA"

# Ruta absoluta del archivo de progreso en la ubicación deseada
ruta_progreso = "progreso.txt"

# Tamaño del fragmento en caracteres
tamaño_fragmento = 10000  # Ajusta el tamaño del fragmento según tus necesidades

# Lista de archivos a procesar
archivos_a_procesar = []

# Recorrer recursivamente la carpeta de entrada y agregar archivos a la lista
for root, dirs, files in os.walk(input_folder):
    for filename in files:
        archivo_path = os.path.join(root, filename)
        archivos_a_procesar.append(archivo_path)

# Si el archivo de progreso existe, leer la lista de archivos procesados
archivos_procesados = []
if os.path.exists(ruta_progreso):
    with open(ruta_progreso, "r") as f:
        archivos_procesados = [line.strip() for line in f]

# Filtrar la lista de archivos a procesar para omitir los ya procesados
archivos_a_procesar = [archivo for archivo in archivos_a_procesar if archivo not in archivos_procesados]

# Calcular el progreso total
total_archivos = len(archivos_a_procesar)
archivos_procesados_count = len(archivos_procesados)

# Procesar los archivos restantes
with concurrent.futures.ThreadPoolExecutor() as executor, tqdm(total=total_archivos) as pbar:
    for archivo_path in archivos_a_procesar:
        print(f"Procesando archivo: {archivo_path}")  # Mensaje de depuración

        # Leer el archivo completo
        with open(archivo_path, "r", encoding="utf-8") as file:
            texto_completo = file.read()

        # Dividir el texto en fragmentos de tamaño específico
        fragmentos = [texto_completo[i:i+tamaño_fragmento] for i in range(0, len(texto_completo), tamaño_fragmento)]

        # Flag para determinar si se encontraron entidades en el archivo actual
        entities_found = False

        # Procesar fragmentos
        for fragmento in fragmentos:
            if tiene_entidades(fragmento, ["PERSON", "ORG", "GPE", "EMAIL", "URL", "PHONE", "ID", "MEDICAL"]):
                entities_found = True
                break  # Detener el procesamiento si se encuentran entidades

        # Crear el directorio de destino si no existe
        nuevo_path = os.path.join(output_folder, os.path.relpath(archivo_path, input_folder))
        os.makedirs(os.path.dirname(nuevo_path), exist_ok=True)

        # Mover el archivo si se encontraron entidades
        if entities_found:
            print(f"Moviendo archivo: {archivo_path}")  # Mensaje de depuración

            # Mover el archivo
            shutil.move(archivo_path, nuevo_path)

        # Registrar el archivo como procesado
        archivos_procesados.append(archivo_path)

        # Actualizar el registro de progreso
        with open(ruta_progreso, "a") as f:
            f.write(archivo_path + "\n")

        archivos_procesados_count += 1
        pbar.update(1)

print("Proceso completado.")

