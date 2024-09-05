# ################
# Der Marsianer ##
# Adventure Game #
# ################

# MODULE
# Standard-Module
# time zum Arbeiten mit Zeiten
import time
# Sys zum Beenden
import sys
# Installierte Module
# Pygame für Benutzeroberfläche
import pygame
# Eigene Module
# Timer-Modul
import timer


# KLASSEN
# Charakter (Spieler)
class Character:
    # Init Methode mit Definition der Variablen
    def __init__(self, x: int, y: int, width: int, height: int, graphic_right, graphic_left):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.graphic_right = picture_load_transform(graphic_right, width, height)
        self.graphic_left = picture_load_transform(graphic_left, width, height)
        self.inventory = []
        self.right = True
        self.left = False
        self.rect = None

    def draw(self, screen):
        if self.right:
            self.rect = self.graphic_right.get_rect()
            self.rect.center = self.x, self.y
            screen.blit(self.graphic_right, self.rect)
        elif self.left:
            self.rect = self.graphic_left.get_rect()
            self.rect.center = self.x, self.y
            screen.blit(self.graphic_left, self.rect)

    # Bewegungen nach oben, unten, links und rechts
    def move_up(self):
        self.y -= 10

    def move_down(self):
        self.y += 10

    def move_left(self):
        self.x -= 10
        self.right = False
        self.left = True

    def move_right(self):
        self.x += 10
        self.right = True
        self.left = False


# Rakete
class Spaceship:
    # Init Methode mit Definition der Variablen
    def __init__(self, x: int, y: int, width: int, height: int, graphic_damaged, graphic_fully_attached):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.graphic_damaged = picture_load_transform(graphic_damaged, width, height)
        self.graphic_fully_attached = picture_load_transform(graphic_fully_attached, width, height)
        self.fully_attached = False
        self.rect = None

    def draw(self, screen):
        if self.fully_attached:
            self.rect = self.graphic_fully_attached.get_rect()
            self.rect.center = self.x, self.y
            screen.blit(self.graphic_fully_attached, self.rect)
        else:
            self.rect = self.graphic_damaged.get_rect()
            self.rect.center = self.x, self.y
            screen.blit(self.graphic_damaged, self.rect)

    # Bewegungen nach oben, unten, links und rechts
    def move_up(self):
        self.y -= 10

    def move_down(self):
        self.y += 10

    def move_left(self):
        self.x -= 10

    def move_right(self):
        self.x += 10


# Raketen-Teile
class SpaceshipPart:
    # Init Methode mit Definition der Variablen
    def __init__(self, x: int, y: int, width: int, height: int, graphic, graphic_attached, inv, inv_slot):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.graphic = graphic
        self.graphic_attached = graphic_attached
        self.attached = False
        self.rect = None
        self.in_inventory = False
        self.inv = inv
        self.inv_slot = inv_slot

    def draw(self, screen):
        if self.attached:
            graphic = picture_load_transform(self.graphic_attached, self.width, self.height)
            self.rect = graphic.get_rect()
            self.rect.center = self.x, self.y
            screen.blit(graphic, self.rect)
        elif self.in_inventory:
            graphic = picture_load_transform(self.graphic, self.inv["width"] - 12, self.inv["height"] - 12)
            self.rect = graphic.get_rect()
            self.rect.center = self.inv["x"][self.inv_slot], self.inv["y"]
            screen.blit(graphic, self.rect)
        else:
            graphic = picture_load_transform(self.graphic, self.width, self.height)
            self.rect = graphic.get_rect()
            self.rect.center = self.x, self.y
            screen.blit(graphic, self.rect)

    # Bewegungen nach oben, unten, links und rechts
    def move_up(self):
        self.y -= 10

    def move_down(self):
        self.y += 10

    def move_left(self):
        self.x -= 10

    def move_right(self):
        self.x += 10


# Tool (z.B. Schaufel oder Waffen)
class Tool:
    # Init Methode mit Definition der Variablen
    def __init__(self, x: int, y: int, width: int, height: int, graphic):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.graphic = picture_load_transform(graphic, width, height)


# Lebensleiste
class Health:
    # Init Methode mit Definition der Variablen
    def __init__(self, x: int, y: int, width: int, height: int, graphic_full, graphic_empty):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.graphic_full = picture_load_transform(graphic_full, width, height)
        self.graphic_empty = picture_load_transform(graphic_empty, width, height)
        self.health = 3

    def damage(self, screen, sound, sound_channel):
        self.health -= 1
        sound_channel.play(sound)
        surface = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
        surface.fill((255, 0, 0, 50))
        screen.blit(surface, (0, 0))
        pygame.display.update()
        time.sleep(0.2)

    def heal(self, screen):
        if self.health < 3:
            self.health = 3
            surface = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
            surface.fill((0, 255, 0, 50))
            screen.blit(surface, (0, 0))
            pygame.display.update()
            time.sleep(0.2)

    def draw(self, screen):
        rect_full = self.graphic_full.get_rect()
        rect_empty = self.graphic_empty.get_rect()
        distance = self.width + 10
        match self.health:
            case 0:
                health_bar = [rect_empty, rect_empty, rect_empty]
            case 1:
                health_bar = [rect_full, rect_empty, rect_empty]
            case 2:
                health_bar = [rect_full, rect_full, rect_empty]
            case 3:
                health_bar = [rect_full, rect_full, rect_full]
            case _:
                health_bar = [rect_empty, rect_empty, rect_empty]
        for i in range(3):
            health_bar[i].center = self.x + i * distance, self.y
            if health_bar[i] == rect_empty:
                screen.blit(self.graphic_empty, health_bar[i])
            else:
                screen.blit(self.graphic_full, health_bar[i])


# Sauerstoffanzeige
class Oxygen:
    # Init Methode mit Definition der Variablen
    def __init__(self, x: int, y: int, width: int, height: int, graphic, time_s: int):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.graphic = picture_load_transform(graphic, width, height)
        self.time_s = time_s

        self.empty = False
        self.rect = None
        self.timer = timer.Timer()
        self.timer.activate()

    def refill(self):
        self.timer.reset()
        self.empty = False
        self.timer.activate()

    def draw(self, screen):
        self.timer.update()
        if self.timer.elapsed_time >= self.time_s:
            self.empty = True
        length_factor = 1 - self.timer.elapsed_time / self.time_s

        self.rect = self.graphic.get_rect()
        self.rect.center = self.x, self.y
        screen.blit(self.graphic, self.rect)

        if length_factor > 0:
            bar_width_max = int(self.width - 15)
            bar_width = bar_width_max * length_factor
            bar = pygame.Rect(0, 0, bar_width, self.height/24+2)
            bar.center = self.x-(bar_width_max-bar_width+2)/2, self.y-1
            pygame.draw.rect(screen, (0, 50, 200), bar)
        else:
            surface = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
            surface.fill((0, 20, 250, 50))
            screen.blit(surface, (0, 0))


# Spielkarte
class Map:
    def __init__(self, x: int, y: int, width: int, height: int, graphic):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.graphic = picture_load_transform(graphic, width, height)
        self.rect = None

    def draw(self, screen):
        self.rect = self.graphic.get_rect()
        self.rect.center = self.x, self.y
        screen.blit(self.graphic, self.rect)

    # Bewegungen nach oben, unten, links und rechts
    def move_up(self):
        self.y -= 10

    def move_down(self):
        self.y += 10

    def move_left(self):
        self.x -= 10

    def move_right(self):
        self.x += 10


# Inventar
class Inventory:
    def __init__(self, x: int, y: int, width: int, height: int, graphic):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.graphic = picture_load_transform(graphic, width, height)
        self.inv_pos_x = []

    def draw(self, screen):
        rect = self.graphic.get_rect()
        for x in self.inv_pos_x:
            rect.center = x, self.y
            screen.blit(self.graphic, rect)

    # Modul zur Festlegung der Positionen der Slots und Übergabe an die Spaceship-Teile
    def inv_pos(self, slots: int = 5):
        for i in range(slots):
            self.inv_pos_x.append(self.x + i * self.width)
        return {"x": self.inv_pos_x, "y": self.y, "width": self.width, "height": self.height}


# FUNKTIONEN
# Bildschirm zeichnen
def draw(screen, *objects):
    for obj in objects:
        obj.draw(screen)


# Bild laden und Größe anpassen
def picture_load_transform(path: str, width: int, height: int):
    img = pygame.image.load(path)
    img = pygame.transform.scale(img, (width, height))
    img.convert()
    return img


# Rauch-Effekt für Montage Bauteile
def smoke(size: int, mid_x: int, mid_y: int, clock, screen):
    path_graphic = r"assets\graphic\smoke.png"
    smoke_graphic = pygame.image.load(path_graphic).convert_alpha()
    timer_smoke = timer.Timer()
    timer_smoke.activate()
    smoke_particles = []
    smoke_particles_alpha = []
    smoke_particles_size = []
    while timer_smoke.elapsed_time < 3:
        timer_smoke.update()
        smoke_particles.append("")
        smoke_particles_alpha.append(255)
        smoke_particles_size.append(size//10)
        for i in range(len(smoke_particles)):
            smoke_particles[i] = pygame.transform.scale(smoke_graphic,
                                                        (smoke_particles_size[i], smoke_particles_size[i]))
            if i % 2 == 0:
                smoke_particles[i] = pygame.transform.rotate(smoke_particles[i], 90)
            smoke_particles[i].set_alpha(smoke_particles_alpha[i])
            smoke_rect = smoke_particles[i].get_rect()
            smoke_rect.center = mid_x, mid_y
            screen.blit(smoke_particles[i], smoke_rect)

            smoke_particles_size[i] += size // 10
            smoke_particles_alpha[i] -= 25

        if smoke_particles_size[0] >= size:
            smoke_particles.pop(0)
            smoke_particles_size.pop(0)
            smoke_particles_alpha.pop(0)

        pygame.display.update()
        clock.tick(10)


# MAIN
def main():
    # Pygame initialisieren
    pygame.init()
    # Parameter für Screen festlegen und Screen erstellen
    flags = pygame.FULLSCREEN | pygame.NOFRAME | pygame.SCALED
    screen = pygame.display.set_mode((1920, 1080), flags=flags)
    pygame.display.set_caption("Der Marsianer")
    pygame.mouse.set_visible(0)
    # Clock für Bildwiederholungsrate definieren
    clock = pygame.time.Clock()

    # Schriftarten einbinden
    path_pixeloid = r"assets\fonts\PixeloidSans-Bold.ttf"
    font_36 = pygame.font.Font(path_pixeloid, 36)
    font_72 = pygame.font.Font(path_pixeloid, 72)

    # Hintergrundmusik
    music_path = r"assets\audio\music\game\Ocean_of_Ice.mp3"
    pygame.mixer.music.load(music_path)
    pygame.mixer.music.play(-1, 0.0)
    pygame.mixer.music.set_volume(0.3)

    # Sound-Effekte laden
    volume_sound_effects = 0.5

    path_damage = r"assets\audio\sound_effects\damage.wav"
    path_breathing = r"assets\audio\sound_effects\breathing.wav"
    path_repairing = r"assets\audio\sound_effects\repairing.wav"
    path_walking = r"assets\audio\sound_effects\walking.wav"
    path_inventory = r"assets\audio\sound_effects\inventory.wav"

    sound_damage = pygame.mixer.Sound(path_damage)
    sound_breathing = pygame.mixer.Sound(path_breathing)
    sound_repairing = pygame.mixer.Sound(path_repairing)
    sound_walking = pygame.mixer.Sound(path_walking)
    sound_inventory = pygame.mixer.Sound(path_inventory)

    sound_damage.set_volume(volume_sound_effects)
    sound_breathing.set_volume(volume_sound_effects)
    sound_repairing.set_volume(volume_sound_effects)
    sound_walking.set_volume(volume_sound_effects)
    sound_inventory.set_volume(volume_sound_effects)

    channel_sound_damage = pygame.mixer.Channel(1)
    channel_sound_breathing = pygame.mixer.Channel(2)
    channel_sound_repairing = pygame.mixer.Channel(3)
    channel_sound_walking = pygame.mixer.Channel(4)
    channel_sound_inventory = pygame.mixer.Channel(5)

    # Grafiken für Objekte importieren
    # Charakter Ausrichtung rechts
    graphic_character_right = r"assets\graphic\character\astronaut_right.png"
    # Charakter Ausrichtung links
    graphic_character_left = r"assets\graphic\character\astronaut_left.png"
    # Spaceship vollständig repariert
    graphic_spaceship_fully_attached = r"assets\graphic/spaceship/spaceship.png"
    # Spaceship kaputt
    graphic_spaceship_damaged = r"assets\graphic\spaceship\spaceship_damaged.png"
    # Spaceship Teile
    graphic_spaceship_part_1 = r"assets\graphic\spaceship\spaceship_part_1.png"
    graphic_spaceship_part_2 = r"assets\graphic\spaceship\spaceship_part_2.png"
    graphic_spaceship_part_3 = r"assets\graphic\spaceship\spaceship_part_3.png"
    graphic_spaceship_part_4 = r"assets\graphic\spaceship\spaceship_part_4.png"
    graphic_spaceship_part_5 = r"assets\graphic\spaceship\spaceship_part_5.png"
    # Spaceship Teile vor Montage
    graphic_spaceship_part_1_not_att = r"assets\graphic\spaceship\before_attachment\spaceship_part_1.png"
    graphic_spaceship_part_2_not_att = r"assets\graphic\spaceship\before_attachment\spaceship_part_2.png"
    graphic_spaceship_part_3_not_att = r"assets\graphic\spaceship\before_attachment\spaceship_part_3.png"
    graphic_spaceship_part_4_not_att = r"assets\graphic\spaceship\before_attachment\spaceship_part_4.png"
    graphic_spaceship_part_5_not_att = r"assets\graphic\spaceship\before_attachment\spaceship_part_5.png"
    # Map
    graphic_map = r"assets\graphic\map.png"
    # Leben-Anzeige
    graphic_heart_full = r"assets\graphic\health\heart_full.png"
    graphic_heart_empty = r"assets\graphic\health\heart_empty.png"
    # Sauerstoff-Anzeige
    graphic_oxygen_bar = r"assets\graphic\oxygen_bar.png"
    # Inventar-Slot
    graphic_inventory_slot = r"assets\graphic\inventory_slot.png"

    # Objekte definieren ##############################################################################################
    # Mitte des Bildschirms in Variablen schreiben
    x_mid_of_screen = screen.get_width()//2
    y_mid_of_screen = screen.get_height()//2
    # Inventar
    inventory = Inventory(x_mid_of_screen - 2 * 128, screen.get_height() - 128 // 2, 128, 128, graphic_inventory_slot)
    inv_positions = inventory.inv_pos()
    # Charakter
    character = Character(x_mid_of_screen, y_mid_of_screen, 128, 128,
                          graphic_character_right, graphic_character_left)
    # Spaceship
    spaceship = Spaceship(x_mid_of_screen - character.width - 30, y_mid_of_screen, 256, 256,
                          graphic_spaceship_damaged, graphic_spaceship_fully_attached)
    # Spaceship-Teile
    coord_part_1 = {"x": x_mid_of_screen + 2000, "y": y_mid_of_screen + 2000}
    coord_part_2 = {"x": x_mid_of_screen - 2000, "y": y_mid_of_screen - 2000}
    coord_part_3 = {"x": x_mid_of_screen + 2300, "y": y_mid_of_screen - 1500}
    coord_part_4 = {"x": x_mid_of_screen - 2000, "y": y_mid_of_screen + 2300}
    coord_part_5 = {"x": x_mid_of_screen + 1000, "y": y_mid_of_screen + 1300}
    spaceship_part_1 = SpaceshipPart(coord_part_1["x"], coord_part_1["y"], 256, 256,
                                     graphic_spaceship_part_1_not_att, graphic_spaceship_part_1,
                                     inv_positions, 0)
    spaceship_part_2 = SpaceshipPart(coord_part_2["x"], coord_part_2["y"], 256, 256,
                                     graphic_spaceship_part_2_not_att, graphic_spaceship_part_2,
                                     inv_positions, 1)
    spaceship_part_3 = SpaceshipPart(coord_part_3["x"], coord_part_3["y"], 256, 256,
                                     graphic_spaceship_part_3_not_att, graphic_spaceship_part_3,
                                     inv_positions, 2)
    spaceship_part_4 = SpaceshipPart(coord_part_4["x"], coord_part_4["y"], 256, 256,
                                     graphic_spaceship_part_4_not_att, graphic_spaceship_part_4,
                                     inv_positions, 3)
    spaceship_part_5 = SpaceshipPart(coord_part_5["x"], coord_part_5["y"], 256, 256,
                                     graphic_spaceship_part_5_not_att, graphic_spaceship_part_5,
                                     inv_positions, 4)
    # Karte
    game_map = Map(x_mid_of_screen, y_mid_of_screen, 5120, 5120, graphic_map)
    # Lebensanzeige
    health = Health(50, screen.get_height()-50, 64, 64, graphic_heart_full, graphic_heart_empty)
    # Sauerstoffanzeige
    oxygen_tank = Oxygen(health.x+health.width+10, health.y-50, 3*health.width+20, 3*health.height+20,
                         graphic_oxygen_bar, 30)

    # Timer für Schaden aus mangelndem Sauerstoff
    time_damage = timer.Timer()

    # Variable run und win definieren
    run = True
    win = None
    # MAIN-LOOP
    while run:
        # Fenster bei Eingabe von ESC schließen
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False

        # Möglichen Schaden berechnen
        if oxygen_tank.empty:
            time_damage.update()
            if not channel_sound_breathing.get_busy():
                channel_sound_breathing.play(sound_breathing)

            if not time_damage.active:
                time_damage.activate()
        else:
            channel_sound_breathing.stop()

        if time_damage.elapsed_time == 5 and health.health == 3:
            health.damage(screen, sound_damage, channel_sound_damage)
        elif time_damage.elapsed_time == 10 and health.health == 2:
            health.damage(screen, sound_damage, channel_sound_damage)
        elif time_damage.elapsed_time == 15 and health.health == 1:
            health.damage(screen, sound_damage, channel_sound_damage)

        if health.health == 0:
            win = False
            run = False

        # Vollständige Reparatur prüfen
        if all([spaceship_part_1.attached, spaceship_part_2.attached, spaceship_part_3.attached,
                spaceship_part_4.attached, spaceship_part_5.attached]):
            spaceship.fully_attached = True
            win = True
            run = False

        # Aktionen bei Tasteneingaben
        pressed_keys = pygame.key.get_pressed()

        parts = [spaceship_part_1, spaceship_part_2, spaceship_part_3, spaceship_part_4, spaceship_part_5]

        move_objects = [game_map, spaceship, *parts]
        walking = False
        if pressed_keys[pygame.K_w]:
            walking = True
            if character.y >= character.height:
                character.move_up()
            elif game_map.y < game_map.height//2:
                for obj in move_objects:
                    obj.move_down()
        if pressed_keys[pygame.K_s]:
            walking = True
            if character.y <= screen.get_height()-character.height*1.6:
                character.move_down()
            elif game_map.y > screen.get_height()//2+(screen.get_height()-game_map.height)//2:
                for obj in move_objects:
                    obj.move_up()
        if pressed_keys[pygame.K_a]:
            walking = True
            if character.x >= character.width*0.8:
                character.move_left()
            elif game_map.x < game_map.width//2:
                for obj in move_objects:
                    obj.move_right()
        if pressed_keys[pygame.K_d]:
            walking = True
            if character.x <= screen.get_width()-character.width*0.8:
                character.move_right()
            elif game_map.x > screen.get_width()//2+(screen.get_width()-game_map.width)//2:
                for obj in move_objects:
                    obj.move_left()
        if pressed_keys[pygame.K_f]:
            for part in parts:
                if character.rect.colliderect(part) and not part.attached:
                    part.in_inventory = True
                    channel_sound_inventory.play(sound_inventory)
            if character.rect.colliderect(spaceship):
                # Alle Teile im Inventar montieren
                smoke_played = False
                for part in parts:
                    if part.in_inventory:
                        if not smoke_played:
                            channel_sound_repairing.play(sound_repairing)
                            smoke(spaceship.width+spaceship.width//3, spaceship.x, spaceship.y, clock, screen)
                            smoke_played = True
                        part.in_inventory = False
                        part.x = spaceship.x
                        part.y = spaceship.y
                        part.attached = True
                # Sauerstofftank auffüllen, Schadens-Timer zurücksetzen und heilen
                time_damage.reset()
                health.heal(screen)
                oxygen_tank.refill()
        if walking and not channel_sound_walking.get_busy():
            channel_sound_walking.play(sound_walking)
        elif not walking:
            channel_sound_walking.stop()

        # Bildschirm beschreiben (Reihenfolge definiert, was oben ist → letztes oben)
        parts_inv = []
        parts_map = []
        for part in parts:
            if part.in_inventory:
                parts_inv.append(part)
            else:
                parts_map.append(part)

        draw(screen, game_map, spaceship, *parts_map, character, inventory, *parts_inv, health, oxygen_tank)
        pygame.display.update()
        if win:
            time.sleep(1)
        # Bildwiederholungsrate von 60 fps festlegen
        clock.tick(60)

    channel_sound_damage.stop()
    channel_sound_breathing.stop()
    channel_sound_repairing.stop()
    channel_sound_walking.stop()
    channel_sound_inventory.stop()

    pygame.mixer.music.stop()
    # Hintergrundmusik Ende
    music_path = r"assets\audio\music\main_menu\Illusory_Realm.mp3"
    pygame.mixer.music.load(music_path)
    pygame.mixer.music.play(-1, 0.0)
    pygame.mixer.music.set_volume(0.1)

    if win:
        text = "Du hast gewonnen!"
        color = (0, 255, 0)
    elif win is False:
        text = "Du hast verloren"
        color = (255, 0, 0)
    else:
        text = "Spiel beenden"
        color = (255, 255, 255)

    text_end = "Drücke ENTER zum Neustarten oder ESC zum Schließen"

    exit_var = False
    while not exit_var:
        screen.fill((0, 0, 0))
        text_win_loose = font_72.render(text, True, color)
        text_replay_close = font_36.render(text_end, True, (255, 255, 255))

        screen.blit(text_win_loose, (x_mid_of_screen-text_win_loose.get_width()//2, y_mid_of_screen-100))
        screen.blit(text_replay_close, (x_mid_of_screen-text_replay_close.get_width()//2, y_mid_of_screen+100))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit_var = True
                elif event.key == pygame.K_RETURN:
                    main()
        clock.tick(24)

    pygame.mixer.music.stop()

    # Pygame am Ende beenden
    pygame.quit()
    sys.exit()


# AUFRUF MAIN
if __name__ == '__main__':
    main()
