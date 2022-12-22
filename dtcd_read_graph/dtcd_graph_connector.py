from .complex_rest_connector import ComplexRestConnector


class DtcdGraphConnector:
    def __init__(self, complex_rest_connector: ComplexRestConnector):
        self._complex_rest_connector = complex_rest_connector

    def get_graph_list(self):
        results = self._complex_rest_connector.get('supergraph/v1/fragments')
        graphs = results['fragments']
        return graphs

    def get_graph_by_id(self, id: str):
        print('id=')
        print(id)
        graph_dict = self._complex_rest_connector.get(f'supergraph/v1/fragments/{id}/graph')
        return graph_dict

    def get_graph(self, name: str, id_part: str = None):
        """
        Arguments:
             name - graph name
             id_part - part of id if several graph with given name exists
        """
        graphs = self.get_graph_list()
        print(graphs)
        graphs = list(
            filter(
                lambda graph_dict: graph_dict['name'] == name, graphs
            )
        )
        graphs_len = len(graphs)
        if graphs_len == 0:
            raise ValueError(f'Graph with name {name} does\'t exist')
        if graphs_len > 1:
            if not id_part:
                raise ValueError(f'{graphs_len} graphs exist with name {name}')
        graph_id = graphs[0]['id']
        return self.get_graph_by_id(graph_id)

