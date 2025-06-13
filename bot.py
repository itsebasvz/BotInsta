from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains

from tkinter import Tk, simpledialog
from tkinter import messagebox

import tkinter as tk
import undetected_chromedriver as uc
import random
import time
import os
import sys
import datetime

# Obtener la fecha y hora actual
fecha_actual = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# Crear archivo de log con esa fecha y hora
log_filename = f"log_instabot_{fecha_actual}.txt"
log_file = open(log_filename, "w", encoding="utf-8")

# Redirigir stdout (consola) al archivo y a la consola al mismo tiempo
class DualLogger:
    def __init__(self, *streams):
        self.streams = streams

    def write(self, message):
        for stream in self.streams:
            stream.write(message)
            stream.flush()

    def flush(self):
        for stream in self.streams:
            stream.flush()

# Redirige todo lo que se imprima a ambos lugares
sys.stdout = DualLogger(sys.stdout, log_file)
sys.stderr = DualLogger(sys.stderr, log_file)

def pedir_credenciales_y_mensaje():
    def enviar():
        nonlocal usuario, contrasena, mensaje
        usuario = entry_usuario.get()
        contrasena = entry_contrasena.get()
        mensaje = entry_mensaje.get()

        if not usuario or not contrasena or not mensaje:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        # Ocultar primera pantalla
        frame_formulario.pack_forget()

        # Mostrar confirmación
        label_confirmacion.config(text=f"📨 El mensaje será:\n\n'{mensaje}'")
        frame_confirmacion.pack()

    def confirmar():
        root.quit()

    def cancelar():
        messagebox.showinfo("Cancelado", "🚫 Operación cancelada.")
        root.destroy()
        exit()

    usuario = contrasena = mensaje = None

    root = tk.Tk()
    root.title("Credenciales y mensaje")
    root.geometry("550x350")
    root.resizable(False, False)

    # -------- Pantalla de formulario --------
    frame_formulario = tk.Frame(root)
    frame_formulario.pack()

    tk.Label(frame_formulario, text="Usuario:", font=("Arial", 14)).pack(pady=(10, 0))
    entry_usuario = tk.Entry(frame_formulario, font=("Arial", 14), width=40)
    entry_usuario.pack()

    tk.Label(frame_formulario, text="Contraseña:", font=("Arial", 14)).pack(pady=(10, 0))
    entry_contrasena = tk.Entry(frame_formulario, font=("Arial", 14), show="*", width=40)
    entry_contrasena.pack()

    tk.Label(frame_formulario, text="Mensaje a enviar:", font=("Arial", 14)).pack(pady=(10, 0))
    entry_mensaje = tk.Entry(frame_formulario, font=("Arial", 14), width=40)
    entry_mensaje.pack()

    tk.Button(frame_formulario, text="Siguiente", font=("Arial", 12), command=enviar).pack(pady=15)

    # -------- Pantalla de confirmación --------
    frame_confirmacion = tk.Frame(root)
    label_confirmacion = tk.Label(frame_confirmacion, text="", font=("Arial", 13), wraplength=500, justify="left")
    label_confirmacion.pack(pady=20)

    tk.Button(frame_confirmacion, text="✅ Confirmar", font=("Arial", 12), command=confirmar).pack(side="left", padx=40)
    tk.Button(frame_confirmacion, text="🚫 Cancelar", font=("Arial", 12), command=cancelar).pack(side="right", padx=40)

    root.mainloop()
    root.destroy()

    if usuario and contrasena and mensaje:
        return usuario, contrasena, mensaje
    else:
        raise SystemExit("⚠️ Proceso cancelado o campos vacíos.")

usuario, contrasena, mensaje_a_enviar = pedir_credenciales_y_mensaje()

if not mensaje_a_enviar:
    print("⛔ No se ingresó ningún mensaje. Cerrando el programa.")
    exit()

def delay(min_time=2, max_time=5):
    t = random.uniform(min_time, max_time)
    print(f"⏳ Esperando {round(t, 2)} segundos...")
    time.sleep(t)

# Crear navegador con opciones
options = uc.ChromeOptions()
options.add_argument("--start-maximized")
# Puedes agregar más argumentos si lo necesitas

# Iniciar driver (ya no necesitas la ruta del ejecutable)
driver = uc.Chrome(options=options)

# Abrir Instagram
driver.get("https://www.instagram.com/accounts/login/")
time.sleep(5)  # Esperar a que cargue la página

# Encontrar campos e ingresar datos
driver.find_element(By.NAME, "username").send_keys(usuario)
driver.find_element(By.NAME, "password").send_keys(contrasena + Keys.RETURN)

try:
    # Espera hasta que aparezca el popup con el div "Ahora no"
    popup = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, "//div[text()='Ahora no']"))
    )
    popup.click()
    print("✅ Popup de 'Guardar info' cerrado automáticamente")
except TimeoutException:
    print("❌ No apareció el popup de 'Guardar info'")


try:
    mensajes = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, "//span[text()='Mensajes']"))
    )
    print("✅ Login detectado (elemento 'Mensajes' encontrado)")
except TimeoutException:
    print("❌ No se detectó inicio de sesión exitoso.")
    driver.quit()
    exit()

# Ir al perfil (puedes poner el username en la URL)
driver.get(f"https://www.instagram.com/{usuario}/")

# Esperar que cargue la página y el botón de la historia esté clickeable
story_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//div[@role='button' and .//canvas]"))
)
story_button.click()
print("✅ Historia abierta")

# 1. Esperar a que cargue la historia
delay(3,4)

# 3. Intentar hacer clic en el botón de vistas en español
try:
    views_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[@role='button'][.//span[contains(text(), 'Vista por')]]"))
    )
    views_button.click()
    print("✅ Click en 'Vista por' exitoso")
except Exception as e:
    print(f"❌ No se encontró el botón 'Vista por': {e}")

# 2. Esperar a que aparezca al menos un usuario
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//a[starts-with(@href, '/') and not(contains(@href, '/stories/'))]"))
)
delay(4,5)

try:
    # 1️⃣ Detectar contenedor con scroll
    scroll_container = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[contains(@style, 'overflow: hidden auto')]"))
    )

    usernames_detectados = set()
    last_scroll_top = 0
    retries = 0
    scroll_step = 400

    while retries < 5:
        scroll_top_before = driver.execute_script("return arguments[0].scrollTop;", scroll_container)
        scroll_height_before = driver.execute_script("return arguments[0].scrollHeight;", scroll_container)

        print(f"⬆️ Scroll actual antes del scroll: {scroll_top_before}")
        print(f"⬇️ Scroll máximo actual (scrollHeight): {scroll_height_before}")

        # Scroll hacia abajo
        driver.execute_script(f"arguments[0].scrollTop += {scroll_step};", scroll_container)
        delay(2.5, 3.5)

        # Recolectar elementos <a> que probablemente sean usernames
        viewer_elements = scroll_container.find_elements(By.XPATH, ".//a[starts-with(@href, '/')]")
        nuevos_usernames = []

        for el in viewer_elements:
            href = el.get_attribute("href")
            if href:
                parts = href.rstrip('/').split('/')
                if len(parts) >= 4:  # formato https://www.instagram.com/username/
                    username = parts[3]
                    if username and len(username) < 30 and username not in usernames_detectados:
                        usernames_detectados.add(username)
                        nuevos_usernames.append(username)

        print(f"🧠 Nuevos usernames en esta ronda: {len(nuevos_usernames)}")
        print(f"📈 Total usernames únicos hasta ahora: {len(usernames_detectados)}")
        if nuevos_usernames:
            print(f"🔍 Ejemplo de nuevos usernames: {nuevos_usernames[:5]}")
            retries = 0
        else:
            retries += 1

        scroll_top_after = driver.execute_script("return arguments[0].scrollTop;", scroll_container)
        scroll_height_after = driver.execute_script("return arguments[0].scrollHeight;", scroll_container)

        print(f"📏 scrollHeight después del scroll: {scroll_height_after}")
        if scroll_top_before == scroll_top_after:
            print("🔁 No hubo cambio en scrollTop, aumentando retry.")
            retries += 1

        print("--------------------------------------------------")

    print(f"✅ Scroll terminado. Viewers totales únicos: {len(usernames_detectados)}")

    # 2️⃣ VISITAR CADA PERFIL Y ENVIAR MENSAJE SI SIGUE
    for username in usernames_detectados:

        profile_url = f"https://www.instagram.com/{username}/"
        driver.get(profile_url)
        print(f"📄 Visitando perfil de {username}")
        delay(3, 6)

        try:
            te_sigue = driver.find_element(By.XPATH, (
                "//*[contains(text(), 'Siguiendo') or contains(text(), 'Follows you') or contains(text(), 'Seguir también')]"
            ))
            print(f"✅ {username} SÍ sigue al bot")

            delay(2, 4)

            mensaje_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//div[text()='Mensaje']"))
            )
            mensaje_btn.click()
            print("💬 Botón 'Mensaje' clickeado")

            try:
                boton_ahora_no = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[text()='Ahora no']"))
                )
                delay(1, 3)
                boton_ahora_no.click()
                print("❌ Notificación de activar notificaciones descartada con 'Ahora no'")
            except:
                print("ℹ️ No apareció la notificación de activar notificaciones")

            delay(2, 4)

            try:
                input_box = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//p[@class='xat24cr xdj266r']"))
                )
                input_box.click()
                delay(1, 2)
                ActionChains(driver).send_keys(mensaje_a_enviar).send_keys(Keys.ENTER).perform()
                print(f"📩 Mensaje enviado a {username}: {mensaje_a_enviar}")
                delay(5, 10)
            except Exception as e:
                print(f"❌ No se pudo enviar el mensaje a {username}: {e}")

        except:
            print(f"⛔ {username} NO sigue al bot (o no se detectó correctamente)")
            continue

except Exception as e:
    print(f"❌ Error durante ejecución: {e}")

log_file.close()
time.sleep(10)

driver.quit()
