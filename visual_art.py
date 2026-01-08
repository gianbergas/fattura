#!/usr/bin/env python3
"""
Visual Art Generator - Un programma con visualizzazioni colorate e animate
"""

import pygame
import sys
import math
import random
from typing import List, Tuple


# Inizializzazione Pygame
pygame.init()

# Costanti
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
FPS = 60

# Colori
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class Particle:
    """Particella per effetti visivi"""
    
    def __init__(self, x: float, y: float, color: Tuple[int, int, int]):
        self.x = x
        self.y = y
        self.color = color
        self.radius = random.randint(2, 5)
        self.vx = random.uniform(-2, 2)
        self.vy = random.uniform(-2, 2)
        self.life = 255
        self.decay = random.uniform(0.5, 2)
    
    def update(self):
        """Aggiorna la particella"""
        self.x += self.vx
        self.y += self.vy
        self.life -= self.decay
        
        # Rimbalzo sui bordi
        if self.x < 0 or self.x > SCREEN_WIDTH:
            self.vx = -self.vx
        if self.y < 0 or self.y > SCREEN_HEIGHT:
            self.vy = -self.vy
        
        # Attrazione verso il centro
        center_x, center_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        dx = center_x - self.x
        dy = center_y - self.y
        dist = math.sqrt(dx*dx + dy*dy)
        if dist > 0:
            self.vx += dx * 0.0001
            self.vy += dy * 0.0001
    
    def draw(self, screen: pygame.Surface):
        """Disegna la particella"""
        if self.life > 0:
            alpha = max(0, min(255, int(self.life)))
            color = tuple(min(255, int(c * alpha / 255)) for c in self.color)
            pygame.draw.circle(screen, color, (int(self.x), int(self.y)), self.radius)


class Wave:
    """Onda per visualizzazioni"""
    
    def __init__(self, y: float, amplitude: float, frequency: float, speed: float, color: Tuple[int, int, int]):
        self.y = y
        self.amplitude = amplitude
        self.frequency = frequency
        self.speed = speed
        self.color = color
        self.time = 0
    
    def update(self):
        """Aggiorna l'onda"""
        self.time += self.speed
    
    def draw(self, screen: pygame.Surface):
        """Disegna l'onda"""
        points = []
        for x in range(0, SCREEN_WIDTH, 2):
            y = self.y + self.amplitude * math.sin((x * self.frequency + self.time) * 0.01)
            points.append((x, int(y)))
        
        if len(points) > 1:
            pygame.draw.lines(screen, self.color, False, points, 3)


class VisualArt:
    """Classe principale per le visualizzazioni"""
    
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Visual Art Generator - Premi 1-5 per cambiare modalità")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        
        self.mode = 1
        self.time = 0
        
        # Inizializza particelle
        self.particles: List[Particle] = []
        self.init_particles()
        
        # Inizializza onde
        self.waves: List[Wave] = []
        self.init_waves()
    
    def init_particles(self):
        """Inizializza le particelle"""
        self.particles = []
        for _ in range(200):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT)
            color = (
                random.randint(100, 255),
                random.randint(100, 255),
                random.randint(100, 255)
            )
            self.particles.append(Particle(x, y, color))
    
    def init_waves(self):
        """Inizializza le onde"""
        colors = [
            (255, 100, 100),
            (100, 255, 100),
            (100, 100, 255),
            (255, 255, 100),
            (255, 100, 255),
            (100, 255, 255),
        ]
        for i, color in enumerate(colors):
            y = SCREEN_HEIGHT // 2 + (i - len(colors)/2) * 80
            self.waves.append(Wave(y, 50 + i*10, 0.1, 2 + i*0.5, color))
    
    def generate_color(self, t: float) -> Tuple[int, int, int]:
        """Genera un colore basato sul tempo"""
        r = int(127 + 127 * math.sin(t * 0.01))
        g = int(127 + 127 * math.sin(t * 0.01 + 2))
        b = int(127 + 127 * math.sin(t * 0.01 + 4))
        return (r, g, b)
    
    def draw_mode_1(self):
        """Modalità 1: Spirali colorate"""
        center_x, center_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        
        for i in range(100):
            angle = self.time * 0.5 + i * 0.1
            radius = i * 3
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            
            color = self.generate_color(self.time + i)
            size = 5 + 3 * math.sin(self.time * 0.1 + i)
            pygame.draw.circle(self.screen, color, (int(x), int(y)), int(size))
    
    def draw_mode_2(self):
        """Modalità 2: Onde colorate"""
        for wave in self.waves:
            wave.update()
            wave.draw(self.screen)
    
    def draw_mode_3(self):
        """Modalità 3: Particelle con attrazione"""
        for particle in self.particles:
            particle.update()
            particle.draw(self.screen)
        
        # Aggiungi nuove particelle
        if len(self.particles) < 200:
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT)
            color = self.generate_color(self.time)
            self.particles.append(Particle(x, y, color))
    
    def draw_mode_4(self):
        """Modalità 4: Mandala rotante"""
        center_x, center_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        
        for layer in range(10):
            radius = 50 + layer * 40
            num_points = 8 + layer * 2
            
            for i in range(num_points):
                angle = (2 * math.pi * i / num_points) + self.time * 0.02
                x = center_x + radius * math.cos(angle)
                y = center_y + radius * math.sin(angle)
                
                color = self.generate_color(self.time + layer * 10)
                size = 8 + 5 * math.sin(self.time * 0.1 + layer)
                pygame.draw.circle(self.screen, color, (int(x), int(y)), int(size))
    
    def draw_mode_5(self):
        """Modalità 5: Effetto tunnel/starfield"""
        center_x, center_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        
        for i in range(200):
            angle = random.uniform(0, 2 * math.pi)
            distance = random.uniform(0, 400)
            speed = random.uniform(0.5, 2)
            
            x = center_x + distance * math.cos(angle + self.time * speed * 0.01)
            y = center_y + distance * math.sin(angle + self.time * speed * 0.01)
            
            # Colore basato sulla distanza
            dist_from_center = math.sqrt((x - center_x)**2 + (y - center_y)**2)
            intensity = max(0, 255 - dist_from_center * 0.5)
            color = (intensity, intensity, 255)
            
            size = max(1, 3 - dist_from_center * 0.01)
            pygame.draw.circle(self.screen, color, (int(x), int(y)), int(size))
    
    def draw(self):
        """Disegna la visualizzazione corrente"""
        # Sfondo nero
        self.screen.fill(BLACK)
        
        # Disegna in base alla modalità
        if self.mode == 1:
            self.draw_mode_1()
        elif self.mode == 2:
            self.draw_mode_2()
        elif self.mode == 3:
            self.draw_mode_3()
        elif self.mode == 4:
            self.draw_mode_4()
        elif self.mode == 5:
            self.draw_mode_5()
        
        # UI
        mode_text = self.font.render(f"Modalità: {self.mode}/5", True, WHITE)
        self.screen.blit(mode_text, (10, 10))
        
        help_text = self.font.render("Premi 1-5 per cambiare modalità | ESC per uscire", True, WHITE)
        self.screen.blit(help_text, (10, SCREEN_HEIGHT - 40))
        
        pygame.display.flip()
    
    def run(self):
        """Loop principale"""
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_1:
                        self.mode = 1
                    elif event.key == pygame.K_2:
                        self.mode = 2
                    elif event.key == pygame.K_3:
                        self.mode = 3
                    elif event.key == pygame.K_4:
                        self.mode = 4
                    elif event.key == pygame.K_5:
                        self.mode = 5
            
            self.time += 1
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()


def main():
    """Funzione principale"""
    app = VisualArt()
    app.run()


if __name__ == "__main__":
    main()
