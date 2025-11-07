import random 
import pygame 
from pygame import mixer
import os 
import sys
import math
import json
from datetime import datetime

def resource_path(relative_path):
    """Función para rutas compatibles con Linux y Windows"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    path = os.path.join(base_path, relative_path)
    return os.path.normpath(path)

def verificar_dependencias():
    """Verificar que todas las dependencias estén disponibles"""
    try:
        pygame.init()
        mixer.init()
        return True
    except Exception as e:
        print(f"Error inicializando Pygame: {e}")
        return False

# Inicializar Pygame con verificación
if not verificar_dependencias():
    print("Error: Pygame no está instalado correctamente.")
    print("Instala con: sudo apt install python3-pygame")
    sys.exit(1)

# CONSTANTES DEL JUEGO - AJUSTADAS PARA MEJOR BALANCE
ANCHO, ALTO = 1400, 900  
TAMANIO_CELDA = 45
FILAS_LABERINTO, COLUMNAS_LABERINTO = 15, 15  # Reducido para hacerlo más fácil
ANCHO_LABERINTO = COLUMNAS_LABERINTO * TAMANIO_CELDA
ALTO_LABERINTO = FILAS_LABERINTO * TAMANIO_CELDA
MARGEN_X = (ANCHO - ANCHO_LABERINTO) // 2 - 150
MARGEN_Y = (ALTO - ALTO_LABERINTO) // 2 - 30

FPS = 90

# PALETA DE COLORES MEJORADA
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
GRIS = (40, 40, 40)
COLOR_BOTON = (70, 130, 200)        # Azul moderno
COLOR_BOTON_HOVER = (100, 160, 230) # Azul claro
COLOR_BOTON_SECUNDARIO = (80, 180, 100) # Verde
COLOR_BOTON_SECUNDARIO_HOVER = (110, 210, 130) # Verde claro
COLOR_FONDO = (8, 8, 25)
COLOR_LABERINTO = (20, 20, 45)
COLOR_BORDE = (80, 80, 160)
COLOR_TEXTO = (230, 245, 255)
COLOR_TEXTO_IMPORTANTE = (180, 220, 255)
COLOR_PARED = (35, 35, 75)
COLOR_CAMINO = (25, 25, 55)
COLOR_JUGADOR = (0, 200, 255)
COLOR_ENEMIGO = (220, 80, 160)
COLOR_OBJETIVO = (220, 180, 40)
COLOR_OBJETO = (60, 220, 140)
COLOR_VISION = (255, 255, 255, 60)

# Gradientes para efectos
GRADIENTE_CIELO = [(8, 8, 25), (15, 15, 40), (25, 25, 60), (40, 40, 100)]
GRADIENTE_PANEL = [(25, 35, 65), (35, 45, 85), (45, 55, 105)]

# Crear pantalla
pantalla = pygame.display.set_mode((ANCHO, ALTO), pygame.DOUBLEBUF | pygame.HWSURFACE)
pygame.display.set_caption("Laberinto Cósmico - Escape Imposible")

# Variables globales para fuentes
fuente = None
fuente_game_over = None
fuente_pista = None

# Configuración de audio
def cargar_audio():
    """Cargar recursos de audio"""
    try:
        mixer.music.set_volume(0.6)
        return True
    except Exception as e:
        print(f"Error inicializando audio: {e}")
        return False

cargar_audio()

# Cargar icono
def cargar_icono():
    """Crear icono programáticamente"""
    try:
        icono = pygame.Surface((32, 32), pygame.SRCALPHA)
        icono.fill((10, 10, 30))
        
        pygame.draw.rect(icono, (0, 200, 255), (6, 6, 20, 20), 1)
        pygame.draw.rect(icono, (220, 180, 40), (18, 18, 8, 8))
        pygame.draw.rect(icono, (0, 200, 255), (8, 8, 4, 4))
        
        pygame.display.set_icon(icono)
        return True
    except Exception as e:
        print(f"No se pudo cargar icono: {e}")
        return False

cargar_icono()

# SISTEMA DE PARTÍCULAS
particulas = []

class Particula:
    def __init__(self, x, y, tipo="brillo", color=None, tamaño_extra=0):
        self.x = x
        self.y = y
        self.tipo = tipo
        self.life = random.uniform(80, 160)
        self.max_life = self.life
        self.size = random.randint(3, 8) + tamaño_extra
        
        if tipo == "brillo":
            self.color = color or (random.randint(200, 255), random.randint(200, 255), random.randint(150, 255))
            self.vx = random.uniform(-1.5, 1.5)
            self.vy = random.uniform(-1.5, 1.5)
            self.gravity = 0.02
        elif tipo == "humo":
            self.color = (random.randint(80, 120), random.randint(80, 120), random.randint(80, 120))
            self.vx = random.uniform(-0.8, 0.8)
            self.vy = random.uniform(-2.5, -1.5)
            self.gravity = -0.01
            self.size = random.randint(4, 10)
        elif tipo == "chispas":
            self.color = color or (random.randint(200, 255), random.randint(150, 255), random.randint(0, 100))
            self.vx = random.uniform(-4, 4)
            self.vy = random.uniform(-6, -3)
            self.gravity = 0.4
            self.trail_length = random.randint(3, 8)
        elif tipo == "estrellas":
            self.color = color or (random.randint(200, 255), random.randint(200, 255), random.randint(150, 255))
            self.vx = random.uniform(-2.5, 2.5)
            self.vy = random.uniform(-2.5, 2.5)
            self.gravity = 0.08
            self.rotation = random.uniform(0, 360)
            self.rotation_speed = random.uniform(-8, 8)
            self.points = random.randint(5, 8)
        else:  # confeti
            self.color = color or random.choice([
                (255, 100, 100), (100, 255, 100), (100, 100, 255), 
                (255, 255, 100), (255, 100, 255), (100, 255, 255)
            ])
            self.vx = random.uniform(-4, 4)
            self.vy = random.uniform(-10, -4)
            self.gravity = 0.3
            self.rotation = random.uniform(0, 360)
            self.rotation_speed = random.uniform(-10, 10)
        
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += self.gravity
        
        if hasattr(self, 'rotation'):
            self.rotation += self.rotation_speed
            
        self.life -= 1
        return self.life > 0
        
    def draw(self, pantalla):
        progress = 1 - (self.life / self.max_life)
        
        if self.tipo == "estrellas":
            current_size = self.size * (0.5 + 0.5 * math.sin(progress * math.pi))
            points = []
            for i in range(self.points):
                angle = self.rotation + i * (360 / self.points)
                rad = math.radians(angle)
                x = self.x + math.cos(rad) * current_size
                y = self.y + math.sin(rad) * current_size
                points.append((x, y))
                
                inner_angle = angle + (180 / self.points)
                inner_rad = math.radians(inner_angle)
                inner_x = self.x + math.cos(inner_rad) * (current_size / 2)
                inner_y = self.y + math.sin(inner_rad) * (current_size / 2)
                points.append((inner_x, inner_y))
                
            alpha = min(255, int(self.life * 2))
            temp_surf = pygame.Surface((current_size * 3, current_size * 3), pygame.SRCALPHA)
            pygame.draw.polygon(temp_surf, (*self.color, alpha), 
                              [(p[0] - self.x + current_size * 1.5, 
                                p[1] - self.y + current_size * 1.5) for p in points])
            pantalla.blit(temp_surf, (self.x - current_size * 1.5, self.y - current_size * 1.5))
            
        elif self.tipo == "brillo":
            pulse = 0.7 + 0.3 * math.sin(progress * math.pi * 2)
            current_size = self.size * pulse
            alpha = min(255, int(self.life * 2))
            
            surf = pygame.Surface((int(current_size * 2.5), int(current_size * 2.5)), pygame.SRCALPHA)
            pygame.draw.circle(surf, (*self.color, alpha), 
                             (current_size * 1.25, current_size * 1.25), current_size)
            pantalla.blit(surf, (self.x - current_size * 1.25, self.y - current_size * 1.25))
            
        elif self.tipo == "chispas":
            for i in range(getattr(self, 'trail_length', 5)):
                trail_progress = i / getattr(self, 'trail_length', 5)
                alpha = 255 * (1 - trail_progress)
                size = max(1, self.size * (1 - trail_progress))
                
                pos_x = self.x - (self.vx * i * 0.3)
                pos_y = self.y - (self.vy * i * 0.3)
                
                if alpha > 0:
                    pygame.draw.circle(pantalla, (*self.color, int(alpha)), 
                                     (int(pos_x), int(pos_y)), int(size))
        else:
            current_size = self.size * (0.8 + 0.2 * math.sin(progress * math.pi))
            alpha = min(255, int(self.life * 2))
            
            surf = pygame.Surface((int(current_size * 2), int(current_size * 2)), pygame.SRCALPHA)
            rotated_rect = pygame.Surface((current_size, current_size), pygame.SRCALPHA)
            pygame.draw.rect(rotated_rect, (*self.color, alpha), (0, 0, current_size, current_size))
            
            if hasattr(self, 'rotation'):
                rotated_rect = pygame.transform.rotate(rotated_rect, self.rotation)
            
            rect = rotated_rect.get_rect(center=(current_size, current_size))
            surf.blit(rotated_rect, rect)
            pantalla.blit(surf, (self.x - current_size, self.y - current_size))

def crear_particulas(x, y, cantidad=50, tipo="confeti", color=None, tamaño_extra=0):
    """Crear efectos de partículas"""
    for _ in range(cantidad):
        particulas.append(Particula(x, y, tipo, color, tamaño_extra))

# Botones
boton_pausa_rect = pygame.Rect(ANCHO - 90, 15, 40, 40)
boton_reiniciar_rect = pygame.Rect(ANCHO - 140, 15, 40, 40)

class SistemaAudio:
    def __init__(self):
        self.sonidos = {}
        self.volumen_efectos = 0.4
    
    def reproducir(self, nombre):
        """Reproducir efecto de sonido"""
        pass

class Estadisticas:
    def __init__(self):
        self.tiempo_juego = 0
        self.objetos_recolectados = 0
        self.enemigos_evitados = 0
        self.movimientos = 0
        self.nivel = 1
        self.puntuacion_combo = 0
        self.ultimo_movimiento_tiempo = 0
        self.combo_activo = False
    
    def registrar_objeto(self):
        self.objetos_recolectados += 1
        ahora = pygame.time.get_ticks()
        if ahora - self.ultimo_movimiento_tiempo < 2000:
            self.puntuacion_combo += 1
            self.combo_activo = True
        else:
            self.puntuacion_combo = 1
        self.ultimo_movimiento_tiempo = ahora
    
    def registrar_enemigo_evitado(self):
        self.enemigos_evitados += 1
    
    def registrar_movimiento(self):
        self.movimientos += 1
        self.ultimo_movimiento_tiempo = pygame.time.get_ticks()
    
    def actualizar_tiempo(self, dt):
        self.tiempo_juego += dt
        if self.combo_activo and pygame.time.get_ticks() - self.ultimo_movimiento_tiempo > 2000:
            self.combo_activo = False
    
    def subir_nivel(self):
        self.nivel += 1
    
    def obtener_estadisticas(self):
        return {
            'Nivel': self.nivel,
            'Tiempo Jugado': f"{self.tiempo_juego // 1000 // 60}:{self.tiempo_juego // 1000 % 60:02d}",
            'Objetos Recolectados': self.objetos_recolectados,
            'Enemigos Evitados': self.enemigos_evitados,
            'Movimientos': self.movimientos,
            'Combo': f'x{self.puntuacion_combo}' if self.combo_activo else ''
        }

class SistemaPuntuaciones:
    def __init__(self):
        self.archivo_puntuaciones = "puntuaciones.txt"
        self.puntuaciones = self.cargar_puntuaciones()
    
    def cargar_puntuaciones(self):
        try:
            with open(self.archivo_puntuaciones, 'r') as f:
                return [int(line.strip()) for line in f.readlines() if line.strip()]
        except:
            return [15000, 12000, 10000, 8000, 6000, 5000, 4000, 3000, 2000, 1000]
    
    def guardar_puntuacion(self, puntuacion):
        self.puntuaciones.append(puntuacion)
        self.puntuaciones.sort(reverse=True)
        self.puntuaciones = self.puntuaciones[:10]
        
        try:
            with open(self.archivo_puntuaciones, 'w') as f:
                for score in self.puntuaciones:
                    f.write(f"{score}\n")
        except Exception as e:
            print(f"Error guardando puntuación: {e}")
    
    def es_puntuacion_alta(self, puntuacion):
        return len(self.puntuaciones) < 10 or puntuacion > min(self.puntuaciones)
    
    def dibujar_tabla_puntuaciones(self, pantalla, fuente, x, y):
        panel_ancho = 280
        panel_alto = 350
        panel_rect = pygame.Rect(x, y, panel_ancho, panel_alto)
        
        # Fondo del panel con gradiente
        for i, color in enumerate(GRADIENTE_PANEL):
            rect_height = panel_alto // len(GRADIENTE_PANEL)
            pygame.draw.rect(pantalla, color, 
                           (x, y + i * rect_height, panel_ancho, rect_height))
        
        pygame.draw.rect(pantalla, COLOR_BORDE, panel_rect, 3, border_radius=12)
        
        # Título
        titulo = fuente.render("MEJORES PUNTUACIONES", True, COLOR_TEXTO_IMPORTANTE)
        pantalla.blit(titulo, (x + panel_ancho//2 - titulo.get_width()//2, y + 25))
        
        # Lista de puntuaciones
        for i, score in enumerate(self.puntuaciones[:8]):
            color = COLOR_TEXTO if i > 2 else [COLOR_TEXTO_IMPORTANTE, COLOR_TEXTO, (200, 200, 200)][i]
            texto = fuente.render(f"{i+1}. {score:08d}", True, color)
            pantalla.blit(texto, (x + 30, y + 80 + i * 35))

class Configuracion:
    def __init__(self):
        self.volumen_musica = 0.6
        self.volumen_efectos = 0.4
        self.controles = {
            'arriba': [pygame.K_UP, pygame.K_w],
            'abajo': [pygame.K_DOWN, pygame.K_s],
            'izquierda': [pygame.K_LEFT, pygame.K_a],
            'derecha': [pygame.K_RIGHT, pygame.K_d],
        }
        self.mostrar_vision = True
        self.mostrar_camino_enemigos = False
        self.efectos_particulas = True
        self.dificultad = "facil"  # Cambiado a fácil por defecto
    
    def guardar_configuracion(self):
        config = {
            'volumen_musica': self.volumen_musica,
            'volumen_efectos': self.volumen_efectos,
            'mostrar_vision': self.mostrar_vision,
            'mostrar_camino_enemigos': self.mostrar_camino_enemigos,
            'efectos_particulas': self.efectos_particulas,
            'dificultad': self.dificultad
        }
        
        try:
            with open('config_laberinto.json', 'w') as f:
                json.dump(config, f)
        except:
            print("Error guardando configuración")
    
    def cargar_configuracion(self):
        try:
            with open('config_laberinto.json', 'r') as f:
                config = json.load(f)
                self.volumen_musica = config.get('volumen_musica', 0.6)
                self.volumen_efectos = config.get('volumen_efectos', 0.4)
                self.mostrar_vision = config.get('mostrar_vision', True)
                self.mostrar_camino_enemigos = config.get('mostrar_camino_enemigos', False)
                self.efectos_particulas = config.get('efectos_particulas', True)
                self.dificultad = config.get('dificultad', 'facil')
        except:
            print("Configuración no encontrada, usando valores por defecto")

class TextoFlotante:
    def __init__(self, texto, x, y, color=COLOR_TEXTO, duracion=1500, tamaño=30, efecto="normal"):
        self.texto = texto
        self.x = x
        self.y = y
        self.color = color
        self.tiempo_inicio = pygame.time.get_ticks()
        self.duracion = duracion
        self.tamaño = tamaño
        self.efecto = efecto
        self.fuente = pygame.font.SysFont('Arial', tamaño)
    
    def actualizar(self):
        return pygame.time.get_ticks() - self.tiempo_inicio < self.duracion
    
    def dibujar(self, pantalla, fuente=None):
        tiempo = pygame.time.get_ticks() - self.tiempo_inicio
        progreso = tiempo / self.duracion
        
        if self.efecto == "rebote":
            y_offset = -60 * (1 - (progreso - 1)**2)
        elif self.efecto == "onda":
            y_offset = -50 * progreso + 10 * math.sin(progreso * math.pi * 4)
        else:
            y_offset = -60 * progreso
        
        alpha = int(255 * (1 - progreso))
        
        texto_surf = self.fuente.render(self.texto, True, self.color)
        texto_surf.set_alpha(alpha)
        
        if self.efecto in ["rebote", "onda"]:
            scale = 0.8 + 0.4 * (1 - progreso)
            new_width = int(texto_surf.get_width() * scale)
            new_height = int(texto_surf.get_height() * scale)
            if new_width > 0 and new_height > 0:
                texto_surf = pygame.transform.scale(texto_surf, (new_width, new_height))
        
        pantalla.blit(texto_surf, (self.x - texto_surf.get_width() // 2, 
                                 self.y + y_offset - texto_surf.get_height() // 2))

class EfectosEspeciales:
    def __init__(self):
        self.animaciones = []
    
    def agregar_explosion(self, x, y, tipo="normal"):
        if tipo == "grande":
            crear_particulas(x, y, 80, "chispas", (255, 255, 100), 2)
            crear_particulas(x, y, 30, "brillo", (255, 200, 50), 3)
        else:
            crear_particulas(x, y, 40, "chispas", (255, 255, 100))
    
    def agregar_texto_flotante(self, texto, x, y, color=COLOR_TEXTO, tamaño=30, efecto="normal"):
        self.animaciones.append(TextoFlotante(texto, x, y, color, 1800, tamaño, efecto))
    
    def actualizar(self):
        self.animaciones = [anim for anim in self.animaciones if anim.actualizar()]
    
    def dibujar(self, pantalla, fuente):
        for anim in self.animaciones:
            anim.dibujar(pantalla, fuente)

class GeneradorLaberinto:
    def __init__(self, filas, columnas, dificultad="facil"):
        self.filas = filas
        self.columnas = columnas
        self.dificultad = dificultad
        self.laberinto = None
    
    def generar_laberinto(self):
        self.laberinto = [[1 for _ in range(self.columnas)] for _ in range(self.filas)]
        
        if self.dificultad == "imposible":
            return self.generar_laberinto_complejo()
        elif self.dificultad == "dificil":
            return self.generar_laberinto_dificil()
        elif self.dificultad == "normal":
            return self.generar_laberinto_normal()
        else:  # facil
            return self.generar_laberinto_facil()
    
    def generar_laberinto_facil(self):
        """Laberinto más simple con caminos más directos"""
        stack = []
        inicio = (1, 1)
        self.laberinto[inicio[1]][inicio[0]] = 0
        stack.append(inicio)
        
        # Generar caminos principales más directos
        while stack:
            x, y = stack[-1]
            
            vecinos = []
            for dx, dy in [(0, -2), (2, 0), (0, 2), (-2, 0)]:
                nx, ny = x + dx, y + dy
                if 0 < nx < self.columnas-1 and 0 < ny < self.filas-1 and self.laberinto[ny][nx] == 1:
                    # Priorizar dirección hacia la salida
                    if (nx, ny) == (self.columnas-2, self.filas-2):
                        vecinos.insert(0, (nx, ny, dx//2, dy//2))
                    else:
                        vecinos.append((nx, ny, dx//2, dy//2))
            
            if vecinos:
                nx, ny, dx, dy = random.choice(vecinos)
                self.laberinto[y + dy][x + dx] = 0
                self.laberinto[ny][nx] = 0
                stack.append((nx, ny))
            else:
                stack.pop()
        
        # Asegurar múltiples caminos a la salida
        self.laberinto[self.filas-2][self.columnas-2] = 0
        self.laberinto[self.filas-2][self.columnas-3] = 0
        self.laberinto[self.filas-3][self.columnas-2] = 0
        
        return self.laberinto
    
    def generar_laberinto_normal(self):
        stack = []
        inicio = (1, 1)
        self.laberinto[inicio[1]][inicio[0]] = 0
        stack.append(inicio)
        
        while stack:
            x, y = stack[-1]
            
            vecinos = []
            for dx, dy in [(0, -2), (2, 0), (0, 2), (-2, 0)]:
                nx, ny = x + dx, y + dy
                if 0 < nx < self.columnas-1 and 0 < ny < self.filas-1 and self.laberinto[ny][nx] == 1:
                    vecinos.append((nx, ny, dx//2, dy//2))
            
            if vecinos:
                nx, ny, dx, dy = random.choice(vecinos)
                self.laberinto[y + dy][x + dx] = 0
                self.laberinto[ny][nx] = 0
                stack.append((nx, ny))
            else:
                stack.pop()
        
        self.laberinto[self.filas-2][self.columnas-2] = 0
        return self.laberinto
    
    def generar_laberinto_dificil(self):
        self.generar_laberinto_normal()
        
        for _ in range(self.filas * self.columnas // 30):  # Menos callejones sin salida
            x, y = random.randint(2, self.columnas-3), random.randint(2, self.filas-3)
            if self.laberinto[y][x] == 0:
                for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
                    nx, ny = x + dx, y + dy
                    if 0 < nx < self.columnas-1 and 0 < ny < self.filas-1 and self.laberinto[ny][nx] == 1:
                        paredes_around = 0
                        for ddx, ddy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
                            if self.laberinto[ny + ddy][nx + ddx] == 1:
                                paredes_around += 1
                        
                        if paredes_around >= 3:
                            continue
                            
                        self.laberinto[ny][nx] = 0
                        break
        
        return self.laberinto
    
    def generar_laberinto_complejo(self):
        self.generar_laberinto_dificil()
        
        for _ in range(self.filas * self.columnas // 20):  # Menos obstáculos
            x, y = random.randint(1, self.columnas-2), random.randint(1, self.filas-2)
            if self.laberinto[y][x] == 0:
                for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
                    nx, ny = x + dx, y + dy
                    if (0 < nx < self.columnas-1 and 0 < ny < self.filas-1 and 
                        self.laberinto[ny][nx] == 0 and random.random() < 0.2):  # Menor probabilidad
                        self.laberinto[ny][nx] = 1
        
        return self.laberinto

class Jugador:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = COLOR_JUGADOR
        self.vision_radio = 5  # Visión aumentada
        self.objetos_recolectados = 0
        self.animacion_movimiento = 0
        self.direccion = (0, 0)
        self.invulnerable = 0  # Tiempo de invulnerabilidad después de escapar
    
    def mover(self, dx, dy, laberinto):
        nuevo_x, nuevo_y = self.x + dx, self.y + dy
        
        if (0 <= nuevo_x < len(laberinto[0]) and 
            0 <= nuevo_y < len(laberinto) and 
            laberinto[nuevo_y][nuevo_x] == 0):
            self.x, self.y = nuevo_x, nuevo_y
            self.direccion = (dx, dy)
            self.animacion_movimiento = 10
            if self.invulnerable > 0:
                self.invulnerable -= 1
            return True
        return False
    
    def obtener_posicion(self):
        return (self.x, self.y)
    
    def actualizar_animacion(self):
        if self.animacion_movimiento > 0:
            self.animacion_movimiento -= 1
    
    def activar_invulnerabilidad(self):
        self.invulnerable = 30  # 0.5 segundos de invulnerabilidad
    
    def dibujar(self, pantalla):
        offset_x, offset_y = 0, 0
        if self.animacion_movimiento > 0:
            progress = 1 - (self.animacion_movimiento / 10)
            offset_x = self.direccion[0] * TAMANIO_CELDA * progress
            offset_y = self.direccion[1] * TAMANIO_CELDA * progress
        
        celda_rect = pygame.Rect(
            MARGEN_X + self.x * TAMANIO_CELDA - offset_x,
            MARGEN_Y + self.y * TAMANIO_CELDA - offset_y,
            TAMANIO_CELDA, TAMANIO_CELDA
        )
        
        # Efecto de parpadeo si es invulnerable
        if self.invulnerable > 0 and self.invulnerable % 6 < 3:
            return  # No dibujar durante el parpadeo
        
        pygame.draw.rect(pantalla, self.color, celda_rect)
        pygame.draw.rect(pantalla, (0, 180, 220), celda_rect, 2)
        
        inner_rect = pygame.Rect(
            celda_rect.x + 4, celda_rect.y + 4,
            TAMANIO_CELDA - 8, TAMANIO_CELDA - 8
        )
        pygame.draw.rect(pantalla, (80, 220, 220), inner_rect, 1)
        
        ojo_radio = TAMANIO_CELDA // 6
        ojo_offset = TAMANIO_CELDA // 4
        
        if self.direccion[0] != 0 or self.direccion[1] != 0:
            eye_dx = self.direccion[0] * ojo_offset * 0.3
            eye_dy = self.direccion[1] * ojo_offset * 0.3
        else:
            eye_dx, eye_dy = 0, 0
        
        ojo_x1 = celda_rect.centerx - ojo_offset + eye_dx
        ojo_x2 = celda_rect.centerx + ojo_offset + eye_dx
        ojo_y = celda_rect.centery - ojo_offset * 0.5 + eye_dy
        
        pygame.draw.circle(pantalla, NEGRO, (int(ojo_x1), int(ojo_y)), ojo_radio)
        pygame.draw.circle(pantalla, NEGRO, (int(ojo_x2), int(ojo_y)), ojo_radio)
        
        pygame.draw.circle(pantalla, BLANCO, (int(ojo_x1 - ojo_radio//3), int(ojo_y - ojo_radio//3)), ojo_radio//4)
        pygame.draw.circle(pantalla, BLANCO, (int(ojo_x2 - ojo_radio//3), int(ojo_y - ojo_radio//3)), ojo_radio//4)

class Enemigo:
    def __init__(self, x, y, tipo="normal"):
        self.x = x
        self.y = y
        self.tipo = tipo
        self.color = COLOR_ENEMIGO if tipo == "normal" else (200, 60, 120)
        self.camino = []
        self.objetivo = None
        # VELOCIDADES REDUCIDAS
        self.velocidad = 0.05 if tipo == "normal" else 0.08  # Más lento
        self.progreso_movimiento = 0
        self.animacion = 0
        self.deteccion_radio = 5 if tipo == "normal" else 6  # Radio reducido
    
    def establecer_objetivo(self, objetivo_x, objetivo_y):
        self.objetivo = (objetivo_x, objetivo_y)
    
    def puede_ver_jugador(self, laberinto, jugador_pos):
        jx, jy = jugador_pos
        distancia = math.sqrt((jx - self.x)**2 + (jy - self.y)**2)
        
        if distancia > self.deteccion_radio:
            return False
            
        steps = int(distancia * 2)
        for i in range(1, steps):
            tx = self.x + (jx - self.x) * i / steps
            ty = self.y + (jy - self.y) * i / steps
            if (0 <= int(tx) < len(laberinto[0]) and 0 <= int(ty) < len(laberinto) and
                laberinto[int(ty)][int(tx)] == 1):
                return False
        return True
    
    def encontrar_camino(self, laberinto, inicio, objetivo):
        cola = [inicio]
        visitados = {inicio: None}
        intentos = 0
        max_intentos = 300  # Menos intentos para hacerlos menos eficientes
        
        while cola and intentos < max_intentos:
            actual = cola.pop(0)
            intentos += 1
            
            if actual == objetivo:
                camino = []
                while actual is not None:
                    camino.append(actual)
                    actual = visitados[actual]
                return camino[::-1]
            
            dx = objetivo[0] - actual[0]
            dy = objetivo[1] - actual[1]
            direcciones = []
            
            if abs(dx) > abs(dy):
                direcciones = [(1 if dx > 0 else -1, 0), (0, 1 if dy > 0 else -1), 
                              (0, -1 if dy > 0 else 1), (-1 if dx > 0 else 1, 0)]
            else:
                direcciones = [(0, 1 if dy > 0 else -1), (1 if dx > 0 else -1, 0),
                              (-1 if dx > 0 else 1, 0), (0, -1 if dy > 0 else 1)]
            
            for dx, dy in direcciones:
                nx, ny = actual[0] + dx, actual[1] + dy
                if (0 <= nx < len(laberinto[0]) and 
                    0 <= ny < len(laberinto) and 
                    laberinto[ny][nx] == 0 and 
                    (nx, ny) not in visitados):
                    cola.append((nx, ny))
                    visitados[(nx, ny)] = actual
        
        return []
    
    def actualizar(self, laberinto, jugador_pos):
        # Menor frecuencia de actualización de camino
        if (self.puede_ver_jugador(laberinto, jugador_pos) or 
            self.objetivo != jugador_pos or 
            not self.camino or 
            random.random() < 0.01):  # 1% de chance en lugar de 2%
            
            self.establecer_objetivo(*jugador_pos)
            self.camino = self.encontrar_camino(laberinto, (self.x, self.y), jugador_pos)
            self.progreso_movimiento = 0
        
        if self.camino and len(self.camino) > 1:
            self.progreso_movimiento += self.velocidad
            if self.progreso_movimiento >= 1:
                self.progreso_movimiento = 0
                self.x, self.y = self.camino[1]
                self.camino.pop(0)
                self.animacion = 5
        
        if self.animacion > 0:
            self.animacion -= 1
    
    def obtener_posicion(self):
        return (self.x, self.y)
    
    def dibujar(self, pantalla, mostrar_camino=False):
        pulse = 1.0
        if self.animacion > 0:
            pulse = 0.8 + 0.2 * math.sin(self.animacion * 2)
        
        celda_rect = pygame.Rect(
            MARGEN_X + self.x * TAMANIO_CELDA,
            MARGEN_Y + self.y * TAMANIO_CELDA,
            TAMANIO_CELDA, TAMANIO_CELDA
        )
        
        color_base = [min(255, int(c * pulse)) for c in self.color]
        pygame.draw.rect(pantalla, color_base, celda_rect)
        pygame.draw.rect(pantalla, (200, 80, 150), celda_rect, 2)
        
        ojo_radio = TAMANIO_CELDA // 7
        ojo_x1 = celda_rect.centerx - TAMANIO_CELDA // 4
        ojo_x2 = celda_rect.centerx + TAMANIO_CELDA // 4
        ojo_y = celda_rect.centery - TAMANIO_CELDA // 6
        
        pygame.draw.circle(pantalla, (40, 0, 0), (ojo_x1, ojo_y), ojo_radio)
        pygame.draw.circle(pantalla, (40, 0, 0), (ojo_x2, ojo_y), ojo_radio)
        
        pygame.draw.circle(pantalla, (220, 0, 0), (ojo_x1, ojo_y), ojo_radio // 2)
        pygame.draw.circle(pantalla, (220, 0, 0), (ojo_x2, ojo_y), ojo_radio // 2)
        
        if mostrar_camino and self.camino:
            for i, (x, y) in enumerate(self.camino):
                if i == 0:
                    continue
                camino_rect = pygame.Rect(
                    MARGEN_X + x * TAMANIO_CELDA + TAMANIO_CELDA // 3,
                    MARGEN_Y + y * TAMANIO_CELDA + TAMANIO_CELDA // 3,
                    TAMANIO_CELDA // 3, TAMANIO_CELDA // 3
                )
                alpha = 100 - (i * 10)
                if alpha > 0:
                    temp_surf = pygame.Surface((TAMANIO_CELDA // 3, TAMANIO_CELDA // 3), pygame.SRCALPHA)
                    pygame.draw.rect(temp_surf, (*self.color, alpha), (0, 0, TAMANIO_CELDA // 3, TAMANIO_CELDA // 3))
                    pantalla.blit(temp_surf, camino_rect)

class Objeto:
    def __init__(self, x, y, tipo="normal"):
        self.x = x
        self.y = y
        self.tipo = tipo
        self.colores = {
            "normal": COLOR_OBJETO,
            "especial": (220, 180, 40),
            "poder": (80, 140, 220)
        }
        self.color = self.colores.get(tipo, COLOR_OBJETO)
        self.recolectado = False
        self.animacion = 0
        self.rotacion = 0
    
    def obtener_posicion(self):
        return (self.x, self.y)
    
    def actualizar(self):
        self.animacion += 0.1
        self.rotacion += 2
    
    def dibujar(self, pantalla):
        if not self.recolectado:
            centro_x = MARGEN_X + self.x * TAMANIO_CELDA + TAMANIO_CELDA // 2
            centro_y = MARGEN_Y + self.y * TAMANIO_CELDA + TAMANIO_CELDA // 2
            
            float_offset = math.sin(self.animacion) * 3
            pulse = 0.8 + 0.2 * math.sin(self.animacion * 2)
            tamaño_base = TAMANIO_CELDA // 3
            radio = int(tamaño_base * pulse)
            
            if self.tipo == "normal":
                pygame.draw.circle(pantalla, self.color, 
                                 (centro_x, centro_y + float_offset), radio)
                pygame.draw.circle(pantalla, BLANCO, 
                                 (centro_x, centro_y + float_offset), radio, 1)
                
                destello_radio = radio // 2
                pygame.draw.circle(pantalla, (180, 240, 180), 
                                 (centro_x, centro_y + float_offset), destello_radio)
            
            elif self.tipo == "especial":
                points = []
                for i in range(5):
                    angle = self.rotacion + i * 72
                    rad = math.radians(angle)
                    x = centro_x + math.cos(rad) * radio
                    y = centro_y + float_offset + math.sin(rad) * radio
                    points.append((x, y))
                    
                    inner_angle = angle + 36
                    inner_rad = math.radians(inner_angle)
                    inner_x = centro_x + math.cos(inner_rad) * (radio / 2)
                    inner_y = centro_y + float_offset + math.sin(inner_rad) * (radio / 2)
                    points.append((inner_x, inner_y))
                    
                pygame.draw.polygon(pantalla, self.color, points)
                
            elif self.tipo == "poder":
                for i in range(3):
                    r = radio * (1 - i * 0.3)
                    alpha = 150 - i * 50
                    temp_surf = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
                    pygame.draw.circle(temp_surf, (*self.color, alpha), (r, r), r)
                    pantalla.blit(temp_surf, (centro_x - r, centro_y + float_offset - r))

class Laberinto:
    def __init__(self, filas, columnas, dificultad="facil"):
        self.filas = filas
        self.columnas = columnas
        self.dificultad = dificultad
        self.grid = None
        self.generador = GeneradorLaberinto(filas, columnas, dificultad)
        self.jugador = None
        self.enemigos = []
        self.objetos = []
        self.objetivo = None
        self.puntuacion = 0
        self.tiempo_inicio = pygame.time.get_ticks()
        self.nivel = 1
        
    def generar(self):
        self.grid = self.generador.generar_laberinto()
        
        posiciones_validas = []
        for y in range(self.filas):
            for x in range(self.columnas):
                if self.grid[y][x] == 0:
                    posiciones_validas.append((x, y))
        
        if posiciones_validas:
            jugador_pos = random.choice(posiciones_validas)
            self.jugador = Jugador(*jugador_pos)
            posiciones_validas.remove(jugador_pos)
            
            self.objetivo = max(posiciones_validas, 
                               key=lambda p: math.dist(p, jugador_pos))
            posiciones_validas.remove(self.objetivo)
            
            # MENOS ENEMIGOS Y MÁS VARIABLES SEGÚN DIFICULTAD
            num_enemigos = {
                "facil": random.randint(1, 2),      # 1-2 enemigos
                "normal": random.randint(2, 3),     # 2-3 enemigos  
                "dificil": random.randint(3, 4),    # 3-4 enemigos
                "imposible": random.randint(4, 5)   # 4-5 enemigos
            }.get(self.dificultad, 1)
            
            num_enemigos = min(num_enemigos, len(posiciones_validas) // 6)  # Más espacio entre enemigos
            
            for i in range(num_enemigos):
                if posiciones_validas:
                    # Colocar enemigos lejos del jugador
                    enemigo_pos = max(posiciones_validas, key=lambda p: math.dist(p, jugador_pos))
                    tipo = "normal"  # Solo enemigos normales en niveles bajos
                    if self.dificultad in ["dificil", "imposible"] and i == num_enemigos - 1:
                        tipo = "rapido"  # Solo un enemigo rápido en dificultades altas
                    
                    self.enemigos.append(Enemigo(*enemigo_pos, tipo))
                    posiciones_validas.remove(enemigo_pos)
            
            num_objetos = min(6, len(posiciones_validas) // 3)  # Menos objetos
            for i in range(num_objetos):
                if posiciones_validas:
                    objeto_pos = random.choice(posiciones_validas)
                    if i == 0 and num_objetos >= 3:
                        tipo = "especial"
                    elif i == 1 and num_objetos >= 5:
                        tipo = "poder"
                    else:
                        tipo = "normal"
                    
                    self.objetos.append(Objeto(*objeto_pos, tipo))
                    posiciones_validas.remove(objeto_pos)
    
    def subir_nivel(self):
        self.nivel += 1
        # Solo aumentar dificultad después del nivel 3
        if self.nivel <= 3:
            self.dificultad = "facil"
        elif self.nivel <= 6:
            self.dificultad = "normal"
        elif self.nivel <= 9:
            self.dificultad = "dificil"
        else:
            self.dificultad = "imposible"
        self.generar()
    
    def actualizar(self):
        self.jugador.actualizar_animacion()
        
        for objeto in self.objetos:
            objeto.actualizar()
        
        jugador_pos = self.jugador.obtener_posicion()
        for enemigo in self.enemigos:
            enemigo.actualizar(self.grid, jugador_pos)
            
            # El jugador es invulnerable brevemente después de escapar
            if (enemigo.obtener_posicion() == jugador_pos and 
                self.jugador.invulnerable == 0):
                return "game_over"
        
        if jugador_pos == self.objetivo:
            tiempo_transcurrido = pygame.time.get_ticks() - self.tiempo_inicio
            base_score = max(0, 15000 - tiempo_transcurrido // 10)  # Más tiempo
            objeto_bonus = self.jugador.objetos_recolectados * 500  # Menos bonus por objetos
            nivel_bonus = self.nivel * 800  # Menos bonus por nivel
            self.puntuacion = base_score + objeto_bonus + nivel_bonus
            return "victoria"
        
        for objeto in self.objetos:
            if not objeto.recolectado and objeto.obtener_posicion() == jugador_pos:
                objeto.recolectado = True
                self.jugador.objetos_recolectados += 1
                self.jugador.activar_invulnerabilidad()  # Invencibilidad al coger objeto
                
                centro_x = MARGEN_X + objeto.x * TAMANIO_CELDA + TAMANIO_CELDA // 2
                centro_y = MARGEN_Y + objeto.y * TAMANIO_CELDA + TAMANIO_CELDA // 2
                
                if objeto.tipo == "normal":
                    crear_particulas(centro_x, centro_y, 25, "brillo", objeto.color)
                elif objeto.tipo == "especial":
                    crear_particulas(centro_x, centro_y, 50, "estrellas", objeto.color, 2)
                elif objeto.tipo == "poder":
                    crear_particulas(centro_x, centro_y, 40, "brillo", objeto.color, 3)
        
        return "jugando"
    
    def dibujar(self, pantalla, mostrar_vision=True, mostrar_camino_enemigos=False):
        laberinto_rect = pygame.Rect(MARGEN_X, MARGEN_Y, ANCHO_LABERINTO, ALTO_LABERINTO)
        
        for i, color in enumerate(GRADIENTE_CIELO):
            rect_height = ALTO_LABERINTO // len(GRADIENTE_CIELO)
            pygame.draw.rect(pantalla, color, 
                           (MARGEN_X, MARGEN_Y + i * rect_height, ANCHO_LABERINTO, rect_height))
        
        pygame.draw.rect(pantalla, COLOR_BORDE, laberinto_rect, 4)
        
        for y in range(self.filas):
            for x in range(self.columnas):
                celda_rect = pygame.Rect(
                    MARGEN_X + x * TAMANIO_CELDA,
                    MARGEN_Y + y * TAMANIO_CELDA,
                    TAMANIO_CELDA, TAMANIO_CELDA
                )
                
                if self.grid[y][x] == 1:
                    pygame.draw.rect(pantalla, COLOR_PARED, celda_rect)
                    
                    if (x + y) % 3 == 0:
                        pygame.draw.rect(pantalla, (45, 45, 85), 
                                       (celda_rect.x + 2, celda_rect.y + 2, 
                                        TAMANIO_CELDA - 4, TAMANIO_CELDA - 4), 1)
                else:
                    pygame.draw.rect(pantalla, COLOR_CAMINO, celda_rect)
                
                pygame.draw.rect(pantalla, (60, 60, 110), celda_rect, 1)
        
        if self.objetivo:
            objetivo_rect = pygame.Rect(
                MARGEN_X + self.objetivo[0] * TAMANIO_CELDA,
                MARGEN_Y + self.objetivo[1] * TAMANIO_CELDA,
                TAMANIO_CELDA, TAMANIO_CELDA
            )
            
            tiempo = pygame.time.get_ticks() / 1000
            pulse = 0.8 + 0.2 * math.sin(tiempo * 3)
            color_portal = (
                min(255, int(COLOR_OBJETIVO[0] * pulse)),
                min(255, int(COLOR_OBJETIVO[1] * pulse)),
                min(255, int(COLOR_OBJETIVO[2] * pulse))
            )
            
            pygame.draw.rect(pantalla, color_portal, objetivo_rect)
            pygame.draw.rect(pantalla, (240, 240, 180), objetivo_rect, 3)
            
            centro_x = objetivo_rect.centerx
            centro_y = objetivo_rect.centery
            radio = TAMANIO_CELDA // 3
            
            for i in range(3):
                r = radio * (1 - i * 0.3) * (0.9 + 0.1 * math.sin(tiempo * 4 + i))
                pygame.draw.circle(pantalla, (240, 240, 140), (centro_x, centro_y), int(r), 2)
        
        for objeto in self.objetos:
            objeto.dibujar(pantalla)
        
        for enemigo in self.enemigos:
            enemigo.dibujar(pantalla, mostrar_camino_enemigos)
        
        self.jugador.dibujar(pantalla)
        
        if mostrar_vision and self.jugador:
            vision_surf = pygame.Surface((ANCHO_LABERINTO, ALTO_LABERINTO), pygame.SRCALPHA)
            vision_surf.fill((0, 0, 0, 180))
            
            centro_x = self.jugador.x * TAMANIO_CELDA + TAMANIO_CELDA // 2
            centro_y = self.jugador.y * TAMANIO_CELDA + TAMANIO_CELDA // 2
            radio = self.jugador.vision_radio * TAMANIO_CELDA
            
            for r in range(int(radio), 0, -5):
                alpha = max(0, 200 - (r / radio) * 180)
                pygame.draw.circle(vision_surf, (0, 0, 0, int(alpha)), (centro_x, centro_y), r)
            
            pygame.draw.circle(vision_surf, (0, 0, 0, 0), (centro_x, centro_y), radio * 0.7)
            
            pantalla.blit(vision_surf, (MARGEN_X, MARGEN_Y))

# ... (el resto del código permanece igual, funciones de dibujar botones, menú, etc.)

def dibujar_boton_reiniciar():
    mouse_pos = pygame.mouse.get_pos()
    color_boton = COLOR_BOTON_HOVER if boton_reiniciar_rect.collidepoint(mouse_pos) else COLOR_BOTON
    color_icono = BLANCO
    
    pygame.draw.rect(pantalla, color_boton, boton_reiniciar_rect, border_radius=8)
    pygame.draw.rect(pantalla, BLANCO, boton_reiniciar_rect, 2, border_radius=8)
    
    centro_x = boton_reiniciar_rect.centerx
    centro_y = boton_reiniciar_rect.centery
    radio = 10
    
    pygame.draw.circle(pantalla, color_icono, (centro_x, centro_y), radio, 2)
    
    puntos_flecha = [
        (centro_x + 5, centro_y - 3),
        (centro_x + 2, centro_y - 6),
        (centro_x - 1, centro_y - 3),
        (centro_x, centro_y),
        (centro_x + 5, centro_y - 3)
    ]
    pygame.draw.polygon(pantalla, color_icono, puntos_flecha)

def dibujar_boton_pausa():
    mouse_pos = pygame.mouse.get_pos()
    color_boton = COLOR_BOTON_HOVER if boton_pausa_rect.collidepoint(mouse_pos) else COLOR_BOTON
    color_icono = BLANCO
    
    pygame.draw.rect(pantalla, color_boton, boton_pausa_rect, border_radius=8)
    pygame.draw.rect(pantalla, BLANCO, boton_pausa_rect, 2, border_radius=8)
    
    barra_ancho = 4
    barra_alto = 20
    espacio = 3
    
    pygame.draw.rect(pantalla, color_icono, 
                   (boton_pausa_rect.x + 12, boton_pausa_rect.y + 10, barra_ancho, barra_alto))
    pygame.draw.rect(pantalla, color_icono, 
                   (boton_pausa_rect.x + 12 + barra_ancho + espacio, boton_pausa_rect.y + 10, barra_ancho, barra_alto))

def dibujar_menu_principal(juego):
    pantalla.fill(COLOR_FONDO)
    
    tiempo = pygame.time.get_ticks() / 1000
    for i in range(100):
        x = (i * 37) % ANCHO
        y = (i * 23) % ALTO
        brillo = 100 + 155 * abs(math.sin(tiempo + i * 0.1))
        tamaño = 1 + abs(math.sin(tiempo * 0.5 + i * 0.05))
        pygame.draw.circle(pantalla, (brillo, brillo, brillo), (x, y), tamaño)
    
    titulo_texto = "LABERINTO CÓSMICO"
    subtitulo = "Escape Imposible"
    
    titulo_sombra = juego.fuente_grande.render(titulo_texto, True, (50, 50, 100))
    pantalla.blit(titulo_sombra, (ANCHO//2 - titulo_sombra.get_width()//2 + 3, 103))
    
    titulo = juego.fuente_grande.render(titulo_texto, True, COLOR_TEXTO_IMPORTANTE)
    titulo_rect = titulo.get_rect(center=(ANCHO//2, 100))
    
    pulse = 0.8 + 0.2 * math.sin(tiempo * 2)
    titulo_temp = pygame.Surface(titulo.get_size(), pygame.SRCALPHA)
    titulo_temp.blit(titulo, (0, 0))
    titulo_temp.set_alpha(200 + int(55 * math.sin(tiempo * 3)))
    pantalla.blit(titulo_temp, titulo_rect)
    
    sub = juego.fuente_mediana.render(subtitulo, True, COLOR_TEXTO)
    pantalla.blit(sub, (ANCHO//2 - sub.get_width()//2, 160))
    
    boton_jugar = pygame.Rect(ANCHO//2 - 120, 300, 240, 70)
    mouse_pos = pygame.mouse.get_pos()
    
    if boton_jugar.collidepoint(mouse_pos):
        color_boton = COLOR_BOTON_HOVER
        pygame.draw.rect(pantalla, (100, 160, 230, 50), 
                       (boton_jugar.x - 5, boton_jugar.y - 5, 
                        boton_jugar.width + 10, boton_jugar.height + 10), 
                       border_radius=15)
    else:
        color_boton = COLOR_BOTON
    
    pygame.draw.rect(pantalla, color_boton, boton_jugar, border_radius=15)
    pygame.draw.rect(pantalla, BLANCO, boton_jugar, 3, border_radius=15)
    
    texto_jugar = juego.fuente_grande.render("JUGAR", True, BLANCO)
    texto_rect = texto_jugar.get_rect(center=boton_jugar.center)
    
    if boton_jugar.collidepoint(mouse_pos):
        texto_sombra = juego.fuente_grande.render("JUGAR", True, (220, 230, 255))
        pantalla.blit(texto_sombra, (texto_rect.x + 2, texto_rect.y + 2))
    
    pantalla.blit(texto_jugar, texto_rect)
    
    instrucciones = [
        "CONTROLES:",
        "W/↑ : MOVER ARRIBA",
        "S/↓ : MOVER ABAJO", 
        "A/← : MOVER IZQUIERDA",
        "D/→ : MOVER DERECHA",
        "",
        "OBJETIVO: LLEGAR A LA SALIDA",
        "RECOLECTA OBJETOS PARA PUNTOS EXTRA",
        "EVITA A LOS ENEMIGOS",
        "COMBO: RECOLECTA RÁPIDO PARA MÁS PUNTOS",
        "",
        "ESC : PAUSA"
    ]
    
    for i, linea in enumerate(instrucciones):
        color = COLOR_TEXTO_IMPORTANTE if "CONTROLES" in linea or "OBJETIVO" in linea else COLOR_TEXTO
        texto = juego.fuente_pista.render(linea, True, color)
        pantalla.blit(texto, (ANCHO//2 - texto.get_width()//2, 400 + i * 28))
    
    if random.random() < 0.03:
        crear_particulas(random.randint(100, ANCHO-100), 200, 10, "estrellas")
    
    version = juego.fuente_pista.render("v2.0", True, (150, 150, 200))
    pantalla.blit(version, (ANCHO - version.get_width() - 20, ALTO - 40))
    
    return boton_jugar

def mostrar_pausa_mejorada(juego):
    s = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
    s.fill((0, 0, 0, 160))
    juego.pantalla.blit(s, (0, 0))
    
    panel_rect = pygame.Rect(ANCHO//2 - 250, ALTO//2 - 200, 500, 400)
    
    for i, color in enumerate(GRADIENTE_PANEL):
        rect_height = panel_rect.height // len(GRADIENTE_PANEL)
        pygame.draw.rect(juego.pantalla, color, 
                       (panel_rect.x, panel_rect.y + i * rect_height, 
                        panel_rect.width, rect_height))
    
    pygame.draw.rect(juego.pantalla, COLOR_BORDE, panel_rect, 4, border_radius=15)
    
    texto_pausa = juego.fuente_grande.render("PAUSA", True, COLOR_TEXTO_IMPORTANTE)
    juego.pantalla.blit(texto_pausa, (ANCHO//2 - texto_pausa.get_width()//2, ALTO//2 - 170))
    
    stats = juego.estadisticas.obtener_estadisticas()
    stats_textos = [
        f"Nivel: {stats['Nivel']}",
        f"Objetos: {stats['Objetos Recolectados']}",
        f"Enemigos Evitados: {stats['Enemigos Evitados']}",
        f"Movimientos: {stats['Movimientos']}",
        f"Tiempo: {stats['Tiempo Jugado']}",
        f"Combo: {stats['Combo']}" if stats['Combo'] else ""
    ]
    
    for i, stat in enumerate(stats_textos):
        if stat:
            color = COLOR_TEXTO_IMPORTANTE if "Combo" in stat and stats['Combo'] else COLOR_TEXTO
            texto = juego.fuente.render(stat, True, color)
            juego.pantalla.blit(texto, (ANCHO//2 - texto.get_width()//2, ALTO//2 - 100 + i * 40))
    
    texto_continuar = juego.fuente_pista.render("Presiona ESC para continuar", True, COLOR_TEXTO)
    juego.pantalla.blit(texto_continuar, (ANCHO//2 - texto_continuar.get_width()//2, ALTO//2 + 150))

class Juego:
    def __init__(self):
        self.pantalla = pygame.display.set_mode((ANCHO, ALTO))
        pygame.display.set_caption("Laberinto Cósmico - Escape Imposible")
        self.reloj = pygame.time.Clock()
        
        self.audio = SistemaAudio()
        self.estadisticas = Estadisticas()
        self.puntuaciones = SistemaPuntuaciones()
        self.config = Configuracion()
        self.efectos = EfectosEspeciales()
        
        self.fuente = self.obtener_fuente(28)
        self.fuente_grande = self.obtener_fuente(60)
        self.fuente_mediana = self.obtener_fuente(36)
        self.fuente_pista = self.obtener_fuente(22)
        
        self.config.cargar_configuracion()
        
        self.reiniciar_juego()
    
    def obtener_fuente(self, tamaño):
        fuentes_linux = [
            'dejavusans',
            'liberationsans', 
            'freesans',
            None
        ]
        
        for fuente_nombre in fuentes_linux:
            try:
                fuente = pygame.font.SysFont(fuente_nombre, tamaño)
                texto_prueba = fuente.render('Test', True, BLANCO)
                if texto_prueba.get_width() > 0:
                    return fuente
            except:
                continue
        
        return pygame.font.Font(None, tamaño)
    
    def reiniciar_juego(self):
        self.laberinto = Laberinto(FILAS_LABERINTO, COLUMNAS_LABERINTO, self.config.dificultad)
        self.laberinto.generar()
        self.juego_activo = True
        self.pausa = False
        self.estado_juego = "menu"
        self.ultima_actualizacion_tiempo = pygame.time.get_ticks()
        self.estadisticas = Estadisticas()
    
    def manejar_eventos(self):
        mouse_pos = pygame.mouse.get_pos()
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.config.guardar_configuracion()
                return False
            
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if self.estado_juego == "menu":
                    boton_jugar = pygame.Rect(ANCHO//2 - 120, 300, 240, 70)
                    if boton_jugar.collidepoint(mouse_pos):
                        self.estado_juego = "jugando"
                        self.audio.reproducir('inicio')
                        print("Iniciando juego...")
                
                elif self.estado_juego == "jugando":
                    if boton_pausa_rect.collidepoint(mouse_pos):
                        self.pausa = not self.pausa
                        continue
                    
                    elif boton_reiniciar_rect.collidepoint(mouse_pos):
                        self.reiniciar_juego()
                        self.estado_juego = "jugando"
                        self.audio.reproducir('reiniciar')
                        print("Juego reiniciado")
                    
                    elif self.pausa:
                        self.pausa = False
                
                elif self.estado_juego in ["victoria", "game_over"]:
                    boton_reiniciar = pygame.Rect(ANCHO//2 - 140, ALTO//2 + 50, 280, 70)
                    boton_menu = pygame.Rect(ANCHO//2 - 140, ALTO//2 + 140, 280, 70)
                    
                    if boton_reiniciar.collidepoint(mouse_pos):
                        self.reiniciar_juego()
                        self.estado_juego = "jugando"
                        self.audio.reproducir('inicio')
                        return True
                    
                    elif boton_menu.collidepoint(mouse_pos):
                        self.reiniciar_juego()
                        self.estado_juego = "menu"
                        self.audio.reproducir('menu')
                        return True
            
            if evento.type == pygame.KEYDOWN:
                if self.estado_juego == "jugando":
                    if evento.key == pygame.K_ESCAPE:
                        self.pausa = not self.pausa
                    
                    elif not self.pausa:
                        movimiento_realizado = False
                        
                        if evento.key in self.config.controles['arriba']:
                            movimiento_realizado = self.laberinto.jugador.mover(0, -1, self.laberinto.grid)
                        elif evento.key in self.config.controles['abajo']:
                            movimiento_realizado = self.laberinto.jugador.mover(0, 1, self.laberinto.grid)
                        elif evento.key in self.config.controles['izquierda']:
                            movimiento_realizado = self.laberinto.jugador.mover(-1, 0, self.laberinto.grid)
                        elif evento.key in self.config.controles['derecha']:
                            movimiento_realizado = self.laberinto.jugador.mover(1, 0, self.laberinto.grid)
                        
                        if movimiento_realizado:
                            self.estadisticas.registrar_movimiento()
                            self.audio.reproducir('mover')
                            
                            if self.config.efectos_particulas:
                                jugador_x = MARGEN_X + self.laberinto.jugador.x * TAMANIO_CELDA + TAMANIO_CELDA // 2
                                jugador_y = MARGEN_Y + self.laberinto.jugador.y * TAMANIO_CELDA + TAMANIO_CELDA // 2
                                crear_particulas(jugador_x, jugador_y, 3, "brillo", COLOR_JUGADOR)
                
                elif self.estado_juego in ["victoria", "game_over"]:
                    if evento.key == pygame.K_RETURN:
                        self.reiniciar_juego()
                        self.estado_juego = "jugando"
                        self.audio.reproducir('inicio')
                    elif evento.key == pygame.K_ESCAPE:
                        self.reiniciar_juego()
                        self.estado_juego = "menu"
                        self.audio.reproducir('menu')
        
        return True

    def actualizar(self):
        tiempo_actual = pygame.time.get_ticks()
        dt = tiempo_actual - self.ultima_actualizacion_tiempo
        self.ultima_actualizacion_tiempo = tiempo_actual
        
        if self.estado_juego == "jugando" and not self.pausa:
            self.estadisticas.actualizar_tiempo(dt)
            self.efectos.actualizar()
            
            resultado = self.laberinto.actualizar()
            if resultado in ["victoria", "game_over"]:
                self.estado_juego = resultado
                self.audio.reproducir(resultado)
                
                if resultado == "victoria":
                    crear_particulas(ANCHO//2, ALTO//2, 200, "confeti")
                    crear_particulas(ANCHO//2, ALTO//2, 50, "estrellas", (200, 200, 100), 2)
                    self.efectos.agregar_texto_flotante("¡VICTORIA!", ANCHO//2, ALTO//2 - 100, 
                                                      COLOR_TEXTO_IMPORTANTE, 40, "rebote")
                    print(f"¡Victoria! Nivel {self.estadisticas.nivel} completado")
                else:
                    crear_particulas(ANCHO//2, ALTO//2, 100, "humo")
                    crear_particulas(ANCHO//2, ALTO//2, 30, "chispas", (200, 60, 60))
                    self.efectos.agregar_texto_flotante("¡CAPTURADO!", ANCHO//2, ALTO//2 - 100, 
                                                      COLOR_TEXTO_IMPORTANTE, 40, "rebote")
                    print("Game Over - Inténtalo de nuevo")
                
                if resultado == "victoria" and self.puntuaciones.es_puntuacion_alta(self.laberinto.puntuacion):
                    self.puntuaciones.guardar_puntuacion(self.laberinto.puntuacion)
    
    def dibujar(self):
        self.pantalla.fill(COLOR_FONDO)
        
        if self.estado_juego == "menu":
            dibujar_menu_principal(self)
            self.puntuaciones.dibujar_tabla_puntuaciones(self.pantalla, self.fuente, 50, 250)
            
        elif self.estado_juego == "jugando":
            self.laberinto.dibujar(self.pantalla, self.config.mostrar_vision, self.config.mostrar_camino_enemigos)
            self.dibujar_informacion()
            dibujar_boton_reiniciar()
            dibujar_boton_pausa()
            self.efectos.dibujar(self.pantalla, self.fuente_grande)
            
            if self.pausa:
                mostrar_pausa_mejorada(self)
                
        elif self.estado_juego in ["victoria", "game_over"]:
            self.dibujar_pantalla_final()
        
        for particula in particulas:
            particula.draw(self.pantalla)
        
        pygame.display.flip()
    
    def dibujar_informacion(self):
        panel_x = MARGEN_X + ANCHO_LABERINTO + 30
        panel_y = MARGEN_Y
        
        panel_principal = pygame.Rect(panel_x, panel_y, 280, 240)
        
        for i, color in enumerate(GRADIENTE_PANEL):
            rect_height = panel_principal.height // len(GRADIENTE_PANEL)
            pygame.draw.rect(self.pantalla, color, 
                           (panel_x, panel_y + i * rect_height, panel_principal.width, rect_height))
        
        pygame.draw.rect(self.pantalla, COLOR_BORDE, panel_principal, 3, border_radius=10)
        
        titulo = self.fuente.render("ESTADÍSTICAS", True, COLOR_TEXTO_IMPORTANTE)
        self.pantalla.blit(titulo, (panel_x + panel_principal.width//2 - titulo.get_width()//2, panel_y + 15))
        
        stats = self.estadisticas.obtener_estadisticas()
        textos = [
            f"Nivel: {stats['Nivel']}",
            f"Objetos: {stats['Objetos Recolectados']}",
            f"Evitados: {stats['Enemigos Evitados']}",
            f"Movimientos: {stats['Movimientos']}",
            f"Tiempo: {stats['Tiempo Jugado']}",
        ]
        
        if stats['Combo']:
            textos.append(f"{stats['Combo']} COMBO!")
        
        for i, texto in enumerate(textos):
            color = COLOR_TEXTO_IMPORTANTE if "COMBO" in texto else COLOR_TEXTO
            texto_surf = self.fuente_pista.render(texto, True, color)
            self.pantalla.blit(texto_surf, (panel_x + 20, panel_y + 60 + i * 32))
        
        panel_leyenda = pygame.Rect(panel_x, panel_y + 260, 280, 220)
        
        for i, color in enumerate(GRADIENTE_PANEL):
            rect_height = panel_leyenda.height // len(GRADIENTE_PANEL)
            pygame.draw.rect(self.pantalla, color, 
                           (panel_x, panel_y + 260 + i * rect_height, panel_leyenda.width, rect_height))
        
        pygame.draw.rect(self.pantalla, COLOR_BORDE, panel_leyenda, 3, border_radius=10)
        
        texto_leyenda = self.fuente.render("LEYENDA", True, COLOR_TEXTO_IMPORTANTE)
        self.pantalla.blit(texto_leyenda, (panel_x + panel_leyenda.width//2 - texto_leyenda.get_width()//2, panel_y + 280))
        
        elementos = [
            (COLOR_JUGADOR, "Jugador"),
            (COLOR_ENEMIGO, "Enemigo"),
            (COLOR_OBJETIVO, "Salida"),
            (COLOR_OBJETO, "Objeto"),
            ((220, 180, 40), "Objeto Especial"),
            ((80, 140, 220), "Objeto de Poder")
        ]
        
        for i, (color, texto) in enumerate(elementos):
            muestra_rect = pygame.Rect(panel_x + 20, panel_y + 330 + i * 30, 20, 20)
            pygame.draw.rect(self.pantalla, color, muestra_rect)
            pygame.draw.rect(self.pantalla, BLANCO, muestra_rect, 1)
            
            texto_surf = self.fuente_pista.render(texto, True, COLOR_TEXTO)
            self.pantalla.blit(texto_surf, (panel_x + 50, panel_y + 330 + i * 30))
    
    def dibujar_pantalla_final(self):
        s = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
        s.fill((0, 0, 0, 180))
        self.pantalla.blit(s, (0, 0))
        
        tiempo = pygame.time.get_ticks() / 1000
        for i in range(50):
            x = (i * 73) % ANCHO
            y = (i * 47) % ALTO
            brillo = 100 + 155 * abs(math.sin(tiempo + i * 0.2))
            pygame.draw.circle(self.pantalla, (brillo, brillo, brillo), (x, y), 2)
        
        panel_rect = pygame.Rect(ANCHO//2 - 350, ALTO//2 - 300, 700, 600)
        
        for i, color in enumerate(GRADIENTE_PANEL):
            rect_height = panel_rect.height // len(GRADIENTE_PANEL)
            pygame.draw.rect(self.pantalla, color, 
                           (panel_rect.x, panel_rect.y + i * rect_height, 
                            panel_rect.width, rect_height))
        
        pygame.draw.rect(self.pantalla, COLOR_BORDE, panel_rect, 5, border_radius=20)
        
        if self.estado_juego == "victoria":
            titulo_texto = "¡VICTORIA!"
            color_titulo = COLOR_TEXTO_IMPORTANTE
        else:
            titulo_texto = "GAME OVER"
            color_titulo = COLOR_TEXTO_IMPORTANTE
        
        titulo = self.fuente_grande.render(titulo_texto, True, color_titulo)
        self.pantalla.blit(titulo, (ANCHO//2 - titulo.get_width()//2, ALTO//2 - 240))
        
        if self.estado_juego == "victoria" and self.puntuaciones.es_puntuacion_alta(self.laberinto.puntuacion):
            texto_alta = self.fuente_mediana.render("¡NUEVO RÉCORD!", True, COLOR_TEXTO_IMPORTANTE)
            self.pantalla.blit(texto_alta, (ANCHO//2 - texto_alta.get_width()//2, ALTO//2 - 320))
            crear_particulas(ANCHO//2, ALTO//2 - 280, 80, "estrellas", COLOR_TEXTO_IMPORTANTE, 3)
        
        estadisticas_y = ALTO//2 - 180
        textos_estadisticas = [
            f'Puntuación: {self.laberinto.puntuacion if self.estado_juego == "victoria" else 0}',
            f'Nivel Alcanzado: {self.estadisticas.nivel}',
            f'Objetos Recolectados: {self.estadisticas.objetos_recolectados}',
            f'Movimientos: {self.estadisticas.movimientos}',
            f'Tiempo: {self.estadisticas.tiempo_juego // 1000 // 60}:{self.estadisticas.tiempo_juego // 1000 % 60:02d}'
        ]
        
        for i, texto in enumerate(textos_estadisticas):
            color = COLOR_TEXTO_IMPORTANTE if "Puntuación" in texto else COLOR_TEXTO
            texto_surf = self.fuente.render(texto, True, color)
            self.pantalla.blit(texto_surf, (ANCHO//2 - texto_surf.get_width()//2, estadisticas_y + i * 50))
        
        boton_reiniciar = pygame.Rect(ANCHO//2 - 140, ALTO//2 + 50, 280, 70)
        mouse_pos = pygame.mouse.get_pos()
        
        if boton_reiniciar.collidepoint(mouse_pos):
            color_reiniciar = COLOR_BOTON_HOVER
            pygame.draw.rect(self.pantalla, (100, 160, 230, 50), 
                           (boton_reiniciar.x - 5, boton_reiniciar.y - 5, 
                            boton_reiniciar.width + 10, boton_reiniciar.height + 10), 
                           border_radius=15)
        else:
            color_reiniciar = COLOR_BOTON
        
        pygame.draw.rect(self.pantalla, color_reiniciar, boton_reiniciar, border_radius=15)
        pygame.draw.rect(self.pantalla, BLANCO, boton_reiniciar, 3, border_radius=15)
        
        texto_reiniciar = self.fuente_mediana.render("JUGAR DE NUEVO", True, BLANCO)
        texto_reiniciar_rect = texto_reiniciar.get_rect(center=boton_reiniciar.center)
        
        if boton_reiniciar.collidepoint(mouse_pos):
            texto_sombra = self.fuente_mediana.render("JUGAR DE NUEVO", True, (220, 230, 255))
            self.pantalla.blit(texto_sombra, (texto_reiniciar_rect.x + 2, texto_reiniciar_rect.y + 2))
        
        self.pantalla.blit(texto_reiniciar, texto_reiniciar_rect)
        
        boton_menu = pygame.Rect(ANCHO//2 - 140, ALTO//2 + 140, 280, 70)
        if boton_menu.collidepoint(mouse_pos):
            color_menu = COLOR_BOTON_SECUNDARIO_HOVER
            pygame.draw.rect(self.pantalla, (110, 210, 130, 50), 
                           (boton_menu.x - 5, boton_menu.y - 5, 
                            boton_menu.width + 10, boton_menu.height + 10), 
                           border_radius=15)
        else:
            color_menu = COLOR_BOTON_SECUNDARIO
        
        pygame.draw.rect(self.pantalla, color_menu, boton_menu, border_radius=15)
        pygame.draw.rect(self.pantalla, BLANCO, boton_menu, 3, border_radius=15)
        
        texto_menu = self.fuente_mediana.render("MENÚ PRINCIPAL", True, BLANCO)
        texto_menu_rect = texto_menu.get_rect(center=boton_menu.center)
        
        if boton_menu.collidepoint(mouse_pos):
            texto_sombra = self.fuente_mediana.render("MENÚ PRINCIPAL", True, (220, 240, 220))
            self.pantalla.blit(texto_sombra, (texto_menu_rect.x + 2, texto_menu_rect.y + 2))
        
        self.pantalla.blit(texto_menu, texto_menu_rect)
        
        tabla_x = ANCHO//2 + 380
        tabla_y = ALTO//2 - 280
        self.puntuaciones.dibujar_tabla_puntuaciones(self.pantalla, self.fuente, tabla_x, tabla_y)

    def correr(self):
        global particulas
        
        corriendo = True
        print("Iniciando Laberinto Cósmico - Versión Equilibrada")
        print("Características de balance:")
        print("- Laberintos más pequeños (15x15)")
        print("- Menos enemigos (1-5 según dificultad)")
        print("- Enemigos más lentos")
        print("- Visión del jugador aumentada")
        print("- Invulnerabilidad temporal al coger objetos")
        print("- Dificultad progresiva")
        
        while corriendo:
            particulas = [p for p in particulas if p.update()]
            
            corriendo = self.manejar_eventos()
            self.actualizar()
            self.dibujar()
            self.reloj.tick(FPS)

def main():
    try:
        juego = Juego()
        
        global fuente, fuente_game_over, fuente_pista
        fuente = juego.fuente
        fuente_game_over = juego.fuente_grande
        fuente_pista = juego.fuente_pista
        
        juego.correr()
    except KeyboardInterrupt:
        print("\nJuego interrumpido por el usuario")
    except Exception as e:
        print(f"Error durante la ejecución: {e}")
        import traceback
        traceback.print_exc()
    finally:
        pygame.quit()
        print("Juego terminado correctamente")

if __name__ == "__main__":
    main()