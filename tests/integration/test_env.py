# Crafting a gym-environment to simultate inventory managment
# Copyright (C) 2021 Mathïs FEDERICO <https://www.gnu.org/licenses/>

import pytest
import numpy as np

from crafting.env import CraftingEnv

from crafting.world.world import World
from crafting.world.items import Item, Tool, ItemStack
from crafting.world.recipes import Recipe
from crafting.world.zones import Zone

from crafting.player.inventory import Inventory
from crafting.player.player import Player

AIR = Tool(0, 'air')
WOODEN_PICKAXE = Tool(18, 'wooden_pickaxe')
DIRT = Item(3, 'dirt', max_stack=64)
WOOD = Item(14, 'wood', max_stack=64)
STICK = Item(280, name='stick', max_stack=64)
WOOD_PLANK = Item(5, name='plank', max_stack=64)
STONE = Item(1, 'stone', max_stack=64)

R_WOOD_PLANK = Recipe(
    recipe_id=5,
    inputs=[ItemStack(WOOD, 1)],
    outputs=[ItemStack(WOOD_PLANK, 4)],
    needed_properties=None,
    added_properties=None
)

R_STICK = Recipe(
    recipe_id=8,
    inputs=[ItemStack(WOOD_PLANK, 2)],
    outputs=[ItemStack(STICK, 4)],
    needed_properties=None,
    added_properties=None
)

R_CRAFTING_TABLE = Recipe(
    recipe_id=28,
    inputs=[ItemStack(WOOD_PLANK, 4)],
    added_properties={'has_crafting': True}
)

R_WOODEN_PICKAXE = Recipe(
    recipe_id=3,
    inputs=[ItemStack(WOOD_PLANK, 3), ItemStack(STICK, 2)],
    outputs=[ItemStack(WOODEN_PICKAXE)],
    needed_properties={'has_crafting': True},
    added_properties=None
)

ITEMS = [DIRT, WOOD, STONE, WOOD_PLANK, STICK, AIR, WOODEN_PICKAXE]
RECIPES = [R_WOOD_PLANK, R_CRAFTING_TABLE, R_STICK, R_WOODEN_PICKAXE]

FOREST = Zone(0, 'forest', {
        DIRT.item_id: [AIR],
        WOOD.item_id: None
})

UNDERGROUND = Zone(1, 'underground', {
    STONE.item_id: [WOODEN_PICKAXE],
    DIRT.item_id: [AIR]
})


@pytest.fixture
def world():
    return World([FOREST, UNDERGROUND], ITEMS, RECIPES)

@pytest.fixture
def inv():
    return Inventory(ITEMS)

class DummyPlayer(Player):

    def choose_tool(self, item):
        if WOODEN_PICKAXE in self.inventory:
            return WOODEN_PICKAXE
        return None

@pytest.fixture
def player(inv):
    return DummyPlayer(inv, FOREST, 'dummy')

def test_env_obtain_stone(world, player):
    env = CraftingEnv(world, player, max_step=50, verbose=1)

    print(env.world.foundable_items)
    print(env.world.recipes)
    print(env.world.zones)
    print(env.observation_legend)

    print(env.render('ansi'))
    observation, _, _, _ = env(env.action('get', WOOD.item_id)) #(Success)

    print(observation)
    expected_obs = [0, 1, 0, 0, 0, 0, 0, 1, 0, 0]
    if np.any(observation != expected_obs):
        raise ValueError('Unexpected observation')
    print(env.render('ansi'))

    observation, _, _, _ = env(env.action('get', DIRT.item_id)) #(Fail)

    print(observation)
    expected_obs = [0, 1, 0, 0, 0, 0, 0, 1, 0, 0]
    if np.any(observation != expected_obs):
        raise ValueError('Unexpected observation')
    print(env.render('ansi'))

    observation, _, _, _ = env(env.action('craft', WOOD_PLANK.item_id)) #(Success)

    print(observation)
    expected_obs = [0, 0, 0, 4, 0, 0, 0, 1, 0, 0]
    if np.any(observation != expected_obs):
        raise ValueError('Unexpected observation')
    print(env.render('ansi'))

    observation, _, _, _ = env(env.action('craft', WOOD_PLANK.item_id)) #(Fail)

    print(observation)
    expected_obs = [0, 0, 0, 4, 0, 0, 0, 1, 0, 0]
    if np.any(observation != expected_obs):
        raise ValueError('Unexpected observation')
    print(env.render('ansi'))

    for _ in range(2):
        observation, _, _, _ = env(env.action('get', WOOD.item_id))
        observation, _, _, _ = env(env.action('craft', WOOD_PLANK.item_id))

    print(observation)
    expected_obs = [0, 0, 0, 12, 0, 0, 0, 1, 0, 0]
    if np.any(observation != expected_obs):
        raise ValueError('Unexpected observation')
    print(env.render('ansi'))

    observation, _, _, _ = env(env.action('move', UNDERGROUND.zone_id))

    print(observation)
    expected_obs = [0, 0, 0, 12, 0, 0, 0, 0, 1, 0]
    if np.any(observation != expected_obs):
        raise ValueError('Unexpected observation')
    print(env.render('ansi'))

    observation, _, _, _ = env(env.action('craft', R_WOODEN_PICKAXE.recipe_id)) #(Fail)

    print(observation)
    expected_obs = [0, 0, 0, 12, 0, 0, 0, 0, 1, 0]
    if np.any(observation != expected_obs):
        raise ValueError('Unexpected observation')
    print(env.render('ansi'))

    observation, _, _, _ = env(env.action('craft', R_CRAFTING_TABLE.recipe_id)) #(Success)

    print(observation)
    expected_obs = [0, 0, 0, 8, 0, 0, 0, 0, 1, 1]
    if np.any(observation != expected_obs):
        raise ValueError('Unexpected observation')
    print(env.render('ansi'))

    observation, _, _, _ = env(env.action('get', STONE.item_id)) #(Fail)

    print(observation)
    expected_obs = [0, 0, 0, 8, 0, 0, 0, 0, 1, 1]
    if np.any(observation != expected_obs):
        raise ValueError('Unexpected observation')
    print(env.render('ansi'))

    observation, _, _, _ = env(env.action('craft', R_STICK.recipe_id)) #(Success)
    observation, _, _, _ = env(env.action('craft', R_WOODEN_PICKAXE.recipe_id)) #(Success)

    print(observation)
    expected_obs = [0, 0, 0, 3, 2, 0, 1, 0, 1, 1]
    if np.any(observation != expected_obs):
        raise ValueError('Unexpected observation')
    print(env.render('ansi'))

    observation, _, _, _ = env(env.action('get', STONE.item_id)) #(Success)

    print(observation)
    expected_obs = [0, 0, 1, 3, 2, 0, 1, 0, 1, 1]
    if np.any(observation != expected_obs):
        raise ValueError('Unexpected observation')
    print(env.render('ansi'))

def test_env_zone_consistency(world, player):
    env = CraftingEnv(world, player, max_step=50, verbose=1)

    env(env.action('get', WOOD.item_id))
    env(env.action('craft', R_WOOD_PLANK.recipe_id))
    env(env.action('craft', R_CRAFTING_TABLE.recipe_id))

    if 'has_crafting' not in env.player.zone.properties:
        raise ValueError('FOREST should have the has_crafting property')

    env(env.action('move', UNDERGROUND.zone_id))
    if 'has_crafting' in env.player.zone.properties:
        raise ValueError('UNDERGROUND should not have the has_crafting property')

    env(env.action('move', FOREST.zone_id))
    if 'has_crafting' not in env.player.zone.properties:
        raise ValueError('FOREST should still have the has_crafting property')
