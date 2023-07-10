import requests
from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from .models import Analisis
from decimal import Decimal

from pymongo import MongoClient

# Create your views here.


class Inicio(TemplateView):
    template_name = "base.html"
    
    def cambioEtiqueta(self, label):
        if label == 'Positive' or label == 'POS':
            return 'POSITIVO'
        if label == 'Neutral' or label == 'NEU':
            return 'NEUTRAL'
        if label == 'Negative' or label == 'NEG':
            return 'NEGATIVO'
    
    
    def get_context_data(self, **kwargs):
        context = super(Inicio, self).get_context_data(**kwargs)
        query = self.request.GET.get("query")
        #print(float("3,5"))
        
        if query:
            headers = {"Authorization": "Bearer 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"}
            url_idioma = "https://api-inference.huggingface.co/models/papluca/xlm-roberta-base-language-detection"
            url_sentimiento_esp = "https://api-inference.huggingface.co/models/MMG/xlm-roberta-base-sa-spanish"
            url_sentimiento_en = "https://api-inference.huggingface.co/models/finiteautomata/bertweet-base-sentiment-analysis"
            data = {
            	"inputs": query
            }
            
            etiqueta_lenguaje = ''
            texto_lenguaje = ''
            #DETECTA IDIOMA    
            response_idioma = requests.post(url_idioma, headers=headers, json=data)
            print(response_idioma)
            status_code = response_idioma.status_code
            
            if status_code == 200:
                primer_elemento = response_idioma.json() [0][0]
                etiqueta_lenguaje = primer_elemento['label']
                #REALIZA ANALISIS
                if etiqueta_lenguaje == 'es' or etiqueta_lenguaje == 'en':
                    if etiqueta_lenguaje == 'es':
                        url_sentimiento = url_sentimiento_esp
                    if etiqueta_lenguaje == 'en':
                        url_sentimiento = url_sentimiento_en
                    response_analisis = requests.post(url_sentimiento, headers=headers, json=data)
                    status_code_analisis = response_analisis.status_code
                    print("response_analisis =", response_analisis )
                    if status_code_analisis == 200:
                        dict_data = response_analisis.json()[0]
                        print("dict_data = ", dict_data)
                        sentimiento = self.cambioEtiqueta(dict_data[0]['label'])
                        score = dict_data[0]['score']
                        sentimiento_2 = self.cambioEtiqueta(dict_data[1]['label'])
                        score_2 = dict_data[1]['score']
                        sentimiento_3 = self.cambioEtiqueta(dict_data[2]['label'])
                        score_3 = dict_data[2]['score']
                        
                        context['etiqueta_lenguaje'] = etiqueta_lenguaje
                        print("etiqueta_lenguaje = ", etiqueta_lenguaje)
                        context['texto_analizado'] = query
                        context['sentimiento'] = sentimiento
                        context['score'] = score
                        context['sentimiento_2'] = sentimiento_2
                        context['score_2'] = score_2
                        context['sentimiento_3'] = sentimiento_3
                        context['score_3'] = score_3
                        
                        messages.success(self.request, "Analisis Finalizado...")
                    else:
                        messages.info(self.request, "Servicio No disponible intente en unos momentos...")
                else:
                    messages.warning(self.request, "El Lenguaje no es soportado, intente Español o Ingles...")
            else:
                messages.info(self.request, "Servicio No disponible intente en unos momentos...")
            
            
            
            
        
        return context
    
    def post(self, request, *args, **kwargs):
        print("post")
        try:
            
            actual_analisis = Analisis()
            actual_analisis.idioma = request.POST.get("idioma")
            actual_analisis.texto = request.POST.get("texto")
            actual_analisis.label = request.POST.get("label")
            actual_analisis.score = float(request.POST.get("score")) 
            actual_analisis.label2 = request.POST.get("label2")
            actual_analisis.score2 = float(request.POST.get("score2"))
            actual_analisis.label3 = request.POST.get("label3")
            actual_analisis.score3 = float(request.POST.get("score3"))
            actual_analisis.rating = int(request.POST.get("rating"))
            actual_analisis.tipo = 'E'
            actual_analisis.save()
            messages.success(self.request, "Guardado exitosamente Revisar Historico ...")
        except:
            messages.error(self.request, "Algo salio mal...")
        return redirect('index')


class ListaHistorico(ListView):
    model = Analisis
    template_name = 'lista_historico.html'
    context_object_name = "lista_analisis"
    globalFiltrado = False
    
    def get_queryset(self):
        queryset = Analisis.objects.all().order_by('-created')
        rating = self.request.GET.get("rating")
        sentimiento = self.request.GET.get("sentimiento")
        limite = self.request.GET.get("nresultados")
        rating_stg = {}
        sentimiento_stg = {}
        limite_stg = {}
        sort_stg = {'$sort': {'created': -1}}
        if 'btnBuscar' in self.request.GET:
            self.globalFiltrado = True
            string_connection = "mongodb+srv://trabajobd2023:trabajobd@cluster0.iwburib.mongodb.net/"
            client = MongoClient(string_connection)
            db = client['analisis_sentimiento']
            collection = db['analisis_analisis']
            pipeline = []
            
            if rating:
                print("rating stage")
                rating_stg = {'$match': {'rating': int(rating)}}
                pipeline.append(rating_stg)
                
            if sentimiento:
                print("sentimiento stage")
                sentimiento_stg = {'$match': {'label': sentimiento}}
                pipeline.append(sentimiento_stg)
                
            if limite:
                print("limite stage")
                limite_stg = {'$limit': int(limite)}
                pipeline.append(limite_stg)
                
            pipeline.append(sort_stg)
                
            
            
            queryset = list(collection.aggregate(pipeline)) 
        
        return queryset
    
    
    def get_context_data(self, **kwargs):
        context = super(ListaHistorico, self).get_context_data(**kwargs)
        cont = 0
        format = self.request.GET.get("formateado")
        if format:
            context['format'] = format    
        
        for key in context['lista_analisis']:
            cont += 1
        
        
        context['filtrado'] = self.globalFiltrado
        context['contador'] = cont
        return context
    
    
class About(TemplateView):
    template_name = 'about.html'

    

#DEPRECATED SE USO LISTVIEWS
def analizaTexto(request):
    valor_texto = request.GET.get('valorTexto', None)
    headers = {"Authorization": "Bearer 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"}
    url = "https://api-inference.huggingface.co/models/papluca/xlm-roberta-base-language-detection"
    url2 = "https://api-inference.huggingface.co/models/MMG/xlm-roberta-base-sa-spanish"
    
    data = {
    	"inputs": valor_texto
    }
    dict_warn = {}
    dict_data = {}
    etiqueta_lenguaje = ''
    
    response_idioma = requests.post(url, headers=headers, json=data)
    #print(response.json())
    print("response = ",response_idioma)
    status_code = response_idioma.status_code
    
    #DETECTA IDIOMA
    
    if status_code == 200:
        primer_elemento = response_idioma.json() [0][0]
        etiqueta_lenguaje = primer_elemento['label']
        #REALIZA ANALISIS
        if etiqueta_lenguaje == 'es' or etiqueta_lenguaje == 'en':
            if etiqueta_lenguaje == 'es':
                etiqueta_lenguaje = "Español"
            if etiqueta_lenguaje == 'en':
                etiqueta_lenguaje = "Ingles"
                url2 = "https://api-inference.huggingface.co/models/finiteautomata/bertweet-base-sentiment-analysis"
            response_analisis = requests.post(url2, headers=headers, json=data)
            status_code_analisis = response_analisis.status_code
            if status_code_analisis == 200:
                dict_data = response_analisis.json()[0]
                print("dict_data = ", dict_data)
            if status_code == 503:
                dict_warn = response_analisis.json()    
                print(dict_warn['error'])
                
        else:
            dict_warn['error'] = "Lenguaje no soportado"
        print(dict_data)
        
    else:
        dict_warn = response_idioma.json()    
        print(dict_warn['error'])
        
        
    
    
    
    
    
    
    
    dict_response = {
        "data": dict_data,
        "warn": dict_warn,
        "len" : etiqueta_lenguaje
    }
    
    
    return JsonResponse( dict_response)