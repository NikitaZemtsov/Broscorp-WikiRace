import unittest

from wikiracing import WikiRacer


class WikiRacerTest(unittest.TestCase):

    """
    The main problem that these tests depend on an internet connection.
    In order for the test to always pass, you need to Mock wikipedia.page to return correct data always
    and make test DB
    """

    def test_1(self):
        racer = WikiRacer()
        path = racer.find_path('Дружба', 'Рим')
        self.assertEqual(path, ['Дружба', 'Якопо Понтормо', 'Рим'])

    def test_2(self):
        racer = WikiRacer()
        path = racer.find_path('Мітохондріальна ДНК', 'Вітамін K')
        self.assertEqual(path, ['Мітохондріальна ДНК', 'Бактерії', 'Вітамін K'])

    def test_3(self):
        racer = WikiRacer()
        path = racer.find_path('Марка (грошова одиниця)', 'Китайський календар')
        self.assertEqual(path, ['Марка (грошова одиниця)', '1549', 'Китайський календар'])

    def test_4(self):
        racer = WikiRacer()
        path = racer.find_path('Фестиваль', 'Пілястра')
        self.assertEqual(path, [])

    def test_5(self):
        racer = WikiRacer()
        path = racer.find_path('Дружина (військо)', '6 жовтня')
        self.assertEqual(path, ['Дружина (військо)', 'Друга світова війна', '6 жовтня'])


if __name__ == '__main__':
    unittest.main()
