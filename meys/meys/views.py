from django.http import HttpResponse
import datetime
from django.shortcuts import render

def holamundo(request): #primera vista
    return HttpResponse('hola esta es nuestra primera pagina')
def hora(request):
    fechaactual=datetime.datetime.now()
    return render(request,'fecha.html',{'fechaactual':fechaactual})
def calculo(request,dato1,dato2):
    resultado=f"El resultado es igual a: {dato1+dato2}"
    return   HttpResponse(resultado)
