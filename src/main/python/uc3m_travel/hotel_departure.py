from uc3m_travel.hotel_management_exception import HotelManagementException
from datetime import datetime
class HotelDeparture:
    def __init__(self,room_key,departure_date_timestamp):
        self.__room_key = room_key
        self.__departure_date_timestamp = departure_date_timestamp
        self.__checkout_time = datetime.timestamp(datetime.utcnow())
        self.is_today_departure(self.__departure_date_timestamp)

    def save_checkout(self, checkout, room_key):
        checkout.load_json_store()
        checkout.find_checkout(room_key, "_HotelDeparture__room_key")
        room_checkout = checkout.create_checkout(room_key)
        checkout.add_checkout_store(room_checkout)
        checkout.save_store()
    def is_today_departure(self, departure_date_timestamp):
        today = datetime.utcnow().date()
        if datetime.fromtimestamp(departure_date_timestamp).date() != today:
            raise HotelManagementException("Error: today is not the departure day")