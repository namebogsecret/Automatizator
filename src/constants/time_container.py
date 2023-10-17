"""
This module contains a TimeContainer class that keeps track of specific time-related information.
The TimeContainer class contains two main attributes: `start_time` and `last_time_otklik`.
The `start_time` attribute stores the date and time when the TimeContainer object is initialized.
The `last_time_otklik` attribute stores the current Unix time and can be updated via a method.
"""

from datetime import datetime
from time import time

class TimeContainer:
    """
    A class to encapsulate time-related data.
    
    Attributes:
    -----------
    start_time : datetime
        The date and time when the object is initialized.
    last_time_otklik : float
        The Unix time when `update_last_time_otklik` method is last called.
    """

    def __init__(self):
        """Initialize the TimeContainer object with the current date-time and Unix time."""
        self.start_time = datetime.now()
        self.last_time_otklik = time()

    def update_last_time_otklik(self):
        """
        Update the `last_time_otklik` attribute with the current Unix time.
        
        Returns:
        --------
        None
        """
        self.last_time_otklik = time()

# Create an instance of TimeContainer
time_container = TimeContainer()
