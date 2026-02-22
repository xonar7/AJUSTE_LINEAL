# AJUSTE LINEAL (Calculadora de Regresión Lineal)

![image](grafico_ajuste.png)

Una herramienta en Python para realizar ajustes lineales (regresión por mínimos cuadrados) sobre un conjunto de datos experimentales. Esta calculadora no solo obtiene la recta de mejor ajuste ($Y = A + BX$), sino que también calcula rigurosamente **la propagación de errores** para la pendiente y la intersección, aplicando reglas estrictas de cifras significativas y redondeo científico/bancario según normas de laboratorio.

## Características Principales

* **Ingreso Secuencial:** Interfaz paso a paso para ingresar primero la variable independiente ($X$) y luego la variable dependiente ($Y$), validando que ambas listas tengan la misma dimensión.
* **Corrección de Datos:** Antes de procesar, permite revisar y corregir cualquier dato ingresado de forma individual.
* **Cálculo Robusto:** Utiliza `scipy.stats.linregress` para obtener los estimadores y sus errores estándar.
* **Reglas de Redondeo (Laboratorio):**
  * Redondeo Bancario (Round-Half-to-Even) mediante `decimal.Decimal`.
  * Ajuste automático de cifras significativas del valor nominal para que coincidan con la posición decimal del error correspondiente.
  * Uso de notación de ingeniería (exponentes múltiplos de 3) cuando el error es mayor o igual a 10.
* **Visualización Interactiva:** Genera un gráfico interactivo (`Qt5Agg`) de los datos experimentales y la recta de ajuste, y guarda automáticamente una copia como imagen (`grafico_ajuste.png`).

---

## 📖 Guía de Ingreso de Datos (Notaciones Admitidas en Python)

Esta herramienta está diseñada para cálculos científicos y de ingeniería, por lo que el ingreso de datos soporta **todas las notaciones de punto flotante válidas estándar de Python**.

A continuación, se presentan los casos de uso más comunes y cómo ingresarlos correctamente cuando el programa solicita un "Dato":

### 1. Números Enteros y Decimales Simples
El formato más elemental. Puedes omitir el cero inicial en los decimales si lo deseas.

* **Ejemplos Válidos:**
  * `5` (Se interpreta como 5.0)
  * `-12`
  * `3.14159`
  * `0.5` o simplemente `.5`
  * `-.75`

### 2. Notación Científica / Exponencial (Recomendada para ciencias)
Ideal para números muy grandes o muy cercanos a cero. Utiliza la letra `e` o `E` seguida de la potencia de base 10. *Nota: No debes dejar espacios en blanco dentro del número.*

**Sintaxis:** `[Mantisa]e[Exponente]` $\rightarrow \text{Mantisa} \times 10^{\text{Exponente}}$

* **Ejemplos Válidos:**
  * `1e3` $\rightarrow 1 \times 10^3 = 1000.0$
  * `4.52E-5` $\rightarrow 4.52 \times 10^{-5} = 0.0000452$
  * `-2e6` $\rightarrow -2 \times 10^6 = -2000000.0$
  * `1.5e+2` $\rightarrow 1.5 \times 10^2 = 150.0$

### 3. Evita usar "Comas" (,) y caracteres no numéricos
En Python, y por ende en este script, **el separador decimal estricto es el punto (`.`)**.

* ❌ **Incorrecto:** `3,14` (Dará un error de valor no numérico).
* ✅ **Correcto:** `3.14`
* ❌ **Incorrecto:** `1.5 x 10^-3` (Usa letras y símbolos no válidos).
* ✅ **Correcto:** `1.5e-3`

---

## Requisitos de Instalación

Asegúrate de tener Python 3 instalado. Las dependencias externas necesarias se instalan de la siguiente manera:

```bash
pip install numpy scipy matplotlib PyQt5
```
*(Nota: `PyQt5` es necesario para la ventana de gráficos interactivos)*

## Cómo Usar

Ejecuta el script desde tu terminal o consola de comandos:

```bash
python ajuste_lineal.py
```

Sigue las instrucciones en pantalla:
1. Ingresa los datos de `X` presionando ENTER por cada dato nuevo.
2. Presiona ENTER en la línea en blanco para finalizar la serie de X.
3. Se te solicitará ingresar exactamente la misma cantidad de datos para `Y`.
4. El programa te mostrará una tabla resumen. Presiona `s` para calcular o `n` para corregir el índice de algún dato mal digitado.
5. Observa los resultados por consola y visualiza el gráfico emergente.
