import pygame

class Button():
	def __init__(self,x, y, image, image_hover, scale):
		width = image.get_width()
		height = image.get_height()
		self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
		self.image_hover = pygame.transform.scale(image_hover, (int(width * scale), int(height * scale)))
		self.rect = self.image.get_rect()
		# self.rect.topleft = (x, y)
		self.rect.x = x
		self.rect.y = y
		self.clicked = False

	def draw(self, surface):
		action = False

		# draw button
		surface.blit(self.image, (self.rect.x, self.rect.y))
		#get mouse position
		pos = pygame.mouse.get_pos()

		#check mouseover and clicked conditions
		if self.rect.collidepoint(pos):
			if self.image_hover:
						surface.blit(self.image_hover, (self.rect.x, self.rect.y))

			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				action = True
				self.clicked = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False


		return action