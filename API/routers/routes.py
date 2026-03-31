from fastapi_kiindulo.API.routers.data.filereader import get_next_basket_id
from schemas.schema import User, Basket, Item
from fastapi.responses import JSONResponse
from fastapi import HTTPException, APIRouter
from data.filehandler import add_user, add_basket, add_item_to_basket, save_json
from data.filereader import get_user_by_id, get_basket_by_user_id, get_all_users, get_total_price_of_basket, load_json
from typing import List

'''

Útmutató a fájl használatához:

- Minden route esetén adjuk meg a response_modell értékét (típus)
- Ügyeljünk a típusok megadására
- A függvények visszatérési értéke JSONResponse() legyen
- Minden függvény tartalmazzon hibakezelést, hiba esetén dobjon egy HTTPException-t
- Az adatokat a data.json fájlba kell menteni.
- A HTTP válaszok minden esetben tartalmazzák a 
  megfelelő Státus Code-ot, pl 404 - Not found, vagy 200 - OK

'''

routers = APIRouter()


@routers.post('/adduser', response_model=User)
def adduser(user: User):
    try:
        user_dict = user.model_dump()
        add_user(user_dict)
        return JSONResponse(status_code=201, content=user_dict)
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))


@routers.post('/addshoppingbag', response_model=str)
def addshoppingbag(userid: int):
    try:
        new_basket = Basket(id=get_next_basket_id(), user_id=userid, items=[])
        add_basket(new_basket.model_dump())
        return JSONResponse(status_code=201, content="Sikeres kosár hozzárendelés.")
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@routers.post('/additem', response_model=Basket)
def additem(userid: int, item: Item):
    try:
        item_dict = item.model_dump()
        add_item_to_basket(userid, item_dict)
        return JSONResponse(status_code=201, content=get_basket_by_user_id(userid))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@routers.put('/updateitem', response_model=Basket)
def updateitem(userid: int, itemid: int, update_item: Item):
    try:
        data = load_json()
        basket = get_basket_by_user_id(userid)
        basket["items"][str(itemid)] = update_item.model_dump()
        for i in range(len(data["Baskets"])):
            if data["Baskets"][i] == basket["id"]:
                data["Baskets"][i] = basket
                break

        save_json(data)
        return JSONResponse(status_code=201, content=get_basket_by_user_id(userid))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@routers.delete('/deleteitem', response_model=Basket)
def deleteitem(userid: int, itemid: int):
    try:
        data = load_json()
        basket = get_basket_by_user_id(userid)
        old_length = len(basket["items"])
        new_list = [item for item in basket["items"] if item["item_id"] == itemid]

        if len(new_list) == old_length:
            raise HTTPException(status_code=404, detail="Item not found.")

        basket["items"] = new_list
        for i in range(len(data["Baskets"])):
            if data["Baskets"][i] == basket["id"]:
                data["Baskets"][i] = basket
                break

        save_json(data)
        return JSONResponse(status_code=201, content=get_basket_by_user_id(userid))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@routers.get('/user', response_model=User)
def user(userid: int):
    try:
        user = get_user_by_id(userid)
        return JSONResponse(status_code=200, content=user)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@routers.get('/users', response_model=List[User])
def users():
    try:
        users = get_all_users()
        return JSONResponse(status_code=200, content=users)
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))


@routers.get('/shoppingbag', response_model=List[Item])
def shoppingbag(userid: int):
    try:
        basket = get_basket_by_user_id(userid)
        return JSONResponse(status_code=200, content=basket["items"])
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@routers.get('/getusertotal', response_model=float)
def getusertotal(userid: int):
    try:
        total = get_total_price_of_basket(userid)
        return JSONResponse(status_code=200, content=total)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@routers.post('/save', response_model=str)
def save(source: str, dest: str):
    try:
        data = load_json(source)
        save_json(data, dest)
        return JSONResponse(status_code=200, content=f"Sikeres mentés a {dest} fájlba.")
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))


@routers.post('/reload', response_model=str)
def reload(dest: str, source: str):
    try:
        data = load_json(source)
        save_json(data, dest)
        return JSONResponse(status_code=200, content=f"Sikeres visszatöltés a {source} fájlból.")
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
