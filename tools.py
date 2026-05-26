import csv
from retriever import retrieve

CARS_CSV = './data/cars.csv'
TEST_DRIVES_CSV = './data/test_drives.csv'

inventory = []
with open(CARS_CSV) as csvfile:
    inventory = list(csv.DictReader(csvfile))

#-------------- INVENTORY -------------
def get_car_price(model: str) -> str:
    """it takes the model and returns its price in EGP from the csv file"""
    for car in inventory:
        if car["model"].lower() == model.lower():
            price = int(car['price_egp'])
            return f"{price:,} EGP"
    return "not available"

def get_available_colors(model: str) -> str:
    """it takes the model and returns its available colors from the csv file"""
    for car in inventory:
        if car["model"].lower() == model.lower():
            return car["colors"]
    return "not available"

def get_all_cars() -> str:
    """return a string with all cars available"""
    return ', '.join([car['model'] for car in inventory])


#------------- TEST DRIVES ----------
def check_test_drive_request(phone:str, car_model:str) -> str:
    """it takes the phone and car_model and returns True or False by checking if the record with same phone and car_model exists"""
    with open(TEST_DRIVES_CSV) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if(
                row['phone'] == phone and
                row['car_model'].lower() == car_model.lower()
            ):
                return "True"
    return "False"



def save_test_drive_request(name: str, phone: str, car_model: str) -> str:
    """takes name, phone, car_model and saves them for test drive request"""
    with open(TEST_DRIVES_CSV, 'a') as csvfile:
        fieldnames = ['name', 'phone', 'car_model']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow({'name': name, 'phone': phone, 'car_model': car_model})

    return "Success"

def edit_test_drive_request(phone: str, car_model: str, new_car_model: str) -> str:
    """takes phone, the old car model and the new model, it updates the car model in the csv file"""
    rows = []
    with open(TEST_DRIVES_CSV) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if (
                    row['phone'] == phone and
                    row['car_model'].lower() == car_model.lower()
            ):
                found = True
                row['car_model'] = new_car_model
            rows.append(row)

        if not found:
            return "Request not found"


        with open(TEST_DRIVES_CSV, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=['name', 'phone', 'car_model'])
            writer.writeheader()
            for row in rows:
                writer.writerow(row)

        return "Success"

# ----------- RAG IMPLEMENTATION
def search_policy(query: str) -> str:
    """using vector db, it returns the text with relevant or similar text with the query"""
    return retrieve(query)
