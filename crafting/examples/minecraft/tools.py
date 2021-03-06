# Crafting a gym-environment to simultate inventory managment
# Copyright (C) 2021 Mathïs FEDERICO <https://www.gnu.org/licenses/>

""" Minecraft Tools

All used minecraft tools

"""

from numpy import inf

from crafting.examples.minecraft.abc import McTool

AIR = McTool(0, 'air', durability=inf, speed=1) #: AIR
WOODEN_PICKAXE = McTool(270, 'wooden_pickaxe', durability=59, speed=2) #: WOODEN_PICKAXE
WOODEN_AXE = McTool(271, 'wooden_axe', durability=59, speed=2) #: WOODEN_AXE
WOODEN_SWORD = McTool(268, 'wooden_sword', durability=59, speed=2) #: WOODEN_SWORD
STONE_PICKAXE = McTool(274, 'stone_pickaxe', durability=131, speed=4) #: STONE_PICKAXE
STONE_AXE = McTool(275, 'stone_axe', durability=131, speed=4) #: STONE_AXE
STONE_SWORD = McTool(272, 'stone_sword', durability=131, speed=4) #: STONE_SWORD
IRON_PICKAXE = McTool(257, 'iron_pickaxe', durability=256, speed=6) #: IRON_PICKAXE
IRON_AXE = McTool(258, 'iron_axe', durability=256, speed=6) #: IRON_AXE
IRON_SWORD = McTool(267, 'iron_sword', durability=256, speed=6) #: IRON_SWORD
GOLD_PICKAXE = McTool(285, 'gold_pickaxe', durability=32, speed=12) #: GOLD_PICKAXE
GOLD_AXE = McTool(286, 'gold_axe', durability=32, speed=12) #: GOLD_AXE
GOLD_SWORD = McTool(283, 'gold_sword', durability=32, speed=12) #: GOLD_SWORD
DIAMOND_PICKAXE = McTool(278, 'diamond_pickaxe', durability=1561, speed=8) #: DIAMOND_PICKAXE
DIAMOND_AXE = McTool(279, 'diamond_axe', durability=1561, speed=8) #: DIAMOND_AXE
DIAMOND_SWORD = McTool(276, 'diamond_sword', durability=1561, speed=8) #: DIAMOND_SWORD

# Tools groups
PICKAXES = [
    WOODEN_PICKAXE, STONE_PICKAXE, IRON_PICKAXE,
    GOLD_PICKAXE, DIAMOND_PICKAXE
]

AXES = [
    WOODEN_AXE, STONE_AXE,
    IRON_AXE, GOLD_AXE, DIAMOND_AXE
]

SWORDS = [
    WOODEN_SWORD, STONE_SWORD, IRON_SWORD,
    GOLD_SWORD, DIAMOND_SWORD
]

MC_TOOLS = [AIR] + PICKAXES + AXES + SWORDS

if __name__ == "__main__":
    print('Tools:', str(MC_TOOLS))
