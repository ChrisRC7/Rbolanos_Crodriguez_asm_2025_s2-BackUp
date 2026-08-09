import cv2
import numpy as np
from customtkinter import *
from complex_maps import *
from complex_shapes import *
from graficador import *

def capture_click(event, x, y, flags, param):
    """Función de callback que guarda las coordenadas de un clic izquierdo."""
    if event == cv2.EVENT_LBUTTONDOWN:
        if not param:
            print(f"Punto seleccionado en: ({x}, {y})")
            param.append((x, y))

def get_user_click(window_name, image, click_list):
    """Muestra una ventana, asigna el callback y espera por un clic del usuario."""
    cv2.namedWindow(window_name)
    cv2.setMouseCallback(window_name, capture_click, click_list)
    print(f"\nINSTRUCCIÓN: En la ventana '{window_name}', haz clic y luego presiona ESC.")
    
    while len(click_list) == 0:
        cv2.imshow(window_name, image)
        if cv2.waitKey(1) & 0xFF == 27:
            print("Operación cancelada por el usuario.")
            return False
    cv2.destroyAllWindows()
    return True

def detect_all_circles(image):
    """Busca TODOS los círculos en la imagen completa."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.medianBlur(gray, 7)
    
    # Los parámetros ajustables
    circles = cv2.HoughCircles(
        blurred, cv2.HOUGH_GRADIENT, dp=1.2, minDist=30,
        param1=100, param2=41, minRadius=15, maxRadius=150
    )
    
    found_circles = []
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for pt in circles[0, :]:
            h, k, r = pt[0], pt[1], pt[2]
            found_circles.append((h, k, r))
    return found_circles

def detect_all_lines(image):
    """Busca TODAS las líneas en la imagen completa."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    
    # Los parámetros ajustables
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 100, minLineLength=120, maxLineGap=300)
    
    found_lines = []
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            found_lines.append((x1, y1, x2, y2))
    return found_lines

def extraer(imagen):
    """Flujo principal del programa."""
    shape_points = []
    shape_names = []
    shape_equations = []
    img_original = imagen
    if img_original is None:
        print(f"Error: No se pudo cargar la imagen en '{imagen}'")
        return

    print("Analizando la imagen en busca de círculos y líneas...")
    
    # PASO 1: Detectar todas las figuras automáticamente
    detected_circles = detect_all_circles(img_original)
    detected_lines = detect_all_lines(img_original)

    if not detected_circles and not detected_lines:
        print("No se detectaron figuras en la imagen.")
        return

    # Dibujar todas las figuras encontradas y mostrar sus datos en píxeles
    img_with_shapes = img_original.copy()
    print("\n--- Figuras Encontradas en Coordenadas de Píxeles ---")
    
    if detected_circles:
        print(f"Se encontraron {len(detected_circles)} círculos:")
        for i, (h, k, r) in enumerate(detected_circles, 1):
            print(f"  Círculo #{i}: Centro=({h}, {k}), Radio={r}")
            cv2.circle(img_with_shapes, (h, k), r, (0, 255, 0), 2)
            cv2.putText(img_with_shapes, f"C{i}", (h - 10, k + 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

    if detected_lines:
        print(f"Se encontraron {len(detected_lines)} líneas:")
        for i, (x1, y1, x2, y2) in enumerate(detected_lines, 1):
            print(f"  Línea #{i}: P1=({x1}, {y1}), P2=({x2}, {y2})")
            cv2.line(img_with_shapes, (x1, y1), (x2, y2), (255, 255, 0), 2)
            cv2.putText(img_with_shapes, f"L{i}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

    # PASO 2: Obtener el nuevo origen del usuario
    new_origin_coords = []
    if not get_user_click("PASO FINAL: Clic en el NUEVO ORIGEN (0,0)", img_with_shapes, new_origin_coords):
        return
        
    origin_x_pix, origin_y_pix = new_origin_coords[0]

    # PASO 3: Transformar coordenadas para TODAS las figuras
    print("\n--- Resultados en tu Nuevo Plano Cartesiano ---")
    print(f"Origen definido en píxeles: ({origin_x_pix}, {origin_y_pix})")
    
    if detected_circles:
            for i, (h_pix, k_pix, r) in enumerate(detected_circles, 1):
                h_math = int(h_pix) - int(origin_x_pix)
                k_math = int(origin_y_pix) - int(k_pix) 
                
                print(f"\n  Círculo #C{i}:")
                
                # Ecuación Cartesiana (la que ya teníamos)
                print(f"    Ecuación Cartesiana: (x - {h_math})^2 + (y - {k_math})^2 = {r**2}")

        
                # Formatear el número complejo z₀ = h + ki de forma legible
                if k_math == 0:
                    z0_str = f"{h_math}"

                elif k_math > 0:
                    z0_str = f"{h_math} + {k_math}j"
                else:
                    # k_math es negativo, así que no necesitamos un signo de más
                    z0_str = f"{h_math} - {-k_math}j"

                # Construir la ecuación final
                # Si el radio es 1, no es necesario mostrarlo (ej. e^iθ en lugar de 1*e^iθ)
                if r == 1:
                    print(f"    Ecuación Compleja: z = ({z0_str}) + e^(iθ)")
                else:
                    print(f"    Ecuación Compleja: z = ({z0_str}) + {r}*e^(iθ)")
                # ---------------------------------------------

                dist_sq = h_math**2 + k_math**2
                if abs(dist_sq - r**2) < r * 0.1: 
                    print(" ✅ Pasa por el nuevo origen.")
                else: 
                    print("❌ NO pasa por el nuevo origen.")

                
                center = complex(z0_str.replace(" ", "").replace(")", ""))
                print(f"Centro en forma compleja: {center}")

                shape_points.append(create_complex_circle(256, r=r, center= center))
                shape_names.append(f"Círculo #{i}")
                shape_equations.append(f"z=({z0_str}) + {r}*e^(iθ)")

    if detected_lines:
        for i, (x1_pix, y1_pix, x2_pix, y2_pix) in enumerate(detected_lines, 1):
            # 1. Transformar los puntos del pixel al plano matemático
            x1_math = int(x1_pix) - int(origin_x_pix)
            y1_math = int(origin_y_pix) - int(y1_pix)
            x2_math = int(x2_pix) - int(origin_x_pix)
            y2_math = int(origin_y_pix) - int(y2_pix)

            print(f"\n  Línea #L{i}:")

            # 2. Calcular los componentes de la ecuación paramétrica z(t) = z₀ + tw
            
            # z₀ es el punto de inicio
            z0 = complex(x1_math, y1_math)
            
            # w es el vector director (del punto 1 al punto 2)
            w_real = x2_math - x1_math
            w_imag = y2_math - y1_math
            w = complex(w_real, w_imag)

            # 3. Formatear las ecuaciones para imprimirlas de forma legible
            
            # Formato para z₀
            if z0.imag == 0:
                z0_str = f"{z0.real:.0f}"
            elif z0.imag > 0:
                z0_str = f"{z0.real:.0f} + {z0.imag:.0f}j"
            else:
                z0_str = f"{z0.real:.0f} - {-z0.imag:.0f}j"

            # Formato para w
            if w.imag == 0:
                w_str = f"{w.real:.0f}"
            elif w.imag > 0:
                w_str = f"{w.real:.0f} + {w.imag:.0f}j"
            else:
                w_str = f"{w.real:.0f} - {-w.imag:.0f}j"
            
            # Imprimir la nueva ecuación compleja
            print(f"    Ecuación Compleja: z(t) = ({z0_str}) + t*({w_str})")
            
            # 4. Generar los puntos y guardarlos para el mapeo
            # Asumimos que la función create_complex_line_parametric ya existe en complex_shapes.py
            shape_points.append(create_complex_line_parametric(z0, w))
            shape_names.append(f"Recta #{i}")
            shape_equations.append(f"z(t) = ({z0_str}) + t*({w_str})")

    output_dir = "complex_geometric_mappings"
    for shapes in shape_points:
        if shape_points is not None:
            shape_name = shape_names.pop(0)
            shape_equation = shape_equations.pop(0)
            print(f"\nFigura: {shape_name}")
            print(f"   Ecuación: {shape_equation}")
            plot_mappings_for_shape(shape_name, shapes, shape_equation, output_dir)
            print("\nProceso completado.")

