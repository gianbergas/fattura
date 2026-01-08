#!/usr/bin/env python3
"""
Breakout Game - Un classico gioco di rimbalzo con mattoncini
"""

import pygame
import sys
import random
from typing import List, Tuple


# Inizializzazione Pygame
pygame.init()

# Costanti
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colori
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
CYAN = (0, 255, 255)

# Dimensioni
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 15
PADDLE_SPEED = 8
BALL_SIZE = 15
BALL_SPEED = 5
BRICK_WIDTH = 75
BRICK_HEIGHT = 30
BRICK_ROWS = 5
BRICK_COLS = 10
BRICK_GAP = 5


class Paddle:
    """Classe per la base/paddle"""
    
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.width = PADDLE_WIDTH
        self.height = PADDLE_HEIGHT
        self.speed = PADDLE_SPEED
        self.rect = pygame.Rect(x, y, self.width, self.height)
    
    def move_left(self):
        """Muove il paddle a sinistra"""
        self.x = max(0, self.x - self.speed)
        self.rect.x = self.x
    
    def move_right(self):
        """Muove il paddle a destra"""
        self.x = min(SCREEN_WIDTH - self.width, self.x + self.speed)
        self.rect.x = self.x
    
    def draw(self, screen: pygame.Surface):
        """Disegna il paddle"""
        pygame.draw.rect(screen, CYAN, self.rect)
        pygame.draw.rect(screen, WHITE, self.rect, 2)


class Ball:
    """Classe per la pallina"""
    
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.size = BALL_SIZE
        self.speed_x = random.choice([-BALL_SPEED, BALL_SPEED])
        self.speed_y = -BALL_SPEED
        self.rect = pygame.Rect(x, y, self.size, self.size)
    
    def update(self):
        """Aggiorna la posizione della pallina"""
        self.x += self.speed_x
        self.y += self.speed_y
        self.rect.x = self.x
        self.rect.y = self.y
        
        # Rimbalzo sui bordi laterali
        if self.x <= 0 or self.x >= SCREEN_WIDTH - self.size:
            self.speed_x = -self.speed_x
        
        # Rimbalzo sul bordo superiore
        if self.y <= 0:
            self.speed_y = -self.speed_y
    
    def draw(self, screen: pygame.Surface):
        """Disegna la pallina"""
        pygame.draw.circle(screen, YELLOW, 
                          (self.x + self.size // 2, self.y + self.size // 2), 
                          self.size // 2)
        pygame.draw.circle(screen, WHITE, 
                          (self.x + self.size // 2, self.y + self.size // 2), 
                          self.size // 2, 2)
    
    def reset(self, x: int, y: int):
        """Riposiziona la pallina"""
        self.x = x
        self.y = y
        self.speed_x = random.choice([-BALL_SPEED, BALL_SPEED])
        self.speed_y = -BALL_SPEED
        self.rect.x = self.x
        self.rect.y = self.y


class Brick:
    """Classe per i mattoncini"""
    
    def __init__(self, x: int, y: int, color: Tuple[int, int, int]):
        self.x = x
        self.y = y
        self.width = BRICK_WIDTH
        self.height = BRICK_HEIGHT
        self.color = color
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.destroyed = False
    
    def draw(self, screen: pygame.Surface):
        """Disegna il mattoncino"""
        if not self.destroyed:
            pygame.draw.rect(screen, self.color, self.rect)
            pygame.draw.rect(screen, WHITE, self.rect, 2)


class Game:
    """Classe principale del gioco"""
    
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Breakout Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.big_font = pygame.font.Font(None, 72)
        
        self.reset_game()
    
    def reset_game(self):
        """Resetta il gioco"""
        # Crea il paddle
        paddle_x = SCREEN_WIDTH // 2 - PADDLE_WIDTH // 2
        paddle_y = SCREEN_HEIGHT - 50
        self.paddle = Paddle(paddle_x, paddle_y)
        
        # Crea la pallina
        ball_x = SCREEN_WIDTH // 2 - BALL_SIZE // 2
        ball_y = SCREEN_HEIGHT - 100
        self.ball = Ball(ball_x, ball_y)
        
        # Crea i mattoncini
        self.bricks: List[Brick] = []
        colors = [RED, ORANGE, YELLOW, GREEN, BLUE]
        
        start_y = 50
        for row in range(BRICK_ROWS):
            color = colors[row % len(colors)]
            start_x = (SCREEN_WIDTH - (BRICK_COLS * (BRICK_WIDTH + BRICK_GAP) - BRICK_GAP)) // 2
            for col in range(BRICK_COLS):
                x = start_x + col * (BRICK_WIDTH + BRICK_GAP)
                y = start_y + row * (BRICK_HEIGHT + BRICK_GAP)
                brick = Brick(x, y, color)
                self.bricks.append(brick)
        
        self.score = 0
        self.lives = 3
        self.game_over = False
        self.victory = False
    
    def check_collisions(self):
        """Controlla le collisioni"""
        # Collisione con il paddle
        if self.ball.rect.colliderect(self.paddle.rect):
            # Calcola il punto di impatto sul paddle
            hit_pos = (self.ball.x + self.ball.size // 2) - self.paddle.x
            normalized = hit_pos / self.paddle.width  # 0 a 1
            angle = normalized * 2 - 1  # -1 a 1
            
            self.ball.speed_x = angle * BALL_SPEED
            self.ball.speed_y = -abs(self.ball.speed_y)
            
            # Assicura che la pallina non entri nel paddle
            self.ball.y = self.paddle.y - self.ball.size
        
        # Collisione con i mattoncini
        for brick in self.bricks:
            if not brick.destroyed and self.ball.rect.colliderect(brick.rect):
                brick.destroyed = True
                self.score += 10
                
                # Determina la direzione del rimbalzo
                ball_center_x = self.ball.x + self.ball.size // 2
                ball_center_y = self.ball.y + self.ball.size // 2
                brick_center_x = brick.x + brick.width // 2
                brick_center_y = brick.y + brick.height // 2
                
                dx = ball_center_x - brick_center_x
                dy = ball_center_y - brick_center_y
                
                if abs(dx) > abs(dy):
                    self.ball.speed_x = BALL_SPEED if dx > 0 else -BALL_SPEED
                else:
                    self.ball.speed_y = BALL_SPEED if dy > 0 else -BALL_SPEED
                
                break
        
        # Controlla se tutti i mattoncini sono distrutti
        if all(brick.destroyed for brick in self.bricks):
            self.victory = True
    
    def update(self):
        """Aggiorna lo stato del gioco"""
        if self.game_over or self.victory:
            return
        
        # Muovi la pallina
        self.ball.update()
        
        # Controlla se la pallina è caduta
        if self.ball.y > SCREEN_HEIGHT:
            self.lives -= 1
            if self.lives <= 0:
                self.game_over = True
            else:
                # Riposiziona la pallina
                ball_x = SCREEN_WIDTH // 2 - BALL_SIZE // 2
                ball_y = SCREEN_HEIGHT - 100
                self.ball.reset(ball_x, ball_y)
        
        # Controlla collisioni
        self.check_collisions()
    
    def draw(self):
        """Disegna tutto sullo schermo"""
        self.screen.fill(BLACK)
        
        if self.game_over:
            text = self.big_font.render("GAME OVER", True, RED)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
            self.screen.blit(text, text_rect)
            
            score_text = self.font.render(f"Punteggio finale: {self.score}", True, WHITE)
            score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
            self.screen.blit(score_text, score_rect)
            
            restart_text = self.font.render("Premi R per ricominciare", True, WHITE)
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
            self.screen.blit(restart_text, restart_rect)
        
        elif self.victory:
            text = self.big_font.render("VITTORIA!", True, GREEN)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
            self.screen.blit(text, text_rect)
            
            score_text = self.font.render(f"Punteggio: {self.score}", True, WHITE)
            score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
            self.screen.blit(score_text, score_rect)
            
            restart_text = self.font.render("Premi R per ricominciare", True, WHITE)
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
            self.screen.blit(restart_text, restart_rect)
        
        else:
            # Disegna mattoncini
            for brick in self.bricks:
                brick.draw(self.screen)
            
            # Disegna paddle
            self.paddle.draw(self.screen)
            
            # Disegna pallina
            self.ball.draw(self.screen)
            
            # Disegna informazioni
            score_text = self.font.render(f"Punteggio: {self.score}", True, WHITE)
            self.screen.blit(score_text, (10, 10))
            
            lives_text = self.font.render(f"Vite: {self.lives}", True, WHITE)
            self.screen.blit(lives_text, (10, 50))
        
        pygame.display.flip()
    
    def run(self):
        """Loop principale del gioco"""
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r and (self.game_over or self.victory):
                        self.reset_game()
                    if event.key == pygame.K_ESCAPE:
                        running = False
            
            # Controlli del paddle
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.paddle.move_left()
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.paddle.move_right()
            
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()


def main():
    """Funzione principale"""
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
