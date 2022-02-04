import requests
from bs4 import BeautifulSoup
import cssutils

name=input("Entre le nom du jeu recherché : ")

file=open("main.html", "w", encoding="utf-8")
file.write(f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Comparatif de prix de jeux</title>
    <link rel="stylesheet" href="index.css">
    <link
        href="https://fonts.googleapis.com/css2?family=Montserrat&family=Nunito+Sans:ital,wght@0,400;0,700;1,400;1,700&display=swap"
        rel="stylesheet">
</head>
<body>
<main>
<h1>Liste des résultats pour le jeu {name} :</h1>
<section>
''')

page = requests.get(f'https://www.instant-gaming.com/fr/rechercher/?q={name.replace(" ", "+")}')

soupdata = BeautifulSoup(page.content, "html.parser")

results = soupdata.find_all("div", class_="item")

file.write('''<h2>Résultats sur instant gaming</h2>
<div>''')

for result in results:

    title = result.find("div", class_="name")
    imageGame = result.find("img", class_="picture")
    dlc = result.find("img", class_="dlc")
    discount = result.find("div", class_="discount")
    price = result.find("div", class_="price")
    discountText = '(' + discount.text + ')' if discount else ""
    priceText = price.text if price else "Non indiqué"
    requests.post('http://localhost:3000/data', {
        "title": " ".join(title.text.split()),
        "plateforme": badge.text,
        "image_src": imageGame,
        "dlc": dlc,
        "discount": discount,
        "price": price
    })
    
    file.write(f'''
        <div class="card">
            <h3 class="title">{title.text} {"<span class='dlc'>DLC</span>" if dlc else ""}</h3>
            <div><img src="{imageGame["data-src"]}"/></div>
            <p>Prix : {priceText} {discountText}</p>
        </div>
    ''')

file.write('''
</div>
</section>
</main>
</body>
</html>''')