from igraph import *


class GraphAnalyser:
    def __init__(self, group_members_friends):
        self._graph = Graph()
        self._vertices = dict()
        self._build_graph(group_members_friends)

    def graph_diameter(self):
        return self._graph.diameter(directed=True, unconn=True)

    def _build_graph(self, group_members_friends):
        for member_id, friends_ids in group_members_friends.items():
            self._add_vertex(member_id)
            for friend_id in friends_ids:
                self._add_vertex(friend_id)
                self._add_edge((member_id, friend_id))

    def _add_vertex(self, vertex_name):
        if vertex_name not in self._vertices:
            vertex_index = len(self._vertices)
            self._vertices[vertex_name] = vertex_index
            self._graph.add_vertex(vertex_index)

    def _add_edge(self, edge):
        v1_index = self._vertices[edge[0]]
        v2_index = self._vertices[edge[1]]
        self._graph.add_edges([(v1_index, v2_index)])
