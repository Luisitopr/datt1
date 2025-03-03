import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import numpy as np


# Cargar el dataset localmente con cache
@st.cache_data
def load_data():
    df = pd.read_csv('covid-19_general_MX.csv')  # Ruta local del archivo
    return df

# Cargar datos
data = load_data()

# Mostrar Logo y Autor
st.image('logo.png', width=150)  # Reemplaza con el archivo correcto de tu logo
st.markdown('Autor: Luis Galindo')

# Visualización de dataset
st.header('Vista General del Dataset')
n_rows = st.slider('Número de filas a mostrar', min_value=5, max_value=100, value=10)
st.dataframe(data.head(n_rows))

# Buscador de información
st.header('Buscador de Información')

# Seleccionar la columna para la búsqueda
column_option = st.selectbox("Selecciona la columna para buscar", data.columns)

# Campo de entrada para la búsqueda
search_term = st.text_input('Ingrese término de búsqueda')

# Si se presiona el botón 'Buscar'
if st.button('Buscar'):
    # Convertir la columna seleccionada a texto (string) y aplicar la búsqueda
    results = data[data[column_option].astype(str).str.contains(search_term, case=False, na=False)]
    
    if results.empty:
        st.write("No se encontraron resultados.")
    else:
        st.write(f'Se encontraron {len(results)} resultados:')
        st.dataframe(results)  # Muestra los resultados en una tabla

# Filtrado de información
st.header('Filtrado de Información')
column = st.selectbox('Seleccione la columna para filtrar', data.columns)
unique_values = data[column].unique()
selected_values = st.multiselect('Seleccione valores', unique_values)
filtered_data = data[data[column].isin(selected_values)]
st.dataframe(filtered_data)

# Histograma
st.header('Histograma de Edad')
fig, ax = plt.subplots()
sns.histplot(data['EDAD'], bins=30, ax=ax)
ax.set_title('Distribución de Edades de Pacientes con COVID-19')
st.pyplot(fig)
st.markdown('Este histograma muestra la distribución de edades de los pacientes con COVID-19 en México.')

# Gráfica de Barras
st.header('Casos por Estado')
state_counts = data['ENTIDAD_RES'].value_counts()
fig = px.bar(state_counts, x=state_counts.index, y=state_counts.values, labels={'x': 'Estado', 'y': 'Número de Casos'})
st.plotly_chart(fig)
st.markdown('Esta gráfica de barras muestra el número de casos de COVID-19 por estado en México.')

# Scatter Plot
st.header('Relación entre Edad y Intubación')
filtered_data = data[data['INTUBADO'].isin([1, 2])]
filtered_data['INTUBADO'] = filtered_data['INTUBADO'].replace({1: 'Sí', 2: 'No'})

# Scatter Plot - Relación entre Edad e Intubación
st.header('Relación entre Edad y Intubación')
filtered_data = data[data['INTUBADO'].isin([1, 2])]
filtered_data['INTUBADO_NUM'] = filtered_data['INTUBADO'].replace({1: 1, 2: 0})
filtered_data['JITTER_INTUBADO'] = filtered_data['INTUBADO_NUM'] + np.random.uniform(-0.1, 0.1, size=len(filtered_data))


fig = px.scatter(
    filtered_data, 
    x='EDAD', 
    y='JITTER_INTUBADO', 
    color='INTUBADO_NUM', 
    color_continuous_scale=['blue', 'red'],
    opacity=0.5,
    labels={'EDAD': 'Edad', 'JITTER_INTUBADO': '¿Fue Intubado? (0 = No, 1 = Sí)'},
    title='Relación entre Edad e Intubación'
)

st.plotly_chart(fig)
st.markdown('Esta gráfica de dispersión muestra la relación entre la edad de los pacientes y si fueron intubados.')