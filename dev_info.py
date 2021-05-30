DEVICE_NAMES = [
    "None",
    "Lavadora",
    "Secadora",
    "TV",
    "AC",
    "Estufa"
]

HOURS_DEVICES = [
    1000000000, # you cna have any amount of no devices
    7, # at most 7 hours of wahser
    5, # at most 5 hours of dryer
    4, # at most 24 hours of tv
    7, # at most 7 hours of AC
    1, # at most 1 hour of stove
]

KW_DEVICES = [ #KW per device
    0, # no devices consume no energy
    0.5, # washer
    3, # dryer
    1.5, #stove
    0.12, #tv
    3.5, #ac
]

NUM_DEVICES = 6
DEVICES_PER_HOUR = 5

