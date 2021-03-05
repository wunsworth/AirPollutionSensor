import json
from datetime import *
import numpy as np
import pandas as pd

class Sensor:
    """ A sensor class containing ID, location, readings etc.
    
    This class is a parent class for our three types of sensors: high-cost static, low-cost static, and low-cost mobile.
    These objects are intended to form the class structure of part of our Network class.

    Attributes:
        ID: the unique ID of the sensor (str)
        sensorType: the type of sensor (high, low, mobile) (str)
        latitude: the latitude coordinate of the sensor (float)
        longitude: the longitude coordinate of the sensor (float)
        readings: the readings taken from the sensor indexed by datetime (dict)
        calibrations: a record of when the sensor has been calibrated indexed by datetime (dict)
    """
    def __init__(self, ID, sensorType, latitude, longitude):
        self.ID = ID
        self.sensorType = sensorType
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
    """ A subclass of the Sensor class describing mobile sensors

    This sensor is low-cost, so it needs to be calibrated.
    
    Attributes:
        Attributes inherited from Sensor class.
        calib_time: the last time the sensor was calibrated (datetime)
    """
    def __init__(self, ID, latitude, longitude, calib_time = None):
        super().__init__(ID = ID, sensorType = 'mobile', latitude = latitude, longitude = longitude)
        self.calib_time = calib_time
        
class lowSensor(Sensor):
    """A subclass of the Sensor class describing the low-cost static sensors

    This sensor is low-cost, so it needs to be calibrated.
    
    Attributes:
        Attributes inherited from Sensor class.
        calib_time: the last time the sensor was calibrated (datetime)
    """
    def __init__(self, ID, latitude, longitude, calib_time = None):
        super().__init__(ID = ID, sensorType = 'low', latitude = latitude, longitude = longitude)
        self.calib_time = calib_time

class highSensor(Sensor):
    """A subclass of the Sensor class describing the high-cost static sensors
    
    Attributes:
        Attributes inherited from Sensor class.
    """
    def __init__(self, ID, latitude, longitude):
        super().__init__(ID = ID, sensorType = 'high', latitude = latitude, longitude = longitude)

class Network:
    """ Describes a sensor network.

    Attributes:
        sensors: a list of Sensor objects, these can be of any type. (list(Sensor))
        IDs: a list of the IDs of the Sensor objects, these can be useful for iterating over.
    """
    def __init__(self, sensors: list):
        self.sensors = {sensor.ID: sensor for sensor in sensors}
        self.IDs = [sensor.ID for sensor in sensors]
    
    def add_sensors(self, sensors):
        """ Takes either a Sensor object or a list of Sensor objects and adds them to the network

        Args:
            sensors: a Sensor object or list of Sensor objects to be added. (Sensor/list(Sensor))

        Returns:
            None            
        """
        sensors = list(sensors)
        for sensor in sensors:
            self.sensors[sensor.ID] = sensor
            self.IDs.append(sensor.ID)

    def networkData(self, df):
        """ Takes a dataframe and returns all the data for the sensors in our network

        Args:
            self: the Network object containing our Sensors
            df: the pandas dataframe containing all the data

        Returns:
            networkDF: the pandas dataframe containing data for our sensors
        """

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