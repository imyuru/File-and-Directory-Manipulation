
import datetime
from datetime import datetime
import os
import tkinter as tk
from tkinter import filedialog
import shutil
import send2trash
import traceback
import zipfile
from cryptography.fernet import Fernet
import difflib

centro = '*'
numparticipante= 0
Path = ""
def seleccionardirectorio():

    root = tk.Tk()
    root.withdraw()  # Hide the main window
    print("Favor seleccionar la ruta de archivos")
    directory_path = filedialog.askdirectory()
    return directory_path

def listararchivodirectorio(extension=None):
    global Path
    directory_path = seleccionardirectorio()
    Path = directory_path
    file_list = []
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if extension is None or file.endswith(extension):
                file_list.append(os.path.join(root, file))
    return file_list



# ...

def seleccionararchivo():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    file_path = filedialog.askopenfilename()
    return file_path

def seleccionardestino():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    folder_path = filedialog.askdirectory()
    return folder_path

def copiararchivo():
    print("Seleccionar Archivo -- Pantalla emergente")
    archivo_origen = seleccionararchivo()

    if archivo_origen == "":
        print("No se seleccionó ningún archivo.")
    else:
        nombre_archivo = os.path.basename(archivo_origen)
        print("Seleccionar Directorio donde se copiara el archivo seleccionado -- Pantalla emergente")
        destino = seleccionardestino()

        mantener_nombre = input("¿Desea mantener el nombre original del archivo? (s/n): ")

        if mantener_nombre.lower() == "s":
            nuevo_nombre = nombre_archivo
        else:
            nuevo_nombre = input("Ingrese el nuevo nombre del archivo copiado (sin extensión): ")

            # Retain the original file extension
            _, file_extension = os.path.splitext(nombre_archivo)
            nuevo_nombre += file_extension

        destino_path = os.path.join(destino, nuevo_nombre)

        try:
            shutil.copy2(archivo_origen, destino_path)
            print(f"Archivo '{nombre_archivo}' copiado correctamente como '{nuevo_nombre}'.")
        except shutil.Error as e:
            print(f"Error al copiar el archivo '{nombre_archivo}': {e}")
        except Exception as e:
            print(f"Ocurrió un error inesperado: {e}")


def seleccionar_archivo_o_directorio():
    root = tk.Tk()
    root.withdraw()
    tipo = input("Seleccione el tipo de elemento (1-archivo/2-directorio): ").lower()
    if tipo == "1":
        path = filedialog.askopenfilename()  # Open file dialog to select a file
    elif tipo == "2":
        path = filedialog.askdirectory()  # Open directory dialog to select a directory
    else:
        path = None
    if path:
        return (tipo, path)
    else:
        return None

def renombrar():
    seleccion = seleccionar_archivo_o_directorio()
    if seleccion:
        tipo, ruta = seleccion
        nuevo_nombre = input("Ingrese el nuevo nombre: ")
        try:
            nuevo_path = os.path.join(os.path.dirname(ruta), nuevo_nombre)
            os.rename(ruta, nuevo_path)
            print(f"{tipo.capitalize()} renombrado correctamente.")
        except FileNotFoundError:
            print(f"No se encontró el {tipo} en la ruta especificada.")
        except FileExistsError:
            print(f"Ya existe un {tipo} con el nombre '{nuevo_nombre}'.")
        except Exception as e:
            print(f"Ocurrió un error al renombrar el {tipo}: {e}")
    else:
        print("No se seleccionó un archivo o directorio válido.")




def mover():
    seleccion = seleccionar_archivo_o_directorio()
    if seleccion:
        tipo, ruta = seleccion
        nuevo_destino = filedialog.askdirectory()  # Open directory dialog to select the new destination
        if nuevo_destino:
            try:
                nuevo_path = os.path.join(nuevo_destino, os.path.basename(ruta))
                shutil.move(ruta, nuevo_path)
                print(f"{tipo.capitalize()} movido correctamente.")
            except FileNotFoundError:
                print(f"No se encontró el {tipo} en la ruta especificada.")
            except shutil.Error as e:
                print(f"Error al mover el {tipo}: {e}")
            except Exception as e:
                print(f"Ocurrió un error al mover el {tipo}: {e}")
        else:
            print("No se seleccionó una nueva ubicación.")
    else:
        print("No se seleccionó un archivo o directorio válido.")


def seleccionar_archivos_o_directorios():
    root = tk.Tk()
    root.withdraw()
    paths = filedialog.askopenfilenames()  # Open file dialog to select multiple files or directories
    return paths
def crear_directorio():
    directorio_padre = seleccionardirectorio()
    if directorio_padre:
        nombre_directorio = input("Ingrese el nombre del directorio: ")
        nuevo_directorio = os.path.join(directorio_padre, nombre_directorio)
        try:
            os.mkdir(nuevo_directorio)
            print(f"Directorio '{nombre_directorio}' creado correctamente en '{directorio_padre}'.")
        except FileExistsError:
            print(f"Ya existe un directorio con el nombre '{nombre_directorio}' en '{directorio_padre}'.")
        except FileNotFoundError:
            print(f'No se encontró el directorio padre en la ruta especificada.')
        except Exception as e:
            print(f"Ocurrió un error al crear el directorio: {e}")
    else:
        print("No se seleccionó un directorio válido.")

def seleccionar_archivos():
    root = tk.Tk()
    root.withdraw()
    archivos = filedialog.askopenfilenames()  # Open file dialog to select multiple files
    return archivos
def fusionar_archivos():
    archivos = seleccionar_archivos()
    num_archivos = len(archivos)
    if num_archivos < 2:
        print("Debe seleccionar al menos dos archivos para fusionar.")
        return
    directorio_destino = filedialog.askdirectory()  # Open directory dialog to select the destination directory
    archivo_destino = input("Ingrese el nombre del archivo de destino fusionado: ")
    archivo_destino = os.path.join(directorio_destino, archivo_destino + ".txt")

    try:
        with open(archivo_destino, "w") as destino:
            for archivo in archivos:
                with open(archivo, "r") as fuente:
                    contenido = fuente.read()
                    destino.write(contenido + "\n")
        print(f"Archivos fusionados correctamente en '{archivo_destino}'.")
    except FileNotFoundError:
        print("No se encontró uno o más archivos seleccionados.")
    except Exception as e:
        print(f"Ocurrió un error al fusionar los archivos: {e}")

def seleccionar_archivos_o_directorios_papelera():
    root = tk.Tk()
    root.withdraw()
    paths = filedialog.askopenfilenames()  # Open file dialog to select multiple files or directories
    return list(paths)

'''def borrararchivodirectorio(file_paths):
    for file_path in file_paths:
        try:
            os.remove(file_path)
            print(f"File '{file_path}' deleted successfully.")
        except OSError as e:
            print(f"Error deleting file '{file_path}': {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

def borrarpapelera2(file_paths):
    for file_path in file_paths:
        if os.path.exists(file_path):
            try:
                trash_path = os.path.join(os.environ.get("HOMEDRIVE"), os.environ.get("HOMEPATH"), ".Trash")
                shutil.move(file_path, trash_path)
                print(f"El archivo '{file_path}' fue enviado satisfactoriamente a la papelera de reciclaje.")
            except Exception as e:
                print(f"Error al mover el archivo '{file_path}' a la papelera de reciclaje: {e}")
        else:
            print(f"El archivo '{file_path}' no existe")'''

def borrarpapelera(file_paths):
    for file_path in file_paths:
        if os.path.exists(file_path):
            try:
                short_path = os.path.normpath(file_path)
                send2trash.send2trash(short_path)
                print(f"El archivo '{file_path}' fue enviado satisfactoriamente a la papelera de reciclaje.")
            except OSError as e:
                print(f"Error al mover el archivo '{file_path}' a la papelera de reciclaje: {e}")
            except Exception as e:
                print(f"Un error inesperado: {e}")
        else:
            print(f"El archivo '{file_path}' no existe.")
def enviar_papelera():
    paths = seleccionar_archivos_o_directorios_papelera()
    num_elementos = len(paths)
    if num_elementos == 0:
        print("No se seleccionaron archivos o directorios.")
        return

    confirmacion = input(f"¿Está seguro de enviar {num_elementos} elementos a la papelera? (s/n): ")
    if confirmacion.lower() != "s":
        print("Operación cancelada.")
        return
    #borrararchivodirectorio(paths)
    borrarpapelera(paths)

def comparardosarchivos():
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    try:
        print("Seleccionar el primer archivo ------Ventana emergente")
        file1 = filedialog.askopenfilename(title="Seleccionar el primer archivo")
        print("Seleccionar el segundo archivo ------Ventana emergente")
        file2 = filedialog.askopenfilename(title="Seleccionar el segundo archivo")

        with open(file1, 'r', encoding='utf-8', errors='replace') as f1, open(file2, 'r', encoding='utf-8',
                                                                                  errors='replace') as f2:
            lines1 = f1.readlines()
            lines2 = f2.readlines()

        differ = difflib.Differ()
        diff = list(differ.compare(lines1, lines2))

        print("La diferencia entre los dos archivos es: ")
        for line in diff:
            if line.startswith('-') or line.startswith('+'):
                print(line.strip())

    except FileNotFoundError:
        print("Uno o ambos archivos no fueron encontrados.")
    except IOError as e:
        print(f"Ocurrió un error al comparar los archivos: {e}")
    except Exception as e:
        print(f"A ocurrido un error no esperado: {e}")

def comprimir_individual():
    print("Seleccionar archivos a comprimir ------Ventana emergente")
    selected_files = seleccionar_archivos()
    if not selected_files:
        print("No se seleccionaron archivos")
        return
    print("Seleccionar la carpeta destino para el archivo comprimido ------Ventana emergente")
    destination_folder = seleccionardestino()
    if not destination_folder:
        print("No se seleccionó una carpeta destino.")
        return

    zip_filename = input("Favor ingresar el nombre del ZIP (sin extensiones): ")
    zip_filename += ".zip"

    zip_path = os.path.join(destination_folder, zip_filename)

    try:
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for file_path in selected_files:
                short_path = os.path.normpath(file_path)
                arcname = os.path.basename(short_path)  # Use only the filename for files
                zipf.write(file_path, arcname=arcname)  # Add each selected file to the ZIP
        print(f"Los archivos seleccionados se comprimieron en '{zip_path}' de forma exitosa.")
    except Exception as e:
        print(f"Ocurrió un error al comprimir los archivos: {e}")

def comprimir_carpeta():
    print("Seleccionar carpeta a comprimir ------Ventana emergente")
    selected_folder = seleccionardirectorio()
    if not selected_folder:
        print("No se seleccionó una carpeta.")
        return
    print("Seleccionar la carpeta destino para el archivo comprimido ------Ventana emergente")
    destination_folder = seleccionardestino()
    if not destination_folder:
        print("No se seleccionó una carpeta destino.")
        return

    zip_filename = input("Favor ingresar el nombre del ZIP (sin extensiones): ")
    zip_filename += ".zip"

    zip_path = os.path.join(destination_folder, zip_filename)

    try:
        shutil.make_archive(zip_path, 'zip', selected_folder)
        print(f"La carpeta '{selected_folder}' se comprimió en '{zip_path}' de forma exitosa.")
    except Exception as e:
        print(f"Ocurrió un error al comprimir la carpeta: {e}")

def comprimir():
    while True:
        try:
            print("Favor seleccionar el tipo de compresion:")
            print("1 - Comprimir archivos individuales.")
            print("2 - Comprimir una carpeta.")
            opcion = int(input("Ingrese el número de opción: "))

            if opcion == 1:
                comprimir_individual()
                break
            elif opcion == 2:
                comprimir_carpeta()
                break
            else:
                print("Opción inválida. Intente nuevamente.")
        except ValueError:
            print("Dato incorrecto; intente nuevamente.")

def descomprimir():
    print("Seleccionar el archivo ZIP a descomprimir ------Ventana emergente")
    zip_file_path = seleccionararchivo()
    if not zip_file_path:
        print("No se seleccionó un archivo ZIP.")
        return

    print("Seleccionar la carpeta destino para la descompresión ------Ventana emergente")
    destination_folder = seleccionardestino()
    if not destination_folder:
        print("No se seleccionó una carpeta destino.")
        return

    try:
        with zipfile.ZipFile(zip_file_path, 'r') as zipf:
            zipf.extractall(destination_folder)
        print(f"El archivo ZIP '{zip_file_path}' se descomprimió en la carpeta '{destination_folder}' correctamente.")
    except zipfile.BadZipFile:
        print("El archivo seleccionado no es un archivo ZIP válido.")
    except Exception as e:
        print(f"Ocurrió un error al descomprimir el archivo ZIP: {e}")

def generar_clave():
    return Fernet.generate_key()

def guardar_clave(clave, output_dir, counter):
    key_file_path = os.path.join(output_dir, f"clave{counter}.key")
    with open(key_file_path, 'wb') as file:
        file.write(clave)
    return key_file_path


def cargar_clave(nombre_archivo):
    with open(nombre_archivo, 'rb') as file:
        return file.read()

def encriptar():
    num_files = int(input("Ingrese el número de archivos a encriptar: "))

    for i in range(num_files):
        clave = generar_clave()

        print(f"Seleccionar el archivo {i + 1} a encriptar ------Ventana emergente")
        archivo_a_encriptar = seleccionararchivo()
        if not archivo_a_encriptar:
            print(f"No se seleccionó un archivo para encriptar {i + 1}.")
            continue

        output_dir = os.path.dirname(archivo_a_encriptar)
        key_file_path = guardar_clave(clave, output_dir, i + 1)

        try:
            with open(archivo_a_encriptar, 'rb') as file:
                datos = file.read()

            fernet = Fernet(clave)
            datos_encriptados = fernet.encrypt(datos)

            with open(archivo_a_encriptar, 'wb') as file:
                file.write(datos_encriptados)

            print(f"El archivo '{archivo_a_encriptar}' se encriptó correctamente.")
            print(f"La clave se guardó en '{key_file_path}'.")
        except Exception as e:
            print(f"Ocurrió un error al encriptar el archivo {i + 1}: {e}")


def desencriptar():
    print("Seleccionar el archivo encriptado a desencriptar ------Ventana emergente")
    archivo_a_desencriptar = seleccionararchivo()
    if not archivo_a_desencriptar:
        print("No se seleccionó un archivo para desencriptar.")
        return

    print("Seleccionar el archivo de clave ------Ventana emergente")
    archivo_clave = seleccionararchivo()
    if not archivo_clave:
        print("No se seleccionó un archivo de clave.")
        return

    try:
        with open(archivo_clave, 'rb') as file:
            clave = file.read()

        with open(archivo_a_desencriptar, 'rb') as file:
            datos_encriptados = file.read()

        fernet = Fernet(clave)
        datos_desencriptados = fernet.decrypt(datos_encriptados)

        with open(archivo_a_desencriptar, 'wb') as file:
            file.write(datos_desencriptados)

        print("El archivo se desencriptó correctamente.")
    except Exception as e:
        print(f"Ocurrió un error al desencriptar el archivo: {e}")

def menu_file_encryption():
    while True:
        print("Favor seleccionar el tipo de operación:")
        print("1 - Encriptar un archivo.")
        print("2 - Desencriptar un archivo.")
        print("3 - Salir")
        try:
            opcion = int(input("Ingrese el número de opción: "))

            if opcion == 1:
                encriptar()
            elif opcion == 2:
                desencriptar()
            elif opcion == 3:
                print("Gracias por utilizar las opciones.")
                break
            else:
                print("Opción inválida. Intente nuevamente.")
        except ValueError:
            print("Dato incorrecto; intente nuevamente.")

def crear_backup():
    global Path
    backup_dir = seleccionardestino()
    if not backup_dir:
        print("No se seleccionó una carpeta para guardar el backup.")
        return

    files_to_backup = seleccionar_archivos_o_directorios()
    if not files_to_backup:
        print("No se seleccionaron archivos o directorios para el backup.")
        return

    try:
        for file_path in files_to_backup:
            shutil.copy2(file_path, backup_dir)
        print(f"Backup creado correctamente en '{backup_dir}'.")
    except shutil.Error as e:
        print(f"Error al crear el backup: {e}")
    except Exception as e:
        print(f"Ocurrió un error al crear el backup: {e}")

def restaurar_backup():
    global Path
    backup_dir = seleccionardirectorio()
    if not backup_dir:
        print("No se seleccionó una carpeta de backup.")
        return

    files_to_restore = seleccionar_archivos_o_directorios()
    if not files_to_restore:
        print("No se seleccionaron archivos o directorios para restaurar.")
        return

    try:
        for file_path in files_to_restore:
            shutil.move(file_path, os.path.join(Path, os.path.basename(file_path)))
        print("Restauración completada correctamente.")
    except shutil.Error as e:
        print(f"Error al restaurar el archivo/directorio: {e}")
    except Exception as e:
        print(f"Ocurrió un error al restaurar el archivo/directorio: {e}")

def backup_and_restore_menu():
    print("Favor seleccionar el tipo de operación:")
    print("1 - Crear un backup.")
    print("2 - Restaurar un backup.")
    sub_opcion = int(input("Ingrese el número de opción: "))

    if sub_opcion == 1:
        crear_backup()
    elif sub_opcion == 2:
        restaurar_backup()
    else:
        print("Opción inválida. Intente nuevamente.")

class Menu():
        def __init__(self, root):
            self.root = root
            self.root.title("Examen Final")
            self.crear_menu()

        def crear_menu(self):
            title_label = tk.Label(self.root,
                                   text="Bienvenido al proyecto final - Manejo de archivos y directorios",
                                   font=("Helvetica", 14, "bold"))
            title_label.pack(pady=10)

            options_frame = tk.Frame(self.root)
            options_frame.pack(pady=10)

            options_label = tk.Label(options_frame, text="Menú", font=("Helvetica", 12, "bold"))
            options_label.grid(row=0, column=0, columnspan=2, pady=5)

            menu_opciones = [
                "Listar los archivos en un directorio.",
                "Crear una copia de un archivo.",
                "Renombrar archivo o directorios.",
                "Mover de ubicación un archivo o directorio.",
                "Crear directorios.",
                "Fusionar archivos.",
                "Borrar archivos o directorios y enviarlos a la papelera de reciclaje.",
                "Comparar Archivos.",
                "Crear un archivo zip a partir de una lista de archivos o de un directorio X.",
                "Descomprimir un archivo zip.",
                "Encriptar y Desencriptar un archivo.",
                "Crear backups de los archivos y restaurar.",
                "Salir"
            ]

            for index, option in enumerate(menu_opciones, start=1):
                option_label = tk.Label(options_frame, text=f"{index}. {option}")
                option_label.grid(row=index, column=0, sticky="w", padx=10)

            self.option_entry = tk.Entry(options_frame)
            self.option_entry.grid(row=len(menu_opciones) + 1, column=0, columnspan=2, pady=5)

            self.error_label = tk.Label(options_frame, text="", fg="red")
            self.error_label.grid(row=len(menu_opciones) + 2, column=0, columnspan=2)

            select_button = tk.Button(options_frame, text="Seleccionar", command=self.proceso_opcion)
            select_button.grid(row=len(menu_opciones) + 3, column=0, columnspan=2, pady=10)

        def proceso_opcion(self):
            try:
                opcion = int(self.option_entry.get())
                if 1 <= opcion <= 13:
                    self.root.iconify()
                    match opcion:
                        case 1:
                            while True:
                                try:
                                    print("Favor selccionarla opcion para desplegar archivos".center(70, '-'))
                                    opcion = int(input(
                                        "1 - Listar todos los archivos de un directorio \n2 - Listar una extension de archivo en un directorio en particular\n"))
                                    print(centro.center(70, '='))
                                    self.root.deiconify()
                                    if opcion == 1:
                                        files = listararchivodirectorio()
                                        if len(files) == 0:
                                            print("No se encontraron archivos en el directorio.")
                                        else:
                                            print(centro.center(70, '*'))
                                            print(f"Lista de archivos ruta = {Path}".center(70, '-'))
                                            print(centro.center(70, '*'))
                                            for file_path in files:
                                                print(file_path)
                                            print(centro.center(70, '*'))
                                        break
                                    elif opcion == 2:
                                        extension = input("Favor insertar la extension a buscar ejemplo (.txt)")
                                        selected_files = listararchivodirectorio(extension)
                                        if len(selected_files) == 0:
                                            print(
                                                f"No se encontraron archivos con la extensión especificada ({extension}) en el directorio.")
                                        else:
                                            print(centro.center(70, '*'))
                                            print(
                                                f"Lista de archivos con la extension {extension} en la ruta = {Path}".center(
                                                    70, '-'))
                                            print(centro.center(70, '*'))
                                            for file_path in selected_files:
                                                print(file_path)
                                            print(centro.center(70, '*'))
                                        break
                                    else:
                                        print("Opcion no es valida")
                                except ValueError:
                                    print("Dato incorrecto; intente nuevamente")

                        case 2:
                            copiararchivo()
                            self.root.deiconify()
                        case 3:
                            renombrar()
                            self.root.deiconify()
                        case 4:
                            mover()
                            self.root.deiconify()
                        case 5:
                            crear_directorio()
                            self.root.deiconify()
                        case 6:
                            fusionar_archivos()
                            self.root.deiconify()
                        case 7:
                            enviar_papelera()
                            self.root.deiconify()
                        case 8:
                            comparardosarchivos()
                        case 9:
                            comprimir()
                            self.root.deiconify()
                        case 10:
                            descomprimir()
                            self.root.deiconify()
                        case 11:
                            menu_file_encryption()
                            self.root.deiconify()
                        case 12:
                            backup_and_restore_menu()
                            self.root.deiconify()
                            pass
                        case 13:
                            print("Gracias por utilizar las opciones, cerro:", datetime.now())
                            self.root.destroy()
                        case _:
                            print("Opción inválida")
                else:
                    self.error_label.config(text="Opción inválida. Intente nuevamente.")
            except ValueError:
                self.error_label.config(text="Dato incorrecto; intente nuevamente.")


if __name__ == "__main__":
    root = tk.Tk()
    app = Menu(root)
    root.mainloop()

