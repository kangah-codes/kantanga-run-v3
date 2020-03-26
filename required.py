from pygame import image
import pygame, sqlite3

def centerText(font, text, window):
    sz = font.size(text)
    return window[0]/2 - sz[0]/2, window[1]/2 - sz[1]/2 

class Animation():
    def __init__(self,sprites,frame_duration, loop=False):
        self.imgs = []
        self.totalTime = 0
        self.movieTime = 0
        self.frameIndex = 0
        self.loop = loop
        for i in sprites:
            self.totalTime += frame_duration
            self.imgs.append(image.load(i).convert_alpha())
        #self.duration = duration
        #self.endAnimation = endAnis
        self.hasEnded = False
        if self.hasEnded:
            loop = False

    def get_mask(self):
        img = self.imgs[self.frameIndex]
        return pygame.mask.from_surface(img)

    def update(self, tm):

        self.hasEnded = False
        if len(self.imgs) > 1:
            self.movieTime += tm

            if self.movieTime >= self.totalTime and self.loop:
                self.movieTime = 0
                self.frameIndex = 0
            if self.movieTime >= self.totalTime and not self.loop:
                self.movieTime = 0
                self.frameIndex = 0
                self.hasEnded = True
  
            self.frameIndex = int ((self.movieTime/float(self.totalTime)) * len(self.imgs))
        pass

    def getImage(self):
        return self.imgs[self.frameIndex]
        pass

    def get_rect(self):
        img = self.imgs[self.frameIndex]
        return img.get_rect()

    def getScaledImage(self, scale):
        img = self.imgs[self.frameIndex]
        return pygame.transform.scale(img, (int(img.get_rect().width * scale),int( img.get_rect().height * scale)))

    def ended(self):
        a = self.hasEnded
        self.hasEnded = True
        return a

    def getCurrentFrame(self,scale):
        width = int(self.imgs[self.frameIndex].get_rect().width*scale)
        height = int(self.imgs[self.frameIndex].get_rect().width*scale)
        i = pygame.transform.scale(self.imgs[self.frameIndex], (width,height))
        return i

class SpriteGroup(pygame.sprite.Group):
    def draw(self, surface):
        sprites = self.sprites()
        surface_blit = surface.blit
        for spr in sprites:
            #self.spritedict[spr] = surface_blit(spr.image, spr.rect)
            spr.draw(surface)
        self.lostsprites = []



'''
DBHandler::  this handles all database activities including saving high scores and saving games.
'''

class DBHandler():
    
    def __init__(self, file='res/svd'):
        str_create_tables =  """CREATE TABLE TOP_SCORE (id integer primary key autoincrement, name text, days integer)"""
        self.connection = sqlite3.connect(file)
        #trying first time setup
        self.cursor = self.connection.cursor()
        try:
            self.cursor.execute(str_create_tables)
            self.connection.commit()
            print('tables created')
            pass
        except:
            
            print('debbug:: error creating tables')
            pass

    def insert(self,name, days):
        str_insert_days = '''INSERT INTO TOP_SCORE(name, days) VALUES ('%s', %s)'''
        try:
            self.cursor.execute(str_insert_days % (name,days))
            self.connection.commit()
        except:
            print("debug:: error inserting into database")


    def getTopScore(self):
        str_top_score = "SELECT name,days FROM TOP_SCORE ORDER BY days DESC"
        try:
            self.cursor.execute(str_top_score)
            return self.cursor.fetchone()
        except:
            print ('DEBUG:: error fetching top score')

    def getHighScores(self, n):
        str_top_score = "SELECT name,days FROM TOP_SCORE ORDER BY days DESC"
        try:
            self.cursor.execute(str_top_score)
            return self.cursor.fetchmany(n)
        except:
            print ('DEBUG:: error fetching top score')
# DBH = DBHandler()