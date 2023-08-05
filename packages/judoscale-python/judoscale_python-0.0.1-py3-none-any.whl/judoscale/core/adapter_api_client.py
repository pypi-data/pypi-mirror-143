from judoscale.core.config import config
import logging
import requests
import json

logger = logging.getLogger(__name__)

class AdapterApiClient:
    def post_report(self, report):
        try:
            logger.debug("[Judoscale] Posting metrics to Judoscale adapter API")
            payload = json.dumps(report.as_dict())
            requests.post(config.api_base_url + '/adapter/v1/reports', timeout=5, json=payload)
        except requests.RequestException as e:
            logger.warn("[Judoscale] Adapter API request failed - {}".format(e))


api_client = AdapterApiClient()
