from .models import CarMake, CarModel

def initiate():
    car_make_data = [
        {"name": "NISSAN", "description": "Great cars. Japanese technology"},
        {"name": "Mercedes", "description": "Great cars. German technology"},
        {"name": "Audi", "description": "Great cars. German technology"},
        {"name": "Kia", "description": "Great cars. Korean technology"},
        {"name": "Toyota", "description": "Great cars. Japanese technology"},
    ]

    # ✅ Ensure CarMakes are only created once
    car_make_instances = []
    for data in car_make_data:
        car_make, created = CarMake.objects.get_or_create(name=data["name"], defaults={"description": data["description"]})
        car_make_instances.append(car_make)

    print(f"✅ {len(car_make_instances)} CarMakes added.")

    # ✅ Now, Create CarModel instances (only if they don’t exist)
    car_model_data = [
        {"name": "Pathfinder", "car_type": "SUV", "year": 2023, "car_make": car_make_instances[0], "dealer_id": 1},
        {"name": "Qashqai", "car_type": "SUV", "year": 2023, "car_make": car_make_instances[0], "dealer_id": 2},
        {"name": "XTRAIL", "car_type": "SUV", "year": 2023, "car_make": car_make_instances[0], "dealer_id": 3},
        {"name": "A-Class", "car_type": "Sedan", "year": 2023, "car_make": car_make_instances[1], "dealer_id": 4},
        {"name": "C-Class", "car_type": "Sedan", "year": 2023, "car_make": car_make_instances[1], "dealer_id": 5},
        {"name": "E-Class", "car_type": "Sedan", "year": 2023, "car_make": car_make_instances[1], "dealer_id": 6},
        {"name": "A4", "car_type": "Sedan", "year": 2023, "car_make": car_make_instances[2], "dealer_id": 7},
        {"name": "A5", "car_type": "Sedan", "year": 2023, "car_make": car_make_instances[2], "dealer_id": 8},
        {"name": "A6", "car_type": "Sedan", "year": 2023, "car_make": car_make_instances[2], "dealer_id": 9},
        {"name": "Sorrento", "car_type": "SUV", "year": 2023, "car_make": car_make_instances[3], "dealer_id": 10},
        {"name": "Carnival", "car_type": "SUV", "year": 2023, "car_make": car_make_instances[3], "dealer_id": 11},
        {"name": "Cerato", "car_type": "Sedan", "year": 2023, "car_make": car_make_instances[3], "dealer_id": 12},
        {"name": "Corolla", "car_type": "Sedan", "year": 2023, "car_make": car_make_instances[4], "dealer_id": 13},
        {"name": "Camry", "car_type": "Sedan", "year": 2023, "car_make": car_make_instances[4], "dealer_id": 14},
        {"name": "Kluger", "car_type": "SUV", "year": 2023, "car_make": car_make_instances[4], "dealer_id": 15},
    ]

    for data in car_model_data:
        CarModel.objects.get_or_create(
            name=data["name"],
            car_make=data["car_make"],
            defaults={"car_type": data["car_type"], "year": data["year"], "dealer_id": data["dealer_id"]}
        )

    print("✅ CarModels added successfully!")