# app/templatetags/menu_tags.py
from django import template

register = template.Library()

@register.inclusion_tag('includes/sidebar_menu_item.html', takes_context=True)
def render_sidebar_menu_item(context, item):
    return {
        'item': item,
        'user': context['user']
    }

@register.inclusion_tag('includes/header_left_menu_item.html', takes_context=True)
def render_header_left_menu_item(context, item):
    return {
        'item': item,
        'user': context['user']
    }

@register.inclusion_tag('includes/header_user_menu_item.html', takes_context=True)
def render_header_user_menu_item(context, item):
    return {
        'item': item,
        'user': context['user']
    }

@register.inclusion_tag('includes/header_right_menu_item.html', takes_context=True)
def render_header_right_menu_item(context, item):
    return {
        'item': item,
        'user': context['user']
    }

@register.inclusion_tag('includes/breadcrumbs.html', takes_context=True)
def render_breadcrumbs(context, breadcrumbs):
    return {
        'breadcrumbs': breadcrumbs,
        'user': context['user']
    }
