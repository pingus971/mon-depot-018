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
            #print('avant le chargement de l image de base')
            #print(MEDIA_ROOT)
            adresse_fichier=MEDIA_ROOT+'/images_de_base/'+nom
            adresse_fichier=adresse_fichier.replace('//','/')
            img = Image.open(adresse_fichier)
            largeur= img.size[0];
            hauteur = img.size[1];
            ratio=hauteur/largeur*100;
            return render(request, 'pavage/crop.html',
                        {'nom': nom,
                         'ratio': ratio,
                        })

    else:
        form = ChargerImageForm()
    return render(request, 'pavage/charger.html', {'form': form})

from .programmes_calcul.production_image_finale import traiter

def pavage_reponse(request):
    sizex = request.POST['sizex']
    sizey = request.POST['sizey']
    tlx = request.POST['tlx']
    tly = request.POST['tly']
    brx = request.POST['brx']
    bry = request.POST['bry']
    nom=request.POST['nom']


    adresse_fichier = MEDIA_ROOT + '/images_de_base/' + nom
    adresse_fichier = adresse_fichier.replace('//', '/')
    img = Image.open(adresse_fichier).convert("RGB")

    largeur_image_de_base, hauteur_image_de_base = img.size
    if sizey ==0:
        facteur_agrandissement=largeur_image_de_base/float(sizex)
    else :
        facteur_agrandissement = hauteur_image_de_base /float(sizey)
    left = facteur_agrandissement * float(tlx)
    right = facteur_agrandissement * float(brx)
    top = facteur_agrandissement * float(tly)
    bottom = facteur_agrandissement * float(bry)
    img_decoup = img.crop((left, top, right, bottom))#après elle sera resized en carré
    #adresse_fichier = MEDIA_ROOT + '/images_de_base_rognees/' + nom
    #adresse_fichier = adresse_fichier.replace('//', '/')
    #img_decoup.save(adresse_fichier)
    #pas forcément utile à sauvegarder?
    traiter(img_decoup,nom)
    return render(request, 'pavage/affichage_pavage.html', {'nom': nom})
