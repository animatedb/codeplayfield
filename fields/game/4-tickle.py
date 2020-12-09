#!/usr/bin/env python
# From https://www.pygame.org/docs/tut/ChimpLineByLine.html
""" pygame.examples.chimp

This simple example is used for the line-by-line tutorial
that comes with pygame. It is based on a 'popular' web banner.
Note there are comments here, but for the full explanation,
follow along in the tutorial.
"""

# Import Modules
import os
import pygame as pg
from pygame.compat import geterror

if not pg.font:
    print("Warning, fonts disabled")
if not pg.mixer:
    print("Warning, sound disabled")

data_dir = "tickle-data"


# functions to create our resources
def load_image(name, colorkey=None):
    fullname = os.path.join(data_dir, name)
    try:
        image = pg.image.load(fullname)
    except pg.error:
        print("Cannot load image:", fullname)
        raise SystemExit(str(geterror()))
    image = image.convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, pg.RLEACCEL)
    return image, image.get_rect()


def load_sound(name):
    class NoneSound:
        def play(self):
            pass

    if not pg.mixer or not pg.mixer.get_init():
        return NoneSound()
    fullname = os.path.join(data_dir, name)
    try:
        sound = pg.mixer.Sound(fullname)
    except pg.error:
        print("Cannot load sound: %s" % fullname)
        raise SystemExit(str(geterror()))
    return sound


# classes for our game objects
class Hand(pg.sprite.Sprite):
    """moves a clenched hand on the screen, following the mouse"""

    def __init__(self):
        pg.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.image, self.rect = load_image("hand.bmp", -1)
        self.tickling = 0

    def update(self):
        """move the hand based on the mouse position"""
        pos = pg.mouse.get_pos()
        self.rect.midtop = pos
        if self.tickling:
            self.rect.move_ip(5, 10)

    def tickle(self, target):
        """returns true if the hand touches with the target"""
        if not self.tickling:
            self.tickling = 1
            hitbox = self.rect.inflate(-5, -5)
            return hitbox.colliderect(target.rect)

    def untickle(self):
        """called to pull the hand back"""
        self.tickling = 0


class Bear(pg.sprite.Sprite):
    """moves a bear across the screen. it can spin the
       bear when it is tickled."""

    def __init__(self):
        pg.sprite.Sprite.__init__(self)  # call Sprite intializer
        # https://www.iconarchive.com/show/tweetscotty-icons-by-lboi/rocket-icon.html
        self.image, self.rect = load_image("laughingbear32trans.png", -1)
        screen = pg.display.get_surface()
        self.area = screen.get_rect()
        self.rect.topleft = 10, 10
        self.move = 9
        self.dizzy = 0

    def update(self):
        """walk or spin, depending on the bears state"""
        if self.dizzy:
            self._spin()
        else:
            self._walk()

    def _walk(self):
        """move the bear across the screen, and turn at the ends"""
        newpos = self.rect.move((self.move, 0))
        if not self.area.contains(newpos):
            if self.rect.left < self.area.left or self.rect.right > self.area.right:
                self.move = -self.move
                newpos = self.rect.move((self.move, 0))
                self.image = pg.transform.flip(self.image, 1, 0)
            self.rect = newpos

    def _spin(self):
        """spin the bear image"""
        center = self.rect.center
        self.dizzy = self.dizzy + 12
        if self.dizzy >= 360:
            self.dizzy = 0
            self.image = self.original
        else:
            rotate = pg.transform.rotate
            self.image = rotate(self.original, self.dizzy)
        self.rect = self.image.get_rect(center=center)

    def tickled(self):
        """this will cause the monkey to start spinning"""
        if not self.dizzy:
            self.dizzy = 1
            self.original = self.image


def main():
    """this function is called when the program starts.
       it initializes everything it needs, then runs in
       a loop until the function returns."""
    # Initialize Everything
    pg.mixer.pre_init(44100, 16, 2, 4096) #frequency, size, channels, buffersize
    pg.init()
    screen = pg.display.set_mode((468, 60))
    pg.display.set_caption("Tickle Bear")
    pg.mouse.set_visible(0)

    # Create The Backgound
    background = pg.Surface(screen.get_size())
    background = background.convert()
    background.fill((250, 250, 250))

    # Put Text On The Background, Centered
    if pg.font:
        font = pg.font.Font(None, 36)
        text = font.render("Tickle the Bear", 1, (10, 10, 10))
        textpos = text.get_rect(centerx=background.get_width() / 2)
        background.blit(text, textpos)

    # Display The Background
    screen.blit(background, (0, 0))
    pg.display.flip()

    # Prepare Game Objects
    clock = pg.time.Clock()
    # https://www.soundjay.com/beep-sounds-1.html
    whiff_sound = load_sound('Poke2.wav')
    tickle_sound = load_sound('Laughing.wav')
    bear = Bear()
    hand = Hand()
    allsprites = pg.sprite.RenderPlain((hand, bear))

    # Main Loop
    going = True
    while going:
        clock.tick(60)

        # Handle Input Events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                going = False
            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                going = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                if hand.tickle(bear):
                    tickle_sound.play()  # tickle
                    bear.tickled()
                else:
                    whiff_sound.play()  # miss
            elif event.type == pg.MOUSEBUTTONUP:
                hand.untickle()

        allsprites.update()

        # Draw Everything
        screen.blit(background, (0, 0))
        allsprites.draw(screen)
        pg.display.flip()

    pg.quit()


# Game Over


# this calls the 'main' function when this script is executed
if __name__ == "__main__":
    main()

