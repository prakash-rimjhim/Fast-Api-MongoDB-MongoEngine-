from fastapi import FastAPI, HTTPException
from mongoengine import connect, Document, StringField
from pydantic import BaseModel

app = FastAPI()


connect(db='fastapiitem', host='localhost', port=27017)


class Items(Document):
    name = StringField(required=True)
    description = StringField(required=True)
    
    meta = {
        "collection": "Items"
    }

class ItemCreate(BaseModel):
    name: str
    description: str
    
class ItemUpdate(BaseModel):
    name: str
    description: str
    
class ItemDelete(BaseModel):
    name : str
    description: str

@app.get("/items/")
def read_items():
    items = Items.objects()
    print(len(items))
   
    data={}
    for item in items:
        print(f"Name: {item.name}, Description: {item.description}")
        data[item.name]=item.description
    return{"data":data}



@app.post("/items/create")
def create_item(item_data :ItemCreate):
    new_item = Items(name=item_data.name , description = item_data.description)
    new_item.save()   
    return {"message": "Item created successfully", "data": {"name": new_item.name, "description": new_item.description}}
    

@app.put("/items/update/{item_id}")
def update_item(item_id: str, item_data: ItemUpdate):
    current_item = Items.objects(id=item_id).first()

    if not current_item:
        raise HTTPException(status_code=404, detail="Item not found")

    current_item.name = item_data.name
    current_item.description = item_data.description

    current_item.save()
    return {"message": "Item updated successfully", "data": {"name": current_item.name, "description": current_item.description}}


@app.delete("/items/delete/{item_id}")
def delete_item(item_id:str, item_data :ItemDelete):
    item = Items.objects(id=item_id).first()
    
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    item.delete()       
    return {"message": "Item deleted successfully", }