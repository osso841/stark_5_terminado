
import json
import re

#crear funcion normalizar datos. sin ella no se podra generar el json

#PUNTO 1.1
def leer_archivo(path:str) -> str:
    """ abre un archivo en modo lectura y devuelve el archivo encontrado.
        param:
            path(str): ruta de acceso al archivo y extension
        return:
            str: el contenido del archivo asignado. en caso de error devuelve un mensaje de error
    """
    try:
        with open(path, "r", encoding="UTF-8") as archivo:
            retorno = archivo.read()
    except FileNotFoundError as e:
        print(f"no se ha encontrado el archivo: {e}")
        retorno =''
    except Exception as e:
        print(f"error: {e}")
        retorno =''
    finally:
        return retorno
    
    
#PUNOT 1.2
def guardar_archivo(path:str, contenido:str) -> str: 
    """ funcion que crea (en caso de no existir) un archivo de texto. si el archivo existe, lo sobreescribe
        param:
            path(str): ruta de acceso donde se guardara el archivo
            contenido(str): contenido nuevo del archivo

        return:
            bool: estado booleano que verifica si un archivo fue modificado correctamente (true) o no (false)
    """
    try:
        retorno = True
        with open(path, "w+", encoding="UTF-8") as archivo:
            archivo.write(contenido)
        print(f"se creo el archivo {path}")
    except Exception:
        print(f"Error al crear el archivo: {path}")
        retorno = False
    finally:
        return retorno
    
#PUNTO 1.3
def generar_csv(path:str, lista:list[dict]) -> False:
    '''generador de csv a partir de una lista de diccionarios. 
        param:
            path(str): ruta donde se generara el csv
            lista(list[dict]): lista de de diccionarios a transformar
        
        return:
            False: si la lista se encuentra vacia
            None: si el proceso fue exitoso

    '''
    claves_personajes = []
    cuerpo = ''
    try:
        if lista:
            for heroes in lista:
                for clave in heroes.keys():
                    if not clave in claves_personajes:
                        claves_personajes.append(clave)

            encabezado = ",".join(claves_personajes) + "\n"

            for pos_heroe in range(len(lista)):
                mensaje = ''
                for valores in lista[pos_heroe].values():
                    mensaje += str(valores) + ','

                if pos_heroe != len(lista) - 1:
                    mensaje = mensaje[:-1] + "\n"
                    cuerpo += mensaje
                else:
                    mensaje = mensaje[:-1]
                    cuerpo += mensaje
                    

            texto_csv = encabezado + cuerpo
            guardar_archivo(path, texto_csv)
        else:
            print("la lista a utilizar se encuentra vacia")
            return False
    except Exception as e:
        print(f"error: {e}")


#PUNTO 1.4
def leer_csv(path:str) -> list[dict]:
    ''' genera una lista a partir de un archivo csv
        param:
            path(str): ruta del archivo a generar
        return:
            list[dict]: lista de diccionarios que representa a los personajes
    '''
    nueva_lista = []

    archivo = leer_archivo(path)
    lista_heroes = archivo.split('\n')
    
    encabezado = lista_heroes[0]
    encabezado = encabezado.split(',')
    lista_heroes.pop(0)

    for heroe in lista_heroes:
        caracteristicas = heroe.split(',')
        diccionario_heroe = {}
        for clave, valor in zip(encabezado, caracteristicas):
            diccionario_heroe[clave] = valor
        nueva_lista.append(diccionario_heroe)

    if nueva_lista:
        retorno = nueva_lista
    else:
        retorno = False

    return retorno

#PUNTO 1.5
def generar_json(path:str, lista:list[dict], nombre_lista:str) -> None:
    ''' crea un archivo json a partir de una lista de diccionarios
        param:
            path(str): ruta del archivo json
            lista(list[dict]): lista de diccionarios que sera estructurado 
            nombre_lista(str): nombre que tendra la lista en el archivo json

        returno:
            None
    '''
    json_generado = {}
    json_generado[nombre_lista] = []
    for heroes in lista:
        json_generado[nombre_lista].append(heroes)
    
    with open(path, "w+", encoding="UTF-8") as archivo:
        json.dump(json_generado, archivo, indent=4)


#PUNTO 1.6
def leer_json(path:str, nombre_lista:str) -> list:
    ''' devuelve una lista de nombre determinado
        param:
            path(str): ruta del archivo json
            nombre_lista: nombre de la lista en el archivo json
        return:
            list: lista de diccionarios
    '''

    try:
        with open(path, "r", encoding="UTF-8") as archivo:
            lista = json.load(archivo)
        retorno = lista[nombre_lista]
    except FileNotFoundError as e:
        print(f"no se ha encotrado la carpeta: {e}")
        retorno = False
    except Exception as e:
        print(f"error identificado: {e}")
        retorno = False
    finally:
        return retorno
    
#PUNTO 2.1
def ordenar_json_ascendente(elemento:str, clave:str, nombre_lista:str) -> None:
    ''' ordena un archivo json de forma ascendente con respecto a una clave especifica
        param:
            elemento (str): Ruta del archivo JSON a ordenar.
            clave (str): Clave según la cual se realizará la ordenación ascendente.
            nombre_lista (str): Nombre de la lista en el archivo JSON.

        Return:
            None: La función modifica el archivo JSON en su lugar, no devuelve ningún valor.

    '''
    list_json = leer_json(elemento, nombre_lista)
    if list_json:
        try:
            for i in range(len(list_json)-1):
                for j in range(i+1, len(list_json)):
                    if float(list_json[i][clave]) > float(list_json[j][clave]):
                        aux = list_json[i]
                        list_json[i] = list_json[j]
                        list_json[j] = aux
            generar_json(elemento, list_json, nombre_lista)
        except Exception as e:
            print(f"error identificado: {e}")
            print(f"no se pudo ordenar el archivo json de manera ascendente")
    else:
        print('no se puede ordenar el archivo json de manera ascendente.')

def ordenar_csv_ascendente(elemento:str, clave:str) ->None:
    ''' ordena un archivo csv de forma ascendente con respecto a una clave especifica
        param:
            elemento (str): Ruta del archivo CSV a ordenar.
            clave (str): Clave según la cual se realizará la ordenación ascendente.

        Return:
            None: La función modifica el archivo CSV en su lugar, no devuelve ningún valor.

    '''
    lista_csv = leer_csv(elemento)
    if lista_csv:
        try:
            for i in range(len(lista_csv)-1):
                for j in range(i+1, len(lista_csv)):
                    if float(lista_csv[i][clave]) > float(lista_csv[j][clave]):
                        aux = lista_csv[i]
                        lista_csv[i] = lista_csv[j]
                        lista_csv[j] = aux
            generar_csv(elemento, lista_csv)
        except Exception as e:
            print(f"error identificado: {e}")
            print(f"no se pudo ordenar el archivo csv de manera ascendente")
    else:
        print('No se pudo ordenar el archivo csv de manera ascendente.')


def ordenar_clave_numerica_ascendente(elemento:str, clave:str, nombre_lista="") -> None:
    ''' Ordena un archivo en formato JSON o CSV de forma ascendente con respecto a una clave numérica específica.

        Param:
            elemento (str): Ruta del archivo a ordenar.
            clave (str): Clave numérica según la cual se realizará la ordenación ascendente.
            nombre_lista (str): Nombre de la lista en el archivo JSON (ignorado para archivos CSV).

        Nota:
            La clave debe ser numérica para realizar una ordenación ascendente adecuada.

        Return:
            None

    '''
    if type(elemento) == str:
        patron_extension = '\.(json|csv)$'
        extension = re.search(patron_extension, elemento)

        if extension is not None:
            if extension.group() == '.json':
                ordenar_json_ascendente(elemento, clave, nombre_lista)        
            elif extension.group() == '.csv':
                ordenar_csv_ascendente(elemento, clave)
        else:
            print("el archivo ingresado no se de extension .json o .csv")
            

#PUNTO 2.2
def ordenar_json_descendente(elemento:str, clave:str, nombre_lista:str) -> None:
    ''' ordena un archivo json de forma descendente con respecto a una clave especifica
        param:
            elemento (str): Ruta del archivo JSON a ordenar.
            clave (str): Clave según la cual se realizará la ordenación descendente.
            nombre_lista (str): Nombre de la lista en el archivo JSON.

        Return:
            None: La función modifica el archivo JSON en su lugar, no devuelve ningún valor.

    '''
    list_json = leer_json(elemento, nombre_lista)
    if list_json:
        try:
            for i in range(len(list_json)-1):
                for j in range(i+1, len(list_json)):
                    if float(list_json[i][clave]) < float(list_json[j][clave]):
                        aux = list_json[i]
                        list_json[i] = list_json[j]
                        list_json[j] = aux
            generar_json(elemento, list_json, nombre_lista)
        except Exception as e:
            print(f"error identificado: {e}")
            print(f"no se pudo ordenar el archivo json de manera descendente")
    else:
        print('no se puede ordenar el archivo json de manera descendente.')


def ordenar_csv_descendente(elemento:str, clave:str) ->None:
    ''' ordena un archivo csv de forma descendente con respecto a una clave especifica
        param:
            elemento (str): Ruta del archivo CSV a ordenar.
            clave (str): Clave según la cual se realizará la ordenación descendente.

        Return:
            None: La función modifica el archivo CSV en su lugar, no devuelve ningún valor.

    '''
    lista_csv = leer_csv(elemento)
    if lista_csv:
        try:
            for i in range(len(lista_csv)-1):
                for j in range(i+1, len(lista_csv)):
                    if float(lista_csv[i][clave]) < float(lista_csv[j][clave]):
                        aux = lista_csv[i]
                        lista_csv[i] = lista_csv[j]
                        lista_csv[j] = aux
            generar_csv(elemento, lista_csv)
        except Exception as e:
            print(f"error identificado: {e}")
            print(f"no se pudo ordenar el archivo csv de manera descendente")
    else:
        print('No se pudo ordenar el archivo csv de manera descendente.')


def ordenar_clave_numerica_descendente(elemento:str, clave:str, nombre_lista:str) -> None:
    ''' Ordena un archivo en formato JSON o CSV de forma descendente con respecto a una clave numérica específica.

        Param:
            elemento (str): Ruta del archivo a ordenar.
            clave (str): Clave numérica según la cual se realizará la ordenación descendente.
            nombre_lista (str): Nombre de la lista en el archivo JSON (ignorado para archivos CSV).

        Nota:
            La clave debe ser numérica para realizar una ordenación descendente adecuada.

        Return:
            None

    '''
    if type(elemento) == str:
        patron_extension = '\.(json|csv)$'
        extension = re.search(patron_extension, elemento)

        if extension is not None:
            if extension.group() == '.json':
                ordenar_json_descendente(elemento, clave, nombre_lista)        
            elif extension.group() == '.csv':
                ordenar_csv_descendente(elemento, clave)
        else:
            print("el archivo ingresado no se de extension .json o .csv")


#PUNTO 2.3
def ordenar_clave_numerica(elemento:str, clave:str, orden:str, nombre_lista="") -> None:
    ''' Ordena un archivo en formato JSON o CSV de forma ascendente o descendente con respecto a una clave numérica específica.

        Param:
            elemento (str): Ruta del archivo a ordenar.
            clave (str): Clave numérica según la cual se realizará la ordenación.
            orden (str): Orden de la clasificación, puede ser "asc" para ascendente o "desc" para descendente.
            nombre_lista (str, opcional): Nombre de la lista en el archivo JSON (ignorado para archivos CSV).

        Excepciones:
            Se imprime un mensaje si la extensión del archivo no es compatible o si la ordenación especificada no es válida.

        Return:
            None: La función modifica el archivo en su lugar, no devuelve ningún valor.
    '''

    if orden == "asc":
        ordenar_clave_numerica_ascendente(elemento, clave, nombre_lista)
    elif orden ==  "desc":
        ordenar_clave_numerica_descendente(elemento, clave, nombre_lista)
    else:
        print("orden incorrecto")


#PUNTO 3.0
def normalizar_datos(lista:list[dict]) -> bool:
    for heroe in lista:
        if type(heroe["altura"]) == str or type(heroe["peso"]) == str or type(heroe["fuerza"]) == str:
            heroe["altura"] = float(heroe["altura"])
            heroe["peso"] = float(heroe["peso"])
            heroe["fuerza"] = int(heroe["fuerza"])
            retorno = True
        else:
            retorno = False
    
    return retorno


def validar_respuesta() -> int:
    opcion = input("seleccione una opcion: ")
    if opcion.isdigit():
        opcion = int(opcion)
    else:
        opcion = None
    
    return opcion


def generar_menu_opciones(patron:str, cantidad:int):
    menu = '''● 1-Normalizar datos 
● 2-Generar CSV
● 3-Listar heroes del archivo CSV ordenados por altura ASC
● 4-Generar JSON
● 5-Listar heroes del archivo JSON ordenados por peso DESC
● 6-Ordenar Lista por fuerza
● 7-Salir
''' 
    print(patron*cantidad)
    print(menu)
    print(patron*cantidad)
    

def stark_app_005(lista:list[dict]):
    estado = None

    while True:
        generar_menu_opciones("*", 50)
        opcion = validar_respuesta()

        match opcion:
            case 1: #NORMALIZAR DATOS
                estado = normalizar_datos(lista)
                if estado:
                    print("datos normalizados")
                else:
                    print("los datos ya han sido normalizados")

            case 2: # GENERAR CSV
                if estado is not None:
                    generar_csv("miarchivocsv.csv",lista)
                else:
                    print("los datos no han sido normalizados")

            case 3: # LISTAR HEROES DEL ARCHIVO CSV ORDENADOS POR ALTURA ASC
                if estado is not None:
                    ordenar_clave_numerica("miarchivocsv.csv", "altura", "asc")
                else:
                    print("los datos no han sido normalizados")

            case 4: #GENERAR JSON
                if estado is not None:
                    generar_json("miarchivojson.json",lista, "personajes")
                else:
                    print("los datos no han sido normalizados")

            case 5: # LISTAR HEROES DEL ARCHIVO JSON ORDENADOS POR PESO DESC
                if estado is not None:
                    ordenar_clave_numerica("miarchivojson.json", "peso", "desc", "personajes")
                else:
                    print("los datos no han sido normalizados")
            case 6:  # ORDENAR LISTA POR FUERZA 
                if estado is not None:
                    opc_orden = input('orden ascendente (asc) | orden descendente (desc): ')
                    opc_archivo = input('ingrese el archivo que desea ordenar: ')
                    ordenar_clave_numerica(opc_archivo, 'fuerza', opc_orden, "personajes")
                else:
                    print('los datos no han sido normalizados')
            case 7:
                break
            case _:
                print("entrada invalida")
