from uc3m_travel.storage.json_store import JsonStore
from uc3m_travel.hotel_management_config import JSON_FILES_PATH
from uc3m_travel.hotel_management_exception import HotelManagementException
from uc3m_travel.attribute.attribute_id_card import IdCard
from uc3m_travel.attribute.attribute_localizer import Localizer
from uc3m_travel.hotel_reservation import HotelReservation
from datetime import datetime
from freezegun import freeze_time
import json
class StoreArrival(JsonStore):
    def __init__(self):
        self._file_name= JSON_FILES_PATH + "store_check_in.json"
        self._data_list = []

    def create_reservation_from_arrival(self, my_id_card, my_localizer):
        # Validamos IdCard
        IdCard(my_id_card).value
        # Validamos Localizer
        Localizer(my_localizer).value
        # buscar en almacen
        file_store = JSON_FILES_PATH + "store_reservation.json"
        # leo los datos del fichero , si no existe deber dar error porque el almacen de reservaa
        # debe existir para hacer el checkin
        store_list = self.load_reservation_store(file_store)
        # compruebo si esa reserva esta en el almacen
        reservation = self.find_reservation(my_localizer, store_list)
        if my_id_card != reservation["_HotelReservation__id_card"]:
            raise HotelManagementException("Error: Localizer is not correct for this IdCard")
        # regenrar clave y ver si coincide
        reservation_date = datetime.fromtimestamp(reservation["_HotelReservation__reservation_date"])
        with freeze_time(reservation_date):
            new_reservation = HotelReservation(credit_card_number=reservation["_HotelReservation__credit_card_number"],
                                               id_card=reservation["_HotelReservation__id_card"],
                                               num_days=reservation["_HotelReservation__num_days"],
                                               room_type=reservation["_HotelReservation__room_type"],
                                               arrival=reservation["_HotelReservation__arrival"],
                                               name_surname=reservation["_HotelReservation__name_surname"],
                                               phone_number=reservation["_HotelReservation__phone_number"])
        if new_reservation.localizer != my_localizer:
            raise HotelManagementException("Error: reservation has been manipulated")
        return new_reservation
    def find_reservation(self, my_localizer, store_list):
        for item in store_list:
            if my_localizer == item["_HotelReservation__localizer"]:
                return item
        raise HotelManagementException("Error: localizer not found")

    def read_input_data_from_file(self, input_list):
        try:
            my_localizer = input_list["Localizer"]
            my_id_card = input_list["IdCard"]
        except KeyError as e:
            raise HotelManagementException("Error - Invalid Key in JSON") from e
        return my_id_card, my_localizer
    def read_input_file(self, file_input):
        try:
            with open(file_input, "r", encoding="utf-8", newline="") as file:
                input_list = json.load(file)
        except FileNotFoundError as ex:
            raise HotelManagementException("Error: file input not found") from ex
        except json.JSONDecodeError as ex:
            raise HotelManagementException("JSON Decode Error - Wrong JSON Format") from ex
        return input_list