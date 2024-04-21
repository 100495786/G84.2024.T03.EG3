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

class HotelManager:
    """Class with all the methods for managing reservations and stays"""
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

        self.save_reservation(my_reservation)

        return my_reservation.localizer

    def save_reservation(self, my_reservation):
        # escribo el fichero Json con todos los datos
        reserva = StoreReservation()
        # leo los datos del fichero si existe , y si no existe creo una lista vacia
        reserva.load_json_store()
        # compruebo que esta reserva no esta en la lista
        reserva.find_item_in_store(my_reservation.localizer, "_HotelReservation__localizer", my_reservation.id_card,
                                   "_HotelReservation__id_card")
        # añado los datos de mi reserva a la lista , a lo que hubiera
        reserva.add_item_in_store(my_reservation)
        # escribo la lista en el fichero
        reserva.save_store()

    def guest_arrival(self, file_input:str)->str:
        """manages the arrival of a guest with a reservation"""
        llegada, my_checkin = self.create_guest_arrival_from_file(file_input)

        #Ahora lo guardo en el almacen nuevo de checkin
        # escribo el fichero Json con todos los datos

        # leo los datos del fichero si existe , y si no existe creo una lista vacia
        llegada.load_json_store()

        # comprobar que no he hecho otro ckeckin antes
        llegada.find_checkin(my_checkin)

        #añado los datos de mi reserva a la lista , a lo que hubiera
        llegada.add_item_in_store(my_checkin)
        llegada.save_store()

        return my_checkin.room_key

    def create_guest_arrival_from_file(self, file_input):
        llegada = StoreArrival()
        input_list = llegada.read_input_file(file_input)
        # comprobar valores del fichero
        my_id_card, my_localizer = llegada.read_input_data_from_file(input_list)
        new_reservation = llegada.create_reservation_from_arrival(my_id_card, my_localizer)
        # compruebo si hoy es la fecha de checkin
        reservation_format = "%d/%m/%Y"
        date_obj = datetime.strptime(new_reservation.arrival, reservation_format)
        if date_obj.date() != datetime.date(datetime.utcnow()):
            raise HotelManagementException("Error: today is not reservation date")
        # genero la room key para ello llamo a Hotel Stay
        my_checkin = HotelStay(idcard=my_id_card, numdays=int(new_reservation.num_days),
                               localizer=my_localizer, roomtype=new_reservation.room_type)
        return llegada, my_checkin

    def guest_checkout(self, room_key:str)->bool:
        """manages the checkout of a guest"""
        RoomKey(room_key).value
        #check thawt the roomkey is stored in the checkins file
        file_store = JSON_FILES_PATH + "store_check_in.json"
        try:
            with open(file_store, "r", encoding="utf-8", newline="") as file:
                room_key_list = json.load(file)
        except FileNotFoundError as ex:
            raise HotelManagementException("Error: store checkin not found") from ex
        except json.JSONDecodeError as ex:
            raise HotelManagementException("JSON Decode Error - Wrong JSON Format") from ex

        # comprobar que esa room_key es la que me han dado
        found = False
        for item in room_key_list:
            if room_key == item["_HotelStay__room_key"]:
                departure_date_timestamp = item["_HotelStay__departure"]
                found = True
        if not found:
            raise HotelManagementException ("Error: room key not found")

        today = datetime.utcnow().date()
        if datetime.fromtimestamp(departure_date_timestamp).date() != today:
            raise HotelManagementException("Error: today is not the departure day")

        file_store_checkout = JSON_FILES_PATH + "store_check_out.json"
        try:
            with open(file_store_checkout, "r", encoding="utf-8", newline="") as file:
                room_key_list = json.load(file)
        except FileNotFoundError as ex:
            room_key_list = []
        except json.JSONDecodeError as ex:
            raise HotelManagementException("JSON Decode Error - Wrong JSON Format") from ex

        for checkout in room_key_list:
            if checkout["room_key"] == room_key:
                raise HotelManagementException("Guest is already out")

        room_checkout={"room_key":  room_key, "checkout_time":datetime.timestamp(datetime.utcnow())}

        room_key_list.append(room_checkout)

        try:
            with open(file_store_checkout, "w", encoding="utf-8", newline="") as file:
                json.dump(room_key_list, file, indent=2)
        except FileNotFoundError as ex:
            raise HotelManagementException("Wrong file  or file path") from ex

        return True
