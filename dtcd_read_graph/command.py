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

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        self.log_progress('Start dtcd_read_graph command')
        graph_name = self.get_arg('name').value
        graph_id = self.get_arg('id').value

        dtcd_address = self.config['dtcd_server']['address']
        cr_connector = ComplexRestConnector(dtcd_address, 'admin', 'admin')
        dtcd_connector = DtcdGraphConnector(cr_connector)

        graph_dict = dtcd_connector.get_graph(graph_name, graph_id)
        print(graph_dict)

        return df
