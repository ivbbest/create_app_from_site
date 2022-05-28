from fast_bitrix24 import Bitrix
from datetime import datetime, timedelta
import requests
from config import WEBHOOK  # конфигурационный файл с вебхуком

webhook = WEBHOOK
b = Bitrix(webhook)

userfields = ['delivery_adress', 'delivery_date', 'delivery_code']
prefix = 'UF_CRM_'

app_from_site = {
    "title": "title",
    "description": "Some description",
    "client": {
        "name": "Jon",
        "surname": "Karter",
        "phone": "+77777777777",
        "adress": "st. Mira, 287, Moscow"
    },
    "products": ["Candy", "Carrot", "Potato"],
    "delivery_adress": "st. Mira, 211, Ekaterinburg",
    "delivery_date": "2021-01-01:16:00",
    "delivery_code": "#232nkF3fAdn"
}


def add_userfield(userfields):
    for userfield in userfields:
        if str(userfield).find('date') != -1:
            new_userfield = [
                {
                    'fields': {
                        "FIELD_NAME": userfield,
                        "EDIT_FORM_LABEL": userfield,
                        "LIST_COLUMN_LABEL": userfield,
                        "USER_TYPE_ID": "datetime"

                    }
                }
            ]
            print(b.call('crm.deal.userfield.add', new_userfield))

        new_userfield = [
            {
                'fields': {
                    "FIELD_NAME": userfield,
                    "EDIT_FORM_LABEL": userfield,
                    "LIST_COLUMN_LABEL": userfield,
                    "USER_TYPE_ID": "string"

                }
            }
        ]

        print(b.call('crm.deal.userfield.add', new_userfield))


def search_client_id(phone):
    contact_id = -1
    client_phone = [
        {
            'filter': {'PHONE': phone},
            'select': ['ID']
        },
    ]

    client_id = b.call('crm.contact.list', client_phone)

    if len(client_id[0]):
        contact_id = client_id[0][0]['ID']

    return contact_id


def search_client(app_from_site):
    phone = app_from_site['client']['phone']
    client_id = search_client_id(phone)

    if client_id == -1:
        client_id = add_new_client(app_from_site['client'])

    return client_id


def add_new_client(client_info):
    new_client = [
        {
            'fields': {
                "NAME": client_info['name'],
                "LAST_NAME": client_info['surname'],
                "ADDRESS": client_info['adress'],
                "PHONE": [{"VALUE": client_info['phone']}]
            }
        }
    ]

    b.call('crm.contact.add', new_client)

    contact_id = search_client_id(client_info['phone'])

    return contact_id



breakpoint()
print()

###############################################################
###############################################################

# app = {
#     "title": "title",
#     "description": "Some description",
#     "client": {
#         "name": "Jon",
#         "surname": "Karter",
#         "phone": "+77777777777",
#         "adress": "st. Mira, 287, Moscow"
#     },
#     "products": ["Candy", "Carrot", "Potato"],
#     "delivery_adress": "st. Mira, 211, Ekaterinburg",
#     "delivery_date": "2021-01-01:16:00",
#     "delivery_code": "#232nkF3fAdn"
# }
#
# app2 = [
#     {
#         'ID': 1,
#         'fields': {
#             'TITLE': '3 New tasks in Bitrix',
#             'RESPONSIBLE_ID': 1,
#             'CREATED_BY': 1
#         }
#     }
# ]
#
# sdelka = [
#     {
#         'fields': {
#             "TITLE": "title6",
#             "SOURCE_DESCRIPTION": "Some description6",
#             'CONTACT_ID': 3,
#             'UF_CRM_MY_STRING': "#232nkF3fAfdn"
#             # 'client': {
#             #     'NAME': 'Jon',
#             #     'LAST_NAME': "Karter",
#             #     'PHONE': "+7777777777",
#             #     'ADDRESS': "st. Mira, 287, Moscow"
#             # },
#
#         }
#     }
# ]
#
# b.call('crm.deal.add', sdelka)
#
# # print(b.call('crm.deal.contact.fields', {}))
#
# params = {"products": ["Candy", "Carrot", "Potato"],
#           "delivery_adress": "st. Mira, 211, Ekaterinburg",
#           "delivery_date": "2021-01-01:16:00",
#           "delivery_code": "#232nkF3fAdn"
#           }
#
# # print(b.call('crm.contact.get', {'id': 3}))
#
# # print(b.call('crm.deal.get', {'id': 5}))
#
# # print(b.call('crm.productrow.fields', {})
#
#
# userfield = [
#     {
#         'fields': {
#             "FIELD_NAME": "MY_STRING3",
#             "EDIT_FORM_LABEL": "Моя строка777",
#             "LIST_COLUMN_LABEL": "Моя строка3",
#             "USER_TYPE_ID": "string"
#
#         }
#     }
# ]
#
#
# # print(b.call('crm.deal.userfield.add', userfield))
#
#
#
# userfilter = [
#     {
#         # 'order': {"ID": "ASC"},
#         'filter': {'UF_CRM_MY_STRING3': "64647hjhff"},
#         'select': ['*']
#     },
# ]
#
#
# # print(b.call('crm.deal.list', userfilter))
# # print(b.call('crm.productrow.fields', {}))
#
#
# product_name = [
#     {
#         'ID': 9,
#         'rows': [
#             ["Candy", "Carrot", "Potato"]
#         ]
#     }
# ]
#
# # print(b.call('crm.userfield.fields', {}))
#
#
# new_user = [
#     {
#         'fields': {
#             "NAME": "Иван",
#             "SECOND_NAME": "Иванович",
#             "LAST_NAME": "Иванов",
#             "PHONE": [{"VALUE": "+7777777777"}]
#         }
#     }
# ]
# # b.call('crm.contact.add', new_user)
#
#
# user_phone = [
#     {
#         'filter': {'PHONE': "+777п7777777"},
#         'select': ['ID']
#     },
# ]

# user_id = b.call('crm.contact.list', user_phone)
# breakpoint()
# print()
