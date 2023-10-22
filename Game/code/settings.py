from mapGeneration.baseGeneration import generateBestLevel
# game setup
WIDTH    = 1280	
HEIGTH   = 720
FPS      = 60
TILESIZE = 64

WORLD_MAP = generateBestLevel(1)

for row in WORLD_MAP:
    print("".join(row))
