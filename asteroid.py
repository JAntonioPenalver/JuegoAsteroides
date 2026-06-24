import pygame
import random
from circleshape import CircleShape
from constants import ASTEROID_MIN_RADIUS
from logger import log_event

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, 2)

    def update(self, dt):
        self.position += self.velocity * dt

    def split(self):
        # Destruir inmediatamente el asteroide actual
        self.kill()

        # Si es un asteroide pequeño, terminamos
        if self.radius <= ASTEROID_MIN_RADIUS:
            return

        # Registrar el evento de división
        log_event("asteroid_split")

        # Generar un ángulo aleatorio entre 20 y 50 grados
        random_angle = random.uniform(20, 50)

        # Crear dos vectores de velocidad rotados
        new_velocity1 = self.velocity.rotate(random_angle)
        new_velocity2 = self.velocity.rotate(-random_angle)

        # Calcular el nuevo radio reducido
        new_radius = self.radius - ASTEROID_MIN_RADIUS

        # Crear los dos nuevos asteroides más pequeños en la posición actual
        asteroid1 = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid2 = Asteroid(self.position.x, self.position.y, new_radius)

        # Asignar velocidades aceleradas por un factor de 1.2
        asteroid1.velocity = new_velocity1 * 1.2
        asteroid2.velocity = new_velocity2 * 1.2
