from django.db import models


# ✅ Car Make Model
class CarMake(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name


# ✅ Car Model
class CarModel(models.Model):
    SEDAN = "Sedan"
    SUV = "SUV"
    WAGON = "Wagon"

    CAR_TYPES = [
        (SEDAN, "Sedan"),
        (SUV, "SUV"),
        (WAGON, "Wagon"),
    ]

    car_make = models.ForeignKey(
        CarMake, on_delete=models.CASCADE
    )  # Many-to-One relation
    dealer_id = models.IntegerField()  # Refers to dealer in Cloudant DB
    name = models.CharField(max_length=50)
    car_type = models.CharField(max_length=10,
    choices=CAR_TYPES, default=SEDAN)
    year = models.IntegerField()  # Year of manufacture

    def __str__(self):
        return f"{self.car_make.name} {self.name} ({self.year})"
