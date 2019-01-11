#Graphs Imports
from bokeh.plotting import figure
from math import pi
import numpy as np
from bokeh.resources import CDN
from bokeh.embed import components
from bokeh.layouts import gridplot
from bokeh import palettes
from colour import Color
from tools import util
import simplejson as json
import pandas as pd
import numpy as np

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import matplotlib.cm as cm
import os
directory = os.getcwd()
#Models from bokeh
from bokeh.models import (
    ColumnDataSource,
    HoverTool,
    LinearColorMapper,
    Label,
    BasicTicker,
    PrintfTickFormatter,
    ColorBar,
)

def graph_model(serie,rows,columns,titulo,showX,showY,maxScale):

    data = pd.DataFrame(data=np.matrix(serie).T ,index=rows,columns=columns)
    
    data.columns.name = 'Cores'
    data.index.name = 'Test'
    data.columns = data.columns.astype(str)
    test = list(data.index)
    cores = list(data.columns)

    df = pd.DataFrame(data.stack(), columns=['rate']).reset_index()
    
    colors = ["#0270BF", "#2683A3", "#4A9788", "#6EAB6D", "#92BE52", "#92BE52", "#DAE61C", "#FFFA01", "#FFFA33"]
    # maximoEscala = 0
    # matrixInNp = np.matrix(serie).T
    # if abs(matrixInNp.max())>abs(matrixInNp.min()):
    #     maximoEscala = abs(matrixInNp.max())
    # else:
    #     maximoEscala = abs(matrixInNp.min())
        #This section uses the matplotlib to retrive a diverging pallet with 256 levels 
    cmap = plt.get_cmap("BrBG")    # PiYG 
    palett256 = [] 
    for i in range(cmap.N): 
        rgb = cmap(i)[:3]# will return rgba, we take only first 3 so we get rgb 
        palett256.append(cm.colors.rgb2hex(rgb)) 
    mapper = LinearColorMapper( palette=palett256, low=-maxScale, high=maxScale,nan_color='black') 
    # mapper = LinearColorMapper( palette=palettes.RdBu11[ :: -1], low=-maximoEscala, high=maximoEscala,nan_color='black')
    
    source = ColumnDataSource(df)

    hover = HoverTool(tooltips=[
    ("Threads", "@Cores"),
    ("Input size", "@Test"),
    ("Value","@rate")
    ])
    # print(list(map(str,cores)))
    hm = figure(title=titulo,x_range=cores,y_range=list(reversed(test)),
           x_axis_location="above", plot_width=500, plot_height=300,
           tools=[hover,"save"], toolbar_location=None)
    
    hm.xaxis.visible = showX
    
    hm.yaxis.visible = showY

    hm.xaxis.major_label_text_font_size  = "11pt"
    hm.yaxis.major_label_text_font_size  = "11pt"

    # hm.y_scale.visible = showX
    hm.rect(x="Cores", y="Test", width=1, height=1,
       source=source,
       fill_color={'field': 'rate', 'transform': mapper},
       line_color=None)
    color_bar = ColorBar(color_mapper=mapper, ticker=BasicTicker(), location=(0, 0),major_label_text_font_size='11pt')

    hm.add_layout(color_bar, 'right')

    # script, div = components(hm, CDN)

    return hm

def graph_model_teste(serie,rows,columns,titulo):
    newRow=[]
    for i in range(len(rows)):
        newRow.append("x"+str(i))
    data = pd.DataFrame(data=np.matrix(serie).T ,index=rows,columns=columns)
    
    data.columns.name = 'Cores'
    data.index.name = 'Test'
    data.columns = data.columns.astype(str)
    test = list(data.index)
    cores = list(data.columns)

    df = pd.DataFrame(data.stack(), columns=['rate']).reset_index()
    
    colors = ["#0270BF", "#2683A3", "#4A9788", "#6EAB6D", "#92BE52", "#92BE52", "#DAE61C", "#FFFA01", "#FFFA33"]
    maximoEscala = 0
    matrixInNp = np.matrix(serie).T
    if titulo=="Scalability":
        matrixInNp = matrixInNp.transpose()

        matrixInNp = matrixInNp[1:].transpose()
    elif titulo=="Weak scalability":
        matrixInNp = matrixInNp.transpose()

        matrixInNp = matrixInNp[1:].transpose()[1:]
    else:
        matrixInNp=np.matrix(serie)
    if abs(matrixInNp.max())>abs(matrixInNp.min()):
        maximoEscala = abs(matrixInNp.max())
    else:
        maximoEscala = abs(matrixInNp.min())
    
    mapper = LinearColorMapper( palette=palettes.Plasma256[ :: -1], low=-maximoEscala, high=maximoEscala)
    
    source = ColumnDataSource(df)

    hover = HoverTool(tooltips=[
    ("Value","@rate"),
    ("Input Size", "@Test"),
    ("Threads", "@Cores")
    ])
    # print(list(map(str,cores)))
    hm = figure(title=titulo,x_range=cores,y_range=list(reversed(test)),
           x_axis_location="above", plot_width=500, plot_height=300,
           tooltips=[hover],tools="save", toolbar_location=None)
    

    hm.rect(x="Cores", y="Test", width=1, height=1,
       source=source,
       fill_color={'field': 'rate', 'transform': mapper},
       line_color=None)
    hm.xaxis.axis_label = "Threads"
    hm.yaxis.axis_label = "Problem size"
    color_bar = ColorBar(color_mapper=mapper, ticker=BasicTicker(), location=(0, 0),major_label_text_font_size="10pt")

    hm.add_layout(color_bar, 'right')

    # script, div = components(hm, CDN)

    return hm
def graph_model_side(serie,rows,columns,titulo):
    serie=serie*100
    newRow=[]
    for i in range(len(rows)):
        newRow.append("x"+str(i))
    data = pd.DataFrame(data=np.matrix(serie).T ,index=newRow,columns=columns)
    
    data.columns.name = 'Cores'
    data.index.name = 'Test'
    data.columns = data.columns.astype(str)
    
    matrixInNp = np.matrix(serie).T
    matrixInNp = matrixInNp.transpose()

    matrixInNp = matrixInNp[1:].transpose()
    test = list(data.index)
    cores = list(data.columns)

    df = pd.DataFrame(data.stack(), columns=['rate']).reset_index()
    
    mapper = LinearColorMapper( palette=palettes.Inferno256[ :: -1], low=matrixInNp.min(), high=matrixInNp.max())
    
    source = ColumnDataSource(df)

    hover = HoverTool(tooltips=[
    ("Value","@rate%"),
    ("Input size", "@Test"),
    ("Threads", "@Cores")
    ])
    # print(list(map(str,cores)))
    # for i in range(len(test)):
    #     test[i]="X"+str(i)
    print(test)
    hm = figure(title=titulo,x_range=cores,y_range=list(reversed(test)),
           x_axis_location="above", plot_width=300, plot_height=200,
           tools=[hover], toolbar_location=None)
    

    hm.rect(x="Cores", y="Test", width=1, height=1,
       source=source,
       fill_color={'field': 'rate', 'transform': mapper},
       line_color=None)
    # hm.xaxis.axis_label = "Threads"
    # hm.yaxis.axis_label = "Problem Size"
    color_bar = ColorBar(color_mapper=mapper, ticker=BasicTicker(), location=(0, 0))
    
    hm.add_layout(color_bar, 'right')

    # script, div = components(hm, CDN)

    return hm
def graph_model_eficincia(serie,rows,columns,titulo):
    serie=serie*100
    newRow=[]
    for i in range(len(rows)):
        newRow.append("i"+str(i+1))
    data = pd.DataFrame(data=np.matrix(serie).T ,index=newRow,columns=columns)
    
    data.columns.name = 'Cores'
    data.index.name = 'Test'
    data.columns = data.columns.astype(str)
    
    matrixInNp = np.matrix(serie).T
    matrixInNp = matrixInNp.transpose()

    matrixInNp = matrixInNp[1:].transpose()
    test = list(data.index)
    cores = list(data.columns)

    df = pd.DataFrame(data.stack(), columns=['rate']).reset_index()
    
    mapper = LinearColorMapper( palette=palettes.Inferno256[ :: -1], low=matrixInNp.min(), high=matrixInNp.max())
    
    source = ColumnDataSource(df)

    hover = HoverTool(tooltips=[
    ("Value","@rate%"),
    ("Input size", "@Test"),
    ("Threads", "@Cores")
    ])
    # print(list(map(str,cores)))
    # for i in range(len(test)):
    #     test[i]="X"+str(i)
    print(test)
    hm = figure(title=titulo,x_range=cores,y_range=list(reversed(test)),
           x_axis_location="above", plot_width=500, plot_height=300,
           tools=[hover], toolbar_location=None)
    

    hm.rect(x="Cores", y="Test", width=1, height=1,
       source=source,
       fill_color={'field': 'rate', 'transform': mapper},
       line_color=None)
    hm.xaxis.major_label_text_font_size  = "11pt"
    hm.yaxis.major_label_text_font_size  = "11pt"
    color_bar = ColorBar(color_mapper=mapper, ticker=BasicTicker(), location=(0, 0),major_label_text_font_size='11pt')
    
    hm.add_layout(color_bar, 'right')

    # script, div = components(hm, CDN)

    return hm

#  PLOTA O HEATMAP
def graph(profiler):
    scripts = []
    divs = []
    for i in range(len(profiler.regions)):
        regiao = profiler.regions[i]
        # print(np.matrix(regiao.get_efficiency()).T)
        newRow=[]
        for i in range(len(regiao.get_header_arguments())):
            newRow.append("i"+str(i+1))
        hm1 = graph_model_eficincia(regiao.get_efficiency(),regiao.get_header_arguments(),regiao.get_header_threads(),"Efficiency")

        maxScale=0
        strong = maiorEmModulo(regiao.get_scalability_on_columns())        
        scalability = maiorEmModulo(regiao.get_scalability_on_rows())        
        if strong>scalability:
            maxScale=strong
        else:
            maxScale=scalability
        
        weak = maiorEmModulo(regiao.get_scalability_on_diagonals())      
        if maxScale<weak:
            maxScale=weak

        hm2 = graph_model(regiao.get_scalability_on_columns(),newRow,regiao.get_header_threads()[1:],"Strong scalability",True,False,maxScale)
        
        hm3 = graph_model(regiao.get_scalability_on_rows(),newRow[1:],regiao.get_header_threads(),"Scalability",False,True,maxScale)
        
        #As the h2 was removed the last column and the last row to make the visualization easier
        hm4 = graph_model(regiao.get_scalability_on_diagonals(),newRow[1:],regiao.get_header_threads()[1:],"Weak scalability",False,False,maxScale)
        hm_1 = graph_model_eficincia(regiao.get_scalability_on_columns_from_idealvariation(),newRow,regiao.get_header_threads(),"Strong scalability (Ideal variation)")
        hm_2 = graph_model_eficincia(regiao.get_scalability_on_rows_from_idealvariation(),newRow,regiao.get_header_threads(),"Scalability (Ideal variation)")
        grid = gridplot([hm1, hm2, hm3,hm4,hm_1,hm_2], ncols=2, toolbar_location="below",merge_tools=True)
    
        [script,div]=components(grid, CDN)
        if regiao.initial_line=='0' and regiao.final_line=='9999':
            div= "<h3 style='text-align: center; padding-top: 30px;'>WHOLE PROGRAM</h3>"+div
        else:
            div= "<h3 style='text-align: center; padding-top: 30px;'>"+regiao.filename+": "+regiao.initial_line+"-"+regiao.final_line+" </h3>"+div
        
        div+="<br/><br/><span>Arguments:</span><br/>"
        for i in range(len(regiao.get_header_arguments())):
            div+="<span> i"+str(i+1)+": " + regiao.get_header_arguments()[i]+"</span><br/>"

        scripts.append(script)
        divs.append(div)
    
    return [scripts,divs]
def maiorEmModulo(serie):
    maximoEscala = 0
    matrixInNp = np.matrix(serie).T
    if abs(matrixInNp.max())>abs(matrixInNp.min()):
        maximoEscala = abs(matrixInNp.max())
    else:
        maximoEscala = abs(matrixInNp.min())
    return maximoEscala
def graph_sidebar(profiler):
    scripts = []
    divs = []
    lines = []
    for i in range(len(profiler.regions)):
        regiao = profiler.regions[i]
        # print(np.matrix(regiao.get_efficiency()).T)
        newRow=[]
        for j in range(len(regiao.get_header_arguments())):
            newRow.append("x"+str(j+1))
        hm1 = graph_model_side(regiao.get_efficiency(),regiao.get_header_arguments(),regiao.get_header_threads(),"Efficiency")

        grid = gridplot([hm1], ncols=1, toolbar_location="below",merge_tools=True)

        [script,div]=components(grid, CDN)
        div= "<h3 style='text-align: center; padding-top: 30px; color: white;'><a href=\"/privateNav/"+str(i)+"\"  %}'>"+regiao.filename+": "+regiao.initial_line+"-"+regiao.final_line+"</a></h3>"+div
        div+="<span  style='color: white;'>Max values to:</span><br/><span  style='color: white;'> <b>Efficiency: </b>"+str(round(np.matrix(regiao.get_efficiency()).max(), 3))+ "<b> Scalability: </b>"+str(round(np.matrix(regiao.get_scalability_on_rows()).max(), 3))+ "<b> Strong scalability: </b>"+str(round(np.matrix(regiao.get_scalability_on_columns()).max(), 3))+ "<b> Weak scalability: </b>"+str(round(np.matrix(regiao.get_scalability_on_diagonals()).max(), 3))+ "</span><br/>"
        div+="<span  style='color: white;'>Min values to:</span><br/><span  style='color: white;'> <b>Efficiency: </b>"+str(round(np.matrix(regiao.get_efficiency()).min(), 3))+ "<b> Scalability: </b>"+str(round(np.matrix(regiao.get_scalability_on_rows()).min(), 3))+ "<b> Strong scalability: </b>"+str(round(np.matrix(regiao.get_scalability_on_columns()).min(), 3))+ "<b> Weak scalability: </b>"+str(round(np.matrix(regiao.get_scalability_on_diagonals()).min(), 3))+ "</span><br/>"
        line = (int(regiao.initial_line),int(regiao.final_line))
        # div+="<br/><br/><label>Arguments:</label><br/>"
        # for i in range(len(regiao.get_header_arguments())):
        #     div+="<label> X"+str(i)+": " + regiao.get_header_arguments()[i]+"</label><br/>"
        
        scripts.append(script)
        divs.append(div)
        lines.append(line)

    return [scripts,divs,lines]