import datetime
import json
import os
from django.conf import settings
from django.utils.translation import gettext as _
from report.models import ReportDefinition


def create_base_report_template(report_type):
    # use a predefined report definition so you don't have to start from scratch in this demo app,
    # for a real world app you would probably start with an empty report if nothing was saved previously

    with open(os.path.join(settings.BASE_DIR, 'albums', 'static', 'report_definition.json')) as json_file:
        report_definition = json.load(json_file)

    ReportDefinition.objects.create(
        report_type = report_type, 
        report_definition = json.dumps(report_definition),
        last_modified_at = datetime.datetime.now()
        )