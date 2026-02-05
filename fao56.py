import math

#We are calculating function to calculate eto(reference evapotranspiration)
def calculate_eto(temp_c, humidity, wind_speed, solar_radiation):

    """
    FAO-56 Simplified Penman-Monteith ETo Calculator

    Inputs:
    temp_c          : Temperature in °C
    humidity        : Relative Humidity in %
    wind_speed      : Wind speed at 2m height (m/s)
    solar_radiation : Solar radiation (MJ/m²/day)

    """

    # Calculation of Saturation vapor pressure (kPa)
    es = 0.6108 * math.exp((17.27 * temp_c) / (temp_c + 237.3))

    #Active vap pressure in kPa
    ea = es * (humidity / 100)

    # Vapr pressure deficit
    vpd = es - ea

    # Slope of vapor pressure curve (Δ)
    delta = (4098 * es) / ((temp_c + 237.3) ** 2)

    # Psychrometric constant (γ)
    gamma = 0.066

    # Soil heat flux (ignored for daily calculation)
    G = 0

    # FAO-56 simplified equation to calculate eto
    eto = (
        (0.408 * delta * (solar_radiation - G)) +
        (gamma * (900 / (temp_c + 273)) * wind_speed * vpd)
    ) / (delta + gamma * (1 + 0.34 * wind_speed))

    return round(eto, 2)
#this will be passed to calculate etc as it is crop related

