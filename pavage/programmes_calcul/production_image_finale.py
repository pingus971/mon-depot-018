import pickle
import numpy as np
from PIL import Image
from monsite.settings import *
#format=1001#format de test
format=1001

if format ==0:
    hauteur=201
    largeur=201
elif format==4:
    hauteur=3508
    largeur=2480
elif format==3:
    hauteur=4961
    largeur=3508
elif format==2:
    hauteur=7016
    largeur=4961
else :
    hauteur=1001
    largeur=1001

xcentre=round(hauteur/2)
ycentre=round(largeur/2)

pourcentmarge=0.98
unitepixel=round(pourcentmarge*largeur/2)

xmin=int(xcentre-unitepixel)
xmax=int(xcentre+unitepixel)
ymin=int(ycentre-unitepixel)
ymax=int(ycentre+unitepixel)
adresse_fichier=STATIC_ROOT+'/imago/imago1001_it7bis.txt'
adresse_fichier=adresse_fichier.replace('//','/')#je suis obligé de faire ça à cause de pythonanywhere
Fichier = open(adresse_fichier,'rb')

imago = pickle.load(Fichier)
# désérialisation
Fichier.close()

#resultat=np.zeros((largeur, hauteur, 3), dtype=np.uint8)

#img1 = np.zeros((hauteur, largeur, 3), dtype=np.uint8)
#imago=np.zeros((hauteur, largeur,2))

# for i in range(xmin,xmax+1):
#     for j in range(ymin,ymax+1):
#         if (i-xcentre)**2+(j-ycentre)**2<unitepixel**2:
#             img1[i,j]=(255,255,255)#blanc

j=complex(0,1)

def pixcomp(pixel):#transforme un pixel (liste de 2 entiers) en complexe
   return (pixel[0]+1/2-xcentre+j*(pixel[1]+1/2-ycentre))/unitepixel


def comppix(complexe):#transforme un complexe en pixel
    u=round(xcentre+np.real(complexe)*unitepixel-1/2)
    v=round(ycentre+np.imag(complexe)*unitepixel-1/2)
    return [int(u),int(v)]

pi=np.pi
e=np.e
sin=np.sin
cos=np.cos
tan=np.tan
conj=np.conjugate
sqrt=np.sqrt
real=np.real
imag=np.imag
abs=np.abs

n=4
p=5

#formes circulaires pour délimiter P0

a=sqrt(cos(pi/p)**2-sin(pi/n)**2)
w1=1/a*cos(pi/p)
w2=e**(j*pi/2)*w1
w3=-w1
w4=-e**(j*pi/2)*w1

ss=1/a*cos(pi/n+pi/p)

s0=ss*e**(j*pi/4)
s1=ss*e**(j*3*pi/4)
s2=-s0
s3=ss*e**(-j*pi/4)

#carré de base
# x compris entre comppix(s2)[0] et comppix(s0)[0]
# y compris entre comppix(s2)[1] et comppix(s0)[1]

#print(comppix(s2)[0])
#print(comppix(s0)[0])

#taille de l'image à traiter
taille_a_traiter=comppix(s0)[0]-comppix(s2)[0]+1
#print(taille_a_traiter)

def traiter(image_a_traiter,nom):
    #img= Image.open("antoine3.png")
    img2 = image_a_traiter.resize((taille_a_traiter,taille_a_traiter), Image.ANTIALIAS)
    print("type ",type(img2))
    print("mode ",img2.mode)
    adresse_fichier = MEDIA_ROOT + '/images_de_base_carrees/' + nom
    adresse_fichier = adresse_fichier.replace('//', '/')
    img2.save(adresse_fichier)
    imgtab = np.array(img2)
    print("type du tableau ",type(imgtab))
    print(imgtab.shape)
    #imgtab = asarray(img2)
    print("cela donne ",imgtab[10,10])
    ########## traitement final
    resultat=np.zeros((hauteur, largeur, 3), dtype=np.uint8)

    for i in range(0,taille_a_traiter):
        for k in range(0,taille_a_traiter):
            resultat[comppix(s2)[0]+i,comppix(s2)[1]+k]=imgtab[i,k]
    for i in range(0,hauteur):
        for k in range(0,largeur):
            u=int(imago[i,k,0])
            v=int(imago[i,k,1])
            if u==0 and v==0:
                resultat[i,k]=(255,255,255)
            else:
                resultat[i,k]=resultat[u,v]

    #plt.imshow(resultat)
    #plt.show()
    #impimg.imsave("antoine3_A2.png",resultat)
    img_decoup=Image.fromarray(resultat)
    #img_decoup.save('pavage_de_base/static/pavage_de_base/pavagesA3/' + nom)
    adresse_fichier = MEDIA_ROOT + '/pavages1001/' + nom
    adresse_fichier = adresse_fichier.replace('//', '/')
    img_decoup.save(adresse_fichier)