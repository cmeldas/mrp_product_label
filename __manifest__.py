{
    'name': 'Product Label Management',
    'version': '18.0.1.0.0',
    'category': 'Manufacturing',
    'summary': 'Add label information to product variants',
    'description': """
        This module adds label management fields to product variants:
        * Label Name
        * Label Subtitle
        * Label Ingredients
        * Label Lifetime
        * Label Weight
        * Label Storage Temperature
    """,
    'author': 'cmeldas@gmail.com',
    'depends': ['product', 'mrp', 'mrp_pasteurization'],
    'data': [
        'views/product_views.xml',
        'views/mrp_production_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
