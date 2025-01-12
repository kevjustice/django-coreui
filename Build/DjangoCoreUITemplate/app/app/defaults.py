# defaults.py
'''
Customize this menu to suit your needs.  The menu is a dictionary with keys for each menu.  Each menu has an 'id' and 'items' key.  The 'items' key is a list of dictionaries, each representing a menu item.  The menu item dictionary has the following keys:
    'id' - a unique identifier for the menu item
    'item_type' - a string representing the type of menu item.  Valid values are 'link', 'separator', 'header'
    'menu_text' - the text that will be displayed for the menu item
    'url' - the URL that the menu item will link to.  This is only used for 'link' items
    'icon' - the icon that will be displayed next to the menu item
    'auth_requirement' - a string representing the authentication requirement for the menu item.  Valid values are 'auth_only', 'unauth_only', 'all'
    'order' - an integer representing the order in which the menu item will be displayed.  Lower numbers are displayed first
    'secondary_text' - a string representing the secondary text that will be displayed for the menu item.  This is only used for 'link' items
    'secondary_class' - a string representing the class that will be applied to the secondary text.  This is only used for 'link' items
    'alt_icon' - a string representing the alternate icon that will be displayed when alt_status is True.  This is only used for 'link' items
    'alt_icon_class' - a string representing the class that will be applied to the alternate icon.  This is only used for 'link' items
    'alt_status' - a boolean representing whether the alternate icon should be displayed.  This is only used for 'link' items
'''

from app.utilities.enums import MenuItemType, AuthRequirement

DEFAULT_MENUS = {
    'sidebar': {
        'id' : 'sidebar',
        'items': [
            {
                'id': 'sidebar_home',
                'item_type': 'link',
                'menu_text': 'Home',
                'url': '/',
                'icon': '/static/modules/@coreui/icons/sprites/free.svg#cil-home',
                'auth_requirement': 'unauth_only',
                'order': 10
            },
            {
                'id': 'sidebar_dashboard',
                'item_type': 'link',
                'menu_text': 'Dashboard',
                'url': '/dashboard',
                'icon': '/static/modules/@coreui/icons/sprites/free.svg#cil-speedometer',
                'auth_requirement': 'auth_only',
                'order': 10
            },
            {
                'id': 'examples',
                'item_type': 'link',
                'menu_text': 'Example Components',
                'url': '/examples',
                'icon': '/static/modules/@coreui/icons/sprites/free.svg#cil-applications',
                'auth_requirement': 'all',
                'order': 13
            },    
            {
                'id': 'sidebar_iconref',
                'item_type': 'link',
                'menu_text': 'Icon Reference',
                'url': '/icons',
                'icon': '/static/modules/@coreui/icons/sprites/free.svg#cil-3d',
                'auth_requirement': 'all',
                'order': 12
            },            
            
            {
                'id': 'sidebar_loginlogoutSEPARATOR',
                'item_type': 'separator',
                'auth_requirement': 'all',
                'order': 9990
            }, 
            {
                'id': 'sidebar_logout',
                'item_type': 'link',
                'menu_text': 'Logout',
                'url': '/logout',
                'icon': '/static/modules/@coreui/icons/sprites/free.svg#cil-exit-to-app',
                'auth_requirement': 'auth_only',
                'order': 9991
            },   
            {
                'id': 'sidebar_login',
                'item_type': 'link',
                'menu_text': 'Login',
                'url': '/login',
                'icon': '/static/modules/@coreui/icons/sprites/free.svg#cil-lock-locked',
                'auth_requirement': 'unauth_only',
                'order': 9992
            },                        
        ]
    },
    'header_right_menu': {
        'id': 'header_right_menu',
        'items': [
            {
                'id': 'sms',
                'item_type': 'link',
                'menu_text': 'SMS',
                'url': '#',
                'icon': '/static/modules/@coreui/icons/sprites/free.svg#cil-send',
                'auth_requirement': 'auth_only',
                'order': 10
            },
            {
                'id': 'newmail',
                'item_type': 'link',
                'menu_text': 'Unread',
                'secondary_text': '17',
                'secondary_class': 'badge bg-warning ms-auto',
                'url': '#',
                'icon': '/static/modules/@coreui/icons/sprites/free.svg#cil-envelope-open',
                'alt_icon': '/static/modules/@coreui/icons/sprites/free.svg#cil-envelope-closed',
                'alt_icon_class':'bg-success',
                'alt_status': True,
                'auth_requirement': 'auth_only',
                'order': 50
            },
        ]
    },
    'header_left_menu': {
        'id': 'header_left_menu',
        'items': [
            {
                'id': 'fly',
                'item_type': 'link',
                'menu_text': 'Fly Away',
                'url': '#',
                'icon': '/static/modules/@coreui/icons/sprites/free.svg#cil-airplane-mode',
                'auth_requirement': 'auth_only',
                'order': 10
            },
            {
                'id': 'TV',
                'item_type': 'link',
                'menu_text': 'TV',
                'url': '#',
                'icon': '/static/modules/@coreui/icons/sprites/free.svg#cil-envelope-open',
                'alt_icon': '/static/modules/@coreui/icons/sprites/free.svg#cil-4k',
                'alt_icon_class':'bg-danger',
                'alt_status': True,
                'auth_requirement': 'auth_only',
                'order': 50
            },
        ]
    },    
    'user_menu': {
        'id': 'user_menu',
        'items': [
            {
                'id': 'user_menu_headerexample',
                'item_type': 'header',
                'menu_text': 'Header Example',
                'auth_requirement': 'auth_only',
                'order': 10
            },
            {
                'id': 'user_menu_alttextexample',
                'item_type': 'link',
                'menu_text': 'Sec.Text/Alt.Icon',
                'secondary_text': "32",
                'secondary_class': 'badge text-bg-primary',
                'url': '#',
                'icon': '/static/modules/@coreui/icons/sprites/free.svg#cil-envelope-open',
                'alt_icon': '/static/modules/@coreui/icons/sprites/free.svg#cil-envelope-closed',
                'alt_icon_class':'bg-danger',
                'alt_status': True,
                'auth_requirement': 'auth_only',
                'order': 100
            },            
            {
                'id': 'user_menu_SEPARATOR99997',
                'item_type': 'separator',
                'auth_requirement': 'auth_only',
                'order': 99997
            }, 
            {
                'id': 'user_menu_logout',
                'item_type': 'link',
                'menu_text': 'Logout',
                'url': '/logout',
                'icon': '/static/modules/@coreui/icons/sprites/free.svg#cil-exit-to-app',
                'auth_requirement': 'auth_only',
                'order': 99999
            },  
        ],
    },
}


