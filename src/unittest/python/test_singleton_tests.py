import unittest
from uc3m_travel import HotelManager
from uc3m_travel.storage.store_reservation import StoreReservation
from uc3m_travel.storage.store_arrival import StoreArrival
from uc3m_travel.storage.store_checkout import StoreCheckout

class MyTestCase(unittest.TestCase):
    def test_singleton1(self):
        primera_instancia = StoreReservation()
        segunda_instancia = StoreReservation()
        tercera_instancia = StoreReservation()
        self.assertEqual(primera_instancia, segunda_instancia)
        self.assertEqual(segunda_instancia, tercera_instancia)
        self.assertEqual(tercera_instancia, primera_instancia)


    def test_singleton2(self):
        primera_instancia = StoreArrival()
        segunda_instancia = StoreArrival()
        tercera_instancia = StoreArrival()
        self.assertEqual(primera_instancia, segunda_instancia)
        self.assertEqual(segunda_instancia, tercera_instancia)
        self.assertEqual(tercera_instancia, primera_instancia)

    def test_singleton3(self):
        primera_instancia = StoreCheckout()
        segunda_instancia = StoreCheckout()
        tercera_instancia = StoreCheckout()
        self.assertEqual(primera_instancia, segunda_instancia)
        self.assertEqual(segunda_instancia, tercera_instancia)
        self.assertEqual(tercera_instancia, primera_instancia)

if __name__ == '__main__':
    unittest.main()