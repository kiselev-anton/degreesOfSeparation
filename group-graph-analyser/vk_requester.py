from urllib.request import urlopen
from urllib.parse import urlencode
import json


class VkRequester:
    def __init__(self):
        self._api_url = 'https://api.vk.com/method/'
        self._access_token = 'fb718ae5a7d94dd78a092605939e1eb4a5da033b40b574bdec24c665ef58f3d3ca84533087f8a3a967eb0'

    def retrieve_friends(self, user_id):
        params = dict()
        params['user_id'] = user_id
        response = self._request('friends.get', params)
        encoded_res = json.loads(response)
        if 'response' in encoded_res:
            return encoded_res['response']
        else:
            return []

    def retrieve_friends_using_vk_execute(self, user_ids):
        # Request example:
        # https://api.vk.com/method/execute?
        # access_token=fb718ae5a7d94dd78a092605939e1eb4a5da033b40b574bdec24c665ef58f3d3ca84533087f8a3a967eb0&
        # code=return [API.friends.get({"user_id":123452}), API.friends.get({"user_id":12343})];
        friends = []
        checked_ids_count = 0
        print('Request size: ' + str(len(user_ids)))
        while checked_ids_count < len(user_ids):
            i = 0
            code = 'return ['
            while (i in range(0, 25)) and (checked_ids_count < len(user_ids)):
                code += 'API.friends.get({{"user_id":{0}}}),'.format(str(user_ids[checked_ids_count]))
                checked_ids_count += 1
                i += 1
            code = code[:-1]
            code += '];'

            params = dict()
            params['code'] = code
            params['access_token'] = self._access_token
            response = self._request('execute', params)
            encoded_res = json.loads(response)
            if 'response' in encoded_res:
                for friend_list in encoded_res['response']:
                    if type(friend_list) is list:
                        friends.append(friend_list)
                    else:
                        friends.append([])
        return friends

    def get_group_members(self, group_name):
        members_ids = []
        offset = 0
        while True:
            members = self._get_group_members_offset(group_name, offset)
            if 'users' in members and len(members['users']) != 0:
                members_ids.extend(members['users'])
                offset = len(members_ids)
            else:
                return members_ids

    def get_group_members_firends(self, group_name):
        friends_graph = dict()
        group_members_ids = self.get_group_members(group_name)
        print('members in group: ', len(group_members_ids))
        for i in range(0, len(group_members_ids), 25):
            members_ids = group_members_ids[i:min(i + 25, len(group_members_ids))]
            members_friends_ids = self.retrieve_friends_using_vk_execute(members_ids)
            for j in range(0, len(members_ids)):
                friends_graph[members_ids[j]] = members_friends_ids[j]
        return friends_graph

    def _get_group_members_offset(self, group_name, offset):
        params = dict()
        params['group_id'] = group_name
        params['offset'] = offset
        
        response = self._request('groups.getMembers', params)
        encoded_res = json.loads(response)
        if 'response' in encoded_res:
            return encoded_res['response']
        else:
            return []

    def _request(self, method_name, params):
        params_str = urlencode(params)
        full_url = self._api_url + method_name + '?' + params_str
        response = urlopen(full_url)
        return response.read().decode(response.headers.get_content_charset())
