import streamlit as st
import pandas as pd
import seaborn as sns
import json
import joblib
st.header('Housing prices in Russia')

PATH_DATA = "data/sotka.csv"
PATH_UNIQUE_VALUES = "data/unique_values.json"
PATH_MODEL = "models/lr_pipeline.sav"

#@st.cache_data
def load_data(path):

    #Load data from path""" 
    data = pd.read_csv(path) 
    # для демонстрации 
    data = data.sample(10000) 
    return data

#@st.cache_data
def load_model(path):
#Load model from path'""'
    model = joblib.load(path)
    return model

def transform(data): 
    #Transforn data""" 
    colors = sns.color_palette("coolwarm").as_hex()
    n_colors = len(colors)

    data = data.reset_index(drop=True)
    data["norm_price"] = data["price"] / data["area"]

    data["label_colors"] = pd.qcut(data["norm_price"], n_colors, labels=colors)
    data["label_colors"] = data["label_colors"].astype("str") 
    return data

df = load_data(PATH_DATA)
df = transform(df)
#st.write(df [:4])

st.map(data=df, latitude="geo_lat", longitude="geo_lon", color='label_colors')

with open(PATH_UNIQUE_VALUES) as file: 
    dict_unique = json.load(file)

# features
building_type = st.sidebar.selectbox('Building type', (dict_unique['building_type']))
object_type = st.sidebar.selectbox("Object type", (dict_unique['object_type']))
level = st.sidebar.slider(
    "level",min_value=min(dict_unique["level"]),	max_value=max(dict_unique["level"])
)
levels = st.sidebar.slider(
    "Levels",min_value=min(dict_unique["levels"]),	max_value=max(dict_unique["levels"])
)
rooms = st.sidebar.selectbox('Rooms', (dict_unique['rooms']))

area = st.sidebar.slider(
    "Area",min_value=min(dict_unique["area"]),	max_value=max(dict_unique["area"])
)

kitchen_area = st.sidebar.slider(
    "Kitchen area",min_value=min(dict_unique["kitchen_area"]), max_value=max(dict_unique["kitchen_area"])
)

st.markdown(
    """
    ### Описание полей
    -	building_type - Facade type. 0 - Other. 1 - Panel. 2 - Monolithic. 3 - Brick. 4 - .Blgoky. 5 - Wooden
    -	object_type - Apartment type. 1 - Secondary real estate narket; 2 - New building
    -	level - Apartment floor
    -	levels - Number of storeys
    -	rooms - the number of living rooms. If the value is '-1' then it means 'studio apartment'
    -	area - the total area of the apartment
    -	kitchen.area - Kitchen area
    -   price - Price, in rubles
"""
)
dict_data = {"building_type": building_type, 
             "object_type": object_type, 
             "level": level, 
             "levels": levels, 
             "rooms": rooms, 
             "area": area, 
             "kitchen_area": kitchen_area}

data_predict = pd.DataFrame([dict_data])
model = load_model(PATH_MODEL)

button = st.button("Predict")
if button:
    output = model.predict(data_predict)[0]
    st.success(f"{round(output)} rub")
    #st.write(output)

#     streamlit run main.py
