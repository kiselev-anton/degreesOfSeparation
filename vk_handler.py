import vk

session = vk.AuthSession(
    app_id=5648449,
    user_login='XXX',
    user_password='XXX')
# session = vk.Session()
vkapi = vk.API(session, lang='ru')


cache = {}


def get_friends_uids(uid):
    # caches the result
    if uid in cache:
        print("From cache:" + str(cache[uid]))
        return cache[uid]
    else:
        try:
            # result = set(vkapi.friends.get(uid=uid, order='name', fields='last_name'))
            for user in vkapi.friends.get(uid=uid, order='hints', fields='last_name'):
                try:
                    print (user)
                except:
                    continue
            exit()
        except Exception as ex:
            print (ex)
            result = set()
        cache[uid] = result
        # print("New:" + str(result))
        return result
