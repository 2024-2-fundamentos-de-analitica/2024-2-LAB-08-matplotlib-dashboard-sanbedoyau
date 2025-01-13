# pylint: disable=line-too-long

import pandas as pd
import matplotlib.pyplot as plt
import os
from glob import glob


def pregunta_01():
    '''
    El archivo `files//shipping-data.csv` contiene información sobre los envios
    de productos de una empresa. Cree un dashboard estático en HTML que
    permita visualizar los siguientes campos:

    * `Warehouse_block`

    * `Mode_of_Shipment`

    * `Customer_rating`

    * `Weight_in_gms`

    El dashboard generado debe ser similar a este:

    https://github.com/jdvelasq/LAB_matplotlib_dashboard/blob/main/shipping-dashboard-example.png

    Para ello, siga las instrucciones dadas en el siguiente video:

    https://youtu.be/AgbWALiAGVo

    Tenga en cuenta los siguientes cambios respecto al video:

    * El archivo de datos se encuentra en la carpeta `data`.

    * Todos los archivos debe ser creados en la carpeta `docs`.

    * Su código debe crear la carpeta `docs` si no existe.

    '''
    def create_ouptput_directory(output_directory: str):    # Función auxiliar para crear y limpiar el directorio de salida
        if os.path.exists(output_directory):
            for file in glob(f'{output_directory}/*'):
                os.remove(file)
            os.rmdir(output_directory)
        os.makedirs(output_directory)
    in_path = 'files/input'                                 # Path del directorio de inputs
    out_path = 'docs'                                 # Path del directorio de outputs

    df = pd.read_csv(f'{in_path}/shipping-data.csv')        # Importar el dataset

    def create_for_shipping_per_warehouse(DataFrame: pd.DataFrame):     # Función para crear el gráfico relacionado con la columna 'Warehouse_block'
        plt.figure()                                                    # Crear una nueva figura
        counts = DataFrame.Warehouse_block.value_counts()               # Extraer las cantidades de envíos de cada almacén
        counts.plot.bar(title = 'Shipping per Warehouse',               # Crear un gráfico de barras con las ocurrencias
                        xlabel = 'Warehouse block',
                        ylabel = 'Record count',
                        color = 'tab:blue',
                        fontsize = 8)
        plt.gca().spines['top'].set_visible('False')                    # Hacer invisible el eje horizontal superior
        plt.gca().spines['right'].set_visible('False')                  # Hacer invisible el eje vertical derecho
        plt.savefig(f'{out_path}/shipping_per_warehouse.png')           # Guardar el gráfico
    
    def create_for_mode_of_shipment(DataFrame: pd.DataFrame):           # Función para crear el gráfico relacionado con la columna 'Mode_of_Shipment'
        plt.figure()                                                    # Crear una nueva figura
        counts = DataFrame.Mode_of_Shipment.value_counts()              # Extraer las ocurrencias de cada modo de envío
        counts.plot.pie(title= 'Mode of Shipment',                      # Crear un gráfico de torta con las ocurrencias
                        wedgeprops = dict(width = 0.35),                # Asigna el ancho del espacio en blanco dentro de la torta
                        ylabel = '',
                        colors = ['tab:blue', 'tab:orange', 'tab:green'])
        plt.savefig(f'{out_path}/mode_of_shipment.png')                 # Guardar el gráfico
    
    def create_for_average_customer_rating(DataFrame: pd.DataFrame):    # Función para crear el gráfico de promedio de calificaciones de los usuarios por el modo de envío
        plt.figure()                                                    # Crear una nueva figura
        df = DataFrame.copy()                                           # Hacer una copia del dataframe para no modificarlo
        df = (df[['Mode_of_Shipment', 'Customer_rating']]               # Crear el dataframe de los estadísticos de las calificaciones de los usuarios
              .groupby('Mode_of_Shipment').describe())                  # agrupados por el modo de envío
        df.columns = df.columns.droplevel()                             # Eliminar el nivel superior del titulo de las columnas ('Customer_rating')
        df = df[['mean', 'min', 'max']]                                 # Escoger únicamente los mínimos, máximos y promedios
        plt.barh(y = df.index.values,                                   # Crear un gráfico de barras horizontal con fondos grises
                 width = df['max'].values - 1,                          
                 left = df['min'].values,
                 height = 0.9,
                 color = 'lightgray',
                 alpha = 0.8)
        colors = ['tab:green' if value >= 3 
                  else 'tab:orange' 
                  for value in df['mean'].values]
        
        plt.barh(y = df.index.values,                                   # Crear un gráfico de barras horizontal con los valores de las medias
                 width = df['mean'].values - 1,                         # sobre el gráfico de barras previo
                 left = df['min'].values,
                 height = 0.5,
                 color = colors,
                 alpha = 1)
        plt.title('Average Customer Rating')                            # Añadir título al gráfico
        plt.gca().spines['left'].set_color('gray')                      # Modificar color a gris del eje vertical izquierdo
        plt.gca().spines['bottom'].set_color('gray')                    # Modificar color a gris del eje horizontal inferior
        plt.gca().spines['top'].set_visible(False)                      # Hacer invisible el eje horizontal superior
        plt.gca().spines['right'].set_visible(False)                    # Hacer invisible el eje vertical derecho
        plt.savefig(f'{out_path}/average_customer_rating.png')          # Guardar el gráfico
    
    def create_for_weight_distribution(DataFrame: pd.DataFrame):        # Función para crear el gráfico relacionado con la columna 'Weight_in_gms'
        plt.figure()                                                    # Crear una figura nueva
        DataFrame.Weight_in_gms.plot.hist(                              # Crear un histograma de las distribución del peso en gramos de los envíos
            title = 'Shipped weight distribution',
            color = 'tab:orange',
            edgecolor = 'white'
        )
        plt.gca().spines['top'].set_visible(False)                      # Hacer invisible el eje horizontal superior
        plt.gca().spines['right'].set_visible(False)                    # Hacer invisible el eje vertical derecho
        plt.savefig(f'{out_path}/weight_distribution.png')              # Guardar el gráfico
    
    # Variable que contiene el texto del archivo HTML
    html = '''<!DOCTYPE html>
<html>
    <head>
        <title>Dashboard</title>
    </head>
    <body>
        <h1>Shipping Dashboard</h1>
        <div style = "width: 45%; float: left">
            <img src = "shipping_per_warehouse.png" alt = "Fig 1">
            <img src = "mode_of_shipment.png" alt = "Fig 2">
        </div>
        <div style = "width: 45%; float: left">
            <img src = "average_customer_rating.png" alt = "Fig 3">
            <img src = "weight_distribution.png" alt = "Fig 4">
        </div>
    </body>
</html>'''

    create_ouptput_directory(f'{out_path}')                             # Crear y limpiar el directorio de salida
    create_for_shipping_per_warehouse(df)                               # Crear y guardar el gráfico relacionado con la columna 'Warehouse_block'
    create_for_mode_of_shipment(df)                                     # Crear y guardar el gráfico relacionado con la columna 'Mode_of_Shipment'
    create_for_average_customer_rating(df)                              # Crear y guardar el gráfico de promedio de calificaciones de los usuarios por el modo de envío
    create_for_weight_distribution(df)                                  # Crear y guardar el gráfico relacionado con la columna 'Weight_in_gms'

    with open(f'{out_path}/index.html', 'w') as file:                   # Crear y escribir el HTML (Dashboard)
        file.write(html)