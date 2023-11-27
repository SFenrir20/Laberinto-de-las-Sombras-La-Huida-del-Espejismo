from mapGeneration.baseGeneration import *
# window setup
WIDTH = 1280
HEIGTH = 720
FPS = 60
TILESIZE = 64

# map setup
ITERATIONS = 100
LEVELWIDTH = 55
LEVELHEIGTH = 35
REMOVEBLOCKS = 789
ENEMYSPAWNS = 20
BOSSSPAWNS = 5

BASE_MAP = generateBestLevel(ITERATIONS, LEVELWIDTH, LEVELHEIGTH, REMOVEBLOCKS)
EXIT_CORD = BASE_MAP[2]
BASE_WALLS = BASE_MAP[0]
generateSecureZone(BASE_MAP[1])
INTERACTION_MAP = generateExitMap(EXIT_CORD)
MONSTERS_MAP = generateBossMap(ENEMYSPAWNS)
BOSS_MAP = generateBossMap(BOSSSPAWNS)
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
    'sword': {'cooldown': 20, 'damage': 50, 'graphic': 'Game/graphics/weapons/sword/full.png'}
}

# enemies
monster_data = {
    'racoon': {'health': 500, 'exp': 300, 'damage': 30, 'attack_type': 'claw', 'speed': 5, 'resistance': 3, 'attack_radius': 120, 'notice_radius': 400},
    'spirit': {'health': 100, 'exp': 50, 'damage': 5, 'attack_type': 'thunder', 'speed': 4, 'resistance': 3, 'attack_radius': 60, 'notice_radius': 350}
}

for row in BASE_WALLS:
    print("".join(row))

for row in INTERACTION_MAP:
    print("".join(row))

for row in MONSTERS_MAP:
    print("".join(row))
    
for row in CURRENT_MAP:
    print("".join(row))