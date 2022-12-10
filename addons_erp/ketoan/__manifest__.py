# -*- coding: utf-8 -*-
{
    'name' : 'Kế toán VN',
    'version' : '1.0',
    'summary': 'Kế toán VN',
    'sequence': 10,
    'description': """
Kế toán VN
    """,
    'category': 'Accounting/Accounting',
    'website': '',    
    'depends' : ['account'],
    'data': [        

        'views/ketoan_thu_chi_quy_tien_mat_thu_tien_view.xml',
        'views/ketoan_thu_chi_quy_tien_mat_chi_tien_view.xml',        
        
        'views/ketoan_menu.xml',
    ],
    'installable': True,
    'application': True,
    'license': '',
}
