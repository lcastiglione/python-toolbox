"""Funciones varias"""

import string
import random
import sys
import re
import json
import base64
from typing import List
import uuid
from io import BytesIO
from zipfile import ZipFile, ZIP_DEFLATED


def remove_special_characters(text: str, special_chars: List[str]=None) -> str:
    """
    Remueve caracteres especiales de un texto.

    Args:
        text (str): El texto del cual se desea remover los caracteres especiales.
        special_chars (List[str]): Una lista de caracteres especiales a remover.

    Returns:
        str: El texto sin los caracteres especiales.
    """
    if not special_chars:
        special_chars = ['\r', '\n', '\t']
    for char in special_chars:
        text = text.replace(char, '')
    return text

def remove_residual_chars(txt: str) -> str:
    """
    Elimina caracteres residuales de una cadena de texto.

    Args:
        txt (str): La cadena de texto.

    Returns:
        str: La cadena de texto sin caracteres residuales.
    """
    return remove_special_characters(txt,['\r','\n','\t',' '])

def get_size(obj: object, seen: set = None) -> int:
    """
    Obtiene el tamaño en bytes de un objeto.

    Args:
        obj (object): El objeto del cual se desea obtener el tamaño.
        seen (set, optional): Un conjunto de objetos ya revisados para evitar recursión infinita.

    Returns:
        int: El tamaño en bytes del objeto.
    """
    size = sys.getsizeof(obj)
    if seen is None:
        seen = set()
    obj_id = id(obj)
    if obj_id in seen:
        return 0
    # Importante marcar como visto *antes* de entrar en recursión para manejar correctamente
    # los objetos autoreferenciales.
    seen.add(obj_id)
    if isinstance(obj, dict):
        size += sum([get_size(v, seen) for v in obj.values()])
        size += sum([get_size(k, seen) for k in obj.keys()])
    elif hasattr(obj, '__dict__'):
        size += get_size(obj.__dict__, seen)
    elif hasattr(obj, '__iter__') and not isinstance(obj, (str, bytes, bytearray)):
        size += sum([get_size(i, seen) for i in obj])
    return size


def random_string(length: int = 15) -> str:
    """
    Genera una cadena de texto aleatoria.

    Args:
        length (int, optional): La longitud de la cadena de texto. Defaults to 15.

    Returns:
        str: La cadena de texto aleatoria generada.
    """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


def get_id() -> str:
    """
    Genera un identificador único (UUID).

    Returns:
        str: El identificador único generado.
    """
    return str(uuid.uuid4())


def write_json_file(path: str, data: dict, encoding: str = 'utf-8') -> None:
    """
    Escribe un diccionario en un archivo JSON.

    Args:
        path (str): La ruta del archivo JSON.
        data (dict): El diccionario a escribir en el archivo.
        encoding (str, optional): Encoding de los datos. Por default está en 'utf-8'.
    """
    with open(path, 'w', encoding=encoding) as file:
        json.dump(data, file, ensure_ascii=False, default=str)


def read_json_file(path: str, encoding: str = 'utf-8') -> dict:
    """
    Lee un archivo JSON y devuelve su contenido como un diccionario.

    Args:
        path (str): La ruta del archivo JSON.
        encoding (str, optional): Encoding de los datos. Por default está en 'utf-8'.

    Returns:
        dict: El contenido del archivo JSON como un diccionario.
    """
    with open(path, encoding=encoding) as file:
        return json.loads(file.read())

def write_file(path:str, data:str,encoding: str = 'utf-8',method:str="w") -> None:
    """Escribe un archivo de texto con la posibilidad de agregar contenido a un archivo existente.

    Args:
        path (str): La ruta del archivo JSON.
        data (str): Datos a escribir
        encoding (str, optional): Encoding de los datos. Por default está en 'utf-8'.
        method (str, optional): Método de escritura. Con 'w' es escribe todo de cero y con 'a' se
        agrega contenido al que ya está. Por default está en "w".
    """
    with open(path, method, encoding=encoding) as outfile:
        outfile.write(data)


def read_file(path:str, encoding: str = 'utf-8') -> str:
    """
    Lee un archivo de texto y devuelve su contenido.

    Args:
        path (str): La ruta del archivo de texto.
        encoding (str, optional): Encoding de los datos. Por default está en 'utf-8'.

    Returns:
        dict: El contenido del archivo de texto.
    """
    with open(path, encoding=encoding) as file:
        return file.read()

def is_file_exist(path: str, encoding: str = 'utf-8') -> bool:
    """
    Verifica si un archivo existe en la ruta especificada.

    Args:
        path (str): La ruta del archivo.

    Returns:
        bool: True si el archivo existe, False en caso contrario.
    """
    try:
        with open(path, encoding=encoding):
            return True
    except IOError:
        return False


def remove_bom_mark(filename: str) -> None:
    """
    Elimina la marca de orden de bytes (BOM) de un archivo.

    Args:
        filename (str): El nombre del archivo.
    """
    with open(filename, mode='rt', encoding='utf-8-sig') as file:
        contenido = file.read()

    with open(filename, mode='wt', encoding='utf-8') as file:
        file.write(contenido)


def decompress(file: bytes) -> dict:
    """
    Extrae los archivos de un archivo comprimido (ZIP) en memoria.

    Args:
        file (bytes): El archivo comprimido en memoria.

    Returns:
        dict: Un diccionario que contiene los nombres de los archivos y sus contenidos como bytes.
    """
    input_zip = ZipFile(BytesIO(file))
    return {name: input_zip.read(name) for name in input_zip.namelist()}


def compress(files: dict) -> bytes:
    """
    Comprime los archivos en un archivo ZIP en memoria.

    Args:
        files (dict): Un diccionario que contiene los nombres de los archivos y sus contenidos como bytes.

    Returns:
        bytes: El archivo ZIP comprimido en memoria.
    """
    mem_zip = BytesIO()
    with ZipFile(mem_zip, mode="w", compression=ZIP_DEFLATED) as zip_file:
        _ = [zip_file.writestr(name, content) for name, content in files.items()]
    return mem_zip.getvalue()


def bytes_to_base64(data: bytes) -> str:
    """
    Convierte datos en formato bytes a una cadena de texto en formato Base64.

    Args:
        data (bytes): Los datos en formato bytes.

    Returns:
        str: Los datos en formato Base64.
    """
    return base64.b64encode(data).decode('utf-8')


def base64_to_bytes(data: str) -> bytes:
    """
    Convierte una cadena de texto en formato Base64 a datos en formato bytes.

    Args:
        data (str): Los datos en formato Base64.

    Returns:
        bytes: Los datos en formato bytes.
    """
    return base64.b64decode(data.encode('utf-8'))


def is_office_file(name: str) -> str:
    """
    Verifica si el nombre de un archivo corresponde a un archivo de Microsoft Office.

    Args:
        name (str): El nombre del archivo.

    Returns:
        str: La extensión del archivo si es un archivo de Microsoft Office, None en caso contrario.
    """
    extensions = ['doc', 'docx', 'ppt', 'pptx', 'xls', 'xlsx']
    ext = name.split('.')[-1]
    return ext if ext in extensions else None


def get_json_pretty(data: dict) -> str:
    """
    Obtiene una representación en formato JSON con formato legible para humanos.

    Args:
        data (dict): El diccionario a representar en formato JSON.

    Returns:
        str: La representación en formato JSON con formato legible para humanos.
    """
    return json.dumps(data, indent=4, default=str, ensure_ascii=False)


def print_json(data: dict) -> None:
    """
    Imprime un diccionario en formato JSON con formato legible para humanos.

    Args:
        data (dict): El diccionario a imprimir en formato JSON.
    """
    print(get_json_pretty(data))
