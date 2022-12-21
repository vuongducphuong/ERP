# -*- coding: utf-8 -*-
{
    'name': "Dashboard ERP",
    'description': """Dashboard ERP""",
    'summary': """dashboard module brings a multipurpose graphical dashboard"""
               """ for module and making the relationship management better and easier""",
    'category': 'Sales',
    'version': '16.0.1.0.0',
    'author': 'Lean Soft',
    'company': 'Lean Soft',
    'maintainer': 'Lean Soft',
    'website': "https://www.leansoft.vn",
    'depends': ['base', 'crm', 'sale_management'],
    'data': [
        'views/dashboard_view.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'dashboard_erp/static/src/css/dashboard.css',
            'dashboard_erp/static/src/css/style.scss',
            'dashboard_erp/static/src/css/material-gauge.css',
            'dashboard_erp/static/src/js/dashboard_view.js',
            'dashboard_erp/static/src/js/custom.js',
            'dashboard_erp/static/src/js/lib/highcharts.js',
            'dashboard_erp/static/src/js/lib/Chart.bundle.js',
            'dashboard_erp/static/src/js/lib/funnel.js',
            'dashboard_erp/static/src/js/lib/d3.min.js',
            'dashboard_erp/static/src/js/lib/material-gauge.js',
            'dashboard_erp/static/src/js/lib/columnHeatmap.min.js',
            'dashboard_erp/static/src/js/lib/columnHeatmap.js',
            'dashboard_erp/static/src/xml/dashboard_view.xml',

        ],
    },
    'images': [
        'static/description/banner.png',
    ],
    'license': '',
    'installable': True,
    'application': True,
    'auto_install': False,
}
