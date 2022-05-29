from fast_bitrix24 import Bitrix
from datetime import datetime, timedelta
import requests
from config import WEBHOOK  # конфигурационный файл с вебхуком
from pprint import pprint
from options import userfields, app_from_site, filter_delivery_date, \
    filter_delivery_adress, filter_delivery_code


webhook = WEBHOOK
b = Bitrix(webhook)


def add_userfield(userfields):
    """
    Создание пользовательских тегов по списку.
    Если поля такие есть, то пропускается работа с перехватом ошибки.
    """
    try:
        for userfield in userfields:
            print(userfield)

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
    except RuntimeError as err:
        print('Runtime Error', err)

    except Exception as err:
        print('Any Error', err)


def search_client_id(phone):
    """
    Поиск клиента по телефону и на выходе id
    """
    contact_id = -1
    client_phone = [
        {
            'filter': {'PHONE': phone},
            'select': ['ID']
        },
    ]

    client_id = b.call('crm.contact.list', client_phone)
    print('Id client', client_id)

    if len(client_id[0]):
        contact_id = client_id[0][0]['ID']

    print('Id client', contact_id)
    return int(contact_id)


def search_client(client_info):
    """
    Поиск клиента по базе. Если нет его, то добавляем.
    На выходе отправляется id клиента
    """
    phone = client_info['phone']
    client_id = search_client_id(phone)
    print('Id client', client_id)

    if client_id == -1:
        client_id = add_new_client(client_info)

    return int(client_id)


def add_new_client(client_info):
    """
    Добавляем нового клиента
    """
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

    contact_id = b.call('crm.contact.add', new_client)
    print('Id contact', contact_id)

    return int(contact_id[0])


def check_delivery_code(delivery_code):
    """
    Анализ delivery_code. Если такой существует, то вывод deal_id.
    В противном случае deal_id = -1
    """

    deal_id = -1

    userfilter = [
        {
            'filter': {filter_delivery_code: delivery_code},
            'select': ['ID']
        },
    ]

    delivery_code_info = b.call('crm.deal.list', userfilter)
    print('Данные по delivery code', delivery_code_info)

    if len(delivery_code_info[0]):
        deal_id = int(delivery_code_info[0][0]['ID'])
        print('Id сделки', deal_id)
    return deal_id


def create_new_deal(purchase):
    """
    Создание новой заявки на сайте
    """
    contact_id = search_client(purchase['client'])

    sdelka = [
        {
            'fields': {
                "TITLE": purchase['title'],
                "SOURCE_DESCRIPTION": purchase['description'],
                'CONTACT_ID': contact_id,
                filter_delivery_code: purchase['delivery_code'],
                filter_delivery_date: purchase['delivery_date'],
                filter_delivery_adress: purchase['delivery_adress']

            }
        }
    ]

    deal_id = b.call('crm.deal.add', sdelka)
    print('Id сделки', deal_id)

    add_product(purchase["products"], deal_id[0])

    return int(deal_id[0])


def update_deal(delivery, deal_id):
    """
    Обновление данных по сделке.
    На вход: delivery_code, delivery_date, delivery_adress, которые можно изменять в заявке
    """
    delivery_code, delivery_date, delivery_adress = delivery
    sdelka = [
        {
            'ID': deal_id,
            'fields': {
                filter_delivery_code: delivery_code,
                filter_delivery_date: delivery_date,
                filter_delivery_adress: delivery_adress

            }
        }
    ]

    b.call('crm.deal.update', sdelka)


def add_product(products, deal_id):
    """
    Добавление товаров в заявку
    """
    rows = [{"PRODUCT_NAME": product} for product in products]

    product_name = [
        {
            'ID': deal_id,
            'rows': rows,
        }

    ]

    print(b.call('crm.deal.productrows.set', product_name))


def main(purchase):
    # добавление новых пользовательских полей
    add_userfield(userfields)

    # Анализ delivery_code и в зависимости от check_deal_id
    # Обновляем заявку или создаем с нуля
    # Если в заявке не хватает каких-то аргументов, то перехват ошибки
    try:
        check_deal_id = check_delivery_code(purchase['delivery_code'])

        if check_deal_id != - 1:
            delivery = (
                        purchase['delivery_code'],
                        purchase['delivery_date'],
                        purchase['delivery_adress']
                        )
            update_deal(delivery, check_deal_id)
        else:
            create_new_deal(purchase)
    except (RuntimeError, KeyError) as err:
        print('Неправильно введенный delivery_code или другой аргумент. '
              'Проверьте корректность заявки.', err)
    except Exception as err:
        print('Any Error', err)

    # for i in range(273, 295, 2):
    #     try:
    #         print(b.call('crm.deal.userfield.delete', {'ID': i}))
    #     except Exception as e:
    #         print(e)
    # add_userfield(userfields)
    # # # analyze_delivery_code(app_from_site)
    # # pprint(b.call('crm.deal.userfield.get', {'ID': 291})['FIELD_NAME'])
    # deals = b.call('crm.deal.list', {
    #     'select': ['UF_*'],
    #     'filter': {'CLOSED': 'N'}
    # })[0]
    # # pprint(deals)


# if __name__ == '__main__':
#     main(app_from_site)
pprint(b.get_all('crm.deal.userfield.list'))
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
#             "TITLE": "title28",
#             "SOURCE_DESCRIPTION": "Some description28",
#             'CONTACT_ID': 3,
#             'UF_CRM_MY_STRING': "#652nkF6fAfdn"
#
#         }
#     }
# ]
# #
# result = b.call('crm.deal.add', sdelka)
# breakpoint()
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
# print(b.call('crm.productrow.fields', {}))

# products = app_from_site['products']
# rows = [{"PRODUCT_NAME": product} for product in products]

# for product in products:
#     rows.append({"PRODUCT_NAME": product})


# product_name = [
#     {
#         'ID': 21,
#         'rows': rows,
#     }
#
# ]
# print(b.call('crm.deal.productrows.set', product_name))

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
# new_user = {
#         'fields': {
#             "NAME": "Masha",
#             "SECOND_NAME": "Masha",
#             "LAST_NAME": "Masha",
#             "PHONE": [{"VALUE": "+4444"}]
#         }
#     }
#
# result = b.call('crm.contact.add', new_user)
# breakpoint()



#
#
# user_phone = [
#     {
#         'filter': {'PHONE': "+4444"},
#         'select': ['ID']
#     },
# ]
#
# user_id = b.call('crm.contact.list', user_phone)
# breakpoint()
