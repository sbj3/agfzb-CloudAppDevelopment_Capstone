from django.db import models
from django.utils.timezone import now


# Create your models here.


class CarMake(models.Model):
    """
    # <HINT> Create a Car Make model `class CarMake(models.Model)`:
    # - Name
    # - Description
    # - Any other fields you would like to include in car make model
    # - __str__ method to print a car make object
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(null=False, max_length=30)
    description = models.CharField(null=False, max_length=50)
    manufacturer = models.CharField(null=False, max_length=50)

    def __str__(self):
        return self.name + ", " + self.description


class CarModel(models.Model):
    """
    # <HINT> Create a Car Model model `class CarModel(models.Model):`:
    # - Many-To-One relationship to Car Make model (One Car Make has many
    #       Car Models, using ForeignKey field)
    # - Name
    # - Dealer id, used to refer a dealer created in cloudant database
    # - Type (CharField with a choices argument to provide limited choices such
    #       as Sedan, SUV, WAGON, etc.)
    # - Year (DateField)
    # - Any other fields you would like to include in car model
    # - __str__ method to print a car make object
    """
    SEDAN = 'sedan'
    SUV = 'suv'
    WAGON = 'wagon'
    TYPE_CHOICES = [
        (SEDAN, 'Sedan'),
        (SUV, 'SUV'),
        (WAGON, 'Wagon')
    ]

    make = models.ForeignKey(CarMake, default=1, on_delete=models.CASCADE)
    dealer_id = models.IntegerField(null=False, default=15)
    name = models.CharField(null=False, max_length=30)

    type = models.CharField(
        null=False,
        max_length=20,
        choices=TYPE_CHOICES,
        default=SEDAN
    )
    year = models.DateField(default=now, null=False)
    trim = models.CharField(null=True, max_length=30)

    def __str__(self):
        return self.name + ", " + \
               self.type + ", " + \
               self.trim + ", " + \
               str(self.year.year)


class CarDealer:
    """
    # <HINT> Create a plain Python class `CarDealer` to hold dealer data
    """

    def __init__(self, address, city, full_name, id,
                 lat, long, short_name, st, zip):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.st = st
        # Dealer zip
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name


class DealerReview:
    """
    # <HINT> Create a plain Python class `DealerReview` to hold review data
    """

    def __init__(self,  id,  name,  dealership,  review,
                 purchase, purchase_date,
                 car_make,  car_model,  car_year, sentiment=None):
        # Review id
        self.id = id
        # Review name
        self.name = name
        # Review dealership
        self.dealership = dealership
        # Review review
        self.review = review
        # Review purchase
        self.purchase = purchase
        # Review purchase_date
        self.purchase_date = purchase_date
        # Review car_make
        self.car_make = car_make
        # Review car_model
        self.car_model = car_model
        # Review car_year
        self.car_year = car_year
        self.sentiment = sentiment

    def __str__(self):
        return "Dealership Id: " + self.dealership + \
                "Reviewer Name: " + self.name
