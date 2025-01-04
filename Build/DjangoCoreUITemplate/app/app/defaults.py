# defaults.py

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
                'order': 11
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
                'order': 99997
            }, 
            {
                'id': 'sidebar_logout',
                'item_type': 'link',
                'menu_text': 'Logout',
                'url': '/logout',
                'icon': '/static/modules/@coreui/icons/sprites/free.svg#cil-exit-to-app',
                'auth_requirement': 'auth_only',
                'order': 99999
            },   
            {
                'id': 'sidebar_login',
                'item_type': 'link',
                'menu_text': 'Login',
                'url': '/login',
                'icon': '/static/modules/@coreui/icons/sprites/free.svg#cil-lock-locked',
                'auth_requirement': 'unauth_only',
                'order': 99998
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
                'order': 5
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
                'order': 5
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
                'order': 100
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
                'order': 10
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


