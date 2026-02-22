import math
from decimal import Decimal, ROUND_HALF_EVEN
import numpy as np
import matplotlib
matplotlib.use('Qt5Agg') # Usamos el backend Qt5Agg para ver los gráficos directamente en ventana
import matplotlib.pyplot as plt
from scipy.stats import linregress

def redondear_bancario(valor, decimales):
    """
    3. Implementa redondeo bancario (round half to even)
    usando el tipo Decimal.
    """
    if decimales == 0:
        formato = Decimal('1')
    else:
        formato = Decimal('0.' + '0' * decimales)
        
    val_dec = Decimal(str(valor))
    return val_dec.quantize(formato, rounding=ROUND_HALF_EVEN)

def redondear_con_error(valor, error):
    """
    4. Redondea valor y error apropiadamente calculando 
    la cifra significativa correspondiente del error para 
    mantener la misma cantidad de decimales en ambos.
    """
    if error == 0:
        decimals = 0
    else:
        mag = math.floor(math.log10(abs(error)))
        decimals = max(0, -mag)
        
    v_round = float(redondear_bancario(valor, decimals))
    e_round = float(redondear_bancario(error, decimals))
    return v_round, e_round, decimals

def obtener_notacion_ingenieria(valor, error):
    """
    1. Convierte a notación científica cuando error >= 10,
    utilizando exponentes que son múltiplos de 3, tal que el 
    error normalizado sea < 10 y con 1 cifra significativa.
    """
    # Magnitud real del error
    mag_error = int(math.floor(math.log10(abs(error))))
    
    # Lógica obligatoria para elegir el exponente
    if mag_error < 3:
        exponente = 3
    else:
        exponente = ((mag_error // 3) + 1) * 3
        
    n_val = valor / (10 ** exponente)
    n_err = error / (10 ** exponente)
    
    # Redondeamos utilizando el error normalizado
    v_round, e_round, decimals = redondear_con_error(n_val, n_err)
    
    fmt = f"{{:.{decimals}f}}"
    str_val = fmt.format(v_round)
    str_err = fmt.format(e_round)
    
    return f"({str_val} ± {str_err}) × 10^{exponente}"

def formatear_valor_error(valor, error):
    """
    2. Formatea la salida utilizando las reglas especificadas:
    Si error >= 10, usa notación de ingeniería obligatoria.
    Si error < 10, usa formato normal manteniendo cifra significativa alineada.
    """
    if abs(error) >= 10:
        return obtener_notacion_ingenieria(valor, error)
    else:
        v_round, e_round, decimals = redondear_con_error(valor, error)
        fmt = f"{{:.{decimals}f}}"
        str_val = fmt.format(v_round)
        str_err = fmt.format(e_round)
        return f"{str_val} ± {str_err}"

def limpiar_formato(val_str):
    """
    Intenta limpiar y mantener el formato de ingreso si es posible.
    """
    return val_str.strip()

def ingresar_array(nombre_var, limite_datos=None):
    """
    Solicita los datos de una variable. Si limite_datos está definido,
    termina automáticamente después de obtener esa cantidad de datos.
    """
    valores_nativos = []
    valores_float = []
    
    print(f"\n--- Ingreso de variable {nombre_var} ---")
    if limite_datos:
        print(f"Ingrese exactamente los {limite_datos} valores de '{nombre_var}'.")
    else:
        print(f"Ingrese uno por uno los valores de '{nombre_var}'.")
        print("Presione ENTER sin escribir nada para terminar.")
    
    contador = 1
    while True:
        # Check limit BEFORE asking for input
        if limite_datos and len(valores_float) >= limite_datos:
            print(f"-> ¡Autocompletado! Se ingresaron los {limite_datos} datos.")
            break
            
        entrada = input(f"Dato de {nombre_var} [{contador}]: ").strip()
        
        if not entrada:
            if limite_datos:
                print(f"Faltan datos. Aún debe ingresar el Dato [{contador}].")
                continue
            elif len(valores_float) < 3:
                print(f"Por favor, ingrese al menos 3 puntos para '{nombre_var}'. (Lleva {len(valores_float)})")
                continue
            break
            
        try:
            val_f = float(entrada)
            valores_float.append(val_f)
            valores_nativos.append(entrada)
            contador += 1
        except ValueError:
            print("Error: El valor debe ser numérico.")
            
    return valores_nativos, valores_float

def mostrar_tabla_datos(x_nat, y_nat):
    """
    Muestra la tabla de datos ingresados.
    """
    print("\n--- Listado de datos ingresados ---")
    print(f"{'Índice':^8} | {'Variable X':^15} | {'Variable Y':^15}")
    print("-" * 44)
    for i in range(len(x_nat)):
        print(f"{i+1:^8} | {x_nat[i]:^15} | {y_nat[i]:^15}")
    print("-" * 44)

def ingresar_datos():
    """
    5. Para entrada de datos separada (X primero, luego Y).
    Obliga a la misma cantidad en ambas. Verifica correcciones.
    """
    while True:
        x_nat, x_float = ingresar_array("independiente X")
        
        while True:
            y_nat, y_float = ingresar_array("dependiente Y", limite_datos=len(x_float))
            if len(x_float) != len(y_float):
                print(f"\n[ERROR] Cantidad dispar de elementos.")
                print(f"Ha ingresado {len(x_float)} datos de X, pero {len(y_float)} datos de Y.")
                print("Por favor, vuelva a ingresar la variable Y.")
            else:
                break
                
        # Proceso de verificación y corrección continua
        while True:
            mostrar_tabla_datos(x_nat, y_nat)
            
            resp = input("\n¿Están bien los datos? ¿Desea proceder a ejecutar el ajuste? (s/n): ").strip().lower()
            if resp == 's':
                return x_float, y_float
            elif resp == 'n':
                while True:
                    idx_str = input("\n¿Qué N° de índice desea corregir? (o presione ENTER para cancelar corrección): ").strip()
                    if not idx_str:
                        break
                        
                    try:
                        idx = int(idx_str) - 1
                        if 0 <= idx < len(x_float):
                            print(f"\nCorrigiendo el Par {idx+1}: (X={x_nat[idx]}, Y={y_nat[idx]})")
                            
                            nuevo_x = input(f"Nuevo valor X (ENTER para dejar '{x_nat[idx]}'): ").strip()
                            if nuevo_x:
                                x_float[idx] = float(nuevo_x)
                                x_nat[idx] = nuevo_x
                                
                            nuevo_y = input(f"Nuevo valor Y (ENTER para dejar '{y_nat[idx]}'): ").strip()
                            if nuevo_y:
                                y_float[idx] = float(nuevo_y)
                                y_nat[idx] = nuevo_y
                                
                            print(f"Dato {idx+1} actualizado a: (X={x_nat[idx]}, Y={y_nat[idx]})")
                            break # Sale al loop principal de verificación para mostrar la tabla de nuevo
                        else:
                            print("Error: Índice fuera de rango.")
                    except ValueError:
                        print("Error: Debe ingresar un número entero válido.")
            else:
                 print("Respuesta no válida. Por favor, ingrese 's' (Sí, proceder) o 'n' (No, quiero corregir).")

def calcular_lineal(x, y):
    """
    7. Realiza el ajuste y calcula errores usando scipy.stats.linregress.
    """
    res = linregress(x, y)
    # linregress retorna (slope, intercept, rvalue, pvalue, stderr, intercept_stderr)
    return res.intercept, res.slope, res.intercept_stderr, res.stderr, res.rvalue

def graficar_ajuste_lineal(x, y, A_raw, B_raw, eq_str):
    """
    6. Genera la gráfica del ajuste lineal (datos y recta) usando matplotlib.
    """
    x_line = np.linspace(min(x), max(x), 100)
    y_line = A_raw + B_raw * x_line
    
    plt.figure(figsize=(9, 6))
    plt.scatter(x, y, color='blue', zorder=5, label='Datos experimentales')
    plt.plot(x_line, y_line, color='red', zorder=4, label=f'Ajuste:\n{eq_str}')
    
    plt.title("Ajuste Lineal (Y = A + BX)")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    
    # Guardamos la imagen en la misma carpeta
    nombre_archivo = "grafico_ajuste.png"
    plt.savefig(nombre_archivo, dpi=300, bbox_inches='tight')
    print(f"\n[✓] El gráfico se ha guardado exitosamente como '{nombre_archivo}' en esta carpeta.")
    
    print("\nMostrando gráfica interactiva... (Cierre la ventana de la gráfica para terminar)")
    plt.show()


def probar_formato():
    """
    9. Función de prueba para verificar el formato (opcional pero útil).
    Incluye todos los ejemplos requeridos por especificación (y otros adicionales).
    """
    print("----- Validando Casos Obligatorios de Formateo -----")
    ejemplos = [
        (250, 20),
        (5420, 234),
        (1234567, 12345),
        (1234567890, 12345678),
        (-0.85, 0.12),    # Error menor a 10
        (4.321, 0.054)    # Error menor a 1
    ]
    for val, err in ejemplos:
        print(f"Input: {val} ± {err}  -->  Output: {formatear_valor_error(val, err)}")
    print("----------------------------------------------------\n")

def main():
    """
    8. Función principal. Integra ingreso de datos, ajuste,
    formateo, display de resultados y graficación final.
    """
    print("====== PROGRAMA DE AJUSTE LINEAL (Y = A + BX) ======\n")
    
    # probar_formato() # <-- Descomentar para visualizar pruebas internas
    
    x, y = ingresar_datos()
    
    # 1. Cálculo de recta
    A_raw, B_raw, err_A_raw, err_B_raw, r = calcular_lineal(x, y)
    
    # 2. Formateo de valores
    formato_A = formatear_valor_error(A_raw, err_A_raw)
    formato_B = formatear_valor_error(B_raw, err_B_raw)
    
    # 3. Presentación de resultados
    print("\n" + "-"*5 + " Resultados del ajuste Y = A + BX " + "-"*5 + "\n")
    
    print("1) Valores SIN REDONDEAR:")
    print(f"    A_raw       = {A_raw:.10f}")
    print(f"    error_A_raw = {err_A_raw:.10f}")
    print(f"    B_raw       = {B_raw:.10f}")
    print(f"    error_B_raw = {err_B_raw:.10f}\n")
    
    print("2) Valores REDONDEADOS:")
    print(f"    A           = {formato_A}")
    print(f"    B           = {formato_B}\n")
    
    print(f"Coeficiente de correlación lineal r = {r:.6f}\n")
    
    print("3) Ecuación final con errores:")
    eq_str = f"Y = ({formato_A}) + ({formato_B})X"
    print(f"    {eq_str}\n")
    
    # 4. Graficación
    print("\nGenerando gráfica con matplotlib...")
    graficar_ajuste_lineal(x, y, A_raw, B_raw, eq_str)

if __name__ == "__main__":
    main()
