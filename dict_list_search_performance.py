"""
This module defines two classes: DictData and ListData, both inheriting from the BaseData abstract base class.
These classes are used to generate data (dictionary or list) and measure the time taken to find elements within these data structures.
This module can be used to compare the performance differences between different data structures (list and dictionary) in terms of search operations.
"""
import logging
import random
import time
from abc import ABCMeta, abstractmethod
from typing import Dict, List, NoReturn, Tuple

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter("%(filename)s:%(lineno)d | %(name)s | %(asctime)s | %(levelname)s >>> %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


class BaseData(metaclass=ABCMeta):
    """Base class for generating data."""

    @abstractmethod
    def generate_data(self, sample_size: int, extraction_number: int) -> Tuple[Dict[str, int], List[int]]:
        pass

    def __measure_search_performance(
        self,
        sample_size: int = 10000,
        extraction_number: int = 1000,
        test_times: int = 100,
    ) -> NoReturn:
        """Test the time it takes to find elements in a list or dictionary."""
        all_data, target_data = self.generate_data(sample_size, extraction_number)
        total_times = 0
        for _ in range(test_times):
            find = 0
            start = time.process_time()
            for data in target_data:
                if data in all_data:
                    find += 1
            end = time.process_time()
            last_time = end - start
            total_times += last_time
        logger.info(f"Type: {all_data.__class__.__name__}, Duration: {round((total_times / test_times)*1000,4)} ms")

    def __call__(self, *args, **kwargs):
        self.__measure_search_performance(*args, **kwargs)


class DictData(BaseData):
    """Generate a dictionary and a list of keys from the dictionary."""

    def generate_data(self, sample_size: int, extraction_number: int) -> Tuple[Dict[str, int], List[int]]:
        """Generate a dictionary and a list of keys from the dictionary.

        @random_dict: A dictionary with keys generated from a random sample of numbers and values set to 0.
            {641309888: 0, 5511636672: 0, 200904104: 0, ...}
        @target_data: A list of keys randomly sampled from the dictionary.
            [5511636672, 641309888, ...]
        """
        random_dict = {i: 0 for i in random.sample(range(int(1e10)), k=sample_size)}
        target_data = [item[0] for item in random.sample(list(random_dict.items()), extraction_number)]
        return random_dict, target_data


class ListData(BaseData):
    """Generate a list of numbers and a sublist from the list."""

    def generate_data(self, sample_size: int, extraction_number: int) -> Tuple[List[int], List[int]]:
        """Generate a list of numbers and a sublist from the list.

        @random_list: A list of numbers generated from a random sample.
            [1775799008, 7306224622, 6431460572, ...]
        @target_data: A sublist randomly sampled from the list.
            [7306224622, 6431460572, ...]
        """
        random_list = random.sample(range(int(1e10)), k=sample_size)
        target_data = random.sample(random_list, extraction_number)
        return random_list, target_data


if __name__ == "__main__":
    dict_data = DictData()
    dict_data(sample_size=10000, extraction_number=1000, test_times=100)

    list_data = ListData()
    list_data(sample_size=10000, extraction_number=1000, test_times=100)
