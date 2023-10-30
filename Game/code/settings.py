from mapGeneration.baseGeneration import *
# window setup
WIDTH = 1280
HEIGTH = 720
FPS = 60
TILESIZE = 64

# map setup
ITERATIONS = 10
LEVELWIDTH = 50
LEVELHEIGTH = 30
REMOVEBLOCKS = 683
ENEMYSPAWNS = 10

BASE_MAP = generateBestLevel(ITERATIONS, LEVELWIDTH, LEVELHEIGTH, REMOVEBLOCKS)
EXIT_CORD = BASE_MAP[1]
BASE_WALLS = BASE_MAP[0]
INTERACTION_MAP = generateExitMap(EXIT_CORD)
MONSTERS_MAP = generateMonstersMap(ENEMYSPAWNS)
CURRENT_MAP = getCurrentMap()

BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200
ENERGY_BAR_WIDTH = 140
ITEM_BOX_SIZE = 80

WATER_COLOR = '#71ddee'
UI_BG_COLOR = '#222222'
UI_BORDER_COLOR = '#111111'
TEXT_COLOR = '#EEEEEE'

HEALTH_COLOR = '#6a1d13'
ENERGY_COLOR = '#4a653e'
UI_BORDER_COLOR_ACTIVE = 'gold'

# weapons
weapon_data = {
    'sword': {'cooldown': 100, 'damage': 15, 'graphic': 'Game/graphics/weapons/sword/full.png'}
}

for row in BASE_WALLS:
    print("".join(row))

for row in INTERACTION_MAP:
    print("".join(row))

for row in MONSTERS_MAP:
    print("".join(row))
    
for row in CURRENT_MAP:
    print("".join(row))