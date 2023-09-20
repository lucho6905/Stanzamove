
Proyecto de Filtrado de Archivos por Entidades en Texto Plano
Este repositorio contiene un script de Python diseñado para procesar archivos de texto plano en busca de entidades específicas y mover los archivos que contienen estas entidades a una ubicación de salida determinada. El proyecto utiliza la biblioteca Stanza para el etiquetado de entidades y proporciona un enfoque eficiente para procesar grandes volúmenes de archivos de texto.

Requisitos
Asegúrate de tener instaladas las siguientes bibliotecas y recursos antes de ejecutar el script:

Python 3.x
Biblioteca Stanza (stanza)
Biblioteca shutil
Biblioteca concurrent.futures
Biblioteca tqdm
Configuración
Antes de ejecutar el script, debes configurar algunos parámetros:

Ruta de la carpeta de entrada (input_folder): Especifica la carpeta que contiene los archivos de texto plano que deseas procesar en busca de entidades. Asegúrate de proporcionar la ruta completa.

Ruta de la carpeta de salida (output_folder): Indica la ubicación donde se moverán los archivos que contienen entidades específicas. Debes proporcionar la ruta completa.

Ruta absoluta del archivo de progreso (ruta_progreso): Esto permite llevar un registro de los archivos ya procesados. Debes proporcionar la ruta completa de un archivo de texto donde se guardará este registro.

Ejecución
Una vez que hayas configurado los parámetros mencionados anteriormente, puedes ejecutar el script. Este realizará las siguientes acciones:

Descargará el modelo de idioma en inglés necesario para el etiquetado de entidades utilizando Stanza.

Escaneará de manera recursiva la carpeta de entrada en busca de archivos de texto plano.

Verificará si los archivos contienen entidades específicas, como personas (PERSON), organizaciones (ORG), lugares (GPE), direcciones de correo electrónico (EMAIL), URL, números de teléfono (PHONE), identificadores (ID) y términos médicos (MEDICAL).

Si un archivo contiene alguna de estas entidades, se moverá a la carpeta de salida especificada.

Mantendrá un registro de los archivos procesados para evitar duplicados.

Proporcionará una barra de progreso para seguir el avance del procesamiento.

Consideraciones adicionales
El script utiliza hilos para acelerar el procesamiento de múltiples archivos de manera concurrente, lo que lo hace eficiente para grandes conjuntos de datos.

Puedes personalizar la lista de entidades específicas que deseas buscar en los archivos modificando la lista ["PERSON", "ORG", "GPE", "EMAIL", "URL", "PHONE", "ID", "MEDICAL"] en el script.

El script es adecuado para archivos de texto plano, por lo que asegúrate de que los archivos en la carpeta de entrada sean compatibles con este formato.

A medida que el script procesa archivos, se actualizará el archivo de progreso, lo que permite detener y reiniciar el proceso en cualquier momento sin perder el progreso.
