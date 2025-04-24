import os
import logging
from metrics_dash_backend_tools import get_all_data,parse_repos_and_orgs_into_objects
from metrics_dash_backend_tools import parse_tracked_repos_file, read_previous_metric_data
from metrics_dash_backend_tools.metrics_definitions import SIMPLE_METRICS, ORG_METRICS, ADVANCED_METRICS
from metrics_dash_backend_tools.metrics_definitions import PERIODIC_METRICS, RESOURCE_METRICS


LOGGER = logging.getLogger(__name__)


def test_metrics_data_gathering():
    os.umask(0)

    metadata_path = os.path.dirname(os.path.realpath(__file__))
    org_urls, repo_urls = parse_tracked_repos_file(metadata_path)

    all_orgs, all_repos = parse_repos_and_orgs_into_objects(org_urls, repo_urls)

    LOGGER.info(all_orgs)
    
    metrics_lists = [SIMPLE_METRICS,ORG_METRICS,ADVANCED_METRICS,PERIODIC_METRICS]
    get_all_data(metadata_path,metadata_path, all_orgs, all_repos,metrics_lists,RESOURCE_METRICS)