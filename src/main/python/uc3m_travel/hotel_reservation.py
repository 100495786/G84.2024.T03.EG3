"""Hotel reservation class"""
import hashlib
from datetime import datetime
import re
from uc3m_travel.hotel_management_exception import HotelManagementException

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
        self.__credit_card_number = self.validatecreditcard(credit_card_number)
        self.__id_card = self.validate_idcard(id_card)
        justnow = datetime.utcnow()
        self.__arrival = self.validate_arrival_date(arrival)
        self.__reservation_date = datetime.timestamp(justnow)
        self.__name_surname = self.validate_name_surname(name_surname)
        self.__phone_number = self.validate_phonenumber(phone_number)
        self.__room_type = self.validate_room_type(room_type)
        self.__num_days = self.validate_numdays(num_days)
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

    def validatecreditcard(self, credit_card):
        """validates the credit card number using luhn altorithm"""
        # taken form
        # https://allwin-raju-12.medium.com/
        # credit-card-number-validation-using-luhns-algorithm-in-python-c0ed2fac6234
        # PLEASE INCLUDE HERE THE CODE FOR VALIDATING THE GUID
        # RETURN TRUE IF THE GUID IS RIGHT, OR FALSE IN OTHER CASE

        myregex = re.compile(r"^[0-9]{16}")
        res = myregex.fullmatch(credit_card)
        if not res:
            raise HotelManagementException("Invalid credit card format")

        def digits_of(n):
            return [int(d) for d in str(n)]

        digits = digits_of(credit_card)
        odd_digits = digits[-1::-2]
        even_digits = digits[-2::-2]
        checksum = 0
        checksum += sum(odd_digits)
        for d in even_digits:
            checksum += sum(digits_of(d * 2))
        if not checksum % 10 == 0:
            raise HotelManagementException("Invalid credit card number (not luhn)")
        return credit_card
    def validate_room_type(self, room_type):
        """validates the room type value using regex"""
        myregex = re.compile(r"(SINGLE|DOUBLE|SUITE)")
        res = myregex.fullmatch(room_type)
        if not res:
            raise HotelManagementException("Invalid roomtype value")
        return room_type
    def validate_arrival_date(self, arrival_date):
        """validates the arrival date format  using regex"""
        myregex = re.compile(r"^(([0-2]\d|-3[0-1])\/(0\d|1[0-2])\/\d\d\d\d)$")
        resultado = myregex.fullmatch(arrival_date)
        if not resultado:
            raise HotelManagementException("Invalid date format")
        return arrival_date
    def validate_phonenumber(self, phone_number):
        """validates the phone number format  using regex"""
        myregex = re.compile(r"^(\+)[0-9]{9}")
        resultado = myregex.fullmatch(phone_number)
        if not resultado:
            raise HotelManagementException("Invalid phone number format")
        return phone_number
    def validate_numdays(self,num_days):
        """validates the number of days"""
        try:
            days = int(num_days)
        except ValueError as ex:
            raise HotelManagementException("Invalid num_days datatype") from ex
        if (days < 1 or days > 10):
            raise HotelManagementException("Numdays should be in the range 1-10")
        return num_days
    def validate_name_surname(self, name_surname):
        expresionRegular = r"^(?=^.{10,50}$)([a-zA-Z]+(\s[a-zA-Z]+)+)$"
        myregex = re.compile(expresionRegular)
        regex_matches = myregex.fullmatch(name_surname)
        if not regex_matches:
            raise HotelManagementException("Invalid name format")
        return name_surname
    def validate_idcard(self, id_card):
        expresionRegular = r'^[0-9]{8}[A-Z]{1}$'
        my_regex = re.compile(expresionRegular)
        if not my_regex.fullmatch(id_card):
            raise HotelManagementException("Invalid IdCard format")
        if not self.validate_dni(id_card):
            raise HotelManagementException("Invalid IdCard letter")
        return id_card
    @staticmethod#Método que no tiene self
    def validate_dni( dni ):
        """RETURN TRUE IF THE DNI IS RIGHT, OR FALSE IN OTHER CASE"""
        diccionarioLetras = {"0": "T", "1": "R", "2": "W", "3": "A", "4": "G", "5": "M",
             "6": "Y", "7": "F", "8": "P", "9": "D", "10": "X", "11": "B",
             "12": "N", "13": "J", "14": "Z", "15": "S", "16": "Q", "17": "V",
             "18": "H", "19": "L", "20": "C", "21": "K", "22": "E"}
        numeros = int(dni[ 0:8 ])
        resto = str(numeros % 23)
        return dni[8] == diccionarioLetras[resto]