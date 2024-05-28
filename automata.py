import os
from graphviz import Digraph

# Crear el directorio si no existe
if not os.path.exists('automatas'):
    os.makedirs('automatas')

def agregar_automata(dot, item, estados, transiciones):
    
    with dot.subgraph(name=f'cluster_{item["category"]}_{item["subcategory"]}') as sub:
        sub.attr(label=f'Category : {item["category"]} \n' +
                 f'Subcategory : {item["subcategory"]} \n'
                 'Autómatas')

        sub.attr(color='blue')
        
        # Configurar el diseño vertical
        sub.attr(rankdir='LR')


        ultimo_estado = list(estados.keys())[-1]

        # Marcar el último estado con un borde adicional
        sub.node(ultimo_estado, label=estados[ultimo_estado], shape='circle', style='filled', color='blue', fontcolor='black', peripheries='2')

        # Agregar estados con círculos azules y letra negra
        for estado, etiqueta in estados.items():
            sub.node(estado, label=etiqueta, shape='circle', style='filled', color='blue', fontcolor='black')

        # Agregar transiciones con círculos azules y líneas grises y completas
        for (origen, destino, etiqueta) in transiciones:
            sub.edge(origen, destino, label=etiqueta, arrowhead='vee', dir='forward', style='solid', color='grey', fontcolor='black')
        # Agregar transiciones con círculos azules y líneas grises y completas
       
def crear_automatas_para_palabras(palabras):
    dot = Digraph(comment='Autómatas para las palabras')
    dot.attr(rankdir='LR') 
    
    palabras_ordenadas = sorted(palabras, key=lambda x: (x["category"], x["subcategory"]))
    palabras_automatas=set()
    for item in palabras_ordenadas:
        category= item["category"]
        palabra = item["value"]
        fila = item["fila"]
        columna= item["columna"]
        if(palabra not in palabras_automatas):
        # Crear transiciones
            transiciones = []
            for i, letra in enumerate(palabra):
                transiciones.append((f'q{i}_{category[0]}-{fila}-{columna}', f'q{i+1}_{category[0]}-{fila}-{columna}', letra))

            # Agregar estados al gráfico
            estados = {f'q{i}_{category[0]}-{fila}-{columna}': f'q{i}_{category[0]}-{fila}-{columna}' for i in range(len(palabra) + 1)}

            agregar_automata(dot,item, estados, transiciones)
            palabras_automatas.add(palabra)

    # Guardar el gráfico
    archivo_salida = 'automatas/automatas_para_palabras.gv'
    dot.render(archivo_salida, view=True)