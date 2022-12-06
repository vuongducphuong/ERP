{
    'name': 'Nhập khẩu dữ liệu',
    'description': """Nhập khẩu dữ liệu từ excel, xml, từ các phần mềm khác...""",
    'depends': [
        'danh_muc',
        ],
    'category': 'Extra Tools',
    'installable': True,
    'auto_install': False,
    'data': [
        'views/base_import_templates.xml',
        'views/base_import_nhap_khau.xml',
    ],
    'qweb': [
        'static/src/xml/base_import.xml',
        'static/src/xml/base_import_excels.xml',
    ],
}
