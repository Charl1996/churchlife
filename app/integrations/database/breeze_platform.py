import json
from datetime import datetime
from app.integrations.database.database_platform import DatabasePlatform, DATABASE_PLATFORM_TYPE
from app.requests import (
    get_request,
)
from app.integrations.database.database_platform_schema import (
    BreezePlatformSchema,
    Entity as EntitySchema
)


class BreezeDatabasePlatform(DatabasePlatform):

    slug = 'breeze'
    subdomain_placeholder = '<subdomain>'
    example_api_url = f'https://{subdomain_placeholder}.breezechms.com/api'

    platform: BreezePlatformSchema

    @classmethod
    def test_connection(cls, configuration):
        subdomain = configuration['subdomain']
        test_base_url = cls.example_api_url.replace(cls.subdomain_placeholder, subdomain)
        api_key = configuration['api_key']

        test_url = f'{test_base_url}/people?limit=1'
        status_code, _content, errors = get_request(test_url, headers=cls.headers(api_key))

        if errors:
            if isinstance(errors, list):
                error_message = errors[0]
            else:
                error_message = errors

            return 403, error_message

        return status_code, None

    @classmethod
    def schema_model(cls):
        return BreezePlatformSchema

    @classmethod
    def create_schema_model(cls):
        return BreezePlatformSchema

    @classmethod
    def create_model(cls, create_schema: BreezePlatformSchema):
        return cls.database_model()(
            slug=cls.slug,
            subdomain=create_schema.subdomain,
            api_key=create_schema.api_key,
            organisation_id=create_schema.organisation_id,
            type=DATABASE_PLATFORM_TYPE,
        )

    @classmethod
    def url(cls, subdomain):
        return cls.example_api_url.replace(cls.subdomain_placeholder, subdomain)

    @classmethod
    def headers(cls, api_key):
        return {
            'Content-Type': 'application/json',
            'Api-Key': f'{api_key}'
        }

    @classmethod
    def init_class_instance(cls, schema_model):
        return cls(platform=schema_model)

    def __init__(self, platform: BreezePlatformSchema):
        self.platform = platform

    @property
    def fields(self) -> BreezePlatformSchema:
        return self.platform

    def get_url(self, endpoint):
        return "{base_url}{endpoint}".format(
            base_url=self.url(self.fields.subdomain),
            endpoint=endpoint
        )

    def get_entities(self, as_dict=False):
        contacts, tags_names = self.get_contacts()
        if as_dict:
            return [EntitySchema(**contact).dict() for contact in contacts]
        else:
            return [EntitySchema(**contact) for contact in contacts]

    def get_contacts(self):
        try:
            tags = self._get_tags()
            people_list = self._get_people(detail=True)

            people_list_with_tags = []
            for person in people_list:
                p = self._parse_person_fields(person)
                people_list_with_tags.append(p)

            tags_names = []
            # for tag in tags:
            #     people = self._get_users_by_tag_id(tag['id'])
            #     people_list_with_tags = self._update_people_in_list_with_tag(people, people_list_with_tags, tag['name'])
            #     tags_names.append(tag['name'])

        except Exception as e:
            raise e

        return people_list_with_tags, tags_names

    def _update_people_in_list_with_tag(self, tags_people, people_list, tag_name):
        for tag_person in tags_people:
            for index, p in enumerate(people_list):
                if p.get('id', '') == tag_person['id']:
                    current_tags = p.get('tags') or []
                    p['tags'] = current_tags + [tag_name]
                    people_list[index] = p

        return people_list

    def _parse_person_fields(self, person):
        def _age(birth_date):
            if not birth_date:
                return ''
            born = datetime.strptime(f'{birth_date} 00:00:00', '%Y-%m-%d %H:%M:%S')
            today = datetime.today()
            return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

        def _mobile(phone_list):
            for item in phone_list:
                if item['phone_type'] == 'mobile':
                    return item['phone_number']
            return ''

        def _email(email_list):
            for item in email_list:
                if item['field_type'] == 'email_primary':
                    return item['address']
            return ''

        parsed_person = dict()

        parsed_person['id'] = person['id']
        parsed_person['first_name'] = person['force_first_name']
        parsed_person['last_name'] = person['last_name']
        parsed_person['gender'] = person['details'].get('757881885', {}).get('name')
        parsed_person['age'] = _age(person['details'].get('birthdate'))
        parsed_person['campus'] = person['details'].get('1847408178', {}).get('name')
        parsed_person['mobile'] = _mobile(person['details'].get('79910291', []))
        parsed_person['email'] = _email(person['details'].get('1676694648', []))
        parsed_person['tags'] = []

        return parsed_person

    def _get_tags(self):
        status_code, content, errors = get_request(self.get_url('/tags/list_tags'), headers=self.headers(self.fields.api_key))
        if status_code != 200:
            return None

        return content

    def _get_people(self, detail=False):
        detail_flag = 0
        if detail:
            detail_flag = 1

        status_code, content, errors = get_request(self.get_url(f'/people/?details={detail_flag}&limit=50'), headers=self.headers(self.fields.api_key))
        if status_code != 200:
            raise Exception('Retrieving tags unsuccessful!')

        return content

    def _get_users_by_tag_id(self, tag_id):
        filter_json = json.dumps({'tag_contains': f'y_{tag_id}'})
        status_code, content, errors = get_request(self.get_url(f'/people/?filter_json={filter_json}'), headers=self.headers(self.fields.api_key))
        if status_code != 200:
            raise Exception('Retrieving tags unsuccessful!')

        return content
