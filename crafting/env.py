# Crafting a gym-environment to simultate inventory managment
# Copyright (C) 2021 Mathïs FEDERICO <https://www.gnu.org/licenses/>

from typing import Tuple
from copy import deepcopy
from colorama import Fore, Style

import gym
import numpy as np
from gym.spaces import Discrete, Box

from crafting.world.world import World
from crafting.player.player import Player

class CraftingEnv(gym.Env):

    def __init__(self, world: World, player: Player, max_step: int=500, verbose: int=0):
        self.world = deepcopy(world)
        self.inital_world = deepcopy(world)

        self.player = deepcopy(player)
        self.inital_player = deepcopy(player)

        self.max_step = max_step
        self.steps = 1
        self.verbose = verbose

        # Action space
        # (get_item or use_recipe or move_to_zone)
        self.action_space = Discrete(
            self.world.n_foundable_items +\
            self.world.n_recipes +\
            self.world.n_zones
        )

        # Observation space
        # (n_stacks_per_item, inv_filled_proportion, one_hot_zone)
        self.observation_space = Box(
            low=np.array(
                [0 for _ in range(self.world.n_items)] +\
                [0 for _ in range(self.world.n_zones)] +\
                [0 for _ in range(self.world.n_zone_properties)]
            ),
            high=np.array(
                [np.inf for _ in range(self.world.n_items)] +\
                [1 for _ in range(self.world.n_zones)] +\
                [1 for _ in range(self.world.n_zone_properties)]
            ),
            dtype=np.float32
        )

        self.observation_legend = np.concatenate((
            [str(item) for item in self.world.items],
            [str(zone) for zone in self.world.zones],
            [str(prop) for prop in self.world.zone_properties]
        ))

    def action(self, action_type, identification) -> int:
        action_id = 0
        if action_type == 'get':
            action_id += self.world.foundable_items_id_to_slot[identification]
        elif action_type == 'craft':
            action_id = self.world.n_foundable_items
            action_id += self.world.recipes_id_to_slot[identification]
        elif action_type == 'move':
            action_id = self.world.n_foundable_items + self.world.n_recipes
            action_id += self.world.zone_id_to_slot[identification]
        return action_id

    def step(self, action: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray, dict]:
        reward = 0

        # Get an item
        if action < self.world.n_foundable_items:
            item_slot = action
            item = self.world.foundable_items[item_slot]
            tool = self.player.choose_tool(item)
            n_found = self.player.search_for(item, tool)
            if self.verbose > 0:
                status_msg = f'{Fore.GREEN}SUCCEDED' if n_found > 0 else f'{Fore.RED}FAILED'
                print(f'{status_msg}{Style.RESET_ALL} at getting {item}[{n_found}] with {tool}')

        # Craft a recipe
        start_index = self.world.n_foundable_items
        if 0 <= action - start_index < self.world.n_recipes:
            recipe_slot = action - start_index
            recipe = self.world.recipes[recipe_slot]
            success = self.player.craft(recipe)
            if self.verbose > 0:
                status_msg = f'{Fore.GREEN}SUCCEDED' if success else f'{Fore.RED}FAILED'
                print(f'{status_msg}{Style.RESET_ALL} at crafting {recipe}')

        # Change zone
        start_index = self.world.n_foundable_items + self.world.n_recipes
        if 0 <= action - start_index < self.world.n_zones:
            zone_slot = action - start_index
            zone = self.world.zones[zone_slot]
            self.player.move_to(zone)
            if self.verbose > 0:
                print(f'Moved to {zone}')

        # Synchronise world zone with player zone
        zone_slot = self.world.zone_id_to_slot[self.player.zone.zone_id]
        self.world.zones[zone_slot] = self.player.zone

        # Termination
        done = self.steps >= self.max_step

        # Infos
        infos = {
            'env_step': self.steps
        }

        self.steps += 1
        return self.get_observation(), reward, done, infos

    def get_observation(self) -> np.ndarray:
        one_hot_zone = np.zeros(self.world.n_zones, np.float32)
        zone_slot = self.world.zone_id_to_slot[self.player.zone.zone_id]
        one_hot_zone[zone_slot] = 1

        inventory_content = self.player.inventory.content

        zone_properties = np.zeros(self.world.n_zone_properties)
        for i, prop in enumerate(self.world.zone_properties):
            if prop in self.player.zone.properties:
                zone_properties[i] = self.player.zone.properties[prop]

        observation = np.concatenate(
            (inventory_content, one_hot_zone, zone_properties),
            axis=-1
        )

        return observation

    def reset(self) -> np.ndarray:
        self.steps = 0
        self.player = deepcopy(self.inital_player)
        self.world = deepcopy(self.inital_world)
        return self.get_observation()

    def render(self, mode='human'):
        print(self.player)

    def __call__(self, action):
        return self.step(action)