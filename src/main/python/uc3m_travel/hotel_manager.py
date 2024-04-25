"""Module for the hotel manager"""
import json
from datetime import datetime
from uc3m_travel.hotel_management_exception import HotelManagementException
from uc3m_travel.hotel_reservation import HotelReservation
from uc3m_travel.hotel_stay import HotelStay
from uc3m_travel.hotel_management_config import JSON_FILES_PATH
from freezegun import freeze_time
from uc3m_travel.storage.store_reservation import StoreReservation
from uc3m_travel.attribute.attribute_id_card import IdCard
from uc3m_travel.attribute.attribute_credit_card import CreditCard
from uc3m_travel.attribute.attribute_localizer import Localizer
from uc3m_travel.attribute.attribute_roomkey import RoomKey
from uc3m_travel.storage.store_arrival import StoreArrival
from uc3m_travel.storage.store_checkout import StoreCheckout
from uc3m_travel.hotel_departure import HotelDeparture

class HotelManager:
    """Class with all the methods for managing reservations and stays"""
    class __HotelManager():
        def __init__(self):
            pass
        def read_data_from_json(self, fi):
            """reads the content of a json file with two fields: CreditCard and phoneNumber"""
            try:
                with open(fi, encoding='utf-8') as f:
                    json_data = json.load(f)
            except FileNotFoundError as e:
                raise HotelManagementException("Wrong file or file path") from e
            except json.JSONDecodeError as e:
                raise HotelManagementException("JSON Decode Error - Wrong JSON Format") from e
            try:
                c = json_data["CreditCard"]
                p = json_data["phoneNumber"]
                req = HotelReservation(id_card="12345678Z",
                                       credit_card_number=c,
                                       name_surname="John Doe",
                                       phone_number=p,
                                       room_type="single",
                                       num_days=3,
                                       arrival="20/01/2024")
            except KeyError as e:
                raise HotelManagementException("JSON Decode Error - Invalid JSON Key") from e
            if not CreditCard(c).value:
                raise HotelManagementException("Invalid credit card number")
            # Close the file
            return req

        # pylint: disable=too-many-arguments
        def room_reservation(self,
                             credit_card:str,
                             name_surname:str,
                             id_card:str,
                             phone_number:str,
                             room_type:str,
                             arrival_date: str,
                             num_days:int)->str:
            """manges the hotel reservation: creates a reservation and saves it into a json file"""

            my_reservation = HotelReservation(id_card=id_card,
                                              credit_card_number=credit_card,
                                              name_surname=name_surname,
                                              phone_number=phone_number,
                                              room_type=room_type,
                                              arrival=arrival_date,
                                              num_days=num_days)

            my_reservation.save_reservation(my_reservation)

            return my_reservation.localizer

        def guest_arrival(self, file_input: str) -> str:
            """manages the arrival of a guest with a reservation"""
            llegada = StoreArrival()
            input_list = llegada.read_input_file(file_input)
            # comprobar valores del fichero
            my_id_card, my_localizer = llegada.read_input_data_from_file(input_list)
            new_reservation = llegada.create_reservation_from_arrival(my_id_card, my_localizer)
            my_checkin = HotelStay(idcard=my_id_card, numdays=int(new_reservation.num_days),
                                   localizer=my_localizer, roomtype=new_reservation.room_type)
            my_checkin.create_guest_arrival_from_file(new_reservation, my_id_card, my_localizer)
            my_checkin.save_arrival(my_checkin)

            return my_checkin.room_key



        def guest_checkout(self, room_key:str)->bool:
            """manages the checkout of a guest"""
            RoomKey(room_key).value
            checkout = StoreCheckout()
            #check thawt the roomkey is stored in the checkins file
            file_store = JSON_FILES_PATH + "store_check_in.json"

            room_key_list = checkout.load_checkin_store(file_store)

            # comprobar que esa room_key es la que me han dado
            departure_date_timestamp = checkout.find_checkin(room_key, room_key_list)
            departure = HotelDeparture(room_key,departure_date_timestamp)
            departure.is_today_departure(departure_date_timestamp)

            self.safe_checkout(checkout, room_key)

            return True

        def safe_checkout(self, checkout, room_key):
            room_key_list = checkout.load_json_store()
            checkout.find_checkout(room_key, room_key_list)
            room_checkout = checkout.create_checkout(room_key)
            checkout.add_checkout_store(room_checkout)
            checkout.save_store()

    __instance = None
    def __new__(cls):
        if not HotelManager.__instance:
            HotelManager.__instance = HotelManager.__HotelManager()
        return HotelManager.__instance











