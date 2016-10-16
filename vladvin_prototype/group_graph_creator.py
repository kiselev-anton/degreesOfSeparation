import sys
import json

from vk_requester import VkRequester

if __name__ == '__main__':
    if (len(sys.argv) < 2):
        print ('Incorrect arguments. Give me group name')
        exit()

    group_name = sys.argv[1]
    vk_requester = VkRequester()
    
    friends_graph = vk_requester.get_friends_graph_of_group_members(group_name)
    
    f = open('group_friends_graph.txt', 'w')
    f.write(json.dumps(friends_graph))
    f.close()
