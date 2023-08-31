import plotly.graph_objects as go
import plotly.colors as colors
import numpy as np
import kaleido
import plotly
plotly.offline.init_notebook_mode(connected=True)


fig = go.Figure()

def make_autopct(values):
    def my_autopct(pct):
        total = sum(values)
        val = int(round(pct*total/100.0))
        return '{v:d}'.format(p=pct,v=val)
    return my_autopct

col = []
for i in np.arange(0,11):
    col.append(colors.qualitative.Set3[i])
for i in np.arange(0,5):
    col.append(colors.qualitative.Set2[i])

country_name = ['USA', 'Canada', 
                'England', 'Germany', 'Italy', 'Netherlands', 'France', 'Russia', 'Spain', 'Poland', 
                'Australia', 
                'China', 'India', 'Japan', 'South African']
country_num2 = [477, 123, 
                256, 229, 145, 135, 94, 79, 49, 34, 
                217, 
                125, 70, 58, 
                39]

continent = [600, 1021, 217, 253, 39]
continent_name = ['North America', 'Europe', 'Oceania', 'Asia', 'African']

fig.data=[]
fig.add_trace(
    go.Pie(
        labels=country_name,
        values=country_num2,
        sort=False,
        marker=dict(colors=col),
        textinfo='label+value',
        hole=0.6,
        hoverinfo='none',
        showlegend=True,
        textposition='inside',
        name='Country',
        rotation=9.6,
        domain={'x': [0.12, 0.68], 'y':[0.15, 0.85] }
    )
)

fig.add_trace(
    go.Pie(
        labels=continent_name,
        values=continent,
        sort=False,
        marker=dict(colors=colors.sequential.Blues),
        textinfo='label+value',
        textfont=dict(color='navy'),
        hole=0.7,
        hoverinfo='none',
        showlegend=True,
        name='Continent',
        rotation=-11,
        domain={'x': [0, 0.8], 'y': [0, 1]}
    )
)

fig.update_layout(
    # title='The article volume of countries',
    # title_x=0.5,
    # title_font=dict(size=20),
    legend=dict(
        x=0.9,  # 调整x值以将图例显示在右边
        y=0.5,
        bgcolor='rgba(0,0,0,0)',
        bordercolor='rgba(0,0,0,0)',
#         font=dict(size=8),
    ),
    width=800,
    height=600,
    margin=dict(t=5, b=5,l=5,r=5)
)

fig.show()

import plotly.io as pio
pio.write_image(fig, 'plot.pdf', format='pdf')
