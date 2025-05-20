# 1.- ---------------- Encabezado ----------------------------------------------

'''
Nombre: Ioshua Daniel Fuertes Espinosa
        Adrian Rodriguez de Matias
Fecha: 08/05/2025
Descripción: Sistema para encontrar la ruta más corta entre estaciones de metro
             utilizando el algoritmo BFS, permitiendo transbordos entre líneas.
'''

# 2.- ---------------- Importación de Módulos y Bibliotecas --------------------
import networkx as nx
import matplotlib.pyplot as plt
from collections import deque

# 3.- ---------------- Definición de Funciones o clases ------------------------
class Nodo:
    def __init__(self, dato):
        self._dato = dato
        self._siguiente = None
        self._anterior = None

class ListaDoblementeEnlazada:
    def __init__(self):
        self._cabeza = None
        self._cola = None

    def agregar(self, dato):
        nuevo_nodo = Nodo(dato)
        if self._cabeza is None:
            self._cabeza = nuevo_nodo
            self._cola = nuevo_nodo
        else:
            nuevo_nodo._anterior = self._cola
            self._cola._siguiente = nuevo_nodo
            self._cola = nuevo_nodo

    def buscar(self, dato):
        nodo_actual = self._cabeza
        while nodo_actual is not None:
            if nodo_actual._dato == dato:
                return nodo_actual
            nodo_actual = nodo_actual._siguiente
        return None

    def recorrer(self):
        resultados = []
        nodo_actual = self._cabeza
        while nodo_actual is not None:
            resultados.append(nodo_actual._dato)
            nodo_actual = nodo_actual._siguiente
        return resultados

class Metro:
    def __init__(self):
        self._grafo = Grafo()  #En esta Parte se coloca un Diccionario en el cual se alacenan el color y lineas de estaciones
        self._lineas = {
            "Rosa": ["Observatorio", "Tacubaya", "Juanacatlán", "Chapultepec", "Sevilla",
                     "Insurgentes", "Cuauhtémoc", "Balderas", "Salto del Agua", "Isabel la Católica",
                     "Pino Suárez", "Merced", "Candelaria", "San Lázaro", "Moctezuma", "Balbuena",
                     "Boulevard Puerto Aéreo", "Gómez Farías", "Zaragoza", "Pantitlán"],
            "Azul": ["Cuatro Caminos", "Panteones", "Tacuba", "Cuitláhuac", "Popotla",
                    "Colegio Militar", "Normal", "San Cosme", "Revolución", "Hidalgo",
                    "Bellas Artes", "Allende", "Zócalo", "Pino Suárez", "San Antonio Abad", "Chabacano", "Viaducto", "Xola"],
            "Verde Olivo": ["Indios Verdes", "Deportivo 18 de Marzo", "Potrero", "La Raza",
                           "Tlatelolco", "Guerrero", "Hidalgo", "Juárez", "Balderas"],
            "Naranja": ["Tacubaya", "Constituyentes", "Auditorio", "Polanco", "San Joaquín", "Tacuba"]
        }

        self._estaciones_info = {}
        self.inicializar_grafo()

    def inicializar_grafo(self): # En esta parte se agregan las vertices osea las estaciones Ej.La Raza.
        for linea, estaciones in self._lineas.items(): # Y se guarda los datos de la estacion
            for estacion in estaciones:
                self._grafo.agregar_vertice(estacion)
                if estacion not in self._estaciones_info:
                    self._estaciones_info[estacion] = {"lineas": [linea]}
                else:
                    self._estaciones_info[estacion]["lineas"].append(linea)
        for linea, estaciones in self._lineas.items(): # Se agregan las Aristas o "Conexiones entre los nodos"
            for i in range(len(estaciones) - 1):
                self._grafo.agregar_arista(estaciones[i], estaciones[i + 1])
                self._grafo.agregar_arista(estaciones[i + 1], estaciones[i])

    def obtener_colores_disponibles(self): # Me refiero a la opcion osea el color de la linea que desea el usurio Ej. Linea color (Azul)
        return sorted(list(self._lineas.keys()))

    def obtener_estaciones_por_color(self, color): # Dependiendo de la linea de color se despliegan los valores del color de la estacion
        if color in self._lineas:                  # Con sus respectivas estciones que se encuentran
            return self._lineas[color]
        return []

    def obtener_linea_de_estacion(self, estacion): # Esta ligada a def obtener_colores_disponibles (acuerdate)
        if estacion in self._estaciones_info:
            return self._estaciones_info[estacion]["lineas"]
        return []

    def obtener_ruta(self, origen, destino): # Se muestra la Ruta del nodo origen a la posicion que deseamos llegar
        return self._grafo.bfs_ruta(origen, destino)

    def obtener_lista_estaciones(self):
        return sorted(list(self._estaciones_info.keys()))

    def mostrar_lineas_disponibles(self): # Se muestran la disponibilidad de las lineas en el menu
        print("\n=== LÍNEAS DE METRO DISPONIBLES ===")
        colores = self.obtener_colores_disponibles()
        for i, color in enumerate(colores):
            print(f"{i+1}. Línea {color}")
        return colores

    def mostrar_estaciones_por_linea(self, color): # Tambien esta ligda a mostrar las estaciones respecto a la linea de color deseada
        if color in self._lineas:
            print(f"\n=== ESTACIONES DE LA LÍNEA {color} ===")
            for i, estacion in enumerate(self._lineas[color]):
                print(f"{i+1}. {estacion}")
            return self._lineas[color]
        else:
            print(f"La línea {color} no existe.")
            return []

    def visualizar_grafo_ruta(self, ruta): # Se creal el grafo con nuestro FIFO en cola con su orden <3 (LA Ruta OJOOOOOOO)
        if not ruta:
            print("No hay ruta para visualizar.")
            return
        G = nx.DiGraph()
        for i, estacion in enumerate(ruta):
            G.add_node(estacion, orden=i+1)
        for i in range(len(ruta) - 1):
            G.add_edge(ruta[i], ruta[i + 1])
        plt.figure(figsize=(14, 10))
        plt.gcf().canvas.manager.set_window_title("Ruta en el Sistema de Metro")
        colores_lineas = {
            "Rosa": '#FF69B4',       # Rosa fuerte
            "Azul": '#1E90FF',       # Azul real
            "Verde Olivo": '#556B2F', # Verde olivo
            "Naranja": '#FF8C00'     # Naranja oscuro
        }
        node_colors = [] # Colorear de su color correspondiente cada nodo
        lineas_por_estacion = {}  # Para incluir en las etiquetas
        for estacion in G.nodes():
            lineas = self.obtener_linea_de_estacion(estacion)
            lineas_por_estacion[estacion] = lineas
            if len(lineas) > 1: # Cuando sea un transbordo se pondra un color diferente
                color = '#800080'  #Purpura
            else:               # Condicionar que color es correspondinte depende de la posicion original a la llegada
                linea = lineas[0]
                color = colores_lineas.get(linea, '#A9A9A9')
            node_colors.append(color)
        lineas_activas = {}      # Calcular la línea activa para cada tramo del recorrido
        for i in range(len(ruta) - 1):
            estacion_actual = ruta[i]
            estacion_siguiente = ruta[i + 1]
            lineas_actuales = set(self.obtener_linea_de_estacion(estacion_actual)) # Se compara que estaciones estan como que comparten ambas estaciones similares
            lineas_siguientes = set(self.obtener_linea_de_estacion(estacion_siguiente))
            lineas_comunes = lineas_actuales.intersection(lineas_siguientes)
            if lineas_comunes:
                linea_activa = sorted(list(lineas_comunes))[0]
            else:
                linea_activa = sorted(list(lineas_actuales))[0] # Esta seccion definimos la estructura que desemamos sobre nuestro eje x.
            lineas_activas[(estacion_actual, estacion_siguiente)] = linea_activa
        pos = {}
        for i, estacion in enumerate(ruta):
            pos[estacion] = (i, 0)
        nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=2000, edgecolors='black', linewidths=1.5) # Dibujr nodos
        for i in range(len(ruta) - 1):         #Dibujar las Aristas con las estaciones activas
            origen = ruta[i]
            destino = ruta[i + 1]
            linea_actual = lineas_activas.get((origen, destino), "")
            color_arista = colores_lineas.get(linea_actual, 'black')
            nx.draw_networkx_edges(
                G, pos,
                edgelist=[(origen, destino)],
                width=3,
                edge_color=color_arista,
                arrowstyle='-|>',
                arrowsize=20,
                alpha=0.8
            )
        labels = {}      # Crear etiquetas con número de orden y líneas
        for node in G.nodes():
            orden = G.nodes[node]['orden']
            lineas_texto = ", ".join(lineas_por_estacion[node])
            labels[node] = f"{node}\n({orden})\n{lineas_texto}"
        nx.draw_networkx_labels(G, pos, labels=labels, font_size=9, font_weight='bold')
        plt.axis('off')
        plt.title(f"Ruta completa del metro a seguir", fontsize=14, fontweight='bold')
        plt.tight_layout()
        plt.show()

class Grafo:
    def __init__(self):
        self._vertices = {}
        self._adyacencias = {}

    def agregar_vertice(self, vertice):
        if vertice not in self._vertices:
            self._vertices[vertice] = []
            self._adyacencias[vertice] = []

    def agregar_arista(self, origen, destino):
        if origen in self._vertices and destino in self._vertices:
            self._vertices[origen].append(destino)
            self._adyacencias[origen].append(destino)

    def mostrar_grafo(self):
        for vertice, aristas in self._vertices.items():
            print(f"{vertice} -> {aristas}")

    def visualizar_grafo(self):  #Toda esta funcion es par visualizar el mapa completo del metro(Osea las 4 estaciones de color como ejemplo tenemos)
        G = nx.DiGraph()
        for nodo, lista_adyacencia in self._vertices.items():
            G.add_node(nodo)
            for vecino in lista_adyacencia:
                G.add_edge(nodo, vecino)
        plt.figure(figsize=(12, 8))
        plt.gcf().canvas.manager.set_window_title("Grafo del Sistema de Metro")
        nx.draw(G, with_labels=True, node_color='lightblue', node_size=1500,
                font_size=10, font_weight='bold', arrowstyle='-|>',
                pos=nx.spring_layout(G, seed=42))
        plt.show()

    def bfs(self, inicio): #Usar un diccionario para rastrear el camino (osea el camino mas corto)
        visitados = set()
        cola = deque([inicio])
        recorrido = []
        while cola:
            nodo = cola.popleft()
            if nodo not in visitados:
                visitados.add(nodo)
                recorrido.append(nodo)
                cola.extend([vecino for vecino in self._adyacencias[nodo] if vecino not in visitados])
        return recorrido
    def bfs_ruta(self, inicio, destino):
        if inicio not in self._vertices or destino not in self._vertices:
            return None
        padres = {inicio: None}
        visitados = set([inicio])
        cola = deque([inicio])
        while cola:
            nodo_actual = cola.popleft()
            if nodo_actual == destino: # Reconstruir el camino
                camino = []
                actual = destino
                while actual is not None:
                    camino.append(actual)
                    actual = padres[actual]
                camino.reverse()
                return camino
            for vecino in self._adyacencias[nodo_actual]:
                if vecino not in visitados:
                    visitados.add(vecino)
                    padres[vecino] = nodo_actual
                    cola.append(vecino)
        return None  # No hay camino entre inicio y destino

class Menu:
    def __init__(self):
        self._metro = Metro()

    def mostrar_menu_principal(self): #Menu con las funciones establecidas
        print("\n========================================")
        print("  SISTEMA DE METRO - BÚSQUEDA DE RUTAS  ")
        print("========================================")
        print("1. Ver líneas de metro disponibles")
        print("2. Ver estaciones por línea")
        print("3. Buscar ruta entre estaciones")
        print("4. Visualizar grafo completo del metro")
        print("5. Salir")

        opcion = input("\nSeleccione una opción (1-5): ")
        return opcion

    def menu_ver_estaciones(self):
        colores = self._metro.mostrar_lineas_disponibles()
        try:
            indice_color = int(input("\nSeleccione el número de la línea para ver sus estaciones: ")) - 1
            if 0 <= indice_color < len(colores):
                color = colores[indice_color]
                self._metro.mostrar_estaciones_por_linea(color)
            else:
                print("Número de línea no válido.")
        except ValueError:
            print("Por favor, ingrese un número entero válido.")
        input("\nPresione Enter para continuar...")

    def menu_buscar_ruta(self): # Mostrar todas las líneas
      colores = self._metro.mostrar_lineas_disponibles() # Obtener y mostrar las líneas disponibles

      try:
          # Seleccionar línea de origen por número
          indice_color_origen = int(input("\nSeleccione el número de la línea donde se encuentra: ")) - 1
          if not (0 <= indice_color_origen < len(colores)):
              print("Número de línea no válido.")
              return

          color_origen = colores[indice_color_origen]
          estaciones_origen = self._metro.mostrar_estaciones_por_linea(color_origen) # Mostrar estaciones de origen

          # Seleccionar estación de origen por número
          indice_estacion_origen = int(input("\nSeleccione el número de la estación donde se encuentra: ")) - 1
          if not (0 <= indice_estacion_origen < len(estaciones_origen)):
              print("Número de estación no válido.")
              return

          estacion_origen = estaciones_origen[indice_estacion_origen]

          # Seleccionar línea de destino por número
          indice_color_destino = int(input("\nSeleccione el número de la línea a donde desea ir: ")) - 1
          if not (0 <= indice_color_destino < len(colores)):
              print("Número de línea no válido.")
              return

          color_destino = colores[indice_color_destino]
          estaciones_destino = self._metro.mostrar_estaciones_por_linea(color_destino) # Mostrar estaciones de destino

          # Seleccionar estación de destino por número
          indice_estacion_destino = int(input("\nSeleccione el número de la estación a donde desea ir: ")) - 1
          if not (0 <= indice_estacion_destino < len(estaciones_destino)):
              print("Número de estación no válido.")
              return

          estacion_destino = estaciones_destino[indice_estacion_destino]

      except ValueError:
          print("Por favor, ingrese un número entero válido.")
          input("\nPresione Enter para continuar...")
          return

      ruta = self._metro.obtener_ruta(estacion_origen, estacion_destino) # Busca la ruta
      if ruta:
          print(f"\n=== RUTA DE {estacion_origen} A {estacion_destino} ===")
          lista_ruta = ListaDoblementeEnlazada()
          for estacion in ruta:
              lista_ruta.agregar(estacion)
          transbordo_anterior = None
          for i, estacion in enumerate(ruta):
              lineas = self._metro.obtener_linea_de_estacion(estacion) # Determinar la línea actual basándose en la conexión
              if i > 0:                                                # Buscar qué línea comparten esta estación y la anterior
                  estacion_anterior = ruta[i-1]
                  lineas_anterior = set(self._metro.obtener_linea_de_estacion(estacion_anterior))
                  lineas_actual = set(lineas)
                  lineas_comunes = lineas_anterior.intersection(lineas_actual)

                  if lineas_comunes:
                      linea_actual = list(lineas_comunes)[0]  # Usar la primera línea común
                  else:                                      # Si no hay línea común, estamos en un transbordo
                      linea_actual = lineas[0]              # Usar la primera línea de la estación actual
              else:                                         # Para la primera estación, usar la línea de origen
                  linea_actual = color_origen if color_origen in lineas else lineas[0]
              if i > 0:                                        # Se detecta el transbordo
                  estacion_anterior = ruta[i-1]
                  lineas_anterior = self._metro.obtener_linea_de_estacion(estacion_anterior)
                  if set(lineas).intersection(set(lineas_anterior)):  # Hay líneas en común, no es transbordo o es en la misma estación
                      pass                                            # No hay líneas en común, es un transbordo
                  else:
                      linea_anterior = lineas_anterior[0]
                      linea_nueva = lineas[0]
                      transbordo = f"TRANSBORDO en {estacion}: Línea {linea_anterior} → Línea {linea_nueva}"
                      if transbordo != transbordo_anterior:
                          print(f"{transbordo}")
                          transbordo_anterior = transbordo
              if i == 0:
                  print(f"Inicio: {estacion} (Línea {linea_actual})")
              elif i == len(ruta) - 1:
                  print(f"Llegada: {estacion} (Línea {linea_actual})")
              else:
                  print(f"{i}. {estacion} (Línea {linea_actual})")
          print(f"\nTotal de estaciones: {len(ruta)}")

          # Preguntar si quiere visualizar la ruta con opciones numéricas
          print("\n¿Desea visualizar la ruta?")
          print("1. Sí")
          print("2. No")
          try:
              opcion_visualizar = int(input("Seleccione una opción (1-2): "))
              if opcion_visualizar == 1:
                  self._metro.visualizar_grafo_ruta(ruta)
          except ValueError:
              print("Opción no válida. No se visualizará la ruta.")
      else:
          print(f"No se encontró ruta entre {estacion_origen} y {estacion_destino}.")

      input("\nPresione Enter para continuar...")

    def ejecutar(self):
        while True:
            opcion = self.mostrar_menu_principal()  #Acciones con el menu

            if opcion == '1':
                self._metro.mostrar_lineas_disponibles()
                input("\nPresione Enter para continuar...")
            elif opcion == '2':
                self.menu_ver_estaciones()
            elif opcion == '3':
                self.menu_buscar_ruta()
            elif opcion == '4':
                print("\nVisualizando grafo completo del metro...")
                self._metro._grafo.visualizar_grafo()
                input("\nPresione Enter para continuar...")
            elif opcion == '5':
                print("\n¡Gracias por usar el Sistema de Metro!")
                break
            else:
                print("\nOpción no válida. Intente de nuevo.")
                input("\nPresione Enter para continuar...")

# 4.- ---------------- Variables Globales --------------------------------------


# 5.- ---------------- Bloque Principal ----------------------------------------
if __name__ == "__main__":
    try:
        menu = Menu()
        menu.ejecutar()
    except Exception as e:
        print(f"Error en la aplicación: {e}")

# 6.- ---------------- Manejo de Excepciones -----------------------------------

# 7.- ---------------- Documentación y Comentarios---------------------------
