import pygame
import csv
import random
from pygame.locals import *
from singleton import Singleton
from champion_factory import ChampionFactory
from weapon_factory import WeaponFactory
from player import Player
from computer import Computer

GAMENAME			= "Samurai Vs. Viking"
SCREENRECT    		= Rect(0, 0, 640, 480)
USE_PYGAME_CLOCK	= False
PYGAME_FPS			= 50
WEAPONS_FILE		= "weapons.txt"

class GameManager(metaclass=Singleton):
	def __init__(self):
		self.__running				= True
		self.__display_surf			= None
		self.__surface				= None
		self.__player				= None
		self.__computer				= None
		self.__random_weapon		= None
		self.__weapons				= []
		self.__updates				= []
		self.__size					= self.weight, self.height = 800, 600
		self.__ground				= [[450,600,-30,705],[365,400,-15,97],[300,330,155,265],[365,400,315,462],[375,400,565,675]]
		self.__random_weapon_rect	= Rect(((self.__ground[0][0]/2)+150, self.__ground[0][0]+60), (40, 40))
		self.__player_weapon_rect	= Rect((0, 30), (40, 40))
		self.__comp_weapon_rect		= Rect((self.__size[0]-45,30), (40, 40))
		self.__player_rect			= Rect((0,self.__ground[0][0]),(120, 100))
		self.__comp_rect			= Rect((self.__ground[0][1],self.__ground[0][0]),(120, 100))

	def __on_init(self):
		pygame.init()
		pygame.display.set_caption(GAMENAME)
		pygame.mouse.set_visible(0)

		self.__init_weapons()

		##Display information:
		#infoObject = pygame.display.Info()
		# self.__size = infoObject.current_w, infoObject.current_h

		SCREENRECT = Rect(0,0,self.weight,self.height)
		self.__display_surf = pygame.display.set_mode(self.__size, pygame.HWSURFACE | pygame.DOUBLEBUF)## | pygame.FULLSCREEN)
		self.__surface = pygame.image.load('background.jpg')
		self.__surface = pygame.transform.scale(self.__surface, self.__size).convert()
		self.__running = True

	def __init_weapons(self):
		self.__weapons = []
		weapfactory = WeaponFactory()
		try:
			with open(WEAPONS_FILE) as f:
				reader = csv.reader(f)
				self.__weapons = [weapfactory.create_weapon(col1, int(col2), int(col3), [champion.capitalize() for champion in col4.split()]) for col1, col2, col3, col4 in reader]
		except Exception as exp:
			print(exp)

	def __on_event(self, event):
		if (event.type == pygame.KEYDOWN) or (event.type == pygame.QUIT):
			if (event.type == pygame.QUIT) or (event.key == pygame.K_ESCAPE):
				self.__running = False

		keystate = pygame.key.get_pressed()
		self.__updates.append(self.__player.update(keystate=keystate))


	def __on_loop(self):
		self.randomWeapon()
		if self.checkWeaponColission():
			self.__random_weapon = None
		if not self.__computer.getChampion().isAlive() or self.__player.getChampion().isAlive():
			self.__updates.append(self.__computer.update())
		self.__updates.append(self.__player.update())
		if self.__computer.getChampion().isAlive() and not self.__player.getChampion().isAlive():
			self.__updates.append(self.__computer.update())

		#Update collected weapons locations
		if self.__player.getChampion().getWeapon() is not None:
			self.__updates.append(self.__player.getChampion().getWeapon().update())
		if self.__computer.getChampion().getWeapon() is not None:
			self.__updates.append(self.__computer.getChampion().getWeapon().update())

	def __on_render(self):
		self.__display_surf.blit(self.__surface,(0,0))
		for update in self.__updates:
			self.__display_surf.blit(update[0], update[1])
		self.__updates = []
		pygame.draw.rect(self.__display_surf,(255,0,0),(10,10,100,15))
		if self.__player.getChampion().getLife()>0:
			pygame.draw.rect(self.__display_surf,(0,255,0),(10,10,100-((100/self.__player.getChampion().getHealth())*(self.__player.getChampion().getHealth() - self.__player.getChampion().getLife())),15))
		pygame.draw.rect(self.__display_surf,(255,0,0),(self.__size[0]-110,10,100,15))
		if self.__computer.getChampion().getLife()>0:
			pygame.draw.rect(self.__display_surf,(0,255,0),(self.__size[0]-110,10,100-((100/self.__computer.getChampion().getHealth())*(self.__computer.getChampion().getHealth() - self.__computer.getChampion().getLife())),15))
		pygame.display.update()

	def __on_cleanup(self):
		pygame.quit()

	def execute(self):
		if self.__on_init() == False:
			self.__running = False

		champfactory = ChampionFactory()

		## Simulates champion select:
		comp_champ = champfactory.create_champion('viking', self.__comp_rect, self.__ground)
		player_champ = champfactory.create_champion('samurai', self.__player_rect, self.__ground)

		self.__computer = Computer(champion=comp_champ)
		self.__player = Player(champion=player_champ, name="Player1")
		self.__computer.setRival(self.__player.getChampion())
		self.__player.setRival(self.__computer.getChampion())

		clock = pygame.time.Clock()
		while(self.__running):
			if not USE_PYGAME_CLOCK:
				clock.tick(PYGAME_FPS)
			else:
				clock.tick()
			self.__on_loop()
			self.__on_render()

			for event in pygame.event.get():
				self.__on_event(event)

		self.__on_cleanup()

	def randomWeapon(self):
		if self.__random_weapon is None:
			rand = random.randint(0,1000)
			if rand <= 10:
				rand = random.randint(0,len(self.__weapons)-1)
				self.__random_weapon = self.__weapons[rand]
				self.__random_weapon.setPosition(self.__random_weapon_rect)
				self.__updates.append(self.__random_weapon.update())
		else:
			rand = random.randint(0,5000)
			if rand <= 1:
				self.__random_weapon=None
			else:
				self.__updates.append(self.__random_weapon.update())

	def checkWeaponColission(self):
		if self.__random_weapon is not None:
			if self.__player.getChampion().checkColission(self.__random_weapon.getPosition()):
				if self.__player.getChampion().setWeapon(self.__random_weapon):
					self.__player.getChampion().getWeapon().setPosition(self.__player_weapon_rect)
				return True
			elif self.__computer.getChampion().checkColission(self.__random_weapon.getPosition()):
				if self.__computer.getChampion().setWeapon(self.__random_weapon):
					self.__computer.getChampion().getWeapon().setPosition(self.__comp_weapon_rect)
				return True
		return False

if __name__ == "__main__" :
	gameManager = GameManager()
	gameManager.execute()
