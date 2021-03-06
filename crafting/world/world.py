# Crafting a gym-environment to simultate inventory managment
# Copyright (C) 2021 Mathïs FEDERICO <https://www.gnu.org/licenses/>

""" A World stiches together every non-player parts of the environment.

"""

from typing import List

from crafting.world.zones import Zone
from crafting.world.items import Item
from crafting.world.recipes import Recipe

class World():

    def __init__(self, zones: List[Zone], items: List[Item], recipes: List[Recipe]):
        # Zones
        self.zones = zones
        self.zone_from_id = {zone.zone_id: zone for zone in zones}
        self.zone_id_to_slot = {
            zone.zone_id: i for i, zone in enumerate(zones)
        }
        self.n_zones = len(zones)

        # Items
        self.items = items
        self.item_from_id = {item.item_id: item for item in items}
        self.item_id_to_slot = {
            item.item_id: i for i, item in enumerate(items)
        }
        self.n_items = len(items)

        # Foundable items
        self.foundable_items_ids = set()
        for zone in zones:
            for item_id in zone.items.keys():
                self.foundable_items_ids.add(item_id)

        self.foundable_items = [
            self.item_from_id[item_id]
            for item_id in self.foundable_items_ids
        ]
        self.foundable_items_id_to_slot = {
            item.item_id: i
            for i, item in enumerate(self.foundable_items)
        }
        self.n_foundable_items = len(self.foundable_items)

        # Recipes
        self.recipes = recipes
        self.recipes_from_id = {recipe.recipe_id: recipe for recipe in recipes}
        self.recipes_id_to_slot = {
            recipe.recipe_id: i for i, recipe in enumerate(recipes)
        }
        self.n_recipes = len(recipes)

        # Zone properties
        self.zone_properties = set()
        for zone in zones:
            for prop in zone.properties:
                self.zone_properties.add(prop)

        for recipe in recipes:
            for prop in recipe.added_properties:
                self.zone_properties.add(prop)

        self.zone_properties = list(self.zone_properties)
        self.n_zone_properties = len(self.zone_properties)

        self.n_actions = self.n_foundable_items + self.n_recipes + self.n_zones
