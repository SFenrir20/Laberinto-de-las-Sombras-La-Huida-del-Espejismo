import random
 
levelWidth = 100
levelHeight = 50

removeBlocks = 2386

### Easy Procedural Generation: Drunken Walk Algorithm
 
def getLevelRow():
    return ['x'] * levelWidth
 
def getWallLevel():
    return [getLevelRow() for _ in range(levelHeight)]
 
def drunkenWalkGenerator():
    drunk = {
        'removeBlocks': removeBlocks,
        'padding': 2,
        'x': int( 3 ),
        'y': int( 3 )
    }
    
    startCoordinate = [drunk['x'], drunk['y']]
    
    level = getWallLevel()
    
    level[drunk['y']][drunk['x']] = 'p'
    
    
    p_x = random.randint(drunk['padding'], levelWidth - 1 - drunk['padding'])
    p_y = random.randint(drunk['padding'], levelHeight - 1 - drunk['padding'])
    
    drunk['x'] = p_x
    drunk['y'] = p_y
    
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
    
    level[y][x] = 'e'
    endCoordinate = [x, y]
    
    return [level, startCoordinate, endCoordinate]

### Easy Pathfinding: Breadth-First Algorithm
 
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
 
### Improved Procedural Generation:
### Drunken Walk + Breadth First Algorithm
 
def generateLevels(amount):
    return [drunkenWalkGenerator() for _ in range(amount)]
 
def evaluateLevels(levels):
    evaluationScores = []
    
    for generatedLevel, startCoordinate, endCoordinate in levels:
        shortestSolution = getShortestPath(
            generatedLevel, 
            startCoordinate, 
            endCoordinate
        )
        
        evaluationScores.append(
            [len(shortestSolution), generatedLevel]
        )
    
    return evaluationScores
 
def generateBestLevel(amountOfLevels):
    levels = generateLevels(amountOfLevels)
    
    evaluationScores = evaluateLevels(levels)
    
    evaluationScores.sort()
    evaluationScores.reverse()
    
    score, bestLevel = evaluationScores.pop(0)
    
    return bestLevel

WORLD_MAP = generateBestLevel(100)

for row in WORLD_MAP:
    print("".join(row))