#Global Variables
PINK = (255,192,203)
Play1 = "Downloads/Projects/Music player/Play.png"
Play2 = "Downloads/Projects/Music player/Play2.png"
Pause1 = "Downloads/Projects/Music player/Pause.png"
Pause2 = "Downloads/Projects/Music player/Pause2.png"
Forwards = "Downloads\Projects\Music player\Forwards.png"
Forwards2 = "Downloads\Projects\Music player\Forwards2.png"
Backward = "Downloads\Projects\Music player\Backwards.png"
Backward2 = "Downloads\Projects\Music player\Backwards2.png"
offset=0

#initialising code
import pygame
from pygame import mixer
import mutagen
from mutagen.mp3 import MP3
import time
import os

pygame.init()
mixer.init()
screen = pygame.display.set_mode((200,200))
screen.fill(PINK)
pygame.display.flip()

#Creating a font
pygame.font.init()
my_font = pygame.font.SysFont("Arial", 25)


#Icons
class Button(pygame.sprite.Sprite):
    def __init__(self,posx,posy, image, image2):
        super().__init__()
        #loading the image
        self.image = pygame.image.load(image)
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()
        self.rect.x = posx
        self.rect.y = posy
        
    #draw on screen
    def draw(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    #checking if button was pressed
    def checkforInput(self, menu_mouse, mouse_click):
        if self.rect.collidepoint(menu_mouse):
            if mouse_click:
                return True
        return False
    
    #hover effect
    def ChangeColour(self,menu_mouse, image, image2):
        if self.rect.collidepoint(menu_mouse):
            self.image = pygame.image.load(image2)
            self.image.set_colorkey((0,0,0))
        else:
            self.image = pygame.image.load(image)
            self.image.set_colorkey((255,255,255))

#to track song timing
class ProgressBar():
    def __init__(self):
        self.startTime = None
        self.elapsedTime = 0
        self.isRunning = False

    def start(self, offset):
        if not self.isRunning:
            self.startTime = time.time() - offset
            self.isRunning = True
    
    def stop(self):
        if self.isRunning:
            self.elapsedTime += time.time() - self.startTime
            self.startTime = None
            self.isRunning = False
    
    def reset(self):
        self.elapsedTime = 0
        self.startTime = None
        self.isRunning = False

    def logTime(self):
        if self.isRunning:
            return self.elapsedTime + (time.time()-self.startTime)
        return self.elapsedTime
    
    def setElapsed(self, seconds):
        self.elapsedTime = seconds
        if self.isRunning:
            self.startTime = time.time() - seconds

# Load all songs
MUSIC_PATH = "Downloads/Projects/Music player/Music files"
SongList = [os.path.join(MUSIC_PATH, f) for f in os.listdir(MUSIC_PATH) if f.endswith(".mp3")]
SongIndex = 0

def load_song(index):
    global SongLength
    song = SongList[index]
    mixer.music.load(song)
    mixer.music.play()
    audio = MP3(song)
    SongLength = audio.info.length
    timePassed.reset()
    timePassed.start(offset)

    return song



# Track time
timePassed = ProgressBar()

# Load first song
currentSong = load_song(SongIndex)

# Progress bar dimensions
bar_w = SongLength
bar_h= 5


# Event when song ends
SONG_END = pygame.USEREVENT+1
pygame.mixer.music.set_endevent(SONG_END)



#initialsing
PlayButton = Button(98, 140, Play1, Play2)
PauseButton = Button(48, 140, Pause1, Pause2)
ForwardButton = Button(160,150,Forwards, Forwards2)
BackwardButton = Button(15,150,Backward, Backward2)
timePassed = ProgressBar()

clock = pygame.time.Clock()


#main loop
while exit:
    screen.fill(PINK)
    text_surface = my_font.render(currentSong[44:].strip(".mp3"), False, (255,255,255))
    screen.blit(text_surface, (30,80))

    
    menu_mouse = pygame.mouse.get_pos()
    mouse_click = pygame.mouse.get_pressed()[0]

    
    PlayButton.draw()
    PlayButton.update(menu_mouse)
    PauseButton.draw()
    PauseButton.update(menu_mouse)
    ForwardButton.draw()
    ForwardButton.update(menu_mouse)
    BackwardButton.draw()
    BackwardButton.update(menu_mouse)
    PlayButton.ChangeColour(menu_mouse, Play1, Play2)
    PauseButton.ChangeColour(menu_mouse, Pause1, Pause2)
    ForwardButton.ChangeColour(menu_mouse, Forwards, Forwards2)
    BackwardButton.ChangeColour(menu_mouse, Backward, Backward2)




    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            exit = False
        
        if event.type == SONG_END:  # Auto play next
            SongIndex = (SongIndex + 1) % len(SongList)
            currentSong = load_song(SongIndex)

        if PauseButton.checkforInput(menu_mouse, mouse_click):
            mixer.music.pause()
            timePassed.stop()

        if PlayButton.checkforInput(menu_mouse, mouse_click):
            mixer.music.unpause()
            timePassed.start(offset=timePassed.logTime())

        if ForwardButton.checkforInput(menu_mouse, mouse_click):
            SongIndex = (SongIndex + 1) % len(SongList)
            currentSong = load_song(SongIndex)
        
        if BackwardButton.checkforInput(menu_mouse, mouse_click):
            SongIndex = (SongIndex - 1) % len(SongList)
            currentSong = load_song(SongIndex)


        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos 
            if (30 <= mx <= 30 + bar_w) and (115 <= my <= 115 + bar_h):
                # Click position ratio
                ratio = (mx - 30) / bar_w
                new_time = ratio * (SongLength)

                # Restart music from new position
                mixer.music.play(start=new_time)
                timePassed.setElapsed(new_time)
                timePassed.start(offset=new_time)

    time_ratio = timePassed.logTime()/(SongLength*1.8 )
    time_ratio = min(time_ratio,1)
    pygame.draw.rect(screen,(0,0,0), (5,115, bar_w, bar_h ))
    pygame.draw.rect(screen,(255,255,255), (5,115, bar_w * time_ratio, bar_h))
    pygame.display.flip()

    clock.tick(20)
pygame.quit()

