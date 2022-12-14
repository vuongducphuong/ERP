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
        'views/ketoan_thu_chi_ngan_hang_chi_tien_view.xml',
        'views/ketoan_thu_chi_ngan_hang_thu_tien_view.xml',
        'views/ketoan_thu_chi_ngan_hang_chuyen_tien_noi_bo_view.xml',
        'views/ketoan_bao_cao_ban_hang_tong_hop_view.xml',
        
        



        'views/ketoan_bao_cao_action.xml',
        'views/ketoan_menu.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'ketoan/static/src/css/report.css',            
            'ketoan/static/src/js/ketoan_bao_cao_so_cai.js',            
            'ketoan/static/src/js/ketoan_bao_cao_quy_tien_mat.js',            


            'ketoan/static/src/xml/ketoan_bao_cao_so_cai_template.xml',
            'ketoan/static/src/xml/ketoan_bao_cao_quy_tien_mat_template.xml',
        ],
    },    
    'installable': True,
    'application': True,
    'license': '',
}
