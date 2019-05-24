# -*- encoding: utf-8 -*-
{
    "name": "Hijri(Islamic) Datepicker",
    'version': '1.0',
    'author': 'Teckzilla Software Solutions pvt. ltd.',
    'summary': """Odoo Web (Hijri)Islamic Datepicker. The Hijri(Islamic) calendar is the official calendar in countries around the Gulf, especially Saudi Arabia.""",
    "description":
        """
        Odoo Web (Hijri)Islamic Datepicker. The Hijri calendar (or Islamic calendar) is a purely lunar calendar. It contains 12 months that are based on the motion of the moon, and because 12 synodic months is only 12 x 29.53=354.36 days, the Islamic calendar is consistently shorter than a tropical year.

        The calendar is based on the Qur'an (Sura IX, 36-37) and its proper observance is a sacred duty for Muslims.

        The Hijri(Islamic) calendar is the official calendar in countries around the Gulf, especially Saudi Arabia. But other Muslim countries use the Gregorian calendar for civil purposes and only turn to the Islamic calendar for religious purposes.
        Hijri Date picker
        """,
    'website': 'http://www.teckzilla.net',
    "depends": ['web'],
    'category': 'web',
    'data': [
         "views/web_hijri.xml"
    ],
   
    'qweb' : [
         "static/src/xml/*.xml",
    ],
    'images': ['static/description/datetime.png'],
    'installable': True,
    'auto_install': False,

}
