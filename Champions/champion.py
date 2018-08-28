import pygame
from pygame.locals import *

INFINITY = 10000000
class Champion:
    def __init__(self, posrect, path, ground, speed, attack_speed, velocity, mass, power, rrange, shield, health):
        self._ground        = ground
        self._speed         = speed
        self._velocity      = self._basicvelocity = velocity
        self._mass          = mass
        self._power         = power
        self._range         = rrange
        self._shield        = shield
        self._health        = health
        self._life          = health
        self._posrect       = posrect
        self._path          = path
        self._attack_speed  = attack_speed
        self._walk          = 0
        self._stand         = 0
        self._hit           = -1
        self._die           = -1
        self._attack        = -1
        self._direction     = 0
        self._isjump        = False
        self._isfall        = False
        self._stand_images  = []
        self._walk_images   = []
        self._attack_images = []
        self._hit_images    = []
        self._die_images    = []
        self._weapon        = None
        for i in range(0,10):
            stand_path = "{}Stand/{}.png".format(self._path,i)
            self._stand_images.append(pygame.image.load(stand_path).convert_alpha())
            walk_path = "{}Run/{}.png".format(self._path,i)
            self._walk_images.append(pygame.image.load(walk_path).convert_alpha())
            attack_path = "{}Attack1H/{}.png".format(self._path,i)
            self._attack_images.append(pygame.image.load(attack_path).convert_alpha())
            hit_path = "{}Hit/{}.png".format(self._path,i)
            self._hit_images.append(pygame.image.load(hit_path).convert_alpha())
            die_path = "{}Die/{}.png".format(self._path,i)
            self._die_images.append(pygame.image.load(die_path).convert_alpha())

        self._rect          = pygame.Rect(self._posrect)
        self._image         = self._stand_images[self._stand]
        self._image         = pygame.transform.scale(self._image, self._rect.size)
        self._image         = self._image.convert_alpha()

    def _type(self):
        return self.__class__.__name__

    def getSpeed(self):
        return self._speed

    def getVelocity(self):
        return self._velocity

    def getMass(self):
        return self._mass

    def getPower(self):
        return self._power

    def getRange(self):
        return self._range

    def getShield(self):
        return  (100 - self._shield) / 100

    def getHealth(self):
        return self._health

    def getLife(self):
        return self._life

    def getRect(self):
        return self._rect

    def getWeapon(self):
        return self._weapon

    def getGround(self, pos):
        top = INFINITY
        left = INFINITY
        for ground in self._ground:
            if ground[0] >= pos.top and (pos.left >= ground[2] and pos.left <= ground[3]):
                if ground[0] < top:
                    top = ground[0]
        return top

    def getBounderies(self,pos):
        left = pos.left
        if pos.left < self._ground[0][2] or pos.left > self._ground[0][3]:
            left = self._ground[0][2] if pos.left < self._ground[0][2] else self._ground[0][3]
        pos.left = left
        top = self.getGround(pos)
        return (top,left)

    def checkRadius(self,rect):
        if isinstance(rect, Rect):
            left = abs(rect.left - self._rect.left)
            top = abs(rect.top - self._rect.top)
            if left <= self._range and top <= self._range:
                return True
        return False

    def checkColission(self,rect):
        if isinstance(rect, Rect):
            if self._rect.colliderect(rect):
                return True
        return False

    def isAlive(self):
        return self._life > 0

    def setVelocity(self, vel):
        self._velocity = vel

    def setWeapon(self, weapon):
        pass

    def _tryMove(self, direction):
        if self._die == -1:
            self._direction = direction
            self._stand = 1
            self._walk = (self._walk+1)%10
            self._rect.left = self._rect.left+(direction*self.getSpeed())
            bounderies = self.getBounderies(self._rect)
            self._rect = pygame.Rect((bounderies[1],self._rect.top),(self._rect.width, self._rect.height))
            if not self._isjump and self._rect.top < bounderies[0]:
                self._isfall = True
            self.__onFall() if self._isfall else None
            self.__onJump() if self._isjump else None
            self._image = self._walk_images[self._walk]
            self._image = pygame.transform.scale(self._image, self._rect.size)
            self._image = self._image.convert_alpha()
            if self._direction < 0:
                self._image = pygame.transform.flip(self._image, True, False)
        return (self._image,self._rect)

    def _tryJump(self):
        if self._die == -1 and not self._isjump:
            self._isjump = True

    ## Formula: Power = (Weapon strength * Power)
    def _tryAttack(self):
        if self._die == -1 and self._attack == -1 and self._hit == -1:
            self._attack = 0
            power = (self._weapon.getWeaponPower() * self._power) if self._weapon is not None else self._power
            return power
        return 0

    def _onStand(self):
        if self._die == -1:
            self._walk = 0
            self._stand = (self._stand+1)%10
            bounderies = self.getBounderies(self._rect)
            self._rect = pygame.Rect((self._rect.left,self._rect.top),(self._rect.width, self._rect.height))
            if not self._isjump and self._rect.top < bounderies[0]:
                self._isfall = True
            self.__onFall() if self._isfall else None
            self.__onJump() if self._isjump else None
            self._image = self._stand_images[self._stand]
            self._image = pygame.transform.scale(self._image, self._rect.size)
            self._image = self._image.convert_alpha()
            if self._direction < 0:
                self._image = pygame.transform.flip(self._image, True, False)
        return (self._image,self._rect)

    def _onAttack(self):
        if self._attack > 8:
            self._attack = -1
        elif self._attack > -1:
            self._walk = 0
            self._stand = 0
            self._attack += (1/self._attack_speed)
            self._image = self._attack_images[int(self._attack)]
            self._image = pygame.transform.scale(self._image, self._rect.size)
            self._image = self._image.convert_alpha()
            if self._direction < 0:
                self._image = pygame.transform.flip(self._image, True, False)
        return (self._image,self._rect)

    def _onHit(self, damage=0):
        if self._life > 0:
            if damage > 0:
                damage = damage/self.getShield()
                self._life = self._life - damage if self._life - damage > 0 else 0
                self._hit = 0
                if self._life == 0:
                    self._hit = -1
                    self._die = 0
            elif self._hit > 8:
                self._hit = -1
            elif self._hit > -1:
                self._walk = 0
                self._stand = 0
                self._attack = -1
                self._hit +=(1/self._attack_speed)
                self._image = self._hit_images[int(self._hit)]
                self._image = pygame.transform.scale(self._image, self._rect.size)
                self._image = self._image.convert_alpha()
                if self._direction < 0:
                    self._image = pygame.transform.flip(self._image, True, False)
        return (self._image,self._rect)

    def _onDie(self):
        if self._die > -1:
            self._die +=1
            self._die = 9 if self._die > 8 else self._die
            self._image = self._die_images[self._die]
            self._image = pygame.transform.scale(self._image, self._rect.size)
            self._image = self._image.convert_alpha()
            if self._direction < 0:
                self._image = pygame.transform.flip(self._image, True, False)
        return (self._image,self._rect)

    ## Kinetic Energy: 1/2*Mass*Velocity^2
    def __onJump(self):
        if self.getVelocity() > 0:
            F = (0.5 * self.getMass() * (self.getVelocity()*self.getVelocity()))
        else:
            F = -(0.5 * self.getMass() * (self.getVelocity()*self.getVelocity()))

        top = self.getGround(self._rect)
        self._rect.top = self._rect.top - F

        if top > self._rect.top:
            self.setVelocity(self.getVelocity() - 1)
        else:
            self._rect.top = top
            self._isjump = False
            self.setVelocity(self._basicvelocity)

    def __onFall(self):
        F = (0.5 * self.getMass() * (self.getVelocity()*self.getVelocity()))
        top = self.getGround(self._rect)
        self._rect.top = self._rect.top + F
        if top > self._rect.top:
            self.setVelocity(self.getVelocity() - 1)
        else:
            self._rect.top = top
            self._isfall = False
            self.setVelocity(self._basicvelocity)
