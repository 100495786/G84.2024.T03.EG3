"""Module for the hotel manager"""
import json
from uc3m_travel.hotel_management_exception import HotelManagementException
from uc3m_travel.hotel_reservation import HotelReservation
from uc3m_travel.hotel_stay import HotelStay
from uc3m_travel.attribute.attribute_credit_card import CreditCard
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
            my_checkin = HotelStay.create_guest_arrival_from_file(file_input)

            my_checkin.save_arrival(my_checkin)

            return my_checkin.room_key

        def guest_checkout(self, room_key:str)->bool:
            """manages the checkout of a guest"""
            checkout, departure = HotelDeparture.create_guest_check_out(room_key)

            departure.save_checkout(checkout, room_key)

            return True

    __instance = None
    def __new__(cls):
        if not HotelManager.__instance:
            HotelManager.__instance = HotelManager.__HotelManager()
        return HotelManager.__instance
