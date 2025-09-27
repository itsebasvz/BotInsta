## BotInsta

Script en Python que automatiza (con Selenium) el envío de mensajes directos en Instagram a las personas que han visto tu historia y que además te siguen. Incluye una pequeña interfaz gráfica (Tkinter) para ingresar credenciales y el mensaje, registro de logs por sesión y desplazamiento automático para recolectar espectadores.

> ⚠️ Aviso importante: El uso de automatización en Instagram puede violar los Términos de Uso de la plataforma. Usa este proyecto bajo tu propia responsabilidad, solo con fines educativos y en cuentas de prueba. No abuses del envío de mensajes ni ejecutes el bot de forma agresiva.

---

## ✨ Características principales

- Interfaz gráfica (Tkinter) para ingresar usuario, contraseña y mensaje, con pantalla de confirmación.
- Uso de perfil de Chrome portable local (`chrome-profile/`) para conservar sesión / apariencia.
- Login automático y cierre de popups ("Guardar info", "Activar notificaciones") si aparecen.
- Abre tu propia historia y abre el panel de vistas ("Vista por").
- Scrollea automáticamente el listado de viewers recolectando usernames únicos.
- Para cada viewer detecta si te sigue (heurística por textos: `Siguiendo`, `Follows you`, `Seguir también`).
- Envía el mensaje solo a quienes te siguen.
- Delays aleatorios (anti‑patrones de bot evidentes).
- Log completo por ejecución: archivo `log_instabot_YYYY-MM-DD_HH-MM-SS.txt`.
- Fallback si falla la creación del driver con `webdriver-manager`.

---

## 🧩 Dependencias

Paquetes principales:

```
selenium
webdriver-manager
```

Opcional / ya incluido muchas veces en entornos:

```
python-dotenv   # (no se usa aún, pero útil si quieres mover credenciales a .env)
pyinstaller     # (si deseas generar ejecutable)
```

### Instalar dependencias

```bash
python -m venv venv
source venv/bin/activate          # En Linux / macOS
# .\\venv\\Scripts\\activate     # En Windows PowerShell

pip install --upgrade pip
pip install selenium webdriver-manager
```

> Nota: Ya existe un `bot.spec`; puedes reutilizarlo: `pyinstaller bot.spec`.
---

## 🚀 Uso

1. Asegura que tienes Google Chrome instalado (misma versión que Chromedriver gestionará `webdriver-manager`).
2. Clona o descarga este repositorio.
3. (Opcional) Activa el entorno virtual e instala dependencias.
4. Ejecuta:
	```bash
	python bot.py
	```
5. En la ventana emergente ingresa:
	- Usuario (sin @)
	- Contraseña
	- Mensaje a enviar
6. Confirma el mensaje.
7. El bot:
	- Inicia Chrome con un perfil local (`chrome-profile/` se crea si no existe)
	- Inicia sesión
	- Abre tu historia y el panel de viewers
	- Scrollea para recolectar usuarios
	- Visita cada perfil y envía el mensaje a quienes te siguen
8. Revisa el archivo de log generado para ver el resumen de la ejecución.

### ▶️ Uso rápido con ejecutable (Windows)

Si ya tienes la carpeta `dist/` con `bot.exe` (generada por PyInstaller) puedes ejecutar el bot sin instalar Python ni dependencias:

1. Asegúrate de tener Google Chrome instalado.
2. Copia toda la carpeta del proyecto (incluyendo `dist/` y no solo el `.exe`) para que pueda crear el perfil `chrome-profile/` y los logs.
3. En Windows, doble clic en `dist/bot.exe`
4. Ingresa credenciales y mensaje en la ventana Tkinter.
5. Se generará un archivo de log en el mismo directorio donde se ejecute el `.exe`.

Notas:
- El primer arranque puede tardar mientras `webdriver-manager` descarga el driver.
- Si el firewall pregunta, permite el acceso local.
- Si Chrome actualiza versión, el driver se descargará de nuevo.

#### ¿Dónde está el log?
Se crea en el directorio de ejecución con nombre: `log_instabot_YYYY-MM-DD_HH-MM-SS.txt`.

#### ¿Puedo mover solo el .exe?
No es recomendable: PyInstaller en modo onefile extrae dependencias a una carpeta temporal cada vez, pero tu perfil de Chrome local y los logs quedarían dispersos. Mantén el árbol completo o empaqueta en .zip.

---

## 📁 Estructura relevante

```
bot.py                # Script principal
bot.spec              # Configuración PyInstaller (opcional)
dist/
	bot.exe             # Ejecutable listo para Windows (si fue generado)
chrome-profile/       # (Se crea al ejecutar si no existe) Perfil persistente de Chrome
log_instabot_*.txt    # Logs por sesión (generados dinámicamente)
build/                # Artefactos de compilación (si usaste PyInstaller)
```

---

## 🛠 Personalización rápida

| Objetivo | Dónde cambiar |
|----------|---------------|
| Rango de delays aleatorios | Función `delay(min_time, max_time)` |
| XPaths si cambia el idioma | Busca expresiones `By.XPATH` en `bot.py` |
| Mensaje dinámico | Modificar antes del envío dentro del loop de viewers |
| Filtrar por número mínimo de viewers | Añadir lógica antes del bucle principal |

### Idioma / XPaths
El script asume interfaz de Instagram en español (detecta textos como `Ahora no`, `Mensajes`, `Vista por`, `Mensaje`). Si tu cuenta muestra otro idioma, deberás adaptar los XPaths que utilizan `text()`.

## 🐞 Problemas comunes

| Problema | Posible causa | Solución |
|----------|---------------|----------|
| Falla al iniciar Chrome | Versión incompatible de Chrome/driver | Cierra todos los Chromes, deja que `webdriver-manager` descargue versión correcta |
| No encuentra `Mensajes` | Login falló o 2FA requerido | Verifica credenciales / agrega manejo 2FA manual |
| No se abre `Vista por` | UI cambió | Ajustar XPath del botón de vistas |
| No envía mensajes | Cambió el selector del input | Actualiza XPath para el cuadro de texto del DM |
| Demasiados bloqueos | Instagram sospecha de automatización | Aumenta delays y reduce número de mensajes por sesión |

---

## 🧪 Ideas de mejora (Roadmap)

- Persistir lista de usuarios ya mensajedos (para no repetir en futuras ejecuciones).
- Rotar mensajes (plantillas con variables `{username}`).
- Añadir soporte multi‑idioma para selectores.
- Modo "dry-run" (simular sin enviar).
- Métricas finales en JSON / CSV (total viewers, enviados, saltados).
- Detección / pausa si aparece un captcha.

---

## 🔐 Consideraciones éticas / legales

Este proyecto es solo con fines educativos. El envío masivo o no solicitado de mensajes puede considerarse spam y provocar suspensión de la cuenta. Úsalo responsablemente.

---

## 📜 Licencia

Este proyecto está distribuido bajo la **Licencia MIT**.

Puedes leer el texto completo en [`LICENSE.md`](LICENSE.md). En resumen:

- Puedes usar, copiar, modificar, fusionar, publicar, distribuir, sublicenciar y/o vender copias del software.
- Debes mantener el aviso de copyright y la nota de licencia.
- El software se entrega "TAL CUAL", sin garantías de ningún tipo.

> Si reutilizas parte del código en otro proyecto público, deja una referencia o mención — no es obligatorio, pero se agradece. :D

---

## 🙌 Contribuciones

Sugerencias y mejoras son bienvenidas. Abre un issue o un pull request describiendo claramente el cambio.

---

## 🧾 Créditos

- Selenium WebDriver
- webdriver-manager
- Tkinter (incluido en la librería estándar de Python)

---

¿Dudas o quieres ampliar funcionalidades? Abre un issue pls 🙂

