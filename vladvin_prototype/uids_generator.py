import random

class UserIdsGenerator:
    def __init__(self, left_bound, right_bound):
        self.__left_bound = left_bound
        self.__right_bound = right_bound

    def generate_user_ids(self, count):
        if (count <= 0):
            return

        user_id_list = []
        for i in xrange(count):
            a = ((self.__right_bound - self.__left_bound + 1) / count) * i + self.__left_bound
            b = ((self.__right_bound - self.__left_bound + 1) / count) * (i + 1) + self.__left_bound - 1
            user_id_list.append(random.randint(a, b))

        return user_id_list