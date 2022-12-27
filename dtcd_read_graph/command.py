import json

import pandas as pd
from otlang.sdk.syntax import Keyword, Positional, OTLType
from pp_exec_env.base_command import BaseCommand, Syntax
from .complex_rest_connector import ComplexRestConnector
from .dtcd_graph_connector import DtcdGraphConnector


class DtcdReadGraphCommand(BaseCommand):
    # define syntax of your command here
    syntax = Syntax(
        [
            Positional("name", otl_type=OTLType.TEXT, required=True),
            Keyword("id", otl_type=OTLType.TEXT, required=False),

        ],
    )
    use_timewindow = False  # Does not require time window arguments
    idempotent = True  # Does not invalidate cache

    def _transform_node_dict_to_df_dict(self, node_dict: dict, edges: dict):
        node_id = node_dict['primitiveID']
        res = (
            node_id,
            node_dict['primitiveName'],
            self._transform_port_dict_to_df_dict(node_dict['initPorts']),
            self._transform_source_node_edges_dict_to_df_dict(node_id, edges),
            self._transform_target_node_edges_dict_to_df_dict(node_id, edges),
            self._transform_prop_dict_to_df_dict(node_dict['properties']),
        )
        return res

    @staticmethod
    def _transform_port_dict_to_df_dict(ports_list):
        return json.dumps(ports_list)

    @staticmethod
    def _transform_source_node_edges_dict_to_df_dict(node_id, edges_list):
        return json.dumps( # filter by sourceNode
            list(filter(
                lambda node: node['sourceNode'] == node_id, edges_list)
            )
        )

    @staticmethod
    def _transform_target_node_edges_dict_to_df_dict(node_id, edges_list):
        return json.dumps( # filter by sourceNode
            list(filter(
                lambda node: node['targetNode'] == node_id, edges_list)
            )
        )

    def _transform_prop_dict_to_df_dict(self, prop_dict):
        return json.dumps(prop_dict)

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        self.log_progress('Start dtcd_read_graph command')
        graph_name = self.get_arg('name').value
        graph_id = self.get_arg('id').value

        dtcd_address = self.config['dtcd_server']['address']
        cr_connector = ComplexRestConnector(
            dtcd_address,
            self.config['dtcd_server']['username'],
            self.config['dtcd_server']['password']
        )
        dtcd_connector = DtcdGraphConnector(cr_connector)

        graph_dict = dtcd_connector.get_graph(graph_name, graph_id)
        list_for_result_df = list(map(
            lambda node: self._transform_node_dict_to_df_dict(node, graph_dict['edges']),
            graph_dict['nodes']
        ))
        df = pd.DataFrame(
            list_for_result_df,
            columns=(
                'primitiveID', 'primitiveName', 'initPorts', 'source_edges', 'target_edges', 'properties'
            )
        )
        return df
