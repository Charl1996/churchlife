from app.requests import *
from configs import BREEZE_API_KEY
from app.integrations.database_service.handlers.breeze.helper import (
    BreezeEndpoints,
    PayloadParser
)


class BreezeRequest(BreezeEndpoints, PayloadParser):

    @classmethod
    def request_headers(cls):
        return {
            'Content-Type': 'application/json',
            'Api-Key': BREEZE_API_KEY,
        }


class Breeze(BreezeRequest):

    def get_people(self, include_tags=True, include_detail=True):
        people = get_request(
            self.get_people_endpoint(include_detail=include_detail)
        )

        if include_tags:
            people = self._add_people_tags(people)

        # parse to relevant "sample file" fields
        return people

    def update_person(self):
        pass

    def _get_tags(self):
        status_code, content = get_request(
            self.get_tags_endpoint(),
            headers=self.request_headers(),
        )
        return content

    def _add_people_tags(self, people):
        people_ids = [p['id'] for p in people]

        for tag in self._get_tags():
            tag_people = get_request(
                self.get_tag_people_endpoint(tag['id'])
            )

            for tag_person in tag_people:
                try:
                    index = people_ids.index(tag_person['id'])
                    person = people[index]

                    current_tags = person.get('tags', [])
                    person['tags'] = current_tags.append(tag['name'])
                except ValueError:
                    continue

        return people
