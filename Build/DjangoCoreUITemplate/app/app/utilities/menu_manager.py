# menu_manager.py
from typing import Dict, List, Optional, Union
from dataclasses import dataclass, field
from .session_manager import UserSessionManager
from app.utilities.enums import AuthRequirement, MenuPosition, MenuItemType
import logging
from urllib.parse import urlparse
import re

logger = logging.getLogger(__name__)

@dataclass
class MenuItem:
    id: str
    item_type: Union[MenuItemType, str] = MenuItemType.LINK
    menu_text: Optional[str] = None
    menu_class: Optional[str] = None
    hover_text: Optional[str] = None
    url: Optional[str] = None
    auth_requirement: Union[AuthRequirement, str] = AuthRequirement.ALL
    icon: Optional[str] = None
    icon_class: Optional[str] = None
    alt_icon: Optional[str] = None
    alt_icon_class: Optional[str] = None
    alt_status: bool = False
    secondary_text: Optional[str] = None
    secondary_class: Optional[str] = None
    new_window: bool = False
    order: int = 0
    items: List['MenuItem'] = field(default_factory=list)
    parent_menu: Optional['Menu'] = field(default=None, repr=False)

    def __post_init__(self):
        """Convert string values to enums if necessary"""
        if isinstance(self.item_type, str):
            try:
                for enum_member in MenuItemType:
                    if enum_member.value == self.item_type.lower():
                        self.item_type = enum_member
                        break
            except ValueError:
                self.item_type = MenuItemType.LINK
        
        if isinstance(self.auth_requirement, str):
            try:
                for enum_member in AuthRequirement:
                    if enum_member.value == self.auth_requirement.lower():
                        self.auth_requirement = enum_member
                        break
            except ValueError:
                self.auth_requirement = AuthRequirement.ALL

    def mark_parent_dirty(self):
        """Mark parent menu as dirty"""
        if self.parent_menu:
            self.parent_menu.mark_dirty()

    @classmethod
    def from_dict(cls, data: Dict) -> 'MenuItem':
        """Create a MenuItem from a dictionary"""
        data_copy = data.copy()
        items_data = data_copy.pop('items', [])
        
        # Convert item_type to string value if it's an enum
        if 'item_type' in data_copy:
            if isinstance(data_copy['item_type'], MenuItemType):
                data_copy['item_type'] = data_copy['item_type'].value
            else:
                data_copy['item_type'] = str(data_copy['item_type']).lower()
        
        # Convert auth_requirement to string value if it's an enum
        if 'auth_requirement' in data_copy:
            if isinstance(data_copy['auth_requirement'], AuthRequirement):
                data_copy['auth_requirement'] = data_copy['auth_requirement'].value
            else:
                data_copy['auth_requirement'] = str(data_copy['auth_requirement']).lower()

        # Create the MenuItem
        item = cls(**data_copy)
        
        # Add nested items
        item.items = [cls.from_dict(item_data) for item_data in items_data]
        return item

    def to_dict(self) -> Dict:
        """Convert MenuItem to dictionary"""
        return {
            'id': self.id,
            'item_type': self.item_type.value,
            'menu_text': self.menu_text,
            'menu_class': self.menu_class,
            'hover_text': self.hover_text,
            'url': self.url,
            'auth_requirement': self.auth_requirement.value,
            'icon': self.icon,
            'icon_class': self.icon_class,
            'alt_icon': self.alt_icon,
            'alt_icon_class': self.alt_icon_class,
            'alt_status': self.alt_status,
            'secondary_text': self.secondary_text,
            'secondary_class': self.secondary_class,
            'new_window': self.new_window,
            'order': self.order,
            'items': [item.to_dict() for item in self.items],
        }
    
    def toggle_alt_state(self):
        """Toggle between normal and alternate states"""
        self.alt_status = not self.alt_status
        self.mark_parent_dirty()

    @property
    def current_icon(self):
        """Get the current icon based on alt_status"""
        return self.alt_icon if self.alt_status else self.icon

    @property
    def current_icon_class(self):
        """Get the current icon class based on alt_status"""
        return self.alt_icon_class if self.alt_status else self.icon_class

    def add_item(self, item: 'MenuItem', position: Optional[int] = None):
        """Add an item to a dropdown menu"""
        if self.item_type != MenuItemType.DROPDOWN:
            raise ValueError("Can only add items to DROPDOWN type menu items")
        
        item.parent_menu = self.parent_menu
        
        if position is not None:
            self.items.insert(position, item)
        else:
            self.items.append(item)
            
        self.mark_parent_dirty()

    def remove_item(self, item_id: str) -> bool:
        """Remove an item from a dropdown menu"""
        if self.item_type != MenuItemType.DROPDOWN:
            return False
        
        initial_length = len(self.items)
        self.items = [item for item in self.items if item.id != item_id]
        if len(self.items) < initial_length:
            self.mark_parent_dirty()
        return len(self.items) < initial_length

@dataclass
class Menu:
    menu_id: str
    items: List[MenuItem] = field(default_factory=list)
    _dirty: bool = field(default=False, init=False)

    def __post_init__(self):
        # Set parent reference for all items
        for item in self.items:
            item.parent_menu = self
            if item.item_type == MenuItemType.DROPDOWN:
                self._set_parent_recursive(item.items)

    def _set_parent_recursive(self, items):
        """Recursively set parent menu for nested items"""
        for item in items:
            item.parent_menu = self
            if item.item_type == MenuItemType.DROPDOWN:
                self._set_parent_recursive(item.items)

    @property
    def is_dirty(self):
        return self._dirty

    def mark_dirty(self):
        self._dirty = True

    def mark_clean(self):
        self._dirty = False

    def add_item(self, item: MenuItem):
        """Add an item and set its parent reference"""
        item.parent_menu = self
        self.items.append(item)
        self.mark_dirty()

    def to_dict(self) -> Dict:
        return {
            'menu_id': self.menu_id,
            'items': [item.to_dict() for item in self.items]
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Menu':
        # Handle both 'id' and 'menu_id' for backwards compatibility
        menu_id = data.get('menu_id') or data.get('id')
        return cls(
            menu_id=menu_id,
            items=[MenuItem.from_dict(item) for item in data.get('items', [])]
        )

class MenuManager:
    def __init__(self, session_manager: UserSessionManager):
        self.session: UserSessionManager = session_manager
        self._menus: Dict[str, Menu] = {}
        self._load_menus()

    def _load_menus(self):
        """Load menus from session"""
        stored_menus = self.session.get('menus', {})
        self._menus = {
            menu_id: Menu.from_dict(menu_data)
            for menu_id, menu_data in stored_menus.items()
        }

    def _save_menus(self):
        """Save menus to session"""
        menu_dict = {
            menu_id: menu.to_dict()
            for menu_id, menu in self._menus.items()
        }
        self.session['menus'] = menu_dict

    def create_menu(self, menu_id: str, name: str):
        """Create a new menu or update if it doesn't exist"""
        if not menu_id:
            raise ValueError("Menu ID cannot be empty")
        
        # Only create the menu if it doesn't exist
        if menu_id not in self._menus:
            logger.info(f"Creating new menu '{menu_id}'")
            new_menu = Menu(menu_id=menu_id, items=[])
            new_menu.mark_clean()
            self._menus[menu_id] = new_menu
            self._save_menus()

    def _reorder_menu(self, menu_id: str):
        """Reorder menu items by order field"""
        if menu_id in self._menus:
            self._menus[menu_id].items.sort(key=lambda x: x.order)
            self._menus[menu_id].mark_dirty()

    def add_item(
        self,
        menu_id: str,
        item: MenuItem,
        position: MenuPosition = MenuPosition.BOTTOM,
        relative_to: Optional[str] = None
    ):
        """Add a menu item at specified position"""
        if menu_id not in self._menus:
            raise ValueError(f"Menu '{menu_id}' does not exist")

        menu = self._menus[menu_id]
        
        # Set parent reference
        item.parent_menu = menu
        
        if position == MenuPosition.TOP:
            min_order = min((item.order for item in menu.items), default=0)
            item.order = min_order - 10
        elif position == MenuPosition.BOTTOM:
            max_order = max((item.order for item in menu.items), default=0)
            item.order = max_order + 10
        elif position in (MenuPosition.BEFORE, MenuPosition.AFTER) and relative_to:
            for existing in menu.items:
                if existing.id == relative_to:
                    if position == MenuPosition.BEFORE:
                        item.order = existing.order - 5
                    else:  # AFTER
                        item.order = existing.order + 5
                    break

        menu.add_item(item)
        self._reorder_menu(menu_id)
        self._save_menus()

    def remove_item(self, menu_id: str, item_id: str):
        """Remove a menu item"""
        if menu_id in self._menus:
            menu = self._menus[menu_id]
            menu.items = [item for item in menu.items if item.id != item_id]
            menu.mark_dirty()
            self._save_menus()

    def get_menu(self, menu_id: str, user_authenticated: bool = False) -> Optional[Menu]:
        """Get menu and its items, filtered by authentication status"""
        if menu_id not in self._menus:
            return None

        def filter_items(items: List[MenuItem]) -> List[MenuItem]:
            filtered = []
            for item in items:
                # Convert string values to enums if necessary
                if isinstance(item.item_type, str):
                    try:
                        for enum_member in MenuItemType:
                            if enum_member.value == item.item_type.lower():
                                item.item_type = enum_member
                                break
                    except ValueError:
                        item.item_type = MenuItemType.LINK

                if isinstance(item.auth_requirement, str):
                    try:
                        for enum_member in AuthRequirement:
                            if enum_member.value == item.auth_requirement.lower():
                                item.auth_requirement = enum_member
                                break
                    except ValueError:
                        item.auth_requirement = AuthRequirement.ALL

                if ((item.auth_requirement == AuthRequirement.ALL) or
                    (user_authenticated and item.auth_requirement == AuthRequirement.AUTH_ONLY) or
                    (not user_authenticated and item.auth_requirement == AuthRequirement.UNAUTH_ONLY)):
                    
                    # For dropdowns, recursively filter nested items
                    if item.item_type == MenuItemType.DROPDOWN:
                        filtered_nested = filter_items(item.items)
                        # Only include dropdown if it has visible items
                        if filtered_nested:
                            item_copy = MenuItem(
                                id=item.id,
                                item_type=item.item_type,
                                menu_text=item.menu_text,
                                menu_class=item.menu_class,
                                url=item.url,
                                auth_requirement=item.auth_requirement,
                                icon=item.icon,
                                icon_class=item.icon_class,
                                alt_icon=item.alt_icon,
                                alt_icon_class=item.alt_icon_class,
                                alt_status=item.alt_status,
                                secondary_text=item.secondary_text,
                                secondary_class=item.secondary_class,
                                new_window=item.new_window,
                                order=item.order,
                                items=filtered_nested
                            )
                            filtered.append(item_copy)
                    else:
                        filtered.append(item)
            return filtered

        menu = self._menus[menu_id]
        filtered_items = filter_items(menu.items)
        return Menu(menu_id=menu.menu_id, items=filtered_items)

    def add_dropdown_item(self, menu_id: str, parent_id: str, item: MenuItem):
        """Add an item to a dropdown menu"""
        if menu_id in self._menus:
            def add_to_dropdown(items: List[MenuItem]) -> bool:
                for menu_item in items:
                    if menu_item.id == parent_id:
                        if menu_item.item_type == MenuItemType.DROPDOWN:
                            menu_item.add_item(item)
                            return True
                        return False
                    elif menu_item.item_type == MenuItemType.DROPDOWN:
                        if add_to_dropdown(menu_item.items):
                            return True
                return False

            if add_to_dropdown(self._menus[menu_id].items):
                self._save_menus()

    def initialize_default_menus(self):
        """Initialize menus with defaults"""
        from app.defaults import DEFAULT_MENUS
        logger.info(f"Initializing default menus.")
        # Clear existing menus first
        self._menus.clear()
        
        for menu_id, menu_config in DEFAULT_MENUS.items():
            # Create the menu
            self.create_menu(menu_id, menu_config.get('menu_id', menu_config.get('id')))
            
            # Add all items
            for item_data in menu_config['items']:
                menu_item = MenuItem.from_dict(item_data)
                self.add_item(menu_id, menu_item)
        
        self._save_menus()

    @classmethod
    def ensure_default_menus(cls, session_manager: UserSessionManager):
        """Ensure default menus exist in session"""
        if 'menus' not in session_manager.session:
            menu_manager = cls(session_manager)
            menu_manager.initialize_default_menus()
            return menu_manager
        return cls(session_manager)
