from django.http import HttpResponse
from django.shortcuts import render

def accueil(request):
    #return HttpResponse("Bonjour, vous êtes dans la page d'accueil de PhotosHyperboliques.")

    return render(request,'pavage/accueil.html')