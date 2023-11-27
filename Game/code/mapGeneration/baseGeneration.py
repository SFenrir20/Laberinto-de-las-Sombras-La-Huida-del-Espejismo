import random
import numpy as np

levelWidth      = 20
levelHeight     = 20
removeBlocks    = 50
currentMap = []

def getCurrentMap():
    return currentMap

def getLevelRow(baseChar):
    return [baseChar] * levelWidth

def getWallLevel(baseChar):
    return [getLevelRow(baseChar) for _ in range(levelHeight)]

def drunkenWalkGenerator():
    drunk = {
        'removeBlocks': removeBlocks,
        'padding': 2,
        'x': int( 3 ),
        'y': int( 3 )
    }
    
    startCoordinate = [drunk['x'], drunk['y']]
    
    level = getWallLevel('x')
    
    while drunk['removeBlocks'] >= 0:
        x = drunk['x']
        y = drunk['y']
        
        if level[y][x] == 'x':
            level[y][x] = ' '
            drunk['removeBlocks'] -= 1
        
        roll = random.randint(1, 4)
        
        if roll == 1 and x > drunk['padding']:
            drunk['x'] -= 1
        if roll == 2 and x < levelWidth - 1 - drunk['padding']:
            drunk['x'] += 1
        if roll == 3 and y > drunk['padding']:
            drunk['y'] -= 1
        if roll == 4 and y < levelHeight - 1 - drunk['padding']:
            drunk['y'] += 1
    
    endCoordinate = [x, y]
    
    return [level, startCoordinate, endCoordinate]

def generateCounting(num, total):
    map = drunkenWalkGenerator()
    porcentaje_completado = (num + 1) / total * 100
    mensaje = f"Generando mapas ({num+1}/{total}) - Completado: {porcentaje_completado:.2f}%"
    print(mensaje, end='\r')
    return map
    
def generateExitMap(exitCord):
    global currentMap
    
    exitMap = getWallLevel(' ')
    
    exitMap[exitCord[1]][exitCord[0]] = '00'
    currentMap[exitCord[1]][exitCord[0]] = '00'
    
    return exitMap

def empty2x2(cord):
    return currentMap[cord[1]][cord[0]] == ' ' and currentMap[cord[1]+1][cord[0]] == ' ' and currentMap[cord[1]][cord[0]+1] == ' ' and currentMap[cord[1]+1][cord[0]+1] == ' '

def fill2x2(map, cord):
    map[cord[1]][cord[0]] = 'o'
    map[cord[1]][cord[0]+1] = 'o'
    map[cord[1]+1][cord[0]] = 'o'
    map[cord[1]+1][cord[0]+1] = 'o'
    
def placeEnemySpawn(monstersMap, numMonsters):
    emptyLocations = [(x, y) for y in range(levelHeight) for x in range(levelWidth) if currentMap[y][x] == ' ']
    
    if numMonsters > len(emptyLocations):
        numMonsters = len(emptyLocations)
    
    random_empty_locations = random.sample(emptyLocations, numMonsters)
    
    for x, y in random_empty_locations:
        monstersMap[y][x] = 'm'
        currentMap[y][x] = 'm'

def generateMonstersMap(numMonsters):
    monstersMap = getWallLevel(' ')
    #placeEnemies(monstersMap, numMonsters)
    placeEnemySpawn(monstersMap, numMonsters)
    return monstersMap
 
def getNextMoves(x, y):
    return {
        'left':  [x-1, y], 
        'right': [x+1, y],
        'up':  [x, y-1],
        'down':  [x, y+1]
    }.values()
 
def getShortestPath(level, startCoordinate, endCoordinate):
    searchPaths = [[startCoordinate]]
    visitedCoordinates = [startCoordinate]
    
    while searchPaths != []:
        currentPath = searchPaths.pop(0)
        currentCoordinate = currentPath[-1]
        
        currentX, currentY = currentCoordinate
        
        if currentCoordinate == endCoordinate:
            return currentPath
        
        for nextCoordinate in getNextMoves(currentX, currentY):
            nextX, nextY = nextCoordinate
            
            if nextX < 0 or nextX >= levelWidth:
                continue
            
            if nextY < 0 or nextY >= levelHeight:
                continue
            
            if nextCoordinate in visitedCoordinates:
                continue
            
            if level[nextY][nextX] == 'x':
                continue
            
            searchPaths.append(currentPath + [nextCoordinate])
            visitedCoordinates += [nextCoordinate]
    
    return []
 
def generateLevels(amount):
    return [generateCounting(i, amount) for i in range(amount)]
 
def evaluateLevels(levels):
    evaluationScores = []
    
    i=0
    
    print()
    
    for i, (generatedLevel, startCoordinate, endCoordinate) in enumerate(levels):
        porcentaje_completado = (i + 1) / len(levels) * 100
        mensaje = f"Evaluando mapas ({i+1}/{len(levels)}) - Completado: {porcentaje_completado:.2f}%"
        print(mensaje, end='\r')
        
        shortestSolution = getShortestPath(
            generatedLevel, 
            startCoordinate, 
            endCoordinate
        )
        
        evaluationScores.append(
            [len(shortestSolution), generatedLevel, endCoordinate]
        )
    
    print()
    
    return evaluationScores
 
def generateBestLevel(amountOfLevels, width, height, blocks):
    
    global levelWidth
    global levelHeight
    global removeBlocks
    global currentMap
    
    levelWidth      = width
    levelHeight     = height
    removeBlocks    = blocks
    
    levels = generateLevels(amountOfLevels)
    
    evaluationScores = evaluateLevels(levels)
    
    evaluationScores.sort(reverse = True)
    
    score, bestLevel, endCoordinate = evaluationScores.pop(0)
    
    print("Mapa seleccionado")
    
    currentMap = np.copy(bestLevel)
    
    return [bestLevel, endCoordinate]