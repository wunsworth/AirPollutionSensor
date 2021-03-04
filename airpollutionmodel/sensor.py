import json
from datetime import *
import numpy as np
import pandas as pd

class Sensor:
    def __init__(self, ID, latitude, longitude):
        self.ID = ID
        self.latitude = latitude
        self.longitude = longitude
        self.readings = dict()
        self.calibrations = dict()

    def __repr__(self):
        return repr(self.as_JSON())

    def new_reading(self, datetime: datetime, reading):
        self.readings[datetime] = reading

    def new_calibration(self, datetime: datetime, calibration_diff):
        self.calibration[datetime] = calibration_diff

    def as_JSON(self):
        d = {
        'ID': self.ID,
        'latitude': self.latitude,
        'longitude': self.longitude,
        'readings': self.readings,
        'calibrations': self.calibrations}

        return json.dumps(d, indent = 4)

class mobileSensor(Sensor):
    def __init__(self, ID, latitude, longitude, calib_time = None):
        super().__init__(ID, latitude, longitude)
        self.calib_time = calib_time
        
class lowSensor(Sensor):
    def __init__(self, ID, latitude, longitude, calib_time = None):
        super().__init__(ID, latitude, longitude)
        self.calib_time = calib_time

class Network:
    def __init__(self):
        self.sensors = dict()
    
    def add_sensors(self, sensors):
        sensors = list(sensors)
        for sensor in sensors:
            self.sensor_list[sensor.ID] = sensor

    def ids(self):
        return [sensor.ID for sensor in self.sensors()]
    
    def readings(self, since: datetime):
        readings = dict()
        for sensor in self.sensors:
            for datetime, reading in sensor.readings.items():
                if datetime >= since:
                    readings[(sensor.ID, datetime)] = reading
        readings_sorted = dict(sorted(readings.items(), key = lambda reading: reading[0][1]))
        return readings_sorted

    def calibrations(self, since: datetime):
        calibrations = dict()
        for sensor in self.sensors:
            for datetime, calibration in sensor.calibrations.items():
                if datetime >= since:
                    readings[(sensor.ID, datetime)] = calibration
        calibrations_sorted = dict(sorted(calibrations.items(), key = lambda calib: calib[0][1]))
        return calibrations_sorted