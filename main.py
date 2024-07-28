import pygame
import sys
from os import walk
import asyncio

# using main function to create asynchronous code
async def main():
	# create window
	window = pygame.display.set_mode((1080, 720))

	# player class inheriting from pygame.sprite.Sprite
	class Player(pygame.sprite.Sprite):
			def __init__(self, pos, groups):
				# player will be inside the "all sprites" group
				super().__init__(groups)
				
				# initializing the animation
				self.import_assets()
				self.frame_index = 0
				# IMPORTANT - change self.status to "up", "down", "left", "right" to see the other walking animations for the other directions
				self.status = "down"
				self.image = self.animations[self.status][self.frame_index]
				
				# for positioning, "rect" is a variable already created in the pygame.sprite.Sprite class, and it will be used in the all_sprites.update() line inside the game loop
				self.rect = self.image.get_rect(center = pos)

			def import_assets(self):

				# importing all 16 files, 4 walking frames for each direction - up, down, left , right
				# storing the animation frames inside a dictionary
				# there are 4 keys - "up", "down", "left", "right"
				# the item corresponding to each key will be a list of 4 surfaces - which are the 4 walking frames of that specific direction.

				self.animations = {}

				# using the walk() function in the os python module
				for index, folder in enumerate(walk("player")):
					# the first item returned by the os.walk function will be a list of the directories inside the player folder - up, down, left, right
					# all the next items will be the images inside the "up", "down", "left", "right" subfolder
					# the first item returned by os.walk is special, so checking to see if index == 0
					if index == 0:
						for subfolder in folder[1]:
							self.animations[subfolder] = []
					# otherwise add each image to the dictionary
					else:
						for file_name in folder[2]:
							# for whatever reason, os.walk gives a \ instead of a / in the file names, so use the replace function
							path = folder[0].replace("\\", "/") + "/" + file_name
							surf = pygame.image.load(path).convert_alpha()
							key = folder[0].split("\\")[1]
							self.animations[key].append(surf)

			def update(self, dt):
				# getting the 4 frames for the current direction in which the player is facing - decided by the self.status variable
				current_animation_list = self.animations[self.status]
				self.frame_index += 5 * dt
				if self.frame_index >= len(current_animation_list):
					self.frame_index = 0
				self.image = current_animation_list[int(self.frame_index)]

	# creating the all_sprites group of sprites and also the player object, then adding the player object to all_sprites via its initialization argument
	all_sprites = pygame.sprite.Group()
	player = Player((640, 360), all_sprites)

	# game loop
	while True:
		# check if window is closed
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

		# filling the window with black and using delta time
		window.fill("black")
		clock = pygame.time.Clock()
		dt = clock.tick(60) / 1000
		
		# updating and drawing every sprite inside of all_sprites (only the player sprite for now) to the window
		all_sprites.update(dt)
		all_sprites.draw(window)
		
		# updating the display
		pygame.display.update()
		await asyncio.sleep(0)

asyncio.run(main())