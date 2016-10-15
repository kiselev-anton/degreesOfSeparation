from vk_handler import get_friends_uids
from functools import reduce
import multiprocessing

# pool = multiprocessing.Pool(processes=1)

def union(left, right):
    return left.union(right)


def get_degree_of_separation(uid_left, uid_right):
    checked_uids = set()
    uids_to_search = set(get_friends_uids(uid_left))
    current_separation_degree = 1
    while True:
        if uid_right in uids_to_search:
            return current_separation_degree
        else:
            current_separation_degree += 1
            print("Separation >= " + str(current_separation_degree))
            checked_uids.update(set(uids_to_search))
            uids_to_search.update(set(
                reduce(union, map(get_friends_uids, uids_to_search))))
            # uids_to_search = reduce(union, get_friends_uids(uids_to_search))
                                    # pool.map(get_friends_uids, uids_to_search))


if __name__ == '__main__':
    get_friends_uids(1)
    # print(get_degree_of_separation(19299070, 95073191))
