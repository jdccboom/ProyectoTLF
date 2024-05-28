class AnalizadorDeLenguaje:
    def __init__(self, ruta_archivo: str):
        # Inicializa el analizador léxico con la ruta del archivo a analizar
        self.ruta_archivo = ruta_archivo 
        self.texto = self.leer_archivo() # Lee el contenido del archivo
         # Diccionario de categorización para palabras clave y operadores
        self.categorization_dict = {
            "Operadores": {
                "Operadores aritméticos": {
                    "SM":"Suma" ,
                    "RT": "Resta",
                    "MT":"Multiplicación",
                    "DV":"División",
                    "PC":"Potencia",
                    "RZ":"Raíz",
                    "MD":"Módulo",
                },
                "Operadores relacionales": {
                    "II" :"Igualdad",
                    "MAQ" :"Mayor o igual" ,
                    "MEQ":"Menor o igual" ,
                    "MA": "Mayor" ,
                    "ME":"Menor" ,
                    "NII": "Desigual",
                },
                "Operadores lógicos": {
                    "YL":"And",
                    "OL":"Or" ,
                    "NL":"Not",
                },
                "Operador(es) de asignación": {
                    "~":"Igual",
                    "+~":"Más Igual",
                    "-~":"Menos Igual",
                    "~+": "Incremento",
                    "~-": "Decremento",
                },
                "Símbolos de abrir": {
                    "(":"Corchete", 
                    "{":"LLave", 
                    "!":"Admiracion"
                },
                "Símbolos de cerrar": {
                    ")":"Corchete", 
                    "}":"LLave", 
                    "¡":"Admiracion"
                },
                "Terminal y/o inicial": {
                    "?":"Interrogante"
                },
                "Separadores de sentencias": {
                    "/":"Barra", 
                    " ":"Espacio"
                },
            },
            "Palabras reservadas": {
                "Palabra reservada para bucle o ciclo": {
                    "fr":"For", 
                    "wh":"While"
                },
                "Palabra para decisión": {
                    "si": "Decisión", 
                    "sinosi": "Decisión", 
                    "sino": "Decisión"
                },
                "Palabra para la clase": {
                    "Clss":"Clase", 
                    "Iface":"Interfas", 
                    "Enm":"Emun"
                },
                "Tipo de dato": {
                    "Ent": "Enteros",
                    "Rea": "Reales",
                    "Txt": "Cadenas de caracteres",
                    "Crt": "Caracteres",
                },
            },
            "Identificadores": {
                "Identificador de variable": {
                    "Vble":"Variable"
                },
                "identificador de método": {
                    "Met":"Metodo"
                },
                "identificador de clase": {
                    "Clss":"Clase"
                },
            },
            "Valor de Asignación": {
                "Enteros": {"ent":"Asignación"},
                "Reales": {"rea":"Asignación"},
                "Cadenas de caracteres": {"txt":"Asignación"},
                "Caracteres": {"crt":"Asignación"},
            }
        }
        # Variables para seguimiento de palabras anteriores y cadenas de texto
        self.anteriorPalabra=''
        self.cadena=""
        self.fila=0
        self.tabla=[]
        self.categorized_text = self.categorize_text(self.texto)
        
    def analizar(self,ruta):
        self.ruta_archivo=ruta
        self.tabla=[]
        self.texto = self.leer_archivo() # Lee el contenido del archivo
        self.categorized_text = self.categorize_text(self.texto)
        
    def leer_archivo(self) -> str:
        """Lee el archivo y devuelve su contenido."""
        with open(self.ruta_archivo, 'r') as archivo:
            return archivo.read()
    
    def _categorize_word(self, word: str, categorization_dict: dict, row: int, column: int, finRow:int) -> dict:
        """Categorize a single word based on the given categorization dictionary."""
        
        categorized_word = {
            "category": "Desconocido",
            "subcategory": "Desconocido",
            "type": "Desconocido",
            "value": word,
            "fila": row,
            "columna": column
        }
        # Inicializa el diccionario de palabras categorizadas
        # Lógica de categorización de palabras
        
        if (self.anteriorPalabra == ''):
            tamano=len(word)
            if (word[0] == '"' and word[tamano-1] != '"'):
                self.anteriorPalabra='"'
                self.cadena=word +" "
                self.fila=row
                return {}
            if (word[0]=="-" and word[1]=='>'):
                self.anteriorPalabra="->"
                self.cadena=word +" "
                self.fila=row
                return {}
            if (word[0]=="%" and word[1]=='-' and word[2]=='>'):
                self.anteriorPalabra='%->'
                self.cadena=word+ " "
                self.fila=row
                return {}
        
        if word == '"' and self.cadena != "" :
            self.cadena+=word
            self.anteriorPalabra=''
            word=self.cadena
            categorized_word["value"]=word
            self.cadena=""
        
        if self.anteriorPalabra== '->' and column==finRow :
            self.cadena+=word
            self.anteriorPalabra=''
            word=self.cadena
            categorized_word["value"]=word
            self.cadena=""
        
        tamano=len(word)
        if(tamano > 2):
            if(word[tamano-3]=='<' and word[tamano-2]=="-" and word[tamano-1]=='%'):
                self.cadena+=word
                self.anteriorPalabra=''
                word=self.cadena
                categorized_word["value"]=word
                self.cadena=""
        
        if self.anteriorPalabra != '':
            self.cadena += word + ' '
            return {}
        
        for category, subcategories in categorization_dict.items():
            for subcategory, words  in subcategories.items():
                if word in words:
                    categorized_word = {
                        "category": category,
                        "subcategory": subcategory,
                        "value": word,
                        "type": words[word],
                        "fila": row,
                        "columna": column
                    }
                
            
        if categorized_word["category"]!= "Desconocido":
            return categorized_word
        else:
            
            if(self.es_numero(categorized_word["value"])):
                categorized_word["category"] = "Variable"
                categorized_word["subcategory"] = "Enteros"
                categorized_word["type"] = "Valor"
                
            elif(self.es_real(categorized_word["value"])):
                categorized_word["category"] = "Variable"
                categorized_word["subcategory"] = "Reales"
                categorized_word["type"] = "Valor"
            
            elif(self.isHexadecimal(categorized_word["value"])):
                categorized_word["category"] = "Variable"
                categorized_word["subcategory"] = "Hexadecimal"
                categorized_word["type"] = "Valor"
                
            elif(self.isCaracterValor(categorized_word["value"])):
                categorized_word["category"] = "Variable"
                categorized_word["subcategory"] = "Carácter"
                categorized_word["type"] = "Valor"
            
            elif(self.isCadena(categorized_word["value"])):
                categorized_word["category"] = "Variable"
                categorized_word["subcategory"] = "Cadena"
                categorized_word["type"] = "Valor"
                
            elif(self.isComentaryLinea(categorized_word["value"])):
                categorized_word["category"]="Comentarios"
                categorized_word["subcategory"]="Línea"
                categorized_word["type"]="comentario"
              
            elif(self.isComentaryBloque(categorized_word["value"])):
                categorized_word["category"]="Comentarios"
                categorized_word["subcategory"]="Bloque"
                categorized_word["type"]="comentario"
                
            elif(self.isVariable(categorized_word["value"])):
                categorized_word["category"]="Variable"
                categorized_word["subcategory"]="Nombre"
                categorized_word["type"]="Asignacion"
            
            return categorized_word

    def categorize_text(self, text: str) -> list:
        """Categorize the text based on the given categorization dictionary."""
        rows = text.split('\n')
        categorized_text = [{"category": "Category", 
                             "subcategory": "Subcategory",
                             "type":"Type", 
                             "value": "Value", 
                             "fila": "Row", 
                             "columna": "Column"}]
        
        for row_idx, row in enumerate(rows):
            words = row.split()
            for col_idx, word in enumerate(words):
                self.tabla.append(self._categorize_word(word, self.categorization_dict, row_idx + 1, col_idx + 1, len(words)))
        
        self.tabla = [d for d in self.tabla if d]
        categorized_text= categorized_text + self.tabla
        
        return categorized_text
    
    
    # Métodos de validación para tipos específicos de palabras (números, cadenas, etc.)
    def es_numero(self, texto):
        for i, caracter in enumerate(texto):
            if not self.isDigito(caracter) and i == 0:
                return False
            if not self.isDigito(caracter):
                return False
        return True
    
    def es_real(self,texto):
        for i, caracter in enumerate(texto):
            if not self.isDigito(caracter) and i == 0:
                return False
            if caracter == '.':
                if i == len(texto) - 1:
                    return False
                if texto.count('.') > 1:
                    return False
                continue 
            if not self.isDigito(caracter):
                return False
        
        return True
    
    def isLetter(self, caracter):
        if (self.isMayuscula(caracter) or self.isMinuscula(caracter)):
            return True
        return False
    
    
    def isDigito(self,caracter):
        digitos = "0123456789"
        if caracter in digitos:
            return True
        return False
    
    def isMayuscula(self, caracter):
        letras = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        if caracter in letras:
            return True
        return False
    
    def isMinuscula(self, caracter):
        letras = "abcdefghijklmnopqrstuvwxyz"
        if caracter in letras:
            return True
        return False
    
    def isCaracter(self, caracter):
        caracterEspeciales="!\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~ "
        
        if not (self.isLetter(caracter) or caracter in caracterEspeciales or self.isDigito(caracter)):
            return False
        return True
    
    
    def isCaracterValor(self, caracter):        
        if len(caracter) != 3:
            return False
        if caracter[0] !="'":
            return False
        if not (self.isCaracter(caracter[1])):
            return False
        if caracter[2] !="'":
            return False
        return True
    
    def isCadena(self, caracter):
        
        if caracter[0] != '"':
            return False
        for c in caracter:
            if not (self.isCaracter(c)):
                return False
        
        if caracter[len(caracter)-1] != '"':
            return False
        return True
    
    def isComentaryLinea(self, texto):
        
        if texto[0] != '-':
            return False
        if texto[1] != '>':
            return False
        for c in texto:
            if not (self.isCaracter(c)):
                return False
            
        return True
    
    def isComentaryBloque(self, texto):
        
        if texto[0] != '%':
            return False
        if texto[1] != '-':
            return False
        if texto[2] != '>':
            return False
        
        for c in texto:
            if not (self.isCaracter(c)):
                return False
        
        if texto[len(texto)-3] != '<':
            return False
        if texto[len(texto)-2] != '-':
            return False
        if texto[len(texto)-1] != '%':
            return False
        
        return True
    
    def isVariable(self, texto):
        if not (self.isLetter(texto[0])):
            return False
        for c in texto:
            if not (self.isCaracter(c)):
                return False
        return True
    
    def isHexadecimal(self, texto):
        letras="ABCDEF"
        if texto[0] != 'H':
            return False
        for c in texto.split()[1:]:
            if not (self.isDigito(c) or (c in letras) ):
                return False
        return True