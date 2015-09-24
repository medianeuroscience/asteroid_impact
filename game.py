'''
'Asteroid Impact'
Copyright (c) 2015 Nick Winters
'''

# to make python3 porting easier:
# see http://lucumr.pocoo.org/2011/1/22/forwards-compatible-python/
from __future__ import absolute_import, division
'''
>>> 6 / 7
1
>>> from __future__ import division
>>> 6 / 7
1.2857142857142858
'''


#Import Modules
import pygame
from pygame.locals import *

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

from screens import *


def main():
	if pygame.mixer:
		pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=1024)
	pygame.init()
	screen = pygame.display.set_mode((640, 480))
	pygame.display.set_caption('Asteroid Impact')
	pygame.mouse.set_visible(0)
	
	gamescreenstack = []
	gamescreenstack.append(AsteroidImpactGameplayScreen(screen, gamescreenstack))
	gamescreenstack.append(ClickToBeginOverlayScreen(screen, gamescreenstack))
	
	pygame.display.flip()

	#Prepare Game Objects
	clock = pygame.time.Clock()

	if pygame.mixer:
		load_music('through space.ogg')
		pygame.mixer.music.set_volume(music_volume)
		pygame.mixer.music.play()
	
	#Main Loop
	while 1:
		millis = clock.tick(60)

		#Handle Input Events
		for event in pygame.event.get(QUIT):
			if event.type == QUIT:
				return
		
		try:
			gamescreenstack[-1].update(millis)
		except QuitGame as e:
			print e
			return

		# draw topmost opaque screen and everything above it
		topopaquescreenindex = -1
		for i in range(-1, -1-len(gamescreenstack), -1):
			topopaquescreenindex = i
			if gamescreenstack[i].opaque:
				break

		for screenindex in range(topopaquescreenindex, 0, 1):
			gamescreenstack[screenindex].draw()
		
		pygame.display.flip()

#Game Over

if __name__ == '__main__': main()