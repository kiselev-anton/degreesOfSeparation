import random
import urllib
import urllib2
import json

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

class VkRequester:
    def __init__(self):
        self.__api_url = 'https://api.vk.com/method/'
        self.__access_token = 'fb718ae5a7d94dd78a092605939e1eb4a5da033b40b574bdec24c665ef58f3d3ca84533087f8a3a967eb0'

    def retrieve_friends(self, user_id):
        params = dict()
        params['user_id'] = user_id
        response = self.__request('friends.get', params)
        encoded_res = json.loads(response)
        if 'response' in encoded_res:
            return encoded_res['response']
        else:
            return []

    def retrieve_friends_using_vk_execute(self, user_ids):
        # Request example:
        # https://api.vk.com/method/execute?
        # access_token=fb718ae5a7d94dd78a092605939e1eb4a5da033b40b574bdec24c665ef58f3d3ca84533087f8a3a967eb0&
        # code=return [API.friends.get({"user_id":123452}), API.friends.get({"user_id":12343}), API.friends.get({"user_id":282197574})];
        friends = []
        checked_ids_count = 0
        print('Request size: ' + str(len(user_ids)))
        while (checked_ids_count < len(user_ids)):
            i = 0
            code = 'return ['
            while (i in xrange(0, 25)) and (checked_ids_count < len(user_ids)):
                code += 'API.friends.get({{"user_id":{0}}}),'.format(str(user_ids[checked_ids_count]))
                checked_ids_count += 1
                i += 1
            code = code[:-1]
            code += '];'

            params = dict()
            params['code'] = code
            params['access_token'] = self.__access_token
            response = self.__request('execute', params)
            encoded_res = json.loads(response)
            if 'response' in encoded_res:
                for friend_list in encoded_res['response']:
                    if type(friend_list) is list:
                        friends.extend(friend_list)
        return friends

    def __request(self, method_name, params):
        params_str = urllib.urlencode(params)
        full_url = self.__api_url + method_name + '?' + params_str
        return urllib2.urlopen(full_url).read()

class Handshaker:
    def __init__(self):
        self.__vk_requester = VkRequester()

    def calc_number_of_handshakes(self, user_ids):
        handshakes = dict()
        search_set = user_ids
        number_of_hands = 0
        while (number_of_hands <= 5) and (not self.__is_handshake_full(handshakes, user_ids)):
            number_of_hands += 1
            tmp_search_set = self.__vk_requester.retrieve_friends_using_vk_execute(search_set)
            for user_id in user_ids:
                if (user_id not in handshakes) and (user_id in tmp_search_set):
                    handshakes[user_id] = number_of_hands
            search_set = tmp_search_set
            print(handshakes)

        return handshakes

    def __is_handshake_full(self, handshakes, user_ids):
        return all(user_id in handshakes for user_id in user_ids)

if __name__ == "__main__":
    id_generator = UserIdsGenerator(1, 100 * 1000 * 1000)
    user_id_list = id_generator.generate_user_ids(10)

    handshaker = Handshaker()
    handshakes = handshaker.calc_number_of_handshakes(user_id_list)

    # How many handshakes between me and Pavel Durov?
    # handshakes = handshaker.calc_number_of_handshakes([67815572, 1])
    # This example doesn't work correctly!!! So, the problem is in the algorithm.

    # Some user id examples:
    # 123452 - 6 friends
    # 282197574 - 41 freinds
    # 12343 - deleted user
