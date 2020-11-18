from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio
pio.renderers.default='iframe'
import pandas as pd
import numpy as np

def make_plot(type_, df, instruct):
   
    color = ['rgb(128, 0, 128)', 'rgb(38, 20, 128)', 'rgb(108, 90, 28)']
    
    if type_ == 'bar':
        figure = go.Bar(x=df[instruct['col']], y=df['feature'], 
                            marker=dict(
                                color='rgba(50, 171, 96, .6)', 
                                line=dict(color='rgba(50, 171, 96, 1.0)')),
                            name=instruct['title'], orientation='h')
    
    if type_ == 'scatter':
        figure = go.Scatter(x=df[instruct['col']], y=df['feature'], mode='lines+markers', line_color=np.random.choice(color), name=instruct['title'])
                                 
                                 
    return figure



def feature_importance_multicolinearity_plot(df, instruction_dict, num_subplots):
    fig = make_subplots(rows=1, cols=num_subplots, specs=[[{}]*num_subplots], 
                    shared_xaxes=False, shared_yaxes=True, 
                    vertical_spacing=.001)

    fig.append_trace(make_plot(type_=instruction_dict['plot1']['type'], df=df, 
                               instruct=instruction_dict['plot1']), 1, 1)
    fig.append_trace(make_plot(type_=instruction_dict['plot2']['type'], df=df, 
                               instruct=instruction_dict['plot2']), 1, 2)
    fig.append_trace(make_plot(type_=instruction_dict['plot3']['type'], df=df, 
                               instruct=instruction_dict['plot3']), 1, 3)




    fig.update_layout(
        title=instruction_dict['figure_title'],

        yaxis=dict(showgrid=True, 
                   showline=False, 
                   showticklabels=True,
                   domain=[0, 0.85]), 

        yaxis2=dict(showgrid=False, 
                    showline=True, 
                    showticklabels=False, 
                    linecolor='rgba(102, 102, 102, 0.8)', 
                    linewidth=2,
                    domain=[0, 0.85]),

        yaxis3=dict(showgrid=False, 
                    showline=True, 
                    showticklabels=False, 
                    linecolor='rgba(102, 102, 102, 0.8)', 
                    linewidth=2.25,
                    domain=[0, 0.85]), 

        xaxis=dict(zeroline=False, 
                   showline=False, 
                   showticklabels=True, 
                   showgrid=True,
                   domain=[0, 0.27]), 

        xaxis2=dict(zeroline=False, 
                    showline=True, 
                    nticks=5, 
                    showgrid=True, 
                    domain=[0.30, 0.62], 
                    side='top', 
                    dtick=2500),

        xaxis3=dict(zeroline=False, 
                    showline=False,
                    nticks=5,
                    showgrid=True, 
                    domain=[.68, 1], 
                    side='bottom', 
                    dtick=2500), 

        legend=dict(x=0.029, y=1, font_size=10), 
        margin=dict(l=100, r=10, t=80, b=80),
        height=1000,
        width=900,
        paper_bgcolor='rgb(248, 248, 255)', 
        plot_bgcolor='rgb(248, 248, 255)')







    fig.show()