import vk

session = vk.Session()
vkapi = vk.API(session, lang='ru')


cache = {}


def get_friends_uids(uid):
    # caches the result
    if uid in cache:
        print("From cache:" + str(cache[uid]))
        return cache[uid]
    else:
        try:
            result = set(vkapi.friends.get(uid=uid))
        except:
            result = set()
        cache[uid] = result
        # print("New:" + str(result))
        return result
