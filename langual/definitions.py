from dagster import Definitions
from graphs2go.resources import DirectoryInputConfig, OutputConfig, RdfStoreConfig
from graphs2go.utils import configure_markus, load_dotenv
from returns.maybe import Nothing

from langual.assets import interchange_graph, release, skos_file, skos_graph
from langual.jobs import files_job
from langual.paths import INPUT_DIRECTORY_PATH, OUTPUT_DIRECTORY_PATH

configure_markus()
load_dotenv()


definitions = Definitions(
    assets=[
        interchange_graph,
        release,
        skos_file,
        skos_graph,
    ],
    jobs=[files_job],
    resources={
        "input_config": DirectoryInputConfig.from_env_vars(
            directory_path_default=INPUT_DIRECTORY_PATH
        ),
        "output_config": OutputConfig.from_env_vars(
            directory_path_default=OUTPUT_DIRECTORY_PATH
        ),
        "rdf_store_config": RdfStoreConfig.from_env_vars(
            directory_path_default=Nothing
        ),
    },
)
