class Sintactico:
    def __init__(self):
        self.a_gramatica = [
            {"ID": 1, "NT": "S", "derivacion": ["if", "(", "E", ")", ";"]},
            {"ID": 2, "NT": "S", "derivacion": ["while", "(", "E", ")", ";"]},

            {"ID": 3, "NT": "E", "derivacion": ["id", "Op", "E"]},
            {"ID": 4, "NT": "E", "derivacion": ["id"]},

            {"ID": 5, "NT": "Op", "derivacion": ["*"]},
            {"ID": 6, "NT": "Op", "derivacion": ["/"]},
            {"ID": 7, "NT": "Op", "derivacion": ["=="]},
            {"ID": 8, "NT": "Op", "derivacion": ["+"]},
            {"ID": 9, "NT": "Op", "derivacion": ["-"]},
            {"ID": 10, "NT": "Op", "derivacion": [">"]},
        ]

        self.tokens = []
        self.indice = 0
        self.pila = []

    def m_analizar(self, tokens):
        # Agregamos token de fin de cadena
        self.tokens = tokens.copy()
        self.tokens.append(("$", "$"))
        self.indice = 0
        self.pila = ["$", "S"]

        print(f"Tokens: {[t[0] for t in self.tokens]}\n")

        # Intentamos parsear desde el simbolo inicial S
        resultado = self.m_parsear()

        if resultado and self.indice < len(self.tokens) and self.tokens[self.indice][0] == "$":
            print("\n[OK] Sintaxis Correcta!\n")
            return True
        else:
            print(f"\n[X] Error Sintactico\n")
            return False

    def m_parsear(self):
        return self.m_parsear_desde(0, ["$", "S"], 0)

    def m_parsear_desde(self, paso_inicial, pila_inicial, indice_inicial):
        self.pila = pila_inicial.copy()
        self.indice = indice_inicial
        paso = paso_inicial

        while len(self.pila) > 0:
            paso += 1
            top = self.pila[-1]

            if self.indice >= len(self.tokens):
                return False

            token_actual, serie_actual = self.tokens[self.indice]

            # Mostrar estado actual
            self.m_mostrarEstado(paso, top, token_actual)

            # Si el tope es $, terminar
            if top == "$":
                if token_actual == "$":
                    return True
                return False

            # Si es no terminal, intentar derivaciones con backtracking
            if self.m_esNoTerminal(top):
                derivaciones_posibles = [p for p in self.a_gramatica if p["NT"] == top]

                # Intentar cada derivacion en orden
                for i, derivacion in enumerate(derivaciones_posibles, 1):
                    print(
                        f"   -> Intentando regla {derivacion['ID']}: {derivacion['NT']} -> {' '.join(derivacion['derivacion'])}")

                    # Guardar estado
                    pila_guardada = self.pila.copy()
                    indice_guardado = self.indice

                    # Aplicar derivacion
                    self.pila.pop()
                    for simbolo in reversed(derivacion['derivacion']):
                        self.pila.append(simbolo)

                    print()

                    # Continuar parseando recursivamente
                    if self.m_parsear_desde(paso, self.pila.copy(), self.indice):
                        return True

                    # Si fallo, hacer backtracking
                    print(f"   <- BACKTRACK: Regla {derivacion['ID']} fallo, probando siguiente...")
                    self.pila = pila_guardada
                    self.indice = indice_guardado

                # Ninguna derivacion funciono
                print(f"   -> Ninguna regla para '{top}' funciono. FALLO\n")
                return False

            # Si es terminal, comparar
            else:
                if self.m_coincide(top, token_actual, serie_actual):
                    print(f"   -> Coincide! Consumir '{token_actual}'")
                    self.pila.pop()
                    self.indice += 1
                    print()
                else:
                    print(f"   -> No coincide '{top}' != '{token_actual}'. FALLO\n")
                    return False

        return True

    def m_mostrarEstado(self, paso, top, token_actual):
        pila_str = " ".join(self.pila)
        print(f"Paso {paso}:")
        print(f"   Pila: [{pila_str}]")
        print(f"   Tope: '{top}' | Token: '{token_actual}'")

    def m_seleccionarderivacion(self, no_terminal, token, serie):
        #Comprueba que la primera deriv. coincida
        derivaciones_posibles = [p for p in self.a_gramatica if p["NT"] == no_terminal]

        for prod in derivaciones_posibles:
            primer_simbolo = prod["derivacion"][0]

            # Para no terminales en la derivacion, siempre intentar
            if self.m_esNoTerminal(primer_simbolo):
                return prod

            # Para terminales, verificar coincidencia
            if self.m_coincide(primer_simbolo, token, serie):
                return prod

        return None

    def m_esNoTerminal(self, simbolo):
        for regla in self.a_gramatica:
            if regla["NT"] == simbolo:
                return True
        return False

    def m_coincide(self, esperado, token, serie):
        if esperado == "id":
            return self.m_esIdentificador(token, serie)
        else:
            return esperado == token

    def m_esIdentificador(self, token, serie):
        try:
            if isinstance(serie, str) and serie.startswith('q'):
                serie_num = int(serie[1:])
            else:
                serie_num = int(serie)

            return serie_num >= 6000
        except:
            return False
