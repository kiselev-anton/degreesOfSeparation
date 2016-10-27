import sys
import json

from vk_requester import VkRequester
from graph_analyser import GraphAnalyser

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Incorrect arguments. Give me group name')
        exit()

    group_name = sys.argv[1]
    vk_requester = VkRequester()
    
    members_friends = vk_requester.get_group_members_firends(group_name)

    graph_analyser = GraphAnalyser(members_friends)
    print('Graph built')
    diameter = graph_analyser.graph_diameter()
    print('Graph diameter: ' + str(diameter))
    
    # f = open('group_friends_graph.txt', 'w')
    # f.write(json.dumps(members_friends))
    # f.close()
