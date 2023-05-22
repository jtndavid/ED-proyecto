import pygame
import sys, os
from generator import Generator

class Uno():
    def __init__(self, game):
        self.game = game
        self.offsetx = self.game.DISPLAY_W/30
        self.offsety = self.game.DISPLAY_H/25
        self.clock = pygame.time.Clock()
        self.dt = 0
        self.run_display = True
        self.select_card = 1
        self.size_deck = 0
        self.turno = 1
        self.players = 4
        generador = Generator()
        self.deck_data = generador.generator()
        self.main_deck = self.deck_data[0]
        self.discard_deck = self.deck_data[1]
        self.deck1 = self.deck_data[2]
        self.deck2 = self.deck_data[3]
        self.deck3 = self.deck_data[4]
        self.deck4 = self.deck_data[5]
        self.max_weight = self.game.DISPLAY_W/10
        self.max_height = self.game.DISPLAY_H/5
        self.reverse = False
        self.block = False

    
    def display_game(self):
        self.run_display = True
        self.play_music()
        while self.run_display:
            self.game.check_events()
            self.chech_input()
            self.game.display.fill(self.game.RED)
            self.draw_decks()
            self.draw_discard_deck()
            self.draw_main_deck()
            self.check_winner()
            self.dt = self.clock.tick(60) / 1000
            self.blit_screen()
            
    def chech_input(self):
        if self.game.BACK_KEY:
            pygame.mixer.music.stop()
            self.run_display = False
            self.game.playing = False
        if self.game.RIGHT_KEY:
            match self.turno:
                case 1:
                    if self.select_card < self.deck1.size:
                        self.select_card += 1
                    else:
                        self.select_card = 1
                case 2:
                    if self.select_card < self.deck2.size:
                        self.select_card += 1
                    else:
                        self.select_card = 1
                case 3:
                    if self.select_card < self.deck3.size:
                        self.select_card += 1
                    else:
                        self.select_card = 1
                case 4:
                    if self.select_card < self.deck4.size:
                        self.select_card += 1
                    else:
                        self.select_card = 1
        if self.game.LEFT_KEY:
            match self.turno:
                case 1:
                    if self.select_card > 1:
                        self.select_card -= 1
                    else:
                        self.select_card = self.deck1.size
                case 2:
                    if self.select_card > 1:
                        self.select_card -= 1
                    else:
                        self.select_card = self.deck2.size
                case 3:
                    if self.select_card > 1:
                        self.select_card -= 1
                    else:
                        self.select_card = self.deck3.size
                case 4:
                    if self.select_card > 1:
                        self.select_card -= 1
                    else:
                        self.select_card = self.deck4.size
        if self.game.START_KEY:
            play = self.play_card()
            if play:
                self.select_card = 1
                if self.block:
                    self.change_turn()
                    self.change_turn()
                    self.block = False
                else:
                    self.change_turn()
        if self.game.UP_KEY:
            self.take_card()

    def change_turn(self):
        if self.reverse: 
            if self.turno > 1:
                self.turno -= 1
            else:
                self.turno = 4
        else:
            if self.turno < self.players:
                self.turno += 1
            else:
                self.turno = 1
    
    def blit_screen(self):
        self.game.window.blit(self.game.display, (0, 0))
        pygame.display.update()
        self.game.reset_keys()

    def play_music(self):
        self.ruta_musica = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'game', 'music'))
        self.musica = pygame.mixer.music.load(os.path.join(self.ruta_musica,'main_menu.mp3'))
        pygame.mixer.music.set_volume(int(self.game.volumen)/100)
        pygame.mixer.music.play()

    def draw_decks(self):
        for i in range(1, 5):
            #dibujar el primer mazo
            if i == 1:
                sizedeck = self.deck1.deck_size()
                puntero = self.deck1.head
                mazo_width = ((self.max_weight/3) * (sizedeck-1)) + self.max_weight
                mazo_height = self.max_height
                mazo_pos_x = (self.game.DISPLAY_W / 2) - (mazo_width/2)
                mazo_pos_y = (self.game.DISPLAY_H - self.offsety) - mazo_height 
                if i == self.turno:
                    for i in range(sizedeck):
                        carta = pygame.image.load(eval(puntero.card["image"]))
                        carta = pygame.transform.scale(carta, (self.max_weight, self.max_height))
                        pos_x = mazo_pos_x + i * self.max_weight/3
                        if i+1 == self.select_card:
                            pos_y = (mazo_pos_y - (3*self.max_height/4)) 
                        else:
                            pos_y = mazo_pos_y
                        self.game.display.blit(carta, (pos_x,pos_y))
                        puntero = puntero.next
                else:
                    for i in range(sizedeck):
                        carta = pygame.image.load(eval(puntero.card["image"]))
                        carta = pygame.transform.scale(carta, (self.max_weight, self.max_height))
                        pos_x = mazo_pos_x + i * self.max_weight/3
                        pos_y = mazo_pos_y
                        self.game.display.blit(carta, (pos_x,pos_y))
                        puntero = puntero.next

            #dibujar el segundo mazo
            if i == 2:
                sizedeck = self.deck2.deck_size()
                puntero = self.deck2.head
                mazo_width = self.max_weight * sizedeck
                mazo_height = self.max_height
                mazo_pos_x = self.game.DISPLAY_W - (self.offsetx + mazo_height)
                mazo_pos_y = (self.game.DISPLAY_H/2) + (mazo_width/6)
                if i == self.turno:
                    for i in range(1,sizedeck+1):
                        carta = pygame.image.load(eval(puntero.card["image"]))
                        carta = pygame.transform.scale(carta, (self.max_weight, self.max_height))
                        rotated_carta = pygame.transform.rotate(carta, 90)
                        pos_y = mazo_pos_y - i * self.max_weight/3
                        if i == self.select_card:
                            pos_x = mazo_pos_x - (3*self.max_height/4)
                        else:
                            pos_x = mazo_pos_x
                        self.game.display.blit(rotated_carta, (pos_x,pos_y))
                        puntero = puntero.next
                else:
                    for i in range(1,sizedeck+1):
                        carta = pygame.image.load(eval(puntero.card["image"]))
                        carta = pygame.transform.scale(carta, (self.max_weight, self.max_height))
                        rotated_carta = pygame.transform.rotate(carta, 90)
                        pos_y = mazo_pos_y - i * self.max_weight/3
                        pos_x = mazo_pos_x
                        self.game.display.blit(rotated_carta, (pos_x,pos_y))
                        puntero = puntero.next
                    
            #dibujar el tercer mazo
            if i == 3:
                sizedeck = self.deck3.deck_size()
                puntero = self.deck3.head
                mazo_width = ((self.max_weight/3) * (sizedeck-1)) + self.max_weight
                mazo_height = self.max_height
                mazo_pos_x = (self.game.DISPLAY_W/2) - (mazo_width/2)
                mazo_pos_y = self.offsety
                if i == self.turno:
                    for i in range(sizedeck):
                        carta = pygame.image.load(eval(puntero.card["image"]))
                        carta = pygame.transform.scale(carta, (self.max_weight, self.max_height))
                        pos_x = mazo_pos_x + i * self.max_weight/3
                        if i+1 == self.select_card:
                            pos_y = mazo_pos_y + (3*self.max_height/4)
                        else:
                            pos_y = mazo_pos_y
                        self.game.display.blit(carta, (pos_x,pos_y))
                        puntero = puntero.next
                else:
                    for i in range(sizedeck):
                        carta = pygame.image.load(eval(puntero.card["image"]))
                        carta = pygame.transform.scale(carta, (self.max_weight, self.max_height))
                        pos_x = mazo_pos_x + i * self.max_weight/3
                        pos_y = mazo_pos_y
                        self.game.display.blit(carta, (pos_x,pos_y))
                        puntero = puntero.next
                    

            #dibujar el cuarto mazo
            if i == 4:
                sizedeck = self.deck4.deck_size()
                puntero = self.deck4.head
                mazo_width = self.max_weight * sizedeck
                mazo_height = self.max_height
                mazo_pos_x = self.offsetx
                mazo_pos_y = (self.game.DISPLAY_H/2) - (mazo_width/6)
                if i == self.turno:
                    for i in range(1,sizedeck+1):
                        carta = pygame.image.load(eval(puntero.card["image"]))
                        carta = pygame.transform.scale(carta, (self.max_weight, self.max_height))
                        rotated_carta = pygame.transform.rotate(carta, 270)
                        pos_y = mazo_pos_y + i * self.max_weight/3
                        if i == self.select_card:
                            pos_x = mazo_pos_x + self.max_height
                        else:
                            pos_x = mazo_pos_x
                        self.game.display.blit(rotated_carta, (pos_x,pos_y))
                        puntero = puntero.next
                else:
                    for i in range(1,sizedeck+1):
                        carta = pygame.image.load(eval(puntero.card["image"]))
                        carta = pygame.transform.scale(carta, (self.max_weight, self.max_height))
                        rotated_carta = pygame.transform.rotate(carta, 270)
                        pos_y = mazo_pos_y + i * self.max_weight/3
                        pos_x = mazo_pos_x
                        self.game.display.blit(rotated_carta, (pos_x,pos_y))
                        puntero = puntero.next

    def draw_discard_deck(self):
        card_data = self.discard_deck.LastCardPlayed()
        carta = pygame.image.load(eval(card_data["image"]))
        carta = pygame.transform.scale(carta, (self.max_weight, self.max_height))
        imagen_pos_x = (self.game.DISPLAY_W - self.max_weight) // 2
        imagen_pos_y = (self.game.DISPLAY_H - self.max_height) // 2
        self.game.display.blit(carta, (imagen_pos_x, imagen_pos_y))
    def draw_main_deck(self):
        ruta_imagen = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'Cards','main_deck.png'))
        carta = pygame.image.load(ruta_imagen)
        carta = pygame.transform.scale(carta, (self.max_weight, self.max_height))
        imagen_pos_x = (self.game.DISPLAY_W - self.max_weight) // 3
        imagen_pos_y = (self.game.DISPLAY_H - self.max_height) // 2
        self.game.display.blit(carta, (imagen_pos_x, imagen_pos_y))

    def play_card(self):
        if self.turno == 1:
            puntero = self.deck1.head
            for i in range(self.select_card-1):
                puntero = puntero.next
            if self.check_play_card(puntero.card):
                self.power_card(puntero.card)
                self.discard_deck.Enqueue(self.deck1.remove_card(puntero.card))
                return True
            else:
                return False
        elif self.turno == 2:
            puntero = self.deck2.head
            for i in range(self.select_card-1):
                puntero = puntero.next
            if self.check_play_card(puntero.card):
                self.power_card(puntero.card)
                self.discard_deck.Enqueue(self.deck2.remove_card(puntero.card))
                return True
            else:
                return False
        elif self.turno == 3:
            puntero = self.deck3.head
            for i in range(self.select_card-1):
                puntero = puntero.next
            if self.check_play_card(puntero.card):
                self.power_card(puntero.card)
                self.discard_deck.Enqueue(self.deck3.remove_card(puntero.card))
                return True
            else:
                return False
        elif self.turno == 4:
            puntero = self.deck4.head
            for i in range(self.select_card-1):
                puntero = puntero.next
            if self.check_play_card(puntero.card):
                self.power_card(puntero.card)
                self.discard_deck.Enqueue(self.deck4.remove_card(puntero.card))
                return True
            else:
                return False

    def check_winner(self):
        if self.deck1.size == 0:
            self.game.draw_center_text("Jugador 1 Gana", self.game.font_size_title, self.game.DISPLAY_W/2,self.game.DISPLAY_H/2)
            self.blit_screen()
            while self.game.playing:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                            self.game.playing = False
                            self.run_display = False
        elif self.deck2.size == 0:
            self.game.draw_center_text("Jugador 2 Gana", self.game.font_size_title, self.game.DISPLAY_W/2,self.game.DISPLAY_H/2)
            self.blit_screen()
            while self.game.playing:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                            self.game.playing = False
                            self.run_display = False
        elif self.deck3.size == 0:
            self.game.draw_center_text("Jugador 3 Gana", self.game.font_size_title, self.game.DISPLAY_W/2,self.game.DISPLAY_H/2)
            self.blit_screen()
            while self.game.playing:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                            self.game.playing = False
                            self.run_display = False
        elif self.deck4.size == 0:
            self.game.draw_center_text("Jugador 4 Gana", self.game.font_size_title, self.game.DISPLAY_W/2,self.game.DISPLAY_H/2)
            self.blit_screen()
            while self.game.playing:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                            self.game.playing = False
                            self.run_display = False
        
    def check_play_card(self,card):
        discardCard = self.discard_deck.LastCardPlayed()
        if "number" in card and "number" in discardCard:
            if card["number"] == discardCard["number"] or card["color"] == discardCard["color"]:
                return True
            else:
                return False
        elif card["color"] == "Black" or card["color"] == discardCard["color"]:
            return True
        elif "power" in card and "power" in discardCard:
            if card["power"] == discardCard["power"]:
                return True
            else:
                return False
        else:
            return False

    def take_card(self):
        card = self.main_deck.PopBack()
        if self.turno == 1:
            self.deck1.add_card(card)
        elif self.turno == 2:
            self.deck2.add_card(card)
        elif self.turno == 3:
            self.deck3.add_card(card)
        elif self.turno == 4:
            self.deck4.add_card(card)

    def power_card(self,card):
        if "power" in card:
            if card["power"] == "Block":
                self.block = not self.block
            elif card["power"] == "+2":
                if self.reverse:
                    if self.turno == 1:
                        for i in range(2):
                            self.deck4.add_card(self.main_deck.PopBack())
                    elif self.turno == 2:
                        for i in range(2):
                            self.deck1.add_card(self.main_deck.PopBack())
                    elif self.turno == 3:
                        for i in range(2):
                            self.deck2.add_card(self.main_deck.PopBack())
                    elif self.turno == 4:
                        for i in range(2):
                            self.deck3.add_card(self.main_deck.PopBack())
                else:
                    if self.turno == 1:
                        for i in range(2):
                            self.deck2.add_card(self.main_deck.PopBack())
                    elif self.turno == 2:
                        for i in range(2):
                            self.deck3.add_card(self.main_deck.PopBack())
                    elif self.turno == 3:
                        for i in range(2):
                            self.deck4.add_card(self.main_deck.PopBack())
                    elif self.turno == 4:
                        for i in range(2):
                            self.deck1.add_card(self.main_deck.PopBack())

            elif card["power"] == "Reverse":
                self.reverse = not self.reverse

            elif card["power"] == "+4":
                if self.reverse:
                    if self.turno == 1:
                        for i in range(4):
                            self.deck4.add_card(self.main_deck.PopBack())
                    elif self.turno == 2:
                        for i in range(4):
                            self.deck1.add_card(self.main_deck.PopBack())
                    elif self.turno == 3:
                        for i in range(4):
                            self.deck2.add_card(self.main_deck.PopBack())
                    elif self.turno == 4:
                        for i in range(4):
                            self.deck3.add_card(self.main_deck.PopBack())
                else:
                    if self.turno == 1:
                        for i in range(4):
                            self.deck2.add_card(self.main_deck.PopBack())
                    elif self.turno == 2:
                        for i in range(4):
                            self.deck3.add_card(self.main_deck.PopBack())
                    elif self.turno == 3:
                        for i in range(4):
                            self.deck4.add_card(self.main_deck.PopBack())
                    elif self.turno == 4:
                        for i in range(4):
                            self.deck1.add_card(self.main_deck.PopBack())
                