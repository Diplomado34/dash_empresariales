import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

# --- 1. Cargar y Preparar los Datos ---
# Carga los datos desde tu archivo CSV
try:
    df = pd.read_csv("datos_ventas.csv")
except FileNotFoundError:
    print("Asegúrate de que 'datos_ventas.csv' esté en la misma carpeta que el script.")
    exit()

# Convertir la columna 'Fecha' a formato de fecha para un mejor manejo
df['Fecha'] = pd.to_datetime(df['Fecha'])

# --- 2. Iniciar la Aplicación Dash ---
app = dash.Dash(__name__)

# --- 3. Definir el Layout de la Aplicación ---
app.layout = html.Div(children=[
    html.H1(
        children='Dashboard de Análisis de Ventas',
        style={'textAlign': 'center', 'color': "#d35b0c"}
    ),

    html.Div(
        children='Un dashboard interactivo para visualizar las ventas por categoría y región.',
        style={'textAlign': 'center', 'marginBottom': '30px'}
    ),

    html.Div(children=[
        html.Label('Filtrar por Región:', style={'fontSize': '18px', 'marginRight': '10px'}),
        dcc.Dropdown(
            id='region-filter',
            options=[{'label': region, 'value': region} for region in sorted(df['Región'].unique())],
            value=sorted(df['Región'].unique())[0],  # Valor inicial del dropdown
            clearable=False,
            style={'width': '50%', 'margin': '0 auto'}
        ),
    ], style={'textAlign': 'center', 'marginBottom': '20px'}),

    dcc.Graph(
        id='sales-bar-chart',
    )
])

# --- 4. Definir la Lógica del Callback ---
@app.callback(
    Output('sales-bar-chart', 'figure'),
    [Input('region-filter', 'value')]
)
def update_graph(selected_region):
    """
    Esta función se activa cada vez que el usuario cambia el valor del dropdown.
    Filtra el DataFrame según la región seleccionada y actualiza el gráfico.
    """
    # Filtrar el DataFrame basado en la región seleccionada
    filtered_df = df[df['Región'] == selected_region]

    # Agrupar por categoría y sumar las ventas para el gráfico
    grouped_df = filtered_df.groupby('Categoría')['Ventas'].sum().reset_index()

    # Crear el gráfico de barras con Plotly Express
    fig = px.bar(
        grouped_df.sort_values('Ventas', ascending=False),
        x='Categoría',
        y='Ventas',
        title=f'Ventas Totales por Categoría en la Región: {selected_region}',
        labels={'Ventas': 'Ventas Totales ($)', 'Categoría': 'Categoría de Producto'},
        color='Categoría',
        template='plotly_white'
    )

    # Personalizar el layout del gráfico
    fig.update_layout(
        title_font_size=22,
        xaxis_title_font_size=16,
        yaxis_title_font_size=16,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )

    return fig

# --- 5. Ejecutar la Aplicación ---
if __name__ == '__main__':
    app.run(debug=True)