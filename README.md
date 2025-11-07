#https://github.com/Alejandro-Mendieta/MAZE/blob/main/assests/FOTOS/FOTO2.png?raw=true
<img width="901" height="636" alt="image" src="https://github.com/Alejandro-Mendieta/MAZE/blob/main/assests/FOTOS/FOTO2.png?raw=true" />
<img width="901" height="636" alt="image" src="https://github.com/Alejandro-Mendieta/MAZE/blob/main/assests/FOTOS/FOTO2.png?raw=true" />

![Laberinto Cósmico](https://img.shields.io/badge/Version-2.0-blue.svg)
![Python](https://img.shields.io/badge/Python-3.6+-green.svg)
![Pygame](https://img.shields.io/badge/Pygame-2.0+-red.svg)

Un emocionante juego de laberintos con temática cósmica, inteligencia artificial y efectos visuales impresionantes. Escapa del laberinto mientras evitas enemigos inteligentes y recolectas objetos especiales.

## ✨ Características Principales

### 🎯 Jugabilidad
- **Generación procedural** de laberintos únicos
- **Sistema de niveles** con dificultad progresiva
- **Enemigos con IA** que te persiguen inteligentemente
- **Múltiples tipos de objetos** coleccionables
- **Sistema de combos** por recolección rápida
- **Puntuación dinámica** basada en tiempo y objetos

### 🎨 Visuales
- **Efectos de partículas** avanzados (confeti, estrellas, chispas)
- **Campo de visión** dinámico del jugador
- **Animaciones fluidas** para todos los elementos
- **Gradientes cósmicos** y paleta de colores espacial
- **Interfaz moderna** y responsive

### ⚙️ Características TécnicasN
- **Pathfinding inteligente** para enemigos
- **Sistema de configuración** persistente
- **Tabla de puntuaciones** con top 10
- **Múltiples dificultades** ajustables
- **Efectos de sonido** virtuales
- **Compatibilidad** Linux/Windows

## 🚀 Instalación

### Prerrequisitos
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip python3-pygame

# Windows
# Descargar Python desde python.org
pip install pygame
```

### Ejecución
```bash
# Clonar o descargar el archivo
python3 laberinto_cosmico.py
```

## 🎮 Controles

| Tecla | Acción |
|-------|--------|
| **W / ↑** | Mover hacia arriba |
| **S / ↓** | Mover hacia abajo |
| **A / ←** | Mover hacia izquierda |
| **D / →** | Mover hacia derecha |
| **ESC** | Pausa/Menú |
| **Click** | Interactuar con botones |

## 🎯 Objetivo del Juego

Tu misión es **escapar del laberinto** llegando al **portal dorado** mientras:

- 🏃‍♂️ **Te mueves** por los caminos del laberinto
- 👾 **Evitas enemigos** que te persiguen
- 💎 **Recolectas objetos** para puntos extra
- ⭐ **Consigues combos** recolectando rápidamente
- 🏆 **Superas niveles** con dificultad creciente

## 🎪 Elementos del Juego

### 👤 Jugador
- **Color cian brillante**
- **Campo de visión** circular
- **Animaciones de movimiento**
- **Invulnerabilidad temporal** al coger objetos

### 👾 Enemigos
- **Persecución inteligente** con pathfinding
- **Diferentes tipos**: normales y rápidos
- **Línea de visión** limitada
- **Velocidades balanceadas**

### 💎 Objetos Coleccionables
| Tipo | Color | Efecto |
|------|-------|--------|
| **Normal** | Verde | Puntos básicos + invulnerabilidad |
| **Especial** | Dorado | Puntos extra + efectos especiales |
| **Poder** | Azul | Puntos premium + bonificación |

### 🎯 Portal de Salida
- **Animación pulsante** dorada
- **Efectos visuales** destacados
- **Objetivo final** de cada nivel

## ⚙️ Dificultades

| Dificultad | Enemigos | Velocidad | Laberinto |
|------------|----------|-----------|-----------|
| **Fácil** | 1-2 | Lenta | Simple |
| **Normal** | 2-3 | Media | Estándar |
| **Difícil** | 3-4 | Rápida | Complejo |
| **Imposible** | 4-5 | Muy rápida | Extremo |

## 🏆 Sistema de Puntuación

La puntuación se calcula basándose en:

```
Puntuación = 
  Tiempo restante (máx 15,000) +
  Objetos × 500 +
  Nivel × 800 +
  Bonificación por combo
```

### 🎯 Combos
- **Recolecta objetos rápidamente** para activar combos
- **Cada combo** multiplica tu puntuación
- **Máximo de 2 segundos** entre objetos

## 🎨 Personalización

El juego incluye opciones configurables:

- ✅ **Mostrar/Ocultar** campo de visión
- ✅ **Mostrar/Ocultar** camino de enemigos
- ✅ **Activar/Desactivar** efectos de partículas
- ✅ **Ajustar** volumen de audio
- ✅ **Cambiar** dificultad

## 🛠️ Estructura del Proyecto

```
laberinto_cosmico/
├── laberinto_cosmico.py      # Archivo principal
├── config_laberinto.json     # Configuración guardada
├── puntuaciones.txt         # Tabla de records
└── README.md               # Este archivo
```

## 🎪 Características Técnicas Detalladas

### 🧩 Generación de Laberintos
- **Algoritmo DFS** mejorado para caminos naturales
- **Diferentes estrategias** por dificultad
- **Garantía de solución** en todos los niveles
- **Posicionamiento inteligente** de elementos

### 🤖 IA de Enemigos
- **Pathfinding BFS** optimizado
- **Detección por línea de visión**
- **Actualización eficiente** de rutas
- **Comportamientos diferenciados** por tipo

### ✨ Sistema de Partículas
- **5 tipos diferentes**: confeti, estrellas, chispas, brillo, humo
- **Física realista** con gravedad y rotación
- **Efectos de desvanecimiento** y pulso
- **Optimizado** para rendimiento

## 🐛 Solución de Problemas

### Error: "Pygame no está instalado"
```bash
# Linux
sudo apt install python3-pygame

# Windows
pip install pygame
```

### El juego va muy lento
- Cierra otras aplicaciones
- Reduce los efectos de partículas en configuración
- Usa dificultad más baja

### No se guardan las puntuaciones
- Verifica permisos de escritura
- El archivo `puntuaciones.txt` se crea automáticamente

## 🎊 Consejos y Estrategias

### Para Principiantes
1. **Empieza en fácil** para aprender los controles
2. **Usa el campo de visión** para planificar rutas
3. **No corras riesgos innecesarios** con enemigos
4. **Prioriza la salida** sobre los objetos

### Para Expertos
1. **Aprovecha los combos** para máxima puntuación
2. **Memoriza patrones** de movimiento de enemigos
3. **Usa objetos para invulnerabilidad** estratégica
4. **Planifica rutas eficientes**

## 🔄 Historial de Versiones

### v2.0 - Actualización Cósmica
- ✅ Balance completo de dificultad
- ✅ Sistema de invulnerabilidad
- ✅ Mejoras visuales
- ✅ Corrección de bugs

### v1.0 - Lanzamiento Inicial
- Funcionalidades básicas del juego
- Sistema de puntuación
- Efectos visuales simples

## 👥 Contribuir

¿Tienes ideas para mejorar el juego? ¡Contribuciones son bienvenidas!

1. Haz fork del proyecto
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

## 📄 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

## 🎯 Próximas Características

- [ ] Modo multijugador
- [ ] Editor de laberintos
- [ ] Más tipos de enemigos
- [ ] Power-ups especiales
- [ ] Logros y desafíos

---

## 👨‍💻 Desarrollo
Por Alejandro Mendieta

creado con ❤️ usando Python y Pygame. Incluye las mejores prácticas modernas de desarrollo de juegos y una arquitectura escalable para futuras mejoras.

---

**¡Diviértete explorando el cosmos!** 🌌