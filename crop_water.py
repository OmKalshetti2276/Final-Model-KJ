
#Defining Crop coefficients for different crops

CROP_KC ={
    "wheat":1.15,
    "maize":1.20,
    "tomato":1.10,
    "rice":1.20,
    "generic":1.0
}

def calculate_etc(eto,crop="generic"):

    kc = CROP_KC.get(crop.lower(),1.0)
    etc=eto*kc

    return round(etc,2)

#This function converts eto to etc using crop coefficient

