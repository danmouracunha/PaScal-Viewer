from django.shortcuts import render
from Private.forms import UploadFileForm
from tools import util, heatmap
import json
import os
directory = os.getcwd()
list=[]
# Create your views here.
def index(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        file = request.FILES['files']
        profiler = util.Profiler(file)
        
        region = profiler.regions[0]
        
        scripts,divs = heatmap.graph(profiler)
        script_side,div_side,lines = heatmap.graph_sidebar(profiler)
        mapa = converte_intervalos_em_arvore(lines)
        print(converte_intervalos_em_arvore(lines))
        request.session['mapa'] = json.dumps(mapa)
        request.session['divAtiva'] = json.dumps(0)
        request.session['divs'] = json.dumps(divs)
        request.session['div_side'] = json.dumps(div_side) # profiler.toJSON()
        
        scripts_juntos =""
        divs_juntos=""
        divs_juntos=divs[0]
        for i in range(len(scripts)):    
                scripts_juntos+=scripts[i] 
        #         divs_juntos += divs[i]
        
        divs_juntos_side=""
        for i in range(len(script_side)):
                scripts_juntos+=script_side[i]
        request.session['scripts_juntos'] = json.dumps(scripts_juntos)
        for i in range(len(mapa[0]['filhos'])):
                divs_juntos_side += "<div class='col-12'>"
                divs_juntos_side += div_side[mapa[0]['filhos'][i]]
                divs_juntos_side += "</div>"
        return render(request, 'Private/index.html',
        {
            'title':'Results',
            'message':'Your application results.',
            'the_script':scripts_juntos,
            'the_div': divs_juntos,
            'the_div_side': divs_juntos_side,
        })
    else:
        form = UploadFileForm()
    return render(request, 'Private/index.html',{'form': form})

def indexNav(request,year):
    divsRaw = request.session['divs']
    divs = json.loads(divsRaw)
    div_sideRaw = request.session['div_side']
    div_side = json.loads(div_sideRaw)
    mapaRaw = request.session['mapa']
    mapa = json.loads(mapaRaw)
    scripts_juntosRaw = request.session['scripts_juntos']
    scripts_juntos = json.loads(scripts_juntosRaw)
    year=int(year)
    print(divs[year])
    
    print(div_side)
    
    divs_juntos=""
    for i in range(len(divs)):
            divs_juntos += divs[i]
    
    divs_juntos_side=""
    print(mapa[year]['filhos'])
    for i in range(len(mapa[year]['filhos'])):
                divs_juntos_side += "<div class='col-12'>"
                divs_juntos_side += div_side[mapa[year]['filhos'][i]]
                divs_juntos_side += "</div>"
    return render(request, 'Private/index.html',
    {
        'title':'Results',
        'message':'Your application results.',
        'the_script':scripts_juntos,
        'the_div': divs[year],
        'the_div_side': divs_juntos_side,
    })
def converte_intervalos_em_arvore(intervalos):
    arvore = []
    for i in intervalos:
        arvore.append({'filhos': [], 'intervalo': i})
    intervalos = sorted(intervalos, key=lambda k: (k[1]-k[0]), reverse=True)
    for i, inter in enumerate(intervalos):
        arvore[i]['intervalo'] = intervalos[i]
        cont = i-1
        while cont >= 0:
            if intervalos[cont][0] <= intervalos[i][0] and intervalos[cont][1] >= intervalos[i][1]:
                arvore[cont]['filhos'].append(i)
                break
            cont -= 1
    return arvore