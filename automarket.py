from fastapi import FastAPI
from pydantic import BaseModel
import pickle
from pandas import json_normalize

app = FastAPI()

class Item(BaseModel):
    model: str
    region: str
    age: float
    liters: float
    horse_power: float
    type_engine: str
    transmission: str
    machine_drive: str
    mileage: float

@app.post("/nissan/")
async def create_item(item: Item):
    with open('/usr/src/app/lgb_nissan.pkl', 'rb') as f:
        pickled_model = pickle.load(f)

    ding = item.dict()  # Convert Item instance to dictionary
    df2 = json_normalize([ding])  # Convert dictionary to DataFrame

    list_str_obj_cols = df2.columns[df2.dtypes == "object"].tolist()
    for str_obj_col in list_str_obj_cols:
        df2[str_obj_col] = df2[str_obj_col].astype("category")

    y_pred = int(pickled_model.predict(df2))
    return {y_pred}
    
@app.post("/toyota/")
async def create_item(item: Item):
    with open('/usr/src/app/lgb_toyota.pkl', 'rb') as f:
        pickled_model = pickle.load(f)

    ding = item.dict()  # Convert Item instance to dictionary
    df2 = json_normalize([ding])  # Convert dictionary to DataFrame

    list_str_obj_cols = df2.columns[df2.dtypes == "object"].tolist()
    for str_obj_col in list_str_obj_cols:
        df2[str_obj_col] = df2[str_obj_col].astype("category")

    y_pred = int(pickled_model.predict(df2))
    return {y_pred}    

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=80)

 