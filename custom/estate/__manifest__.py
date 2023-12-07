# -*- coding: utf-8 -*-
{
    'name': 'estate',
    'depends': [ 'base' ],
    'application': True,
    'data': [
      'security/ir.model.access.csv',
      'views/estate_property_type_view.xml',
      'views/estate_property_tag_view.xml',
      'views/estate_property_offer_view.xml',
      'views/estate_property_view.xml',
      'views/menus/estate_menus.xml',
      'views/search/estate_search.xml',
    ]
}