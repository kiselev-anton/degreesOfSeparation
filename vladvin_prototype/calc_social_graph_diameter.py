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
