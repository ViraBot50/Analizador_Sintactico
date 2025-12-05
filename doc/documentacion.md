# Documentación - Analizador Sintáctico (Sintactico.py)

## 📚 ¿Qué es un Analizador Sintáctico?

El **Analizador Sintáctico** (o Parser) es la segunda fase de un compilador. Su trabajo es verificar que la secuencia de tokens generada por el Analizador Léxico cumple con las reglas gramaticales del lenguaje.

**Analogía:** Si el analizador léxico identifica las "palabras" del lenguaje, el analizador sintáctico verifica que esas palabras estén en el "orden correcto" según la gramática.

## 🔧 Tipo de Analizador Implementado

Este es un **Analizador Sintáctico por Descendencia Recursiva con Autómata de Pila y Backtracking**.

### Características principales:
- ✅ **Autómata de Pila**: Usa una pila explícita para controlar el proceso de parsing
- ✅ **Backtracking**: Si una regla falla, retrocede y prueba la siguiente
- ✅ **Sin Lookahead**: No mira tokens futuros para decidir qué regla aplicar
- ✅ **Prueba Reglas en Orden**: Siempre intenta las producciones en el orden definido

---

## 📖 Gramática Utilizada

La gramática define las reglas sintácticas del lenguaje:

```
S  -> if ( E ) ;          [Regla 1]
S  -> while ( E ) ;       [Regla 2]

E  -> id Op E             [Regla 3]
E  -> id                  [Regla 4]

Op -> *                   [Regla 5]
Op -> /                   [Regla 6]
Op -> ==                  [Regla 7]
Op -> +                   [Regla 8]
Op -> -                   [Regla 9]
Op -> >                   [Regla 10]
```

**Símbolos:**
- **Terminales**: `if`, `while`, `(`, `)`, `;`, `id`, `*`, `/`, `==`, `+`, `-`, `>`
- **No Terminales**: `S`, `E`, `Op`
- **Símbolo Inicial**: `S`

---

## 🎯 ¿Cómo funciona el Autómata de Pila?

### 1. Inicialización
La pila comienza con:
```
Pila: [$ S]
```
- `$`: Símbolo de fondo (marca el fin de la pila)
- `S`: Símbolo inicial (de donde parte el análisis)

### 2. Proceso de Análisis

En cada paso:

1. **Toma el tope de la pila** y **el token actual**
2. **Si el tope es un NO TERMINAL:**
   - Busca todas las producciones para ese no terminal
   - Intenta aplicar cada producción **EN ORDEN**
   - Si una producción falla, hace **BACKTRACKING** y prueba la siguiente
   
3. **Si el tope es un TERMINAL:**
   - Compara con el token actual
   - Si coinciden: retira el terminal de la pila y consume el token
   - Si NO coinciden: **FALLO**

4. **Si el tope es `$` y el token es `$`:**
   - **¡ÉXITO!** La entrada fue parseada correctamente

---

## 🔄 ¿Qué es el Backtracking?

**Backtracking** significa "retroceder" cuando una decisión resulta incorrecta.

### Ejemplo con `while(x);`:

```
Paso 1: Pila: [$ S] | Token: 'while'
   -> Intentando Regla 1: S -> if ( E ) ;
   
Paso 2: Pila: [$ ; ) E ( if] | Token: 'while'
   -> Terminal 'if' != 'while'  ❌ FALLO
   <- BACKTRACK: Restaurar pila a [$ S] ⏪
   
   -> Intentando Regla 2: S -> while ( E ) ;
   
Paso 2: Pila: [$ ; ) E ( while] | Token: 'while'
   -> Terminal 'while' == 'while'  ✅ ÉXITO
```

---

## 📝 Estructura de la Clase `Sintactico`

### Atributos

```python
self.a_gramatica = [...]  # Lista de producciones gramaticales
self.tokens = []           # Tokens de entrada
self.indice = 0            # Índice del token actual
self.pila = []             # Pila del autómata
```

---

## 🔍 Métodos Principales

### 1. `__init__(self)`

**Propósito:** Inicializa el analizador sintáctico con la gramática.

**Qué hace:**
- Define todas las producciones gramaticales en `self.a_gramatica`
- Cada producción tiene:
  - `ID`: Número de regla
  - `NT`: No Terminal (lado izquierdo)
  - `Produccion`: Lista de símbolos (lado derecho)

**Ejemplo de producción:**
```python
{"ID": 1, "NT": "S", "Produccion": ["if", "(", "E", ")", ";"]}
```
Representa: `S -> if ( E ) ;`

---

### 2. `m_analizar(self, tokens)`

**Propósito:** Método principal que inicia el análisis sintáctico.

**Parámetros:**
- `tokens`: Lista de tuplas `(lexema, serie)` del analizador léxico

**Proceso:**
1. Agrega token de fin `("$", "$")`
2. Inicializa la pila con `["$", "S"]`
3. Llama a `m_parsear()` para procesar
4. Retorna `True` si la sintaxis es correcta, `False` si hay error

**Ejemplo de entrada:**
```python
tokens = [('while', 'q1200'), ('(', 'q5010'), ('x', 'q6001'), (')', 'q5020'), (';', 'q3020')]
resultado = analizador.m_analizar(tokens)
```

---

### 3. `m_parsear(self)`

**Propósito:** Wrapper que inicia el parsing recursivo.

**Qué hace:**
- Llama a `m_parsear_desde(0, ["$", "S"], 0)`
- Comienza desde el paso 0, con pila inicial `["$", "S"]` e índice 0

---

### 4. `m_parsear_desde(self, paso_inicial, pila_inicial, indice_inicial)`

**Propósito:** Motor principal del parser con backtracking.

**Parámetros:**
- `paso_inicial`: Número de paso para la salida
- `pila_inicial`: Estado de la pila al inicio
- `indice_inicial`: Posición en los tokens

**Algoritmo:**

```
MIENTRAS la pila NO esté vacía:
    1. Obtener tope de pila y token actual
    2. Mostrar estado
    
    3. SI tope == '$':
       -> Verificar si token == '$'
       -> Retornar éxito o fallo
    
    4. SI tope es NO TERMINAL:
       PARA cada producción del no terminal (en orden):
           a. Guardar estado (pila e índice)
           b. Aplicar producción
           c. Continuar parseando recursivamente
           d. SI tuvo éxito -> Retornar True
           e. SI falló -> BACKTRACK (restaurar estado)
       
       -> Si ninguna producción funcionó -> Retornar False
    
    5. SI tope es TERMINAL:
       -> Comparar con token actual
       -> SI coincide: quitar de pila y avanzar token
       -> SI NO coincide: Retornar False

RETORNAR True (pila procesada exitosamente)
```

**Clave del Backtracking:**
```python
# Guardar estado antes de aplicar producción
pila_guardada = self.pila.copy()
indice_guardado = self.indice

# Aplicar producción...

# Si falla, restaurar
self.pila = pila_guardada
self.indice = indice_guardado
```

---

### 5. `m_mostrarEstado(self, paso, top, token_actual)`

**Propósito:** Muestra el estado actual del análisis.

**Salida típica:**
```
Paso 4:
   Pila: [$ ; ) E]
   Tope: 'E' | Token: 'x'
```

---

### 6. `m_esNoTerminal(self, simbolo)`

**Propósito:** Verifica si un símbolo es no terminal.

**Lógica:**
- Busca el símbolo en el lado izquierdo de alguna producción
- Si lo encuentra -> Es no terminal
- Si no -> Es terminal

**Ejemplo:**
```python
m_esNoTerminal("E")     # True (hay producciones E -> ...)
m_esNoTerminal("if")    # False (no hay producciones if -> ...)
```

---

### 7. `m_coincide(self, esperado, token, serie)`

**Propósito:** Verifica si un símbolo esperado coincide con el token actual.

**Casos:**

1. **Si esperado es "id":**
   - Llama a `m_esIdentificador()` para verificar la serie

2. **Si es otro terminal:**
   - Compara directamente: `esperado == token`

**Ejemplo:**
```python
m_coincide("id", "x", "q6001")      # True (serie 6000+)
m_coincide("if", "if", "q1110")     # True (coincidencia exacta)
m_coincide("+", "*", "q2010")       # False (no coincide)
```

---

### 8. `m_esIdentificador(self, token, serie)`

**Propósito:** Verifica si un token es un identificador válido.

**Criterio:**
- Serie >= 6000 son identificadores (`q6001`, `q6002`, ...)
- Serie >= 7000 son números (`q7001`, ...)
- Serie >= 8000 son reales (`q8001`, ...)

**Manejo de series:**
```python
"q6001" -> extrae 6001 -> >= 6000 -> True
"q1110" -> extrae 1110 -> < 6000  -> False
```

---

## 📊 Ejemplo Completo de Ejecución

### Entrada: `while(x);`

**Tokens:** `[('while','q1200'), ('(','q5010'), ('x','q6001'), (')','q5020'), (';','q3020')]`

### Paso a Paso:

```
Paso 1:
   Pila: [$ S]
   Tope: 'S' | Token: 'while'
   -> Intentando regla 1: S -> if ( E ) ;
   
Paso 2:
   Pila: [$ ; ) E ( if]
   Tope: 'if' | Token: 'while'
   -> No coincide 'if' != 'while'. FALLO
   <- BACKTRACK ⏪
   
   -> Intentando regla 2: S -> while ( E ) ;

Paso 2:
   Pila: [$ ; ) E ( while]
   Tope: 'while' | Token: 'while'
   -> Coincide! Consumir 'while'

Paso 3:
   Pila: [$ ; ) E (]
   Tope: '(' | Token: '('
   -> Coincide! Consumir '('

Paso 4:
   Pila: [$ ; ) E]
   Tope: 'E' | Token: 'x'
   -> Intentando regla 3: E -> id Op E

Paso 5:
   Pila: [$ ; ) E Op id]
   Tope: 'id' | Token: 'x'
   -> Coincide! Consumir 'x'

Paso 6:
   Pila: [$ ; ) E Op]
   Tope: 'Op' | Token: ')'
   -> Intentando reglas 5-10 (Op -> *, /, ==, +, -, >)
   -> Todas fallan (ninguna es ')')
   <- BACKTRACK ⏪
   
   -> Intentando regla 4: E -> id

Paso 5:
   Pila: [$ ; ) id]
   Tope: 'id' | Token: 'x'
   -> Coincide! Consumir 'x'

Paso 6:
   Pila: [$ ; )]
   Tope: ')' | Token: ')'
   -> Coincide! Consumir ')'

Paso 7:
   Pila: [$ ;]
   Tope: ';' | Token: ';'
   -> Coincide! Consumir ';'

Paso 8:
   Pila: [$]
   Tope: '$' | Token: '$'
   
[OK] Sintaxis Correcta!
```

---

## 🎓 Conceptos Clave

### 1. **Pila del Autómata**
- Controla qué símbolos faltan por procesar
- Se expande cuando aplica una producción
- Se reduce cuando consume terminales

### 2. **Expansión de No Terminales**
Cuando encuentra un no terminal en el tope:
```
Pila: [$ ; ) E]  ->  Aplicar E -> id Op E
Pila: [$ ; ) E Op id]  (símbolos en orden inverso)
```

### 3. **Backtracking**
Si una rama del árbol de derivación falla, retrocede y prueba otra:
```
E con token 'x' y siguiente ')'
├─ Intenta E -> id Op E  ❌ (Op no coincide con ')')
└─ Intenta E -> id       ✅ (Éxito)
```

### 4. **Símbolos Especiales**
- `$`: Marca el fin de la pila y de la entrada
- `id`: Representa cualquier identificador (serie >= 6000)

---

## 🚀 Modo de Uso

```python
from clases.Sintactico import Sintactico

# Tokens del analizador léxico
tokens = [
    ('while', 'q1200'),
    ('(', 'q5010'),
    ('x', 'q6001'),
    ('+', 'q2040'),
    ('y', 'q6002'),
    (')', 'q5020'),
    (';', 'q3020')
]

# Crear analizador
analizador = Sintactico()

# Analizar
resultado = analizador.m_analizar(tokens)

if resultado:
    print("Sintaxis correcta")
else:
    print("Error sintáctico")
```

---

## ⚠️ Limitaciones

1. **No optimizado**: El backtracking puede ser ineficiente para gramáticas complejas
2. **Gramática fija**: Las reglas están codificadas en el `__init__`
3. **Expresiones simples**: Solo maneja expresiones binarias simples

---

## 🔧 Posibles Mejoras

1. **Gramática configurable**: Leer de archivo externo
2. **Tabla de parsing**: Usar tablas LL(1) para evitar backtracking
3. **Mensajes de error**: Más descriptivos con ubicación exacta
4. **Soporte para más construcciones**: for, do-while, funciones, etc.

---

## 📚 Referencias Teóricas

- **Parsing Top-Down**: Construye el árbol desde el símbolo inicial
- **LL(k)**: Left-to-right, Leftmost derivation, k tokens lookahead
- **Autómata de Pila**: PDA (Pushdown Automaton)
- **Backtracking**: Búsqueda con retroceso

---

## ✅ Conclusión

Este analizador sintáctico implementa un **autómata de pila no determinista con backtracking**, ideal para propósitos educativos porque:

- ✅ Muestra explícitamente la pila en cada paso
- ✅ Visualiza el proceso de backtracking
- ✅ No requiere tablas de parsing complejas
- ✅ Es fácil de entender y depurar

Es menos eficiente que un parser LL(1) con tabla, pero mucho más claro para aprender cómo funcionan los analizadores sintácticos.
