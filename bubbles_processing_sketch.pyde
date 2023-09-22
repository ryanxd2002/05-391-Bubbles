import random

# Spinoff of https://github.com/ryanxd2002/Bubbles
# Added powerups, hover effect, and pause button. Also bug fixes and aesthetics. 

def setup():
    global score, bubbles, radius, newBubbleTimer, poppedBubbles, gameOver, change, powerups, bubbleColor, activePowerup, paused
    size(400, 400)
    score = 0
    change = 1
    newBubbleTimer = 0
    radius = random.randint(25, 35)
    bubbleColor = color(255, 255, 0)
    
    bubbles = []
    poppedBubbles = []
    powerups = []
    
    activePowerup = None
    gameOver = False
    paused = False

def draw():
    global newBubbleTimer, change, gameOver, radius, bubbles, bubbleColor, paused
    if paused:
        fill(255, 255, 0)
        noStroke
        rect(0, 0, 400, 400)
        textSize(25)
        fill(0, 0, 0)
        text("Game Paused", 120, 200)
        return
    
    background(255)
    if gameOver:
        textSize(25)
        fill(0)
        text("GAME OVER", 130, 100)
        text("SCORE: " + str(score), 145, 125)
        text("Press r to restart", 110, 150)
        return
    
    new_bubbles = []
    for x, y, r in bubbles:
        if y + r > 0:
            new_y = y - change
            new_bubbles.append((x, new_y, r))
            drawBubble(x, new_y, r, bubbleColor)
        else:
            gameOver = True
    
    bubbles = new_bubbles
    
    newBubbleTimer += 1
    if newBubbleTimer % 60 == 0:
        radius = random.randint(25, 35)
        x = random.randint(radius, 400 - radius)
        bubbles.append((x, 400 - radius, radius))
        
    if newBubbleTimer % 100 == 0:
        change += 0.25
        
    if newBubbleTimer % 600 == 0:  # Create powerups periodically
        createPowerup(random.choice(['slow', 'color']))
    
    textSize(25)
    fill(0)
    text("Score: " + str(score), 150, 30)
    text("Active Powerup: " + str(activePowerup), 70, 60)
    text("Press o to use", 120, 90)
    
    for x, y, type in powerups:
        drawPowerup(x, y, type)

def mousePressed():
    global score, activePowerup, paused
    if paused:
        return 
    
    to_remove = []
    for x, y, r in bubbles:
        if dist(mouseX, mouseY, x, y) <= r:
            to_remove.append((x, y, r))
            score += 1
            
    for bubble in to_remove:
        bubbles.remove(bubble)
    
    for x, y, type in powerups:
        if dist(mouseX, mouseY, x, y) <= 20:
            activePowerup = type
            powerups.remove((x, y, type))
            
def keyPressed():
    global change, bubbleColor, activePowerup, paused
    if key == 'r':
        setup()
    elif key == 'p':
        paused = not paused
        return
    elif key == 'o' and activePowerup:
        if activePowerup == 'slow':
            change = 1
        elif activePowerup == 'color':
            bubbleColor = color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        activePowerup = None
        
def drawBubble(x, y, r, color):
    fill(color)
    stroke(0, 0, 255)
    d = dist(mouseX, mouseY, x, y)
    weight = 1
    if d <= r:
        weight = map(d, 0, r, 5, 1)
    strokeWeight(weight)
    ellipse(x, y, r * 2, r * 2)

def drawPowerup(x, y, type):
    fill(0, 255, 0)
    ellipse(x, y, 40, 40)
    fill(0)
    if type == 'color':
        text('C', x - 8, y + 8)
    elif type == 'slow':
        text('S', x - 8, y + 8)

def createPowerup(type):
    x = random.randint(20, 380)
    y = random.randint(20, 380)
    powerups.append((x, y, type))
