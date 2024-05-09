from random import randint
import unittest
from datetime import datetime, time, timedelta
from unittest.mock import patch
from castom_time_utils import get_next_active_period_start, is_active_time, get_sleep_time, active_periods, active_sleep_time_min, active_sleep_time_max, inactive_sleep_time_min, inactive_sleep_time_max
from unittest import mock

class TestActiveTimeFunctions(unittest.TestCase):

    def test_get_next_active_period_start(self):
        # Тестирование функции get_next_active_period_start
        datetime_now = datetime(2021, 1, 1, 7, 30)  # Например, 7:30 утра
        expected_next_active_start = time(8, 0)  # Ожидаемое время начала следующего активного периода
        with mock.patch('castom_time_utils.datetime') as mock_datetime:
            mock_datetime.now.return_value = datetime_now
            self.assertEqual(get_next_active_period_start(), expected_next_active_start)

    def test_is_active_time(self):
        # Тестирование функции is_active_time
        active_time = datetime(2021, 1, 1, 9, 0)  # Например, 9:00 утра, активный период
        non_active_time = datetime(2021, 1, 1, 11, 0)  # Например, 11:00 утра, неактивный период
        with mock.patch('castom_time_utils.datetime') as mock_datetime:
            mock_datetime.now.return_value = active_time
            self.assertTrue(is_active_time())
            mock_datetime.now.return_value = non_active_time
            self.assertFalse(is_active_time())

    def test_get_sleep_time(self):
        # Тестирование функции get_sleep_time
        with mock.patch('castom_time_utils.is_active_time') as mock_is_active_time:
            mock_is_active_time.return_value = True
            sleep_time = get_sleep_time()
            self.assertTrue(active_sleep_time_min <= sleep_time <= active_sleep_time_max)  # Проверка для активного периода
            mock_is_active_time.return_value = False
            sleep_time = get_sleep_time()
            self.assertTrue(0 <= sleep_time <= 1800)  # Проверка для неактивного периода
    


    def test_get_next_active_period_start_end_of_day(self):
        datetime_now = datetime(2021, 1, 1, 23, 59)  # Время перед полуночью
        expected_next_active_start = time(8, 0)  # Начало первого активного периода следующего дня
        with patch('castom_time_utils.datetime') as mock_datetime:
            mock_datetime.now.return_value = datetime_now
            self.assertEqual(get_next_active_period_start(), expected_next_active_start)


    def test_get_next_active_period_start_early_morning(self):
        # Проверка возвращаемого времени начала активного периода рано утром
        datetime_now = datetime(2021, 1, 1, 0, 10)
        expected_next_active_start = time(8, 0)
        with patch('castom_time_utils.datetime') as mock_datetime:
            mock_datetime.now.return_value = datetime_now
            self.assertEqual(get_next_active_period_start(), expected_next_active_start)

    def test_get_sleep_time_during_active_period(self):
        # Проверка времени сна во время активного периода
        datetime_now = datetime(2021, 1, 1, 9, 30)  # В середине активного периода
        with patch('castom_time_utils.datetime') as mock_datetime:
            mock_datetime.now.return_value = datetime_now
            sleep_time = get_sleep_time()
            self.assertTrue(active_sleep_time_min <= sleep_time <= active_sleep_time_max)

    def test_get_sleep_time_long_wait_before_active_period(self):
        # Проверка длительности времени сна, когда до следующего активного периода долго
        datetime_now = datetime(2021, 1, 1, 11, 30)
        with patch('castom_time_utils.datetime') as mock_datetime:
            mock_datetime.now.return_value = datetime_now
            sleep_time = get_sleep_time()
            self.assertTrue(1800 <= sleep_time <= 3600)  # 30 минут до 1 часа

    def test_get_sleep_time_randomness(self):
        datetime_now = datetime(2021, 1, 1, 11, 30)
        # В этом тесте будем симулировать более длительное время между вызовами функции get_sleep_time,
        # чтобы дать больше пространства для случайности.
        sleep_times = []
        with patch('castom_time_utils.datetime') as mock_datetime:
            mock_datetime.now.return_value = datetime_now
            for _ in range(100):  # Увеличим число выборок до 100
                sleep_times.append(get_sleep_time())
                # Имитация увеличения текущего времени
                mock_datetime.now.return_value += timedelta(seconds=randint(0, 1800))
            
            # Проверим, что есть хотя бы некоторое количество уникальных времен сна
            unique_sleep_times = set(sleep_times)
            self.assertTrue(len(unique_sleep_times) > 1, f"Not enough randomness in sleep times: {unique_sleep_times}")


    # Тесты для функции get_sleep_time с использованием переменных

    def test_get_sleep_time_active_sleep_time_edge_case(self):
        # Проверяем случай, когда до начала активного периода осталось меньше или равно времени неактивного сна
        start_time = active_periods[0][0]
        edge_case_time = datetime.combine(datetime.today(), start_time) - timedelta(seconds=inactive_sleep_time_min)
        with patch('castom_time_utils.datetime') as mock_datetime:
            mock_datetime.now.return_value = edge_case_time
            sleep_time = get_sleep_time()
            # Проверяем, что время сна в этом случае равно оставшемуся времени плюс случайное от active_sleep_time_min до active_sleep_time_max
            self.assertTrue(inactive_sleep_time_min + active_sleep_time_min <= sleep_time <= inactive_sleep_time_min + active_sleep_time_max)

    def test_get_sleep_time_inactive_sleep_time_edge_case(self):
        # Проверяем случай, когда до начала активного периода осталось больше времени неактивного сна, но меньше inactive_sleep_time_max минут
        start_time = active_periods[1][0]
        edge_case_time = datetime.combine(datetime.today(), start_time) - timedelta(seconds=(inactive_sleep_time_min + inactive_sleep_time_max) // 2)
        with patch('castom_time_utils.datetime') as mock_datetime:
            mock_datetime.now.return_value = edge_case_time
            sleep_time = get_sleep_time()
            # Проверяем, что время сна случайно между inactive_sleep_time_min и (inactive_sleep_time_min + inactive_sleep_time_max) // 2
            self.assertTrue(inactive_sleep_time_min <= sleep_time <= (inactive_sleep_time_min + inactive_sleep_time_max) // 2)

    def test_get_sleep_time_inactive_sleep_time_max_case(self):
        # Проверяем случай, когда до начала активного периода осталось больше inactive_sleep_time_max минут
        start_time = active_periods[2][0]
        edge_case_time = datetime.combine(datetime.today(), start_time) - timedelta(seconds=inactive_sleep_time_max + 100)
        with patch('castom_time_utils.datetime') as mock_datetime:
            mock_datetime.now.return_value = edge_case_time
            sleep_time = get_sleep_time()
            # Проверяем, что время сна случайно между inactive_sleep_time_min и inactive_sleep_time_max
            self.assertTrue(inactive_sleep_time_min <= sleep_time <= inactive_sleep_time_max)


    def test_get_sleep_time_not_active_near_active_period(self):
        with mock.patch('castom_time_utils.datetime') as mock_datetime:
            mock_datetime.now.return_value = datetime(2021, 1, 1, 12, 58)
            sleep_time = get_sleep_time()
            # Проверяем, что время сна соответствует ожидаемому
            self.assertTrue(120 <= sleep_time <= inactive_sleep_time_min + active_sleep_time_max)

    def test_get_sleep_time_active_period_starting_soon(self):
        # Проверка времени сна, когда начало активного периода скоро
        datetime_now = datetime(2021, 1, 1, 7, 58)
        with patch('castom_time_utils.datetime') as mock_datetime:
            mock_datetime.now.return_value = datetime_now
            sleep_time = get_sleep_time()
            self.assertTrue(120 <= sleep_time <= inactive_sleep_time_min + active_sleep_time_max)

    def test_get_sleep_time(self):
        # Тестирование функции get_sleep_time
        with mock.patch('castom_time_utils.is_active_time') as mock_is_active_time:
            mock_is_active_time.return_value = True
            sleep_time = get_sleep_time()
            self.assertTrue(active_sleep_time_min <= sleep_time <= active_sleep_time_max)
            mock_is_active_time.return_value = False
            sleep_time = get_sleep_time()
            self.assertTrue(inactive_sleep_time_min <= sleep_time <= inactive_sleep_time_max)


# Остальной код...


if __name__ == '__main__':
    unittest.main()
