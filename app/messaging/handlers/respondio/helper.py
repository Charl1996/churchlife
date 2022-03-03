from configs import RESPONDIO_BASE_URL


WIX_PURCHASE_TEMPLATE = 'wix_purchase'
WIX_PURCHASE_TAGS = ['Origin - Bybelstudie']

TEMPLATES = {
    WIX_PURCHASE_TEMPLATE: {
        'name': 'bybelstudie_website_test1',
        'text': 'Hi {{1}} Baie dankie vir jou bestelling by www.bybelstudie.co.za. Ons bid en vertrou dat die studies vir jou tot groot seën sal wees. Indien jy enige vrae het, kontak my gerus deur op hierdie boodskap te reaggeer. Ek is altyd beskikbaar om te help. Die Here seën, Riaan le Roux',
        'params': ['first_name'],
    }
}


def get_template_info(template):
    return TEMPLATES[template]['name'], TEMPLATES[template]['text'], TEMPLATES[template].get('params', None)


class RespondIOEndpoints:

    base_url = RESPONDIO_BASE_URL

    @classmethod
    def send_message_endpoint(cls, contact_id):
        return f"{cls.base_url}/message/sendContent/{contact_id}"

    @classmethod
    def get_contact_endpoint(cls, phone_number):
        return f"{cls.base_url}/contact/by_custom_field?name=phone&value={phone_number}"

    @classmethod
    def add_tags_endpoint(cls, contact_id):
        return f"{cls.base_url}/contact/{contact_id}/tags"

    @classmethod
    def create_contact_endpoint(cls):
        return f"{cls.base_url}/contact/"


class PayloadParser:

    @classmethod
    def parse_create_contact_data(cls, data):
        return {
            'custom_fields': cls._custom_fields(data)
        }

    @classmethod
    def parse_template_message_data(cls, template, **kwargs):
        template_name, template_text, params = get_template_info(template)

        if params:
            params_info = [kwargs.get(param, '') for param in params]
            return cls._template_params_message(template_text, template_name, params_info)
        else:
            return cls._template_text_message(template_text, template_name)

    @classmethod
    def parse_add_tags_data(cls, tags):
        return {
            'tags': tags
        }

    @classmethod
    def _template_params_message(cls, message_text, template_name, params):
        def _parse_params(params_list):
            return [
                {'type': 'text', 'text': str(param)}
                for param in params_list
            ]

        return {
            'body': [{
                'type': 'whatsapp_template',
                'template': {
                    'name': template_name,
                    'languageCode': 'af',
                    'components': [{
                        'type': 'body',
                        'text': message_text,
                        'parameters': _parse_params(params),
                    }]
                }
            }]
        }

    @classmethod
    def _template_text_message(cls, message_text, template_name):
        return {
            'body': [{
                'type': 'whatsapp_template',
                'template': {
                    'name': template_name,
                    'languageCode': 'af',
                    'components': [{
                        'type': 'body',
                        'text': message_text,
                    }]
                }
            }]
        }

    @classmethod
    def _custom_fields(cls, data: dict):
        return [
            {'name': key, 'value': value}
            for key, value in data.items()
        ]
