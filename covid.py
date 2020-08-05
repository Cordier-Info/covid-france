import requests
import csv
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime as dt
from dateutil.parser import parse

url = "https://www.data.gouv.fr/fr/datasets/r/63352e38-d353-4b54-bfd1-f1b3ee1cabd7"
download = requests.get(url)
dep, jour, rad = [],[],[]
brut = download.content.decode('utf-8')
lignes = brut.split('\n')
tab = []
for ligne in lignes[1:-1:3] : # on saute l'en-tête et ne garde que les sexes 0 correspondant à la somme féminin+masculin
    champs = ligne.split(';')
    dep.append(champs[0].strip('"'))
    jour.append(parse(champs[2].strip('"'))) # parse() sert à convertir la chaîne de caractères en une date
    rad.append(int(champs[3]))

tab = zip(rad,jour,dep)
dates , rad = [],[]
for r in tab :
    if r[2]=='17' :
        rad.append(r[0])
        dates.append(r[1])
        # dates.append(r[1].strftime("%d/%m")) # strftime() permet de donner le format souhaité aux dates

fig, ax = plt.subplots(figsize=(15,10))
ax.plot(dates,rad)
fig.suptitle("Évolution du nombre d'hospitalisations en Charente-Maritime", fontsize=16)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))
ax.xaxis.set_major_locator(mdates.DayLocator(interval=5))
fig.autofmt_xdate()
plt.show()
