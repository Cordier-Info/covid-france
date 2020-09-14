import requests
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from dateutil.parser import parse

dep = input("Numéro du département ? ")

# données gouvernementales covid
url = "https://www.data.gouv.fr/fr/datasets/r/63352e38-d353-4b54-bfd1-f1b3ee1cabd7"
download = requests.get(url)
brut = download.content.decode('utf-8') # pour transformer les bytes récupérés en string
lignes = brut.split('\n')
date, hosp = [],[]
jour = parse("2020-03-18")
# ces andouilles ont changé de format de date pour quelques données,
# du coup on profite que parse reonnaît n'importe quel format comme une date propre.
hosp_tot = 0

for ligne in lignes[1:-1:3] : # on saute l'en-tête et ne garde que les sexes 0 correspondant à la somme féminin+masculin
    champ = ligne.split(';')
    if champ[0] == '"{}"'.format(dep) :
        date.append(parse(champ[2].strip('"'))) # parse() sert à convertir la chaîne de caractères en une date
        hosp.append(int(champ[3]))
    elif dep == "0" :
        if parse(champ[2].strip('"')) == jour :
            hosp_tot += int(champ[3])
        else :
            hosp.append(hosp_tot)
            date.append(jour)
            hosp_tot = 0
            jour = parse(champ[2].strip('"'))


# liste noms des départements
url2 = "https://static.data.gouv.fr/resources/departements-et-leurs-regions/20190815-175403/departements-region.csv"
download2 = requests.get(url2)
brut2 = download2.content.decode('utf-8')
lignes2 = brut2.split('\n')
for li in lignes2 :
    ch = li.split(',')
    if ch[0]==str(dep) :
        nom_dep = ch[1]

fig, ax = plt.subplots(figsize=(15,10))
ax.plot(date,hosp)
if dep == "0" :
    fig.suptitle("Évolution du nombre d'hospitalisations en France", fontsize=16)
else :
    fig.suptitle("Évolution du nombre d'hospitalisations en {}".format(nom_dep), fontsize=16)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))
ax.xaxis.set_major_locator(mdates.DayLocator(interval=10))
fig.autofmt_xdate()
plt.show()
