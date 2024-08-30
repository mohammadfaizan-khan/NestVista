import json
import pickle

__locations = None
__model = None
__data_columns = None

def load_saved_artifacts():
    global __model
    global __data_columns
    global __locations
    with open("./Artifacts/columns.json", "r") as f:
        __data_columns = json.load(f)['data_columns']
        __locations = __data_columns[4:]  # first 4 columns are sqft, bath, bhk, balcony
    with open("./Artifacts/banglore_home_prices_model.pickle", "rb") as f:
        __model = pickle.load(f)

def get_estimated_price(location, sqft, bath, balcony, bhk):
    global __model
    global __data_columns
    global __locations

    if __model is None:
        load_saved_artifacts()

    loc_index = __data_columns.index(location.lower()) if location.lower() in __data_columns else -1
    if loc_index == -1:
        loc_index = 0

    x = [0] * len(__data_columns)
    x[0] = sqft
    x[1] = bath
    x[2] = bhk
    x[3] = balcony
    if loc_index >= 0:
        x[loc_index] = 1

    return round(__model.predict([x])[0], 2)

def get_location_names():
    return __locations
