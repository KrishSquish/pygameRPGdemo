#importing libraraies
import pygame, time, random,math

pygame.init()


screen = pygame.display.set_mode((1280,720))
#clock and timing
FPS = 60
clock = pygame.time.Clock()
prevTime = time.time()
frameNum = 0

gameState = "Main"

#Names the window
pygame.display.set_caption(("RPG Game"))

#loading sprites
walkLeft1 = pygame.image.load("assets\\walkingImages\\leftWalk1.png")
walkLeft2 = pygame.image.load("assets\\walkingImages\\leftWalk2.png")
walkLeft3 = pygame.image.load("assets\\walkingImages\\leftWalk3.png")

walkRight1 = pygame.image.load("assets\\walkingImages\\rightWalk1.png")
walkRight2 = pygame.image.load("assets\\walkingImages\\rightWalk2.png")
walkRight3 = pygame.image.load("assets\\walkingImages\\rightWalk3.png")

walkFront1 = pygame.image.load("assets\\walkingImages\\frontWalk1.png")
walkFront2 = pygame.image.load("assets\\walkingImages\\frontWalk2.png")
walkFront3 = pygame.image.load("assets\\walkingImages\\frontWalk3.png")

walkBack1 = pygame.image.load("assets\\walkingImages\\backWalk1.png")
walkBack2 = pygame.image.load("assets\\walkingImages\\backWalk2.png")
walkBack3 = pygame.image.load("assets\\walkingImages\\backWalk3.png")

tiles = []
for i in range(0, 35):
    if i <10:
        tile = pygame.image.load(f'assets\\tiles\\tile00{i}.png')
    if i >= 10:
        tile = pygame.image.load(f'assets\\tiles\\tile0{i}.png')
    tiles.append(tile)

walkLeftList = [walkLeft1,walkLeft2,walkLeft1,walkLeft3 ]
walkRightList = [walkRight1,walkRight2,walkRight1,walkRight3]
walkFrontList = [walkFront1,walkFront2,walkFront1,walkFront3]
walkBackList = [walkBack1,walkBack2,walkBack1,walkBack3]

#making map/terrain
map = [
    ['14','15','15','15','15','15','15','15','15','15','15','15','15','15','15','15','15','15','15','15','15','15','15','15','16'],
    ['20','21','21','21','21','21','21','21','21','21','21','21','21','21','21','21','34','21','21','21','21','21','21','21','22'],
    ['20','21','21','21','21','21','21','21','21','21','21','21','21','32','21','21','21','21','34','21','21','21','21','33','22'],
    ['20','21','21','34','21','21','21','21','21','21','21','21','21','21','21','21','32','21','21','21','21','21','21','21','22'],
    ['20','21','21','21','21','21','21','21','21','21','21','21','21','21','21','21','21','21','21','21','21','21','21','21','22'],
    ['20','21','21','21','21','21','21','21','21','21','21','21','21','21','21','21','21','21','21','21','21','21','34','21','22'],
    ['20','21','21','21','32','21','21','21','21','21','21','21','21','21','21','21','21','21','21','33','21','21','21','21','22'],
    ['20','21','21','21','21','21','21','21','21','21','21','21','21','21','21','21','21','21','21','21','21','21','21','21','22'],
    ['20','21','21','21','21','21','21','21','21','21','21','21','21','21','21','21','21','21','21','21','21','33','21','34','22'],
    ['20','21','21','21','21','21','21','21','33','21','21','21','21','21','21','21','21','21','21','21','21','21','21','21','22'],
    ['20','21','21','21','21','21','21','21','33','33','21','21','21','21','21','21','33','21','21','21','21','21','21','21','22'],
    ['20','21','21','21','21','21','21','21','21','21','21','21','21','21','21','21','21','21','21','21','21','21','21','21','22'],
    ['20','21','21','21','21','21','21','21','21','21','21','21','21','21','21','21','21','21','21','21','21','21','21','32','22'],
    ['26','27','27','27','27','27','27','27','27','27','27','27','27','27','27','27','27','27','27','27','27','27','27','27','28']
]

tileSize = 50

#scaling images
#need diff loops because one is by a percent, other is fixed amount
def scaling (list,scalingAmount):
    for i in range(len(list)):
        list[i] = pygame.transform.scale(list[i], 
        (int(list[i].get_width()*scalingAmount), int(list[i].get_height()*scalingAmount)))

for i in range (len(tiles)):
    tiles[i] = pygame.transform.scale(tiles[i],(50,50))

scaling(walkLeftList,2)
scaling(walkRightList,2)
scaling(walkFrontList,2)
scaling(walkBackList,2)

currentWalkList = walkFrontList

#classes for interactable objects
class Player():
    def __init__(self):
        self.x = 220
        self.y = 210
        self.img = walkFront1
        self.pos = (self.x,self.y)
        self.speedX = 0
        self.speedY = 0 
        self.health = 100
        self.baseHealth = 100
        self.attackPower = 0
        self.attacking = False
        self.hitbox = (self.x,self.y, 50,100)    
        self.hitbox = pygame.draw.rect(screen,"red",self.hitbox,1 )
    def originalPlace(self):
        self.originX = self.x
        self.originY = self.y

class Enemy():
    def __init__(self,name,x,y):
        self.x = x
        self.y = y
        self.name = name
        self.img = pygame.image.load("assets\\something.png")
        self.img = pygame.transform.scale(self.img,(100,100))
        self.pos = (self.x,self.y)
        self.attackPower = None
        self.attacking = False
        self.health = 100
        self.width = 40
        self.height = 70 
        self.hitbox = (self.x+30,self.y+17,self.width,self.height)
        self.hitbox = pygame.draw.rect(screen,"purple",self.hitbox,1)  
        self.detectPlayerHitbox = pygame.draw.circle(screen,"blue",(self.x+self.width,self.y+self.height),75) 
        enemyList.append(self)
        enemyHBList.append(self.hitbox)
        enemyPlayerDetectHB.append(self.detectPlayerHitbox)
    def drawHB(self):
        self.hitbox = pygame.draw.rect(screen,"purple",self.hitbox,1)
        self.detectPlayerHitbox = pygame.draw.circle(screen,"blue",(self.x,self.y),75) 


class NPC():
    def __init__(self,x,y,npcImage):
        self.x = x
        self.y = y
        self.img = pygame.image.load(npcImage)
        self.img = pygame.transform.scale(self.img,(37,54))
        self.talkedTo = False
        self.hitbox = None
        self.dialog = None

class Potion():
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.img = pygame.image.load("assets\\healthPotion.png")
        self.img = pygame.transform.scale(self.img,(45,45))
        self.pickedUp = False
        self.hitbox = None     

#creating the objects
player = Player()

enemyHBList = []
enemyList = []
enemyPlayerDetectHB = []

something1 = Enemy("name of enemy 1",100,500)
something2 = Enemy("name of enemy 2",500,100)

mari = NPC(300,300,"assets\\npc.png")
mari.dialog = ["Hello Player!","I'm an NPC", "Thanks for talking with me"]

healthPotion = Potion(500,500)
healthPotion.hitbox = (healthPotion.x+10,healthPotion.y+5, 26,34)    

dialogNumber = 0
returnKeyPressed = False

#looping game
running = True
while running:
    def drawSprite(className):
        screen.blit(className.img, (className.x,className.y))

    #health bar requirement 2
    def drawHealthBar(x,y):
        pygame.draw.rect(screen,"white",(x-2,y-2,player.baseHealth*2+5,25))
        pygame.draw.rect(screen,"black",(x,y,player.baseHealth*2,20))
        pygame.draw.rect(screen,"red",(x,y,player.health*2,20))
    clock.tick(FPS)

    #gets current time
    now = time.time()
    #calc time between frames
    deltaTime = now - prevTime
    #sets the previous time to the time of the last frame
    prevTime = now
    frameNum +=1
    if frameNum >= 60:
        frameNum = 0
    
    #creating boxes
    player.hitbox = (player.x+9,player.y, 45,65)    
    player.hitbox = pygame.draw.rect(screen,"red",player.hitbox,1 )
    healthPotion.hitbox = pygame.draw.rect(screen,"green",healthPotion.hitbox,1 )
    mari.hitbox = (mari.x-2,mari.y-1,50,50)
    mari.hitbox = pygame.draw.rect(screen,"purple",mari.hitbox,1)

    for i in enemyList:
        i.drawHB

    screen.fill(("lightskyblue"))

    if gameState == "Main":
        #requirement 5
        def displayNpcText():
            global dialogNumber, returnKeyPressed
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RETURN and returnKeyPressed == False:
                    dialogNumber +=1
                    if dialogNumber == len(mari.dialog):
                        dialogNumber = len(mari.dialog)-1
                    returnKeyPressed = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    returnKeyPressed = False

            dialogBox = pygame.image.load('assets\\dialogBox.png')
            screen.blit(dialogBox,(320,600))
            fontObj = pygame.font.Font("C:\Windows\Fonts\Arial.ttf",25) 
            textObj = fontObj.render(mari.dialog[dialogNumber],True,"white","black") 
            textRect = textObj.get_rect()
            textRect.center = (610,650)
            screen.blit(textObj,textRect)
        
        tileY = 0
        for row in map:
            tileX = 0
            for tile in row:
                    screen.blit(tiles[int(tile)], (tileX * tileSize, tileY * tileSize))
                    tileX += 1
            tileY += 1

        #player movement
        if not player.hitbox.collidelistall(enemyPlayerDetectHB):
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                player.speedX = -50 *deltaTime
                currentWalkList = walkLeftList
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                player.speedX = 50 *deltaTime
                currentWalkList = walkRightList
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                player.speedY = -50 *deltaTime
                currentWalkList = walkBackList
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                player.speedY = 50 *deltaTime
                currentWalkList = walkFrontList

        player.img = currentWalkList[frameNum // 15]

        player.x += player.speedX
        player.y += player.speedY
        
        #grid system challenge 1
        if round(player.x) % 50 == 44 and not keys[pygame.K_LEFT] and not keys[pygame.K_a] and not keys[pygame.K_RIGHT] and not keys[pygame.K_d] and not keys[pygame.K_UP] and not keys[pygame.K_w] and not keys[pygame.K_DOWN] and not keys[pygame.K_s]:
            player.speedX = 0
        if round(player.y) % 50 == 15 and not keys[pygame.K_LEFT] and not keys[pygame.K_a] and not keys[pygame.K_RIGHT] and not keys[pygame.K_d] and not keys[pygame.K_UP] and not keys[pygame.K_w] and not keys[pygame.K_DOWN] and not keys[pygame.K_s]:
            player.speedY = 0
        if player.speedX == 0 and player.speedY == 0:
            player.img = currentWalkList[0]
        
        #challenge 4
        if player.hitbox.colliderect(healthPotion.hitbox) and healthPotion.pickedUp == False:
            player.health += 25
            if player.health>100:
                player.health = 100
            healthPotion.pickedUp = True

        if healthPotion.pickedUp == False:
            drawSprite(healthPotion)

        if player.hitbox.colliderect(mari.hitbox):
            displayNpcText()
        else:
            dialogNumber = 0
        
        if player.hitbox.collidelistall(enemyHBList):
            opponent = enemyList[player.hitbox.collidelist(enemyHBList)]
            player.originalPlace()
            winner = None
            gameState = "Fight"
        
        # challenge 2
        if player.hitbox.collidelistall(enemyPlayerDetectHB):
            opponent = enemyList[player.hitbox.collidelist(enemyPlayerDetectHB)]
            # Calculate the distance between the two rectangles
            dist = math.sqrt((player.hitbox.x - opponent.hitbox.x)**2 + (player.hitbox.y - opponent.hitbox.y)**2)

            # Calculate the angle between the two rectangles
            angle = math.atan2(player.hitbox.y - opponent.hitbox.y, player.hitbox.x - opponent.hitbox.x)

            # Update the position of rect1 based on the angle and speed
            # aka nerd stuff 
            opponent.x += (100*deltaTime) * math.cos(angle)
            opponent.hitbox.x += (100*deltaTime) * math.cos(angle)
            opponent.y += (100*deltaTime) * math.sin(angle)
            opponent.hitbox.y += (100*deltaTime) * math.sin(angle)

        drawHealthBar(50,675)
        drawSprite(mari)
        drawSprite(player)
        for i in enemyList:
            drawSprite(i)

    #requirement 3 and 4
    if gameState == "Fight":
        battleDialog = ["You've entered a battle",f"Your opponent is {opponent.name}","How do you want to attack?",f"You hit {opponent.name} for {player.attackPower}",f"{opponent.name} attacks, dealing {opponent.attackPower} damage",f"{winner} has won",""]
        def dialog():
            global dialogNumber, winner, returnKeyPressed
            dialogBox = pygame.image.load('assets\\dialogBox.png')
            screen.blit(dialogBox,(320,600))
            fontObj = pygame.font.Font("C:\Windows\Fonts\Arial.ttf",25) 
            if not dialogNumber >= len(battleDialog):
                textObj = fontObj.render(battleDialog[dialogNumber],True,"white","black")      
            else:
                textObj = fontObj.render(battleDialog[len(battleDialog)],True,"white","black")      
            textRect = textObj.get_rect()
            if dialogNumber == 2:
                textRect.center = (610,620)
                swordAttack = pygame.draw.rect(screen,"White",(370,640,200,50))
                swordButtonText = fontObj.render("Sword",True,"black","white")        
                swordTextRect = swordButtonText.get_rect() 
                swordTextRect.center = (470,665)

                magicAttack = pygame.draw.rect(screen,"White",(650,640,200,50))
                magicButtonText = fontObj.render("Magic",True,"black","white")        
                magicTextRect = magicButtonText.get_rect() 
                magicTextRect.center = (750,665)

                screen.blit(swordButtonText,swordTextRect)
                screen.blit(magicButtonText,magicTextRect)

                #challenge 3
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if swordAttack.collidepoint(event.pos):
                        player.attackPower = 10
                        player.attacking = True
                    elif magicAttack.collidepoint(event.pos):
                        player.attackPower = 15
                        player.attacking = True
                    if player.attacking == True:
                        opponent.health -= player.attackPower
                        if opponent.health <= 0:
                            winner = "Player" 
                            dialogNumber = 5
                        else:
                            dialogNumber +=1
                        player.attacking = False
            else:
                textRect.center = (610,650)

            if dialogNumber == 3:
                    opponent.attackPower = random.randint(1,15)
                    opponent.attacking = False
            
            if dialogNumber == 4:
                if opponent.attacking == False:
                    player.health -= opponent.attackPower
                    opponent.attacking = True
                if player.health <= 0:
                    winner = opponent.name

            screen.blit(textObj,textRect)

        player.img = walkBack1
        player.img = pygame.transform.scale(player.img,(200,200))
        player.x = 50
        player.y = 500

        opponent.img = pygame.transform.scale(opponent.img,(400,400))
        opponent.x = 1000
        opponent.y = 50

        if dialogNumber != 2:
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RETURN and returnKeyPressed == False:
                    dialogNumber +=1
                    if winner == None and dialogNumber == len(battleDialog)-2:
                        dialogNumber = 2
                    if winner != None and dialogNumber == len(battleDialog)-1:
                        enemyList.remove(opponent)
                        enemyHBList.remove(opponent.hitbox)
                        enemyPlayerDetectHB.remove(opponent.detectPlayerHitbox)
                        player.x = player.originX
                        player.y = player.originY
                        winner = None
                        gameState = "Main"
                    returnKeyPressed = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    returnKeyPressed = False
        
        drawSprite(opponent)
        drawSprite(player)
        drawHealthBar(50,50)
        dialog()
        

    #checks if anything is happenign in game (char walking, fighting, ect) it will update it
    for event in pygame.event.get():
        #if you close window you can leave the game
        if event.type== pygame.QUIT:
            running = False

    pygame.display.update()