import pygame
import sys
import time
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from logger import log_state, log_event
from player import Player
from asteroid import Asteroid
from shot import Shot
from asteroidfield import AsteroidField

def main():
    # Inicializar pygame
    pygame.init()

    # Crear la ventana
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # Control de FPS
    clock = pygame.time.Clock()
    dt = 0.0

    # Crear grupos
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    # Asignar grupos a las clases
    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    Shot.containers = (shots, updatable, drawable)
    AsteroidField.containers = (updatable,)

    # Crear el jugador
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    # Crear el campo de asteroides
    asteroid_field = AsteroidField()

    # Tiempo de inicio para ejecutar durante 5 segundos
    start_time = time.time()

    # Game loop
    while True:
        # Registrar estado
        log_state(player, updatable, drawable, asteroids, shots)

        # Procesar eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        # Actualizar todos los objetos updatable
        updatable.update(dt)

        # Verificar colisiones con asteroides
        for asteroid in asteroids:
            if player.collides_with(asteroid):
                log_event("player_hit")
                print("Game over!")
                sys.exit()

        # Verificar colisiones entre disparos y asteroides
        for asteroid in asteroids:
            for shot in shots:
                if asteroid.collides_with(shot):
                    log_event("asteroid_shot")
                    shot.kill()
                    # Cambiado de .kill() a .split()
                    asteroid.split()

        # Llenar pantalla de negro
        screen.fill("black")

        # Dibujar todos los objetos drawable
        for sprite in drawable:
            sprite.draw(screen)

        # Actualizar pantalla
        pygame.display.flip()

        # Controlar FPS (60 FPS max)
        dt = clock.tick(60) / 1000

        # Salir automáticamente después de 5 segundos
        if time.time() - start_time > 5:
            return

if __name__ == "__main__":
    main()
