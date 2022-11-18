# -*- coding: utf-8 -*-

{
    'name': 'Clinic',
    'version': '15.0.1.2',
    'category': 'Hospital',
    'author': 'Candidroot',
    'sequence': '-100',
    'website': "www.www.www",
    "description": """To manage Clinic""",
    'application': True,
    'depends': ['payment'],
    'data': [
        'security/clinic_security.xml',
        'security/ir.model.access.csv',
        'report/report.xml',
        'report/report_clinic.xml',
        'wizard/doctor_details_wizard_view.xml',
        'views/patient_details_view.xml',
        'views/doctor_details_view.xml',
        'views/opd_details_view.xml',
        'views/doctor_department_view.xml',
    ],

    'demo': [
        'data/patient_demo.xml',
        'data/doctor_demo.xml',
        'data/opd_demo.xml',
        'data/doctor_department.xml',
    ],

}
