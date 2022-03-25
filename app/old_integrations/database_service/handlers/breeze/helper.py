import json
from configs import BREEZE_BASE_URL


class BreezeEndpoints:

    base_url = BREEZE_BASE_URL

    @classmethod
    def get_people_endpoint(cls, include_detail=False):
        return f"{cls.base_url}/people/details={include_detail}"

    @classmethod
    def get_tags_endpoint(cls):
        return f"{cls.base_url}/tags/list_tags"

    @classmethod
    def get_tag_people_endpoint(cls, tag_id):
        filter_json = PayloadParser.parse_tag_people_data(tag_id)
        return f"{cls.base_url}/people/?filter_json={filter_json}"


class PayloadParser:

    @classmethod
    def parse_tag_people_data(cls, tag_id):
        return json.dumps({'tag_contains': f'y_{tag_id}'})