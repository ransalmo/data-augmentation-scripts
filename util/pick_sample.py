import random


def pick_sample_files_from_directory(file_list: list, percentage: int):
    cant_elements_to_pick: int = (len(file_list) * percentage) // 100
    return random.sample(file_list, cant_elements_to_pick)
