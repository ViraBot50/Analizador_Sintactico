from warnings import catch_warnings

from clases.archivo import Archivo

class Automata:
    a_estaInicial=""
    a_matriz={}
    a_constantes={}
    a_tokeInvalido=""
    a_excepciones={}


    def __init__(self):
        self.a_estaInicial="q0"
        self.a_matriz=Archivo().m_cargMatrTransicion("input/Matriz_Lexico.xlsx")
        self.a_constantes["q6000"]=  6001
        self.a_constantes["q7000"] = 7001
        self.a_constantes["q8000"] = 8001
        self.a_excepciones={"q2060","q2090","q2120","q2130","q2150","q2170"}

    def m_inicReviLexico(self):
        v_respuesta=""
        v_listTokens=self.m_obteListTokens()


        # Estados de error:
        # q999: Identificador no valido
        # q998: Cadena numerica no valida
        if "q999" in v_listTokens:
            print("Error(id): q999")
            v_respuesta= v_listTokens["q999"]
        elif "q998" in v_listTokens:
            print("Error(num): q998")
            v_respuesta = v_listTokens["q998"]
        else:
            v_respuesta= self.m_tabuListTokens(v_listTokens)

        return v_respuesta

    def m_tabuListTokens(self, p_listTokens):
        # Quitar prefijo 'q' de los estados antes de procesar
        tokens_limpios = {token: estado.replace("q", "") for token, estado in p_listTokens.items()}

        # Calcular anchos dinámicos
        ancho_token = max(len("TOKEN"), max(len(token) for token in tokens_limpios.keys())) + 2
        ancho_serie = max(len("SERIE"), max(len(serie) for serie in tokens_limpios.values())) + 2

        # Encabezados (ligeramente hacia la izquierda → sin centrar demasiado)
        titulo_token = "TOKEN".ljust(ancho_token)
        titulo_serie = "SERIE".ljust(ancho_serie)

        v_respuesta = f"{titulo_token}{titulo_serie}\n"
        v_respuesta += "-" * (ancho_token + ancho_serie) + "\n"

        # Filas
        for token, serie in tokens_limpios.items():
            v_respuesta += f"{token.ljust(ancho_token)}{serie.ljust(ancho_serie)}\n"

        return v_respuesta

    def m_obteListTokens(self):
        v_respuesta={}
        v_codigo=Archivo().m_leerDocumento("input/code.in")
        v_linea=0
        v_error=False

        while v_linea<len(v_codigo) and not v_error:
            if (v_codigo[v_linea]!= " ") :
                print("Linea: ",v_linea)
                v_error=self.m_veriErroLinea(v_codigo[v_linea],v_respuesta)

            v_linea+=1

        if v_error:
            v_respuesta.clear()
            if v_error == "q999":
                v_respuesta["q999"]="Error en la linea: "+str(v_linea)+". Por identificador no valido... "+self.a_tokeInvalido+" <--"
            elif v_error == "q998":
                v_respuesta["q998"]="Error en la linea: "+str(v_linea)+". Por valor numérico no valido... "+self.a_tokeInvalido+" <--"

        return v_respuesta



    def m_veriErroLinea(self,p_linea,p_listTokens):
        v_respuesta=False
        v_estaActual = self.a_estaInicial
        v_tokeActual=""
        v_caracter=""
        v_posicion=0
        v_lengLinea=len(p_linea)
        while v_posicion<v_lengLinea and (v_estaActual!="q999" and v_estaActual != "q998" ):
            v_caracter = ""
            v_tokeActual = ""
            v_estaActual = self.a_estaInicial

            #while automata
            while v_posicion<v_lengLinea and v_estaActual in self.a_matriz and self.a_matriz[v_estaActual]["a"]!="-" :
                v_caracter=p_linea[v_posicion]
                v_tokeActual+=v_caracter

                if v_caracter==" ":
                    v_caracter="espacio"

                v_estaActual=self.a_matriz[v_estaActual][v_caracter]
                v_posicion+=1
            #end while automata
            print("Estado actual: ",v_estaActual,"+ Token actual: ",v_tokeActual)
            if v_estaActual!="q0" :

                if v_estaActual=="q999" or v_estaActual=="q998":
                    # Si empieza con digito y dio error, asignar q998 (error numerico)
                    if v_tokeActual and v_tokeActual[0].isdigit():
                        v_respuesta="q998"
                    else:
                        v_respuesta=v_estaActual
                    self.a_tokeInvalido=v_tokeActual
                else:
                    if v_caracter != "espacio" and (self.m_veriRequEspacio(v_estaActual,2000,5040) or v_estaActual in self.a_excepciones) :
                        v_posicion -= 1
                        v_tokeActual = v_tokeActual[:-1] 

                    v_tokeActual = v_tokeActual.strip() #! cambio
                    if v_tokeActual not in p_listTokens:
                        if v_estaActual in self.a_constantes:
                            p_listTokens[v_tokeActual]="q"+str(self.a_constantes[v_estaActual])
                            self.a_constantes[v_estaActual]+=1
                        else:
                            p_listTokens[v_tokeActual] = v_estaActual




        return v_respuesta


    def m_veriRequEspacio(self,p_Serie,p_limiInferior,p_limiSuperior):
        v_respuesta=False
        num = int(p_Serie[1:])
        if not (p_limiInferior <= num <= p_limiSuperior):
            v_respuesta=True

        return v_respuesta