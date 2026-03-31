import json
import os
from typing import Dict, Any


'''
Útmutató a fájl függvényeinek a használatához

Új felhasználó hozzáadása:

new_user = {
    "id": 4,  # Egyedi felhasználó azonosító
    "name": "Szilvás Szabolcs",
    "email": "szabolcs@plumworld.com"
}

Felhasználó hozzáadása a JSON fájlhoz:

add_user(new_user)

Hozzáadunk egy új kosarat egy meglévő felhasználóhoz:

new_basket = {
    "id": 104,  # Egyedi kosár azonosító
    "user_id": 2,  # Az a felhasználó, akihez a kosár tartozik
    "items": []  # Kezdetben üres kosár
}

add_basket(new_basket)

Új termék hozzáadása egy felhasználó kosarához:

user_id = 2
new_item = {
    "item_id": 205,
    "name": "Szilva",
    "brand": "Stanley",
    "price": 7.99,
    "quantity": 3
}

Termék hozzáadása a kosárhoz:

add_item_to_basket(user_id, new_item)

Hogyan használd a fájlt?

Importáld a függvényeket a filehandler.py modulból:

from filehandler import (
    add_user,
    add_basket,
    add_item_to_basket,
)

 - Hiba esetén ValuErrort kell dobni, lehetőség szerint ezt a 
   kliens oldalon is jelezni kell.

'''

def load_json(src: str = "data.json") -> Dict[str, Any]:
    json_file_path = os.path.join(os.path.dirname(__file__), src)
    if not os.path.exists(json_file_path):
        raise ValueError("A fájl nem létezik!")

    with open(json_file_path, "r", encoding='utf-8') as f:
        return json.load(f)

def save_json(data: Dict[str, Any], dest: str = "data.json") -> None:
    json_file_path = os.path.join(os.path.dirname(__file__), dest)
    with open(json_file_path, "w", encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def add_user(user: Dict[str, Any]) -> None:
    data = load_json()

    if any(u["id"] == user["id"] for u in data["Users"]):
        raise ValueError(f"A felhasználó már létezik ezzel az azonosítóval: {user['id']}")

    data["Users"].append(user)
    save_json(data)

def add_basket(basket: Dict[str, Any]) -> None:
    data = load_json()

    if any(b["id"] == basket["id"] for b in data["Baskets"]):
        raise ValueError(f"A kosár már lézetik ezzel az azonosítóval: {basket['id']}")

    if all(b["user_id"] != basket["user_id"] for b in data["Baskets"]):
        raise ValueError(f"A felhasználó nem található ezzel az azonosítóval: {basket["user_id"]}")

    data["Baskets"].append(basket)
    save_json(data)

def add_item_to_basket(user_id: int, item: Dict[str, Any]) -> None:
    data = load_json()
    basket_found = False

    for basket in data["Baskets"]:
        if basket["user_id"] == user_id:
            basket_found = True
            if any(i["item_id"] == item["item_id"] for i in basket["items"]):
                raise ValueError(f"A termék már szerepel a kosárban ezzel az azonosítóval: {item['item_id']}")
            else:
                basket["items"].append(item)
            break

    if not basket_found:
        raise ValueError(f"Nem található kosár ezzel a felhasználói azonosítóval: {user_id}")

    save_json(data)
