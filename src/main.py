import cv2
import numpy as np
from customtkinter import *
from complex_maps import *
from complex_shapes import *
from extract_ecuation import *

def seleccionar_y_extraer():
    # Llama al explorador de archivos usando la ruta inicial
    filepath = filedialog.askopenfilename(
        title="Selecciona una imagen",
        initialdir= 'imagenes de prueba',  # <-- Aquí se establece la carpeta por defecto
        filetypes=[("Archivos de Imagen", "*.png *.jpg *.jpeg *.bmp"), 
                   ("Todos los archivos", "*.*")]
    )
    
    if filepath:
        """
        Función para leer imágenes que están en rutas con caracteres especiales.
        """
        try:
            # Lee el archivo en memoria como un array de bytes
            stream = open(filepath, "rb")
            bytes = bytearray(stream.read())
            numpyarray = np.asarray(bytes, dtype=np.uint8)
            # Decodifica el array de bytes para obtener la imagen
            imagen= cv2.imdecode(numpyarray, cv2.IMREAD_UNCHANGED)
            extraer(imagen)
        
        except Exception as e:
            print(f"Error al leer la imagen con imread_unicode: {e}")
            return None

def main():
    set_appearance_mode('light')  # Establece el modo de apariencia a blanco
    set_default_color_theme('blue')
    deactivate_automatic_dpi_awareness()

    window= CTk()
    window.title("Mapeo de Figuras Geométricas")
    ancho= 500
    alto= 500

    ancho_pantalla = window.winfo_screenwidth()
    alto_pantalla = window.winfo_screenheight() 
    x = (ancho_pantalla // 2) - (ancho // 2)
    y = (alto_pantalla // 2) - (alto // 2)
    window.geometry(f"{ancho}x{alto}+{x}+{y}")
    window.resizable(width = NO, height = NO)
    window.focus_force()

    Label1= CTkLabel(window, text= "Crear un circulo", font= ("Arial", 20))
    Label1.pack(pady= 10)
    
    radio= CTkEntry(window, placeholder_text= "Radio: Ej. 1.5", width= 200, height= 30)
    radio.pack(pady= 10)

    center= CTkEntry(window, placeholder_text= "Centro: Ej. 2+3j", width= 200, height= 30)
    center.pack(pady= 10)

    CrearCirculo= CTkButton(window, text= 'Crear Circulo', command= lambda: crearCirculo(radio.get(), center.get()))
    CrearCirculo.pack(pady= 10)

    Label2= CTkLabel(window, text= "Crear Linea", font= ("Arial", 20))
    Label2.pack(pady= 10)

    pendiente= CTkEntry(window, placeholder_text= "Punto de inicio z₀ (ej. 1+2j)", width= 200, height= 30)
    pendiente.pack(pady= 10)

    Interceccion= CTkEntry(window, placeholder_text= "Vector director w", width= 200, height= 30)
    Interceccion.pack(pady= 10)

    CrearLinea= CTkButton(window, text= 'Crear Linea', command= lambda: crearLinea(pendiente.get(), Interceccion.get()))
    CrearLinea.pack(pady= 10)

    Escoger= CTkButton(window, text= "Escoger Imagen", command= seleccionar_y_extraer)
    Escoger.pack(pady= 10)

    window.mainloop()

def crearCirculo(radio, centro):
    name= 'Círculo'
    ecuacion= (f"z=({centro}) + {radio}*e^(iθ)")

    radio = float(radio.replace(" ", "").replace(")", ""))
    centro= complex(centro.replace(" ", "").replace(")", ""))

    puntos= create_complex_circle(256, radio, centro)

    output_dir = "complex_geometric_mappings"
    plot_mappings_for_shape(name, puntos, ecuacion, output_dir)


def crearLinea(z0, w):
    name= 'Línea'
    ecuacion= (f"y = {z0}x + {w}")

    z0 = complex(z0.replace(" ", "").replace(")", ""))
    w = complex(w.replace(" ", "").replace(")", ""))

    puntos= create_complex_line_parametric(z0, w)

    output_dir = "complex_geometric_mappings"
    plot_mappings_for_shape(name, puntos, ecuacion, output_dir)


if __name__ == '__main__':
    main()