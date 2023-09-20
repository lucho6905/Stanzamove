import os
import stanza
import shutil
import concurrent.futures
from tqdm import tqdm

# Configuración de Stanza para etiquetado de entidades
stanza.download("en")  # Descarga el modelo de idioma en inglés
nlp = stanza.Pipeline("en", processors="tokenize,ner")

# Función para verificar si hay entidades específicas en un archivo
def tiene_entidades(archivo, entidades):
    with open(archivo, "r", encoding="utf-8") as f:
        texto = f.read()

    # Procesar el texto para etiquetar entidades
    doc = nlp(texto)

    # Verificar si hay entidades específicas
    for entity in doc.ents:
        if entity.type in entidades:
            return True

    return False

# Ruta de la carpeta de entrada y salida
input_folder = "C:/Users/lucho/OneDrive/Documentos/Nueva carpeta/clapgruphackingEnTextoplano/"
output_folder = "C:/Users/lucho/OneDrive/Documentos/Nueva carpeta/clapgruphackingfiltradosyordenados/filtrados/a"

# Ruta absoluta del archivo de progreso en la ubicación deseada
ruta_progreso = "C:/Users/lucho/Downloads/Nueva/progreso.txt"

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

        # Verificar si hay entidades específicas
        tiene_entidades_result = tiene_entidades(archivo_path, ["PERSON", "ORG", "GPE", "EMAIL", "URL",
                                                                "PHONE", "ID", "MEDICAL"])

        # Mover el archivo si tiene entidades
        if tiene_entidades_result:
            print(f"Moviendo archivo: {archivo_path}")  # Mensaje de depuración

            # Mover el archivo
            nuevo_path = os.path.join(output_folder, os.path.relpath(archivo_path, input_folder))
            shutil.move(archivo_path, nuevo_path)

        # Registrar el archivo como procesado
        archivos_procesados.append(archivo_path)

        # Actualizar el registro de progreso
        with open(ruta_progreso, "a") as f:
            f.write(archivo_path + "\n")

        archivos_procesados_count += 1
        pbar.update(1)

print("Proceso completado.")