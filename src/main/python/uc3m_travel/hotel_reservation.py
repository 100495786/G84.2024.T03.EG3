"""Hotel reservation class"""
import hashlib
from datetime import datetime
from uc3m_travel.attribute.attribute_name_surname import NameSurname
from uc3m_travel.attribute.attribute_id_card import IdCard
from uc3m_travel.attribute.attribute_phone_number import PhoneNumber
from uc3m_travel.attribute.attribute_arrival import Arrival
from uc3m_travel.attribute.attribute_credit_card import CreditCard
from uc3m_travel.attribute.attribute_room_type import RoomType
from uc3m_travel.attribute.attribute_num_days import NumDays
from uc3m_travel.storage.store_reservation import StoreReservation

class HotelReservation:
    """Class for representing hotel reservations"""
    #pylint: disable=too-many-arguments, too-many-instance-attributes
    def __init__(self,
                 id_card:str,
                 credit_card_number:str,
                 name_surname:str,
                 phone_number:str,
                 room_type:str,
                 arrival:str,
                 num_days:int):
        """constructor of reservation objects"""
        self.__credit_card_number = CreditCard(credit_card_number).value
        self.__id_card = IdCard(id_card).value
        justnow = datetime.utcnow()
        self.__arrival = Arrival(arrival).value
        self.__reservation_date = datetime.timestamp(justnow)
        self.__name_surname = NameSurname(name_surname).value
        self.__phone_number = PhoneNumber(phone_number).value
        self.__room_type = RoomType(room_type).value
        self.__num_days = NumDays(num_days).value
        self.__localizer = hashlib.md5(str(self).encode()).hexdigest()
    def __str__(self):
        """return a json string with the elements required to calculate the localizer"""
        #VERY IMPORTANT: JSON KEYS CANNOT BE RENAMED
        json_info = {"id_card": self.__id_card,
                     "name_surname": self.__name_surname,
                     "credit_card": self.__credit_card_number,
                     "phone_number:": self.__phone_number,
                     "reservation_date": self.__reservation_date,
                     "arrival_date": self.__arrival,
                     "num_days": self.__num_days,
                     "room_type": self.__room_type,
                     }
        return "HotelReservation:" + json_info.__str__()
    @property
    def credit_card(self):
        """property for getting and setting the credit_card number"""
        return self.__credit_card_number
    @credit_card.setter
    def credit_card(self, value):
        self.__credit_card_number = value
    @property
    def id_card(self):
        """property for getting and setting the id_card"""
        return self.__id_card
    @id_card.setter
    def id_card(self, value):
        self.__id_card = value
    @property
    def localizer(self):
        """Returns the md5 signature"""
        return self.__localizer
    @property
    def arrival(self):
        return self.__arrival
    @property
    def num_days(self):
        return self.__num_days
    @property
    def room_type(self):
        return self.__room_type

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
