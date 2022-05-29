userfields = ['delivery_code', 'delivery_adress', 'delivery_date']
prefix = 'UF_CRM_'
app_from_site = {
    "title": "Test title3",
    "description": "Test description3",
    "client": {
        "name": "Sasha",
        "surname": "Suhov",
        "phone": "+666",
        "adress": "st. Kerch, 2, Belgorod"
    },
    "products": ["Kasha", "Arbuz", "Kuraga", "Apple"],
    "delivery_adress": "st. Ivanovo, 211, Vladivostok",
    "delivery_date": "2022-02-03:17:00",
    "delivery_code": "8864557sshff"
}
filter_delivery_code = prefix + 'DELIVERY_CODE'
filter_delivery_date = prefix + 'DELIVERY_DATE'
filter_delivery_adress = prefix + 'DELIVERY_ADRESS'