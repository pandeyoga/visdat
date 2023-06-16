import pandas as pd
import streamlit as st
from bokeh.plotting import figure
from bokeh.models import HoverTool, ColumnDataSource
from bokeh.models import CategoricalColorMapper
from bokeh.palettes import Category20

# Load the data
url = 'https://raw.githubusercontent.com/pandeyoga/visdat/main/top10s.csv'
data = pd.read_csv(url)
data.set_index('year', inplace=True)

# Define genre and color mapper
genre = data.top_genre.unique().tolist()
color_mapper = CategoricalColorMapper(factors=genre, palette=Category20[20])

# Create ColumnDataSource
source = ColumnDataSource(data={
    'x': data.loc[2010].bpm,
    'y': data.loc[2010].nrgy,
    'Title': data.loc[2010].title,
    'id': (data.loc[2010].ID / 20000000) + 2,
    'genre': data.loc[2010].top_genre,
})

# Create figure
plot = figure(
    title='2010',
    x_axis_label='bpm',
    y_axis_label='nrgy',
    plot_height=500,
    plot_width=500,
    tools=[HoverTool(tooltips='@Title')]
)

# Add scatter plot
plot.circle(
    x='x',
    y='y',
    source=source,
    fill_alpha=0.8,
    color=dict(field='genre', transform=color_mapper),
    legend_field='genre'
)

# Define update function
def update_plot(year, x_axis, y_axis):
    plot.xaxis.axis_label = x_axis
    plot.yaxis.axis_label = y_axis

    new_data = {
        'x': data.loc[year][x_axis],
        'y': data.loc[year][y_axis],
        'genre': data.loc[year].top_genre,
        'id': (data.loc[year].ID / 20000000) + 2,
        'Title': data.loc[year].title,
    }
    source.data = new_data

    plot.title.text = f'Data for {year}'

# Streamlit app
def main():
    # Set page title
    st.title('Interactive Data Visualization')

    # Select widgets
    year = st.slider('Select year', 2010, 2019, 2010, 1)
    x_axis = st.selectbox('Select x-axis data', ['bpm', 'nrgy', 'val', 'pop'])
    y_axis = st.selectbox('Select y-axis data', ['bpm', 'nrgy', 'val', 'pop'])

    # Update plot
    update_plot(year, x_axis, y_axis)

    # Render plot using Bokeh server
    st.bokeh_chart(plot, use_container_width=True)

if __name__ == '__main__':
    main()
