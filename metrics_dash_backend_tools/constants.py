"""
Defines constants for use in metricsLib
"""
import datetime
import os
from pathlib import Path
from enum import Enum

TIMEOUT_IN_SECONDS = 120
REQUEST_RETRIES = 5
# Folder Names to send over our projects tracked data
DATESTAMP = datetime.datetime.now().date().isoformat()
TOKEN = os.getenv("GITHUB_TOKEN")
GH_GQL_ENDPOINT = "https://api.github.com/graphql"
AUGUR_HOST = os.getenv("AUGUR_HOST")

PATH_TO_TEMPLATES = (Path(__file__).parent / "../../templates").resolve()

template_path = os.path.join(PATH_TO_TEMPLATES, "repo_report_template.md")
with open(template_path, "r", encoding="utf-8") as file:
    REPO_REPORT_TEMPLATE = file.read()

with open(os.path.join(PATH_TO_TEMPLATES, "org_report_template.md"), "r", encoding="utf-8") as file:
    ORG_REPORT_TEMPLATE = file.read()

class DesiredReportBehavior(Enum):
    """
    Enumeration class to define constants for report
    heading generation behavior
    """
    VALUE_INCREASE = 1
    VALUE_DECREASE = -1
