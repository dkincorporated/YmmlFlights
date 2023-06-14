"""
Testing program for fetching data from Melbourne Airport's flights page

Note: This does not use an officially published API endpoint, so it may break or change without notice.
"""

__author__ = "David Kong"
__docformat__ = "reStructuredText"

from enum import Enum
import json, requests, datetime
from prettytable import PrettyTable

ENDPOINT = "https://www.melbourneairport.com.au/api/data/search?queries%5B0%5D%5BindexName%5D=melair_flights&queries%5B0%5D%5Bparams%5D%5Bfacets%5D%5B3%5D=status&queries%5B0%5D%5Bparams%5D%5Bfilters%5D=flightDirection%3A{0}%20AND%20scheduledTimeStamp%3A%20{1}%20TO%20{2}&queries%5B0%5D%5Bparams%5D%5BhitsPerPage%5D={3}"


class FlightDirection(Enum):
    """
    Enumeration of the direction of flights
    """

    DEFAULT = None
    DEPARTURE = "departure"
    ARRIVAL = "arrival"

    @classmethod
    def from_string(cls, string: str):
        """
        Get the flight direction from a string
        :param string: the direction in string format
        :return: the corresponding direction
        """
        for direction in FlightDirection:
            if direction.name == string:
                return direction
        return None


class RouteType(Enum):
    """
    Enumeration of the types of routes
    """

    DEFAULT = None
    DOMESTIC = "domestic"
    INTERNATIONAL = "international"

    @classmethod
    def from_string(cls, string: str):
        """
        Get the route type from a string
        :param string: the route type in string format
        :return: the corresponding route type
        """
        for route_type in RouteType:
            if route_type.name == string:
                return route_type
        return None


class Flight:
    """
    Contains the data of a flight (departure or arrival)
    """

    flight_number = None
    airline_code = None
    airline_name = None
    airline_logo_src = None
    airport_name = None
    airport_code = None
    scheduled_time = None
    estimated_time = None
    last_updated_time = None
    terminal = None
    gate = None
    status = None
    route_type = None
    flight_direction = None

    def __init__(self, json_obj: dict) -> None:
        """
        Parse the JSON object, and set the attributes
        :param json_obj: the JSON object for the flight provided from the API
        """
        self.flight_number = json_obj["flightNumber"]
        self.airline_code = json_obj["airlineCode"]
        if "airlineName" in json_obj:
            self.airline_name = json_obj["airlineName"]
            self.airline_logo_src = json_obj["airlineLogo"]["src"]
        self.airport_name = json_obj["airportNames"][0]
        self.airport_code = json_obj["airportCodes"][0]
        self.scheduled_time = json_obj["scheduledTimeStamp"]
        if "estimatedTimeStamp" in json_obj:
            self.estimated_time = json_obj["estimatedTimeStamp"]
        self.last_updated_time = json_obj["lastUpdatedTimeStamp"]
        self.terminal = json_obj["terminal"]
        self.gate = json_obj["gate"]
        self.status = json_obj["status"]
        self.route_type = RouteType.from_string(json_obj["routeType"])
        self.flight_direction = FlightDirection.from_string(json_obj["flightDirection"])

    def get_scheduled_time(self) -> str:
        """
        Get the scheduled time in display format
        :return: scheduled time for display
        """
        if self.scheduled_time is None:
            return ""
        return datetime.datetime.fromtimestamp(self.scheduled_time / 1000).strftime("%H:%M")

    def get_estimated_time(self) -> str:
        """
        Get the estimated time in display format
        :return: estimated time for display
        """
        if self.estimated_time is None:
            return ""
        return datetime.datetime.fromtimestamp(self.estimated_time / 1000).strftime("%H:%M")


def fetch_flights(flight_direction: FlightDirection, min_in_past: int = 30, min_in_future: int = 180, quantity: int = 10) -> [Flight]:
    """
    Fetch the flights, process them, and return a list of the flights
    :param flight_direction: the direction of the flights
    :param min_in_past: how far in the past, in min, to fetch flights
    :param min_in_future: how far into the future, in min, to fetch flights
    :param quantity: the number of flights to fetch
    :return: a list of the flights
    """
    time_now = datetime.datetime.now() - datetime.timedelta(minutes=min_in_past)
    time_future = time_now + datetime.timedelta(minutes=min_in_future)
    request_url = ENDPOINT.format(flight_direction.name, int(time_now.timestamp()) * 1000,
                                  int(time_future.timestamp()) * 1000, quantity)
    flights_request = json.loads(requests.get(request_url).text)
    request_results = flights_request["results"]
    request_hits = request_results[0]["hits"]
    flights_list = [Flight(flt) for flt in request_hits]
    return flights_list


if __name__ == "__main__":
    direction = FlightDirection.ARRIVAL  # set the direction

    # Fetch the flights
    flight_list = fetch_flights(direction)

    # Set up the table for printing
    table_header = ["Airline", "Flight", "Destination", "Scheduled", "Estimated", "Terminal", "Gate", "Status"]
    if direction == FlightDirection.ARRIVAL:
        table_header = ["Airline", "Flight", "Origin", "Scheduled", "Estimated", "Terminal", "Gate", "Status"]

    table = PrettyTable(table_header)
    for flight in flight_list:
        table.add_row([flight.airline_name, flight.flight_number, flight.airport_name, flight.get_scheduled_time(),
                       flight.get_estimated_time(), flight.terminal, flight.gate, flight.status])

    # Print the output
    print(direction.name + "S")
    print(table)
