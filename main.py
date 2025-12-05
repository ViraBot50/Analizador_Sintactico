from clases.Automata import Automata
from clases.archivo import Archivo

v_objAutomata=Automata()
v_ctrlArchivos=Archivo()
v_tokens=v_objAutomata.m_obteListTokens()

if isinstance(v_tokens, str):
    v_ctrlArchivos.m_geneOutput(v_tokens, "lexico")
else:
    from clases.Sintactico import Sintactico
    v_objSintactico = Sintactico()
    v_objSintactico.m_analizar(v_tokens)


