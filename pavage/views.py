from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("Bonjour, vous êtes dans l'index de pavage")

import os.path
from monsite.settings import *
from PIL import Image
from .forms import ChargerImageForm
from numpy import floor

def charger(request):
    if request.method == 'POST':
        form = ChargerImageForm(request.POST, request.FILES)#
        if form.is_valid():
            p=form.save()
            nom = os.path.basename(p.photo.path)
            print('avant le chargement de l image de base')
            print(MEDIA_ROOT)
            adresse_fichier=MEDIA_ROOT+'/images_de_base/'+nom
            adresse_fichier=adresse_fichier.replace('//','/')
            #img = Image.open(MEDIA_ROOT+'images_de_base/'+nom)
            img = Image.open(adresse_fichier)
            print('OK pour le chargement de l image')
            #construction de l'image ajustée pour le canvas : min(width,height)=500px
            largeur=img.size[0]
            hauteur=img.size[1]
            if largeur>hauteur:
                largeur_canvas,hauteur_canvas=int(floor(largeur/hauteur*500)),500
            else:
                largeur_canvas, hauteur_canvas =500, int(floor(hauteur/largeur*500))
            # print('largeur du canvas :',largeur_canvas)
            # print('hauteur du canvas :',hauteur_canvas)
            img = img.resize((largeur_canvas,hauteur_canvas), Image.ANTIALIAS)
            # print('ça marche')
            # print('le nom c est',nom)
            adresse_fichier = MEDIA_ROOT + '/images_ajustees/' + nom
            adresse_fichier = adresse_fichier.replace('//', '/')
            #img.save(MEDIA_ROOT+'images_ajustees/'+ nom)
            img.save(adresse_fichier)
            #return HttpResponse("jusque la c'est bon avec : " + nom)
            # print('OK pour la sauvegarde de l image ajustee')
            #return HttpResponse("jusque la c'est bon")
            adresse = '/media/images_ajustees/'+nom
            # print(adresse)
            #return HttpResponse("jusque la c'est bon avec : " + nom)
            #return render(request, 'pavage/decoupe_image_mobile.html',
            return render(request, 'pavage/essaitouch.html',
                {'nom': nom,
                 'largeur_canvas': largeur_canvas,
                 'hauteur_canvas':hauteur_canvas,
                 'adresse':adresse
                })
    else:
        form = ChargerImageForm()
    return render(request, 'pavage/charger.html', {'form': form})

from .programmes_calcul.production_image_finale import traiter

def pavage_reponse(request):
    #coords = request.POST['coordonnes']
    coordx = request.POST['coordx']
    coordy = request.POST['coordy']
    #coordsbis = request.POST['coordonnes1']
    coordxx = request.POST['coordxx']
    coordyy = request.POST['coordyy']
    nom=request.POST['nom']
    #largeur=request.POST['largeur']#c'est la largeur sélectionnée dans le canvas découpé
    #hauteur=request.POST['hauteur']#idem ici pour la hauteur.
    #il faut ensuite retailler l'image téléchargée par le client avec ces indications
    #pour avoir le carré de base selon le format choisi. Il faudrait donc savoir quel est la dimension
    #de ce carré de base selon le format.
    adresse_fichier = MEDIA_ROOT + '/images_de_base/' + nom
    adresse_fichier = adresse_fichier.replace('//', '/')
    img = Image.open(adresse_fichier).convert("RGB")
    # construction de l'image ajustée pour le canvas : min(width,height)=500px
    largeur_image_de_base, hauteur_image_de_base = img.size
    print("solution :",largeur_image_de_base, hauteur_image_de_base)
    #je calcule le facteur d'agrandissement pour repasser à l'extraction dans l'image de base
    if largeur_image_de_base > hauteur_image_de_base:
        facteur_agrandissement = hauteur_image_de_base/500
    else:
        facteur_agrandissement = largeur_image_de_base/500
    left = facteur_agrandissement * float(coordx)
    right = facteur_agrandissement * float(coordxx)
    top = facteur_agrandissement * float(coordy)
    bottom = facteur_agrandissement * float(coordyy)
    img_decoup = img.crop((left, top, right, bottom))#après elle sera resized
    adresse_fichier = MEDIA_ROOT + '/images_de_base_rognees/' + nom
    adresse_fichier = adresse_fichier.replace('//', '/')
    img_decoup.save(adresse_fichier)
    #pas forcément utile à sauvegarder?
    traiter(img_decoup,nom)
    #return HttpResponse("jusque là c'est bon le pavage" + nom)
    return render(request, 'pavage/affichage_pavage.html', {'nom': nom})
