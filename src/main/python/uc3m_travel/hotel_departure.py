from datetime import datetime
from uc3m_travel.hotel_management_exception import HotelManagementException
from uc3m_travel.hotel_stay import HotelStay
from uc3m_travel.storage.store_checkout import StoreCheckout
from uc3m_travel.attribute.attribute_roomkey import RoomKey
from uc3m_travel.hotel_management_config import JSON_FILES_PATH
class HotelDeparture:
    def __init__(self,room_key,departure_date_timestamp):
        self.__room_key = RoomKey(room_key).value
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

    @classmethod
    def create_guest_check_out(cls, room_key):
        room_key = RoomKey(room_key).value
        checkout = StoreCheckout()
        # check thawt the roomkey is stored in the checkins file
        file_store = JSON_FILES_PATH + "store_check_in.json"
        room_key_list = HotelStay.load_checkin_store(file_store)
        # comprobar que esa room_key es la que me han dado
        departure_date_timestamp = HotelStay.find_checkin(room_key, room_key_list)
        departure = HotelDeparture(room_key, departure_date_timestamp)
        departure.is_today_departure(departure_date_timestamp)
        return checkout, departure
