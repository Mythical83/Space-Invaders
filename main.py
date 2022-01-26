# Space Invaders
# Tyler Artinger

# A simple space invaders game


import pygame as pg
import pgzrun as pgz
import random

class Enemy:
  def __init__(self, Actor, direction):
    self.health = 3
    self.Actor = Actor

HEIGHT = 200
WIDTH = 500

total_health = HEIGHT - 10
remaining_health = HEIGHT - 10

player = Actor("player/ship")
player.pos = (30, (HEIGHT - 16) - 5)

left = False
right = False

aliens_won = False
player_won = False

health = 5
missiles = []

enemies = []

def remove_health():
  global remaining_health, total_health
  health_to_remove = total_health/25
  remaining_health -= health_to_remove

def handle_damage():
  for i in range(0, 5):
    clock.schedule(remove_health, i/15)

def fire_missile():
  missiles.append(Actor("player/missile", pos=(player.x, player.top)))

def update_missiles():
  for missile in missiles:
    missile.top -= HEIGHT/100
    if (missile.bottom < 0):
      missiles.remove(missile)
      handle_damage()

def handle_movement():
  if (right):
    player.right += WIDTH/250
  if (left):
    player.left -= WIDTH/250
  
  if (player.left < 0):
    player.left = 0
  elif player.right > WIDTH - (WIDTH/(WIDTH/15) - 5) - (WIDTH/(WIDTH/15)):
    player.right = WIDTH - (WIDTH/(WIDTH/15) - 5) - (WIDTH/(WIDTH/15))

def spawn_enemies():
  for i in range(0, random.randrange(5, 10)):
    enemies.append(Enemy(Actor("enemies/ship", pos=(random.randrange(0, WIDTH - (WIDTH/(WIDTH/15))), random.randrange(0, 30))), random.randrange(1,2)))

def update_enemies():
  for enemy in enemies:
    
    for missile in missiles:
      if (missile.colliderect(enemy.Actor)):
        missiles.remove(missile)
        enemy.health -= 1
        if (enemy.health <= 0):
          enemies.remove(enemy)

def draw_health_bar():
  screen.draw.filled_rect(pg.Rect((WIDTH - ( WIDTH/(WIDTH/15))) - 5, (HEIGHT - total_health)/2, WIDTH/(WIDTH/15), total_health), (255, 0, 0))
  screen.draw.filled_rect(pg.Rect((WIDTH - ( WIDTH/(WIDTH/15))) - 5, (HEIGHT - remaining_health)/2, WIDTH/(WIDTH/15), remaining_health), (0, 255, 0))

def alien_win():
  global aliens_won
  aliens_won = True

def on_key_down(key):
  global left, right
  if (key == keys.D or key == keys.RIGHT):
    right = True
  if (key == keys.A or key == keys.LEFT):
    left = True
  if (key == keys.SPACE):
    fire_missile()

def on_key_up(key):
  global left, right
  if (key == keys.D or key == keys.RIGHT):
    right = False
  if (key == keys.A or key == keys.LEFT):
    left = False

def draw():
  global aliens_won
  screen.clear()
  player.draw()
  draw_health_bar()
  for missile in missiles:
    missile.draw()
  for enemy in enemies:
    enemy.Actor.draw()
  if (remaining_health <= 8):
    clock.schedule(alien_win, 0.09)
  if (aliens_won):
    screen.clear()
    screen.fill((255, 0, 0))
    screen.draw.text("The aliens took over the world!", (30, 30))

def update():
  handle_movement()
  update_missiles()
  update_enemies()

spawn_enemies()

pgz.go()