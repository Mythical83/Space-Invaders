# Space Invaders
# Tyler Artinger
# 2/10/22
# A simple space invaders game
# I pledge
import math
import random

import pgzrun as pgz
import pygame as pg


class Enemy:
  def __init__(self, actor, direction, enemy_health, enemy_type):
    self.health = enemy_health
    self.actor = actor
    self.direction = direction
    self.enemy_type = enemy_type


HEIGHT = 200
WIDTH = 500

total_health = HEIGHT - 10
remaining_health = HEIGHT - 10
game_right = WIDTH - (WIDTH / (WIDTH / 15))

player = Actor("player/ship")
player.pos = (30, (HEIGHT - 16) - 5)

left = False
right = False

aliens_won = False
player_won = False

final_level = False

mouse_pos = (0, 0)

background = pg.transform.scale(pg.image.load("images/menu/menu.png"), (500, 200))

start_button = Actor("menu/start")
start_button.pos = 65, 150

next_level_button = Actor("menu/next_level")
next_level_button.pos = WIDTH / 2, HEIGHT - 50

main_menu_button = Actor("menu/main_menu")
main_menu_button.pos = WIDTH - 65, 150

health = 5
lasers = []

enemies = []

started = False
time_up = False
menu = True

level = 1


def end_game():
  global time_up
  time_up = True


def alien_win():
  global aliens_won
  aliens_won = True


def remove_health_player():
  global remaining_health, total_health
  remaining_health -= total_health / 5


def fire_laser():
  lasers.append(Actor("player/laser", pos=(player.x, player.top)))


def spawn_enemies():
  global game_right, level
  for i in range(0, random.randrange(5 * level, 10 * level)):
    enemies.append(
    Enemy(Actor("enemies/full_health", pos=(random.randrange(0, game_right), random.randrange(0, 30))), random.randrange(1, 3), 3, "common"))


def handle_movement():
  global game_right, right, left
  if right:
    player.right += WIDTH / 250
  if left:
    player.left -= WIDTH / 250

  if player.left < 0:
    player.left = 0
  elif player.right > game_right:
    player.right = game_right


def update_enemies():
  for enemy in enemies:
    if enemy.enemy_type == "common":
      if enemy.health == 2:
        enemy.actor.image = 'enemies/medium_health'
      elif enemy.health == 1:
        enemy.actor.image = 'enemies/low_health'
    if enemy.direction == 1:
      enemy.actor.left -= 2
      if (enemy.enemy_type == "boss"):
        if (enemy.health <= 5):
          enemy.actor.left -= 2
    else:
      enemy.actor.right += 2
      if (enemy.enemy_type == "boss"):
        if (enemy.health <= 5):
          enemy.actor.right += 2
    if enemy.actor.left < 0:
      enemy.direction = 2
      enemy.actor.bottom += 5
    if enemy.actor.right > game_right - (WIDTH / (WIDTH / 15)):
      enemy.direction = 1
      enemy.actor.bottom += 5
    for laser in lasers:
      if laser.colliderect(enemy.actor):
        lasers.remove(laser)
        enemy.health -= 1
        if enemy.health <= 0:
          enemies.remove(enemy)


def update_lasers():
  for laser in lasers:
    laser.top -= HEIGHT / 100
    if laser.bottom < 0:
      lasers.remove(laser)
      remove_health_player()


def draw_health_bar():
  screen.draw.filled_rect(pg.Rect(game_right - 5, (HEIGHT - total_health) / 2, WIDTH / (WIDTH / 15), total_health), (255, 0, 0))
  screen.draw.filled_rect(
  pg.Rect(game_right - 5, (HEIGHT - remaining_health) / 2, WIDTH / (WIDTH / 15), remaining_health), (0, 255, 0))

def draw_boss_bar(boss):
  bar_width = boss.health * 5
  screen.draw.filled_rect(pg.Rect(boss.actor.x - 25, boss.actor.y + 20, 50, 5), (255, 0, 0))
  screen.draw.filled_rect(pg.Rect(boss.actor.x - (bar_width/2), boss.actor.y + 20, bar_width, 5), (0, 255, 0))


def draw_map(surface, w, h):
  surface1 = pg.image.load("images/map/Surface_Layer1.png")
  surface2 = pg.image.load("images/map/Surface_Layer2.png")
  surface3 = pg.image.load("images/map/Surface_Layer3.png")
  surface4 = pg.image.load("images/map/Surface_Layer4.png")
  for w in range(0, math.ceil(w / surface1.get_width())):
    surface.blit(surface1, (w * surface1.get_width(), h - (surface1.get_height() * 2) - 128))
    surface.blit(surface2, (w * surface1.get_width(), h - (surface1.get_height() * 2) - 96))
    surface.blit(surface3, (w * surface1.get_width(), h - (surface1.get_height() * 2) - 64))
    surface.blit(surface4, (w * surface1.get_width(), h - (surface1.get_height() * 2)))


def check_win_conditions():
  global started, level, time_up
  global final_level
  if aliens_won:
    screen.clear()
    started = False
    screen.blit(pg.transform.scale(pg.image.load("images/menu/lose.png"), (500, 200)), (0, 0))
    level = 1
    start_button.draw()
    main_menu_button.draw()
  if len(enemies) <= 0 and level < 6:
    screen.clear()
    screen.fill((0, 0, 0))
    started = False
    font = pg.font.Font('fonts/space age.ttf', 16)
    text_surface = font.render('Level: ' + str(level), True, (240, 240, 240), (0, 0, 0))
    text_rect = text_surface.get_rect()
    text_rect.center = (WIDTH / 2, HEIGHT / 2)
    screen.blit(text_surface, text_rect)
    next_level_button.draw()
    main_menu_button.draw()
  if len(enemies) <= 0 and level == 6:
    screen.clear()
    screen.fill((0, 0, 0))
    started = False
    font = pg.font.Font('fonts/space age.ttf', 16)
    text_surface = font.render('Final Level', True, (240, 240, 240), (0, 0, 0))
    text_rect = text_surface.get_rect()
    text_rect.center = (WIDTH / 2, HEIGHT / 2)
    screen.blit(text_surface, text_rect)
    final_level = True
    next_level_button.draw()
    main_menu_button.draw()
  if len(enemies) <= 0 and level == 7:
    final_level = False
    screen.clear()
    started = False
    screen.blit(pg.transform.scale(pg.image.load("images/menu/win.png"), (500, 200)), (0, 0))
    level = 1
    start_button.draw()
    main_menu_button.draw()
  if time_up:
    main_menu_button.draw()
    level = 1
    screen.clear()
    started = False
    screen.blit(pg.transform.scale(pg.image.load("images/menu/time.png"), (500, 200)), (0, 0))
    start_button.draw()


def on_key_down(key):
  global left, right, enemies
  if key == keys.D or key == keys.RIGHT:
    right = True
  if key == keys.A or key == keys.LEFT:
    left = True
  if key == keys.SPACE:
    fire_laser()defin


def on_key_up(key):
  global left, right
  if key == keys.D or key == keys.RIGHT:
    right = False
  if key == keys.A or key == keys.LEFT:
    left = False


def on_mouse_down(pos, button):
  global started, start_button, menu
  global aliens_won, time_up
  global enemies, lasers
  global remaining_health
  global level, next_level_button, final_level
  if button == mouse.LEFT:
    if start_button.collidepoint(pos) and not started:
      lasers = []
      enemies = []
      remaining_health = HEIGHT - 10
      clock.schedule_unique(end_game, 60.0)
      spawn_enemies()
      aliens_won = False
      time_up = False
      started = True
      menu = False
      level += 1
    if next_level_button.collidepoint(pos) and not started:
      if not final_level:
        lasers = []
        enemies = []
        remaining_health = HEIGHT - 10
        clock.schedule_unique(end_game, 60.0)
        spawn_enemies()
        aliens_won = False
        started = True
        menu = False
        level += 1
      else:
        lasers = []
        enemies = [Enemy(Actor("enemies/boss", pos=(WIDTH / 2, 20)), 1, 10, "boss")]
        remaining_health = HEIGHT - 10
        started = True
        level += 1
      if main_menu_button.collidepoint(pos) and not started:
        menu = True


def draw():
  global aliens_won, time_up
  global started
  global menu
  global final_level
  if started:
    screen.clear()
    draw_map(screen, WIDTH, HEIGHT)
    player.draw()
    draw_health_bar()
    for laser in lasers:
      laser.draw()
    for enemy in enemies:
      enemy.actor.draw()
    check_win_conditions()
    if remaining_health <= 8:
      clock.schedule(alien_win, 0.09)
    for enemy in enemies:
      if enemy.enemy_type == "boss":
        draw_boss_bar(enemy)

  if menu:
    screen.blit(background, (0, 0))
    start_button.draw()


def update():
  global final_level
  handle_movement()
  update_lasers()
  update_enemies()


pgz.go()