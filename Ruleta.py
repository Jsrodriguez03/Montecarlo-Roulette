import tkinter as tk
import random
import math
import time
from tkinter.tix import IMAGETEXT
from PIL import Image, ImageTk
from tkinter import PhotoImage
import pygame
from PIL import Image, ImageTk


class RuletaMontecarlo:
    def __init__(self, root):
       # Ventana Principal
        self.root = root
        self.root.title("Simulación de Ruleta de Montecarlo")

        # Lienzo para dibujar la ruleta y la bolita
        self.canvas = tk.Canvas(root, width=400, height=400)
        self.canvas.pack()
        self.canvas.configure(bg="#632218")

        # Botón Para Girar la Ruleta
        self.boton_girar = tk.Button(
            root, text="Girar la ruleta", command=self.animar_giro)
        self.boton_girar.pack()

        self.canvas.create_text(200, 25, text="Monte-Carlos Roulette", font=(
            "Times New Roman", 20, "bold"), fill="white")

        self.dibujar_ruleta()

        # Variables Necesarias
        self.angulo = 0
        self.velocidad = 100  # Velocidad de giro
        self.girando = False
        self.friction = 0.8  # Factor de fricción
        self.resultado = None
        self.bolita_diametro = 15
        self.bolita_x = None
        self.bolita_y = None

    # Función para Animar el Giro

    def animar_giro(self):
        if not self.girando:
            self.girando = True
            self.resultado = None
            self.angulo_inicial = random.uniform(
                0, 360)  # Ángulo inicial aleatorio
            self.bolita_x = 200
            self.bolita_y = 50
            self.canvas.delete("bolita")  # Limpia cualquier bolita anterior
            # Limpia cualquier resultado anterior
            self.canvas.delete("resultado")
            self.girar_ruleta()
        else:
            self.girando = False
            # Limpia la bolita si se detiene manualmente
            self.canvas.delete("bolita")

        # Luego, en el método detener_bolita, después de mostrar el resultado:
        self.girando = False

    # Función para Girar Ruleta
    def girar_ruleta(self):
        self.canvas.delete("flecha")
        self.angulo += self.velocidad
        self.dibujar_ruleta()

        if self.angulo < 360:
            self.root.after(100, self.girar_ruleta)
        else:
            self.angulo = self.angulo % 360
            self.detener_bolita()

    def detener_bolita(self):
        velocidad_inicial = self.velocidad
        while velocidad_inicial > 0.5:
            self.angulo += velocidad_inicial
            self.bolita_x = 200 + 150 * \
                math.cos(math.radians(self.angulo_inicial + self.angulo))
            self.bolita_y = 200 + 150 * \
                math.sin(math.radians(self.angulo_inicial + self.angulo))
            velocidad_inicial *= self.friction
            # Elimina la bolita anterior antes de redibujarla
            self.canvas.delete("bolita")
            self.dibujar_ruleta()
            self.dibujar_bolita()
            self.root.update()
            time.sleep(0.05)

        # Calcula el número de la casilla en función del ángulo final y la disposición de los números
        angulo_final = (self.angulo_inicial + self.angulo) % 360
        casilla = int((angulo_final / (360 / len(self.numeros_ruleta))))

        # Obtiene el número de la casilla
        numero_resultado = self.numeros_ruleta[casilla]

        # Determina el color de la casilla
        color_casilla = "Red" if numero_resultado in [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36] else (
            "Black" if numero_resultado in [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35] else "Green")

        # Determina si el número es par o impar
        par_impar = "Odd" if numero_resultado % 2 == 0 else "Even"

        # Crea el mensaje con la información
        mensaje = f"{numero_resultado} - {color_casilla} - {par_impar}"

        self.canvas.delete("resultado")
        self.canvas.create_text(200, 380, text=mensaje, font=(
            "Times New Roman", 16), tag="resultado", fill="white")

    # Función para Dibujar la Ruleta

    def dibujar_ruleta(self):
        # Agrega esta lista de números en la inicialización de la clase RuletaMontecarlo Números del 0 al 36
        self.numeros_ruleta = [6, 27, 13, 36, 11, 30, 8, 23, 10, 5, 24, 16, 33, 1, 20, 14,
                               31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26, 0, 32, 15, 19, 4, 21, 2, 25, 17, 34]

        colores_fondo = ["red", "black", "red", "black", "red", "black", "red", "black", "red", "green", "black", "red",
                         "black", "red", "black", "red", "black", "red", "black", "red", "black",
                         "red", "black", "red", "black", "red", "black", "red", "black", "red", "black",
                         "red", "black", "red", "black", "red", "black"]

        # Dibuja un círculo para representar la ruleta
        self.canvas.create_oval(50 + 1, 50 + 1, 350 - 1,
                                350 - 1, outline="#FFC455", width=4)

        # Dibuja las divisiones de la ruleta con números
        for i, numero in enumerate(self.numeros_ruleta):
            angulo = i * (360 / len(self.numeros_ruleta))
            x1 = 200 + 150 * (0.9 if i % 2 == 0 else 0.95) * \
                (-(1 if i % 2 == 0 else -1) * 0.9 * 0.5)
            y1 = 200 + 150 * (0.9 if i % 2 == 0 else 0.95) * \
                (-0.5 if i % 2 == 0 else 0.5)
            x2 = 200 + 150 * (0.9 if i % 2 == 0 else 0.95) * \
                (-(1 if i % 2 == 0 else -1) * 0.9)
            y2 = 200 + 150 * (0.9 if i % 2 == 0 else 0.95) * \
                (-1 if i % 2 == 0 else 1)

            # Determina el color de fondo de la casilla
            color_fondo = colores_fondo[i]

            # Dibuja el arco de la división
            self.canvas.create_arc(50 + 1, 50 + 1, 350 - 1, 350 - 1, start=angulo,
                                   extent=360 / len(self.numeros_ruleta), outline="#FFC455", width=2, fill=color_fondo)

            # Dibuja el número en el centro de la división
            angulo = i * (360 / len(self.numeros_ruleta))
            x_text = 200 + 135 * \
                math.cos(math.radians(
                    angulo + (360 / (len(self.numeros_ruleta) * 2))))
            y_text = 200 + 135 * \
                math.sin(math.radians(
                    angulo + (360 / (len(self.numeros_ruleta) * 2))))
            numero_tag = f"numero_{numero}"

            self.canvas.create_text(x_text, y_text, text=str(
                numero), font=("Times New Roman", 13, "bold"), fill="white", tags=(numero_tag,))

            # Superposición de Números
            self.canvas.tag_raise(f"numero_{i}")
            self.canvas.tag_raise("numero_6")
            self.canvas.tag_raise("numero_27")
            self.canvas.tag_raise("numero_13")
            self.canvas.tag_raise("numero_11")
            self.canvas.tag_raise("numero_30")
            self.canvas.tag_raise("numero_8")
            self.canvas.tag_raise("numero_23")
            self.canvas.tag_raise("numero_10")
            self.canvas.tag_raise("numero_5")
            self.canvas.tag_raise("numero_24")
            self.canvas.tag_raise("numero_16")
            self.canvas.tag_raise("numero_1")
            self.canvas.tag_raise("numero_20")
            self.canvas.tag_raise("numero_14")
            self.canvas.tag_raise("numero_9")

            # Dibuja las líneas radiales desde el centro hasta el final de la ruleta
        for i in range(len(self.numeros_ruleta)):
            angulo = i * (360 / len(self.numeros_ruleta))
            x1 = 200
            y1 = 200
            x2 = 200 + 110 * math.cos(math.radians(angulo))
            y2 = 200 + 110 * math.sin(math.radians(angulo))

            # Dibuja la línea radial desde el centro hasta el círculo negro
            self.canvas.create_line(x1, y1, x2, y2, fill="#FFC455", width=4)

            # Luego, dibuja la línea radial desde el círculo negro hasta el círculo bajo los números
            x2 = 200 + 150 * math.cos(math.radians(angulo))
            y2 = 200 + 150 * math.sin(math.radians(angulo))
            self.canvas.create_line(x1, y1, x2, y2, fill="#FFC455", width=2)

        # Dibuja un círculo debajo de los numeros
        # Calcula el tamaño proporcional para el círculo negro
        radio_circulo = 0.7 * 160  # 70% del radio de la ruleta

        # Calcula las coordenadas para el círculo negro
        x1_circulo = 200 - radio_circulo
        y1_circulo = 200 - radio_circulo
        x2_circulo = 200 + radio_circulo
        y2_circulo = 200 + radio_circulo

        # Dibuja el círculo negro proporcional
        self.canvas.create_oval(
            x1_circulo, y1_circulo, x2_circulo, y2_circulo, outline="#FFC455", width=4)

        # Dibuja un círculo negro en la mitad de la ruleta
        # Calcula el tamaño proporcional para el círculo negro
        radio_circulo_negro = 0.7 * 120  # 70% del radio de la ruleta

        # Calcula las coordenadas para el círculo negro
        x1_circulo = 200 - radio_circulo_negro
        y1_circulo = 200 - radio_circulo_negro
        x2_circulo = 200 + radio_circulo_negro
        y2_circulo = 200 + radio_circulo_negro

        # Dibuja el círculo negro proporcional
        self.canvas.create_oval(
            x1_circulo, y1_circulo, x2_circulo, y2_circulo,  outline="#FFC455")

        # Cargar la imagen con transparencia
        self.imagen_redimensionada = Image.open("Centro.png").convert("RGBA")
        self.image_tk = ImageTk.PhotoImage(self.imagen_redimensionada)

        # Redimensionar la imagen a 260x260 píxeles
        self.imagen_redimensionada = self.imagen_redimensionada.resize(
            (260, 260))

        # Crear la imagen Tkinter
        self.image_tk = ImageTk.PhotoImage(self.imagen_redimensionada)

        # Mostrar la imagen sin fondo blanco y elevarla sobre otros elementos
        self.canvas.create_image(71, 71, anchor=tk.NW,
                                 image=self.image_tk, tag="imagen")
        # Elevar la imagen sobre otros elementos
        self.canvas.tag_raise("imagen")

    def dibujar_bolita(self):
        if self.bolita_x is not None and self.bolita_y is not None:
            # Dibuja la bolita sobre la imagen de la ruleta
            self.canvas.create_oval(self.bolita_x - self.bolita_diametro / 2,
                                    self.bolita_y - self.bolita_diametro / 2,
                                    self.bolita_x + self.bolita_diametro / 2,
                                    self.bolita_y + self.bolita_diametro / 2,
                                    fill="white", tag="bolita")


if __name__ == "__main__":
    root = tk.Tk()
    app = RuletaMontecarlo(root)
    root.mainloop()
