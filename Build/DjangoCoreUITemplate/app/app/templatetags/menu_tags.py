# app/templatetags/menu_tags.py
from django import template

register = template.Library()

@register.inclusion_tag('includes/sidebar_menu_item.html')
def render_sidebar_menu_item(item):
    return {'item': item}

@register.inclusion_tag('includes/header_left_menu_item.html')
def render_header_left_menu_item(item):
    return {'item': item}

@register.inclusion_tag('includes/header_user_menu_item.html')
def render_header_user_menu_item(item):
    return {'item': item}

@register.inclusion_tag('includes/header_right_menu_item.html')
def render_header_right_menu_item(item):
    return {'item': item}

@register.inclusion_tag('includes/breadcrumbs.html')
def render_breadcrumbs(breadcrumbs):
    return {'breadcrumbs': breadcrumbs}
