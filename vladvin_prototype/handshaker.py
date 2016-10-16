class Handshaker:
    def __init__(self):
        self._vk_requester = VkRequester()

    def calc_number_of_handshakes(self, user_ids):
        handshakes = dict()
        search_set = user_ids
        number_of_hands = 0
        while (number_of_hands <= 5) and (not self._is_handshake_full(handshakes, user_ids)):
            number_of_hands += 1
            tmp_search_set = []
            for tmp_ss in self._vk_requester.retrieve_friends_using_vk_execute(search_set):
                tmp_search_set.extend(tmp_ss)
            
            for user_id in user_ids:
                if (user_id not in handshakes) and (user_id in tmp_search_set):
                    handshakes[user_id] = number_of_hands
            search_set = tmp_search_set
            print(handshakes)

        return handshakes

    def _is_handshake_full(self, handshakes, user_ids):
        return all(user_id in handshakes for user_id in user_ids)
