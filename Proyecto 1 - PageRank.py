"""
Programación 9292
Proyecto 1 - PageRank
autor: Jiménez Malvaez Raúl Emilio
"""

#Comenzamos por crear la clase Grafica, la cual dispone de nodos y aristas, que pueden ser agregados o eliminados
class Grafica:
    #En primer lugar, asignamos a la clase Gráfica sus dos elementos: nodos y aristas.
    def __init__(self):
        """
        Inicializa una gráfica con nodos y aristas vacíos. Un diccionario que almacena las aristas de la gráfica.
        Los nodos pueden ser almacenados como set, pues constan de un solo valor, mientras que
        Las aristas se almacenan en un diccionario donde tenemos (nodo1, nodo2) y los pesos de las aristas.
        """
        self.nodos = set()
        self.aristas = {}

    #Ahora definimos los métodos.
    #Con esta función asignamos a la clase Grafica la capacidad de agregar nodos
    def agregar_nodo(self, nodo):
        self.nodos.add(nodo)
    """
    Con esta función asignamos a la clase Grafica la capacidad de agregar aristas (unión entre 2 nodos)
    Incluimos un argumento llamado peso, cuyo valor por defecto será 1
    """
    def agregar_arista(self, nodo1, nodo2, peso=1):
        self.agregar_nodo(nodo1)
        self.agregar_nodo(nodo2)
        self.aristas[(nodo1, nodo2)] = peso

    #Con esta función asignamos a la clase Grafica la capacidad de eliminar nodos
    def eliminar_nodo(self, nodo):
        if nodo in self.nodos:
            self.nodos.remove(nodo)
            for arista in list(self.aristas.keys()):  # Iterar sobre una copia de las llaves
                if nodo in arista:
                    del self.aristas[arista]

    #Con esta función asignamos a la clase Grafica la capacidad de eliminar aristas
    def eliminar_arista(self, nodo1, nodo2):
        if (nodo1, nodo2) in self.aristas:
            del self.aristas[(nodo1, nodo2)]

"""
Ahora definimos la clase Red, que hereda de la clase Grafica.
Esta clase tendrá una funcion para relacionar las aristas con sus pesos
"""
class Red(Grafica):
    #Inicializamos la red con su respectiva funcion
    def __init__(self, funcion):
        #Se usa la funcion super() para conservar métodos y atributos de la clase padre (Gráfica)
        super().__init__()
        self.funcion = funcion

    #Definimos una función que calcule la importancia de una página de acuerdo a la fórmula estipulada
    def calcular_importancia(self, pagina):
        #La importancia predeterminada es cero, pero cambiará para cada nodo de acuerdo a la cantidad de referencias
        importancia = 0
        for nodo in self.nodos:
            if (nodo, pagina) in self.aristas:
                peso_arista = self.funcion((nodo, pagina))
                """
                Suma la importancia de los nodos que enlazan a la página, de acuerdo al peso de la arista 
                y la cantidad de enlaces
                # salientes del nodo.
                """
                importancia += peso_arista / sum(1 for _, dest in self.aristas.keys() if _ == nodo)
        return importancia

#Por último, creamos una clase que calcule el Ranking de cada red
class PageRank:
    #Inicializamos la  clase para las redes para las cuales calcularemos el Ranking
    def __init__(self, red):
        self.red = red

    #Definimos la funcion que calculará el ranking según cierto número de iteraciones
    def calcular_ranking(self, d=0.85, num_iteraciones=100):
        """
        Investigando más a profundidad la historia de PageRank noté que en el código original se implementó un
        "factor de amortiguación", que representa la probabilidad de que un usuario siga un enlace a la página actual.
        Este factor parece ser necesario para el código, pues evita que las páginas que no tienen enlaces salientes
        acumulen todo el Ranking. Utilicé el factor de amortiguación propuesto por los creadores de PageRank.
        """
        #n es el número de nodos definidos
        n = len(self.red.nodos)
        #pagerank nos da el ranking del sitio
        pagerank = {pagina: 1/n for pagina in self.red.nodos}
        #Con un ciclo for recorremos el rango de todas las iteraciones
        for _ in range(num_iteraciones):
            #Definimos pagerank_actual como un diccionario que enlazara cada sitio con su ranking
            pagerank_actual = {}
            #Con un ciclo for iteramos sobre cada página en la red de nodos
            for pagina in self.red.nodos:
                #Ingresamos una variable suma que inicialmente valdrá cero
                suma = 0
                #Con un ciclo for iteramos sobre cada nodo en la red de nodos
                for nodo in self.red.nodos:
                    #Si existe una arista entre el nodo y la pagina, este condicional se ejecuta
                    if (nodo, pagina) in self.red.aristas:
                        """
                        Esta es la parte más relevante del código, por lo que la describiremos a profundidad:
                        suma += acualiza la variable suma y acumula la importancia total de la pagina de acuerdo a las aristas que llegan de otros nodos
                        pagerank[nodo] accede a los valores del diccionario pagerank
                        self.red.funcion(nodo, página) llama a la funcion f para obtener el peso de la arista que va de nodo a página
                        sum(1 for _, dest in self.red.aristas.keys() if _ == nodo) calcula los enlaces salientes
                        """
                        suma += pagerank[nodo] * self.red.funcion((nodo, pagina)) / sum(1 for _, dest in self.red.aristas.keys() if _ == nodo)
                #Modificamos el diccionario actual para cada pagina, en base al factor de amortiguación, la cantidad de nodos y su suma
                pagerank_actual[pagina] = (1 - d) / n + d * suma
            #Lo anterior nos devuelve un diccionario con los ranking de cada pagina    
            pagerank = pagerank_actual
        return pagerank
"""
Para evitar importar los datos desde excel, vamos a facilitar este proceso creando un diccionario que relacione las keys
"Pagina", "Indice", y "Citada por"
"""

datos = {
    "Pagina": ["nytimes.com", "washingtonpost.com", "cnn.com", "foxnews.com", "forbes.com", "bloomberg.com",\
               "wsj.com", "huffpost.com", "businessinsider.com", "npr.org", "techcrunch.com", "theverge.com",\
                "reuters.com", "politico.com", "mashable.com", "yandex.ru", "lenta.ru", "gazeta.ru", \
                    "ria.ru", "rbk.ru", "tass.ru", "iz.ru", "kommersant.ru", "vedomosti.ru", \
                          "regnum.ru", "federalreserve.gov"
               ],
    "Indice": ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", \
               "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26"
               ],
    "Citada por": ["2, 7, 11", "1, 4, 6, 9", "1, 5, 9, 11", "2, 3, 8, 14", "3, 12, 15", "2, 8, 13, 15", \
                   "3, 9, 10", "2, 4, 5, 12", "2, 3, 7, 13, 15", "4, 7, 8", "1, 3, 15", "5, 8, 13", \
                   "1, 9, 12, 15", "4, 5, 6", "5, 6, 9, 11, 13", "17, 18, 20", "16, 19, 21", "16, 20, 22", \
                   "17, 21, 24", "16, 18, 22, 23", "17, 19, 24", "18, 20, 25", "20, 24, 25", "19, 21, 23, 25", \
                   "22, 23, 24", "1, 2, 5, 7, 9, 26"
                   ]
}

#Una vez concluido lo anterior, ejecutamos el código principal
if __name__ == "__main__":
    #n será la cantidad de páginas
    n = len(datos["Pagina"])
    # Función lambda (para crear funciones anónimas y sin necesidad de definirlas formalmente) que asigna 1/n a cada arista
    funcion = lambda arista: 1/n

    #Llamamos a la clase red
    red = Red(funcion)

    # Agregamos los nodos y las aristas a la red
    for i in range(n):
        #Extraemos la totalidad de páginas de nuestro diccionario
        pagina = datos["Pagina"][i]
        #Extraemos las citas de nuestro diccionario, utilizando "," para separar cada elemento
        citada_por = datos["Citada por"][i].split(',')
        #Se agrega una arista cada vez que una página cite a otra
        for j in citada_por:
            red.agregar_arista(int(j), pagina)

    #Llamamos a la clase PageRank
    pagerank = PageRank(red)

    """
    A partir de este punto, vamos a imprimir los datos que respondan a las preguntas del proyecto, que son las siguientes:
    """

    #Pregunta I
    print("(I) ¿Cuál es la página web más importante según el algoritmo si se inicia con el vector (1/n,...,1/n)?")

    #Calcular el PageRank con el vector de pesos
    ranking = pagerank.calcular_ranking()
    pagina_mas_importante = max(ranking, key=ranking.get)
    print("\033[91mPágina más importante:\033[00m" + pagina_mas_importante)

    #Pregunta II
    print("\n(II) Defina ahora un vector π de la siguiente forma \
πk =\n\
1/s si la página k tiene terminación .ru,\t\t\
0 e.o.c.\n\
donde s es el número de páginas con terminación .ru. ¿La página de la pregunta 1 sigue siendo la más\
importante?")

    #Para responder a la pregunta modificamos el vector de pesos
    def funcion_modificada(arista):
        # Asignar 1/s si la página tiene terminación .ru, 0 en caso contrario
        pagina_destino = arista[1]
        if pagina_destino.endswith(".ru"):
            #s es el numero de paginas en el diccionario con terminación "".ru"
            s = sum(1 for pagina in datos["Pagina"] if pagina.endswith(".ru"))
            return 1/s
        else:
            return 0

    # Actualizar la función de pesos en la red
    red.funcion = funcion_modificada

    # Calcular el Ranking con el nuevo vector de pesos inicial
    ranking_ru = pagerank.calcular_ranking()
    pagina_mas_importante_ru = max(ranking_ru, key=ranking_ru.get)
    print("\033[91mPágina más importante con terminación .ru:\033[00m" + pagina_mas_importante_ru)

    #Pregunta III
    print("\n(III) Considere ahora la ecuación iterativa πm+1 = πm(dP + (1−d)U ), donde la matriz U queda definida \
con entradas ui,j = 1/n, para toda i, j ∈ {1,...,n} y d ∈ [0,1]. Utilice los valores 0.5,0.85,1 para d y \
reporte los resultados. De los tres valores anteriores para d, \
¿cuál considera que es el mejor (según los ordenamientos obtenidos) y por qué?")

    #Para responder a la última pregunta, tenemos que modificar nuestro factor de amortiguación d con los valores 0.5, 0.85, y 1
    #Comenzamos con d = 0.5
    def calcular_ranking(self, d=0.5, num_iteraciones=100):
        """
        En esta ocasión, y de acuerdo a lo que pide el proyecto, utilicé 0.5 como factor de amortiguación.
        """
        #n es el número de nodos definidos
        n = len(self.red.nodos)
        #pagerank nos da el ranking del sitio
        pagerank = {pagina: 1/n for pagina in self.red.nodos}
        #Con un ciclo for recorremos el rango de todas las iteraciones
        for _ in range(num_iteraciones):
            #Definimos pagerank_actual como un diccionario que enlazara cada sitio con su ranking
            pagerank_actual = {}
            #Con un ciclo for iteramos sobre cada página en la red de nodos
            for pagina in self.red.nodos:
                #Ingresamos una variable suma que inicialmente valdrá cero
                suma = 0
                #Con un ciclo for iteramos sobre cada nodo en la red de nodos
                for nodo in self.red.nodos:
                    #Si existe una arista entre el nodo y la pagina, este condicional se ejecuta
                    if (nodo, pagina) in self.red.aristas:
                        """
                        Esta es la parte más relevante del código, por lo que la describiremos a profundidad:
                        suma += acualiza la variable suma y acumula la importancia total de la pagina de acuerdo a las aristas que llegan de otros nodos
                        pagerank[nodo] accede a los valores del diccionario pagerank
                        self.red.funcion(nodo, página) llama a la funcion f para obtener el peso de la arista que va de nodo a página
                        sum(1 for _, dest in self.red.aristas.keys() if _ == nodo) calcula los enlaces salientes
                        """
                        suma += pagerank[nodo] * self.red.funcion((nodo, pagina)) / sum(1 for _, dest in self.red.aristas.keys() if _ == nodo)
                #Modificamos el diccionario actual para cada pagina, en base al factor de amortiguación, la cantidad de nodos y su suma
                pagerank_actual[pagina] = (1 - d) / n + d * suma
            #Lo anterior nos devuelve un diccionario con los ranking de cada pagina    
            pagerank = pagerank_actual
        return pagerank

    #Calculamos el ranking para d = 0.5
    ranking = pagerank.calcular_ranking()
    pagina_mas_importante_050 = max(ranking, key=ranking.get)

    #Y ahora calculamos para d = 1.0
    def calcular_ranking(self, d= 1.0, num_iteraciones=100):
        """
        En esta ocasión, y de acuerdo a lo que pide el proyecto, utilicé 1.0 como factor de amortiguación.
        """
        #n es el número de nodos definidos
        n = len(self.red.nodos)
        #pagerank nos da el ranking del sitio
        pagerank = {pagina: 1/n for pagina in self.red.nodos}
        #Con un ciclo for recorremos el rango de todas las iteraciones
        for _ in range(num_iteraciones):
            #Definimos pagerank_actual como un diccionario que enlazara cada sitio con su ranking
            pagerank_actual = {}
            #Con un ciclo for iteramos sobre cada página en la red de nodos
            for pagina in self.red.nodos:
                #Ingresamos una variable suma que inicialmente valdrá cero
                suma = 0
                #Con un ciclo for iteramos sobre cada nodo en la red de nodos
                for nodo in self.red.nodos:
                    #Si existe una arista entre el nodo y la pagina, este condicional se ejecuta
                    if (nodo, pagina) in self.red.aristas:
                        """
                        Esta es la parte más relevante del código, por lo que la describiremos a profundidad:
                        suma += acualiza la variable suma y acumula la importancia total de la pagina de acuerdo a las aristas que llegan de otros nodos
                        pagerank[nodo] accede a los valores del diccionario pagerank
                        self.red.funcion(nodo, página) llama a la funcion f para obtener el peso de la arista que va de nodo a página
                        sum(1 for _, dest in self.red.aristas.keys() if _ == nodo) calcula los enlaces salientes
                        """
                        suma += pagerank[nodo] * self.red.funcion((nodo, pagina)) / sum(1 for _, dest in self.red.aristas.keys() if _ == nodo)
                #Modificamos el diccionario actual para cada pagina, en base al factor de amortiguación, la cantidad de nodos y su suma
                pagerank_actual[pagina] = (1 - d) / n + d * suma
            #Lo anterior nos devuelve un diccionario con los ranking de cada pagina    
            pagerank = pagerank_actual
        return pagerank

    #Calculamos el ranking para d = 1.0
    ranking = pagerank.calcular_ranking()
    pagina_mas_importante_100 = max(ranking, key=ranking.get)
    
    #Imprimimos nuestros datos para cada valor de d
    print("\033[91mPágina más importante modificando el factor de amortiguación:\033[00m")
    print("Para el valor d = \033[91m 0.5\033[00m : "  + pagina_mas_importante_050)
    print("Para el valor d = \033[91m 0.85\033[00m : " + pagina_mas_importante)
    print("Para el valor d = \033[91m 1.0\033[00m : " + pagina_mas_importante_100)
    #E imprimimos cuál es el mejor de los ordenamientos
    print("Como explicamos entre las línes 80 y 85 de este código, \033[91m el mejor valor para d es 0.85\033[00m , el valor propuesto \
originalmente por Larry Page y Sergey Brin. Recordemos que el factor de amortiguación d representa la \
probabilidad de que un usuario siga un enlace en cierta página.")