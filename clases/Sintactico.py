class Sintactico:
    def __init__(self):
        # Pila inicializada con el símbolo de fondo ($) y el símbolo inicial (S)
        self.pila = ["$", "S"]

    def m_analizar(self, tokens):
        # tokens es una lista de tuplas (lexema, serie)
        # Agregamos un token de fin de cadena para facilitar el manejo
        tokens.append(("$", "$"))
        
        indice = 0
        print(f"Tokens: {tokens}")

        while len(self.pila) > 0:
            top = self.pila[-1] # Ver el tope de la pila
            token_actual, serie_actual = tokens[indice]

            print(f"Pila: {self.pila} \t | Token actual: {token_actual} ({serie_actual})")


            if top == "$":
                if token_actual == "$":
                    print("--> Pila vacía y entrada consumida. ¡Sintaxis Correcta!")
                    return
                else:
                    print("--> Error: Pila vacía pero queda entrada.")
                    return

            # Expansión de No Terminales
            if top == "S":
                self.pila.pop()
                # S -> if ( C ) ;
                
                # S = simbolo inicial (sentencai)
                # C = condicion

                # Empujar en orden inverso: ;, ), C, (, if
                self.pila.append(";")
                self.pila.append(")")
                self.pila.append("C")
                self.pila.append("(")
                self.pila.append("if")
            
            elif top == "C":
                self.pila.pop()
                # C -> ID OP ID

                # C = condicion
                # ID = identificador
                # OP = operador

                # Empujar en orden inverso: ID, OP, ID
                self.pila.append("ID")
                self.pila.append("OP")
                self.pila.append("ID")

            # Coincidencia de Terminales
            elif top in ["if", "(", ")", ";", "ID", "OP"]:
                if self.m_coincide(top, token_actual, serie_actual):
                    self.pila.pop()
                    indice += 1
                else:
                    print(f"--> Error Sintáctico: Se esperaba '{top}' pero se encontró '{token_actual}' ({serie_actual})")
                    return
            
            else:
                print(f"--> Error Interno: Símbolo desconocido en pila '{top}'")
                return

    def m_coincide(self, esperado, token, serie):
        # Aquí definimos las reglas de coincidencia basadas en los tokens del analizador léxico
        
        if esperado == "if":
            return token == "if"
        
        elif esperado == "(":
            return token == "("
        
        elif esperado == ")":
            return token == ")"
        
        elif esperado == ";":
            return token == ";"
        
        elif esperado == "ID":
            # Series 6000+ son identificadores/constantes
            try:
                if isinstance(serie, str) and serie.startswith('q'):
                    serie_num = int(serie[1:])  # Quitamos el primer carácter 'q'
                else:
                    serie_num = int(serie)
                return serie_num >= 6000 or serie_num == 1000 # Ajustar según series reales
            except:
                return False

        elif esperado == "OP":
            return token in [">", "<", "=", ">=", "<=", "=="]
            
        return False
