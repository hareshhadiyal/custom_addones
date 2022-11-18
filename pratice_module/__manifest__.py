# -*- coding: utf-8 -*-

{
    'name': 'Hotel',
    'version': '15.0.1.2.5',
    'author': 'Candidroot',
    'sequence': '-100',
    'website': "www.candidroot.com",
    'application': True,

    'demo': [
        'demo/booking_demo.xml',
        'demo/payment_demo.xml',
    ],

    'data': [
        'security/ir.model.access.csv',
        'wizard/other_details_view.xml',
        'views/hotel_booking_view.xml',
        'views/hotel_payment_view.xml',
    ],
}
