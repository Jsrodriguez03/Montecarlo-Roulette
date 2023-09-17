import pygame
import sys
import math
import random

# Inicializa Pygame
pygame.init()

# Tamaño de la ventana
width, height = 800, 600

# Crea la ventana
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Ruleta con Bolita en Pygame")

# Carga una imagen de la ruleta
imagen_ruleta = pygame.image.load("ruleta.png")

# Redimensiona la imagen al 50% de su tamaño original
nuevo_ancho = int(imagen_ruleta.get_width() * 0.5)
nuevo_alto = int(imagen_ruleta.get_height() * 0.5)
imagen_ruleta = pygame.transform.scale(
    imagen_ruleta, (nuevo_ancho, nuevo_alto))

# Carga una imagen para la bolita
bolita = pygame.image.load("bolita.png")

# Redimensiona la bolita al tamaño deseado
bolita = pygame.transform.scale(bolita, (20, 20))

# Ángulo inicial aleatorio para la animación de la bolita
angulo_inicial = random.uniform(0, 360)

# Velocidad de rotación aleatoria
# Puedes ajustar el rango de velocidad aquí
velocidad_rotacion = random.uniform(2, 5)

# Factor de rozamiento
rozamiento = 0.99

# Radio de la ruleta
radio_ruleta = min(width, height) // 3  # Radio igual al tercio del menor lado

# Centro de la ventana
centro_x = width // 2
centro_y = height // 2

# Controla si se ha determinado el resultado
resultado_determinado = False

# Controla el bucle principal del juego
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Calcula las nuevas coordenadas polares de la bolita para simular su giro
    angulo_inicial += velocidad_rotacion
    x = int(centro_x + radio_ruleta * math.cos(math.radians(angulo_inicial)))
    y = int(centro_y + radio_ruleta * math.sin(math.radians(angulo_inicial)))

    # Dibuja la imagen de la ruleta en el lienzo centrada en el centro de la ventana
    screen.blit(imagen_ruleta, (centro_x - imagen_ruleta.get_width() //
                2, centro_y - imagen_ruleta.get_height() // 2))

    # Dibuja la bolita en su posición actual
    screen.blit(bolita, (x - bolita.get_width() //
                2, y - bolita.get_height() // 2))

    # Determina el resultado cuando la velocidad es muy baja y no se ha determinado antes
    if abs(velocidad_rotacion) < 0.1 and not resultado_determinado:
        # Calcula el ángulo en función del cual se determina el resultado
        angulo_resultado = (angulo_inicial + 360) % 360

        # Calcula la casilla en la que cayó la bolita
        # 37 casillas en total (0 al 36)
        casilla = int(angulo_resultado / (360 / 37))

        # Verifica si la casilla es par o impar
        par_impar = "Par" if casilla % 2 == 0 else "Impar"

        # Determina el color de la casilla
        color_casilla = "Rojo" if casilla in [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36] else (
            "Negro" if casilla in [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35] else "Verde")

        # Renderiza el resultado como texto en una superficie
        resultado = f"Resultado: {casilla} - {color_casilla} - {par_impar}"
        font = pygame.font.Font(None, 36)
        texto_superficie = font.render(resultado, True, (255, 255, 255))
        texto_rect = texto_superficie.get_rect()
        texto_rect.center = (width // 2, height - 30)  # Posición del texto

        # Dibuja el resultado en el lienzo
        screen.blit(texto_superficie, texto_rect)

        resultado_determinado = True

    # Actualiza la ventana
    pygame.display.flip()

    # Aplica rozamiento para reducir la velocidad gradualmente
    velocidad_rotacion *= rozamiento

    # Detiene la bolita cuando la velocidad es muy baja
    if abs(velocidad_rotacion) < 0.1 and resultado_determinado:
        pass

# Cierra Pygame al salir
pygame.quit()
sys.exit()
