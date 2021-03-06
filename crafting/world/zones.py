# Crafting a gym-environment to simultate inventory managment
# Copyright (C) 2021 Mathïs FEDERICO <https://www.gnu.org/licenses/>

""" Zone

Gives an abstract way of doing spacialization.
The Zones have special properties for finding or crafting items.

"""

from typing import List, Dict

from crafting.world.items import Item, Tool, ItemStack

class Zone():

    """ Zones are to represent abstract places in the world.

    Zone have specific properties that can change how items can be gathered
    and how craftings are done.

    By default

    Attributes:
        zone_id (int): Unique zone identification number.
        name (str): Zone name.
        items (dict): Dictionary associating an item_id
            with the tools needed to gather it and how efficient it is.
        properties (dict): Dictionary of properties.

    """

    def __init__(self, zone_id: int, name: str, items: Dict[int, Item], properties: dict=None):
        """ Zones are to represent abstract places in the world.

        Zone have specific properties that can change how items can be gathered
        and how craftings are done.

        Args:
            zone_id: Unique zone identification number.
            name: Zone name.
            items: Dictionary mapping an item_id to
                the tools needed to gather it.
            properties: List of all properties names.

        """
        self.zone_id = zone_id
        self.name = name
        self.items = items
        self.properties = properties if properties is not None else {}

    def search_for(self, item:Item, tool:Tool=None) -> List[ItemStack]:
        """ Searches for the given item using a tool

        Args:
            item: The item to look for.
            tool: The tool to use.

        Return:
            The found item stacks.

        """
        if item.item_id in self.items:

            usable_tools = self.items[item.item_id]

            # If no tool is needed, just gather items
            if usable_tools is None:
                return [ItemStack(item)]

            # If a tool is needed, gather items relative to used tool
            usable_tools_ids = [usable_tool.item_id for usable_tool in usable_tools]
            if tool is not None and tool.item_id in usable_tools_ids:
                return tool.use(item)

        return []

    def __str__(self):
        return f"{self.name.capitalize()}({self.zone_id})"

    def __repr__(self):
        name = f"{self.name.capitalize()}({self.zone_id})"
        if len(self.properties) > 0:
            name += str(self.properties)
        if len(self.items) > 0:
            name += str(list(self.items.keys()))
        return name
