import json
import os
from typing import Dict, Any, List

'''
Útmutató a fájl használatához:

Felhasználó adatainak lekérdezése:

user_id = 1
user = get_user_by_id(user_id)
print(f"Felhasználó adatai: {user}")

Felhasználó kosarának tartalmának lekérdezése:

user_id = 1
basket = get_basket_by_user_id(user_id)
print(f"Felhasználó kosarának tartalma: {basket}")

Összes felhasználó lekérdezése:

users = get_all_users()
print(f"Összes felhasználó: {users}")

Felhasználó kosarában lévő termékek összárának lekérdezése:

user_id = 1
total_price = get_total_price_of_basket(user_id)
print(f"A felhasználó kosarának összára: {total_price}")

Hogyan futtasd?

Importáld a függvényeket a filehandler.py modulból:

from filereader import (
    get_user_by_id,
    get_basket_by_user_id,
    get_all_users,
    get_total_price_of_basket
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

def get_user_by_id(user_id: int) -> Dict[str, Any]:
    data = load_json()
    for user in data["Users"]:
        if user["id"] == user_id:
            return user

    raise ValueError(f"A felhasználó nem található ezzel az azonosítóval: {user_id}")

def get_basket_by_user_id(user_id: int) -> Dict[str, Any]:
    data = load_json()
    for basket in data["Baskets"]:
        if basket["user_id"] == user_id:
            return basket

    raise ValueError(f"A kosár nem található ezzel a felhasználói azonosítóval: {user_id}")


def get_all_users() -> List[Dict[str, Any]]:
    data = load_json()
    return data["Users"]

def get_total_price_of_basket(user_id: int) -> float:
    try:
        basket = get_basket_by_user_id(user_id)
    except ValueError:
        return 0.0

    return round(sum([item["price"] * item["quantity"] for item in basket["items"]]), 2)

def get_next_basket_id() -> int:
    data = load_json()
    return max([b['id'] for b in data["Baskets"]], default=100) + 1