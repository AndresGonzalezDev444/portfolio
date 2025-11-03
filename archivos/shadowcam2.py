# ShadowCam - Enhanced Ethical Camera Detection & Remote Access System v2.1
# Sistema integrado de detección y visualización de cámaras de red con acceso remoto

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import psutil
import socket
import ipaddress
from scapy.all import ARP, Ether, srp
import threading
from mac_vendor_lookup import MacLookup
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import nmap
import cv2
from PIL import Image, ImageTk
import webbrowser
import json
import time
import requests

resultados = []
camaras_guardadas = []  # Nueva lista para cámaras guardadas
COLOR_FONDO = "#0d0d0d"
COLOR_TEXTO = "#00ff00"
FUENTE_CONSOLA = ("Consolas", 11)

# Archivo para guardar cámaras persistentes
ARCHIVO_CAMARAS = "camaras_guardadas.json"

# Credenciales por defecto para probar en cámaras
DEFAULT_CREDS = [
    ("admin", "admin"),
    ("admin", "12345"),
    ("admin", "password"),
    ("root", "root"),
    ("user", "user"),
    ("admin", "1234"),
    ("admin", "1111111"),  # Samsung común
    ("admin", "4321"),     # Samsung común
    ("admin", "123456"),
    ("root", "admin"),
    ("service", "service"),
    ("", "admin"),
    ("supervisor", "supervisor"),
    ("", "")
]


# Puertos comunes para cámaras IP
CAM_PORTS = [80, 554, 8080, 8888]

# ---------------------- NUEVA FUNCIONALIDAD: GESTIÓN DE CÁMARAS REMOTAS ----------------------

class CameraManager:
    def __init__(self):
        self.cargar_camaras_guardadas()
    
    def cargar_camaras_guardadas(self):
        """Cargar cámaras guardadas desde archivo JSON"""
        global camaras_guardadas
        try:
            with open(ARCHIVO_CAMARAS, 'r') as f:
                camaras_guardadas = json.load(f)
        except FileNotFoundError:
            camaras_guardadas = []
        except json.JSONDecodeError:
            camaras_guardadas = []
    
    def guardar_camaras(self):
        """Guardar cámaras en archivo JSON"""
        try:
            with open(ARCHIVO_CAMARAS, 'w') as f:
                json.dump(camaras_guardadas, f, indent=4)
            return True
        except Exception as e:
            print(f"Error al guardar cámaras: {e}")
            return False
    
    def agregar_camara(self, nombre, url, ip_local, descripcion=""):
        """Agregar una nueva cámara a la lista guardada"""
        nueva_camara = {
            "id": len(camaras_guardadas) + 1,
            "nombre": nombre,
            "url": url,
            "ip_local": ip_local,
            "descripcion": descripcion,
            "fecha_agregada": time.strftime("%Y-%m-%d %H:%M:%S"),
            "activa": True,
            "intentos_conexion": 0,
            "ultima_conexion": None
        }
        camaras_guardadas.append(nueva_camara)
        return self.guardar_camaras()
    
    def verificar_acceso_remoto(self, camara):
        """Verificar si una cámara es accesible remotamente"""
        url = camara['url']
        try:
            # Para RTSP
            if url.startswith('rtsp://'):
                cap = cv2.VideoCapture(url)
                if cap.isOpened():
                    ret, _ = cap.read()
                    cap.release()
                    return ret
            
            # Para HTTP
            elif url.startswith('http://'):
                response = requests.get(url, timeout=5)
                return response.status_code == 200
            
            return False
        except Exception as e:
            print(f"Error verificando acceso: {e}")
            return False
    
    def generar_url_remota(self, ip_local, puerto, usuario, password):
        """Generar URLs para acceso remoto usando diferentes métodos"""
        urls_remotas = []
        
        # Método 1: Acceso directo por IP pública (requiere port forwarding)
        try:
            # Obtener IP pública
            ip_publica = requests.get('https://httpbin.org/ip', timeout=5).json()['origin']
            urls_remotas.append({
                "tipo": "IP Pública + Port Forwarding",
                "url": f"rtsp://{usuario}:{password}@{ip_publica}:{puerto}/",
                "descripcion": "Requiere configurar port forwarding en el router",
                "nota": f"Configurar redirección del puerto {puerto} hacia {ip_local}"
            })
        except:
            pass
        
        # Método 2: URLs con IP local (para documentación)
        urls_remotas.append({
            "tipo": "Acceso Local",
            "url": f"rtsp://{usuario}:{password}@{ip_local}:{puerto}/",
            "descripcion": "Solo funciona dentro de la red local",
            "nota": "Para referencia y pruebas locales"
        })
        
        # Método 3: Sugerir servicios de túnel
        urls_remotas.append({
            "tipo": "Túnel Ngrok",
            "url": f"Configurar ngrok para exponer puerto {puerto}",
            "descripcion": "Usar ngrok tcp {puerto} para crear túnel",
            "nota": "Proporciona acceso temporal desde internet"
        })
        
        return urls_remotas

def mostrar_gestion_camaras():
    """Ventana para gestionar cámaras guardadas"""
    ventana_gestion = tk.Toplevel()
    ventana_gestion.title("ShadowCam - Gestión de Cámaras Remotas")
    ventana_gestion.geometry("900x650")
    ventana_gestion.configure(bg=COLOR_FONDO)
    
    # Título
    tk.Label(ventana_gestion, text="🎥 GESTIÓN DE CÁMARAS REMOTAS", 
             font=("Consolas", 18, "bold"), fg=COLOR_TEXTO, bg=COLOR_FONDO).pack(pady=10)
    
    # Frame principal
    frame_principal = tk.Frame(ventana_gestion, bg=COLOR_FONDO)
    frame_principal.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    # Lista de cámaras guardadas
    frame_lista = tk.Frame(frame_principal, bg=COLOR_FONDO)
    frame_lista.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    tk.Label(frame_lista, text="Cámaras Guardadas:", fg=COLOR_TEXTO, 
             bg=COLOR_FONDO, font=FUENTE_CONSOLA).pack(anchor='w')
    
    # Listbox con scrollbar
    frame_listbox = tk.Frame(frame_lista)
    frame_listbox.pack(fill=tk.BOTH, expand=True)
    
    listbox_guardadas = tk.Listbox(frame_listbox, bg="#1a1a1a", fg=COLOR_TEXTO, 
                                  font=FUENTE_CONSOLA, height=15)
    scrollbar = tk.Scrollbar(frame_listbox)
    listbox_guardadas.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=listbox_guardadas.yview)
    
    listbox_guardadas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    # Panel de información
    frame_info = tk.Frame(frame_principal, bg=COLOR_FONDO)
    frame_info.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))
    
    tk.Label(frame_info, text="Información de la Cámara:", fg=COLOR_TEXTO, 
             bg=COLOR_FONDO, font=FUENTE_CONSOLA).pack(anchor='w')
    
    text_info = scrolledtext.ScrolledText(frame_info, width=40, height=20, 
                                         bg="#1a1a1a", fg=COLOR_TEXTO, 
                                         font=FUENTE_CONSOLA)
    text_info.pack(fill=tk.BOTH, expand=True, pady=5)
    
    def actualizar_lista():
        """Actualizar la lista de cámaras guardadas"""
        listbox_guardadas.delete(0, tk.END)
        for i, camara in enumerate(camaras_guardadas):
            estado = "✅" if camara.get('activa', True) else "❌"
            listbox_guardadas.insert(tk.END, f"{estado} {camara['nombre']} - {camara['ip_local']}")
    
    def mostrar_info_camara(event):
        """Mostrar información detallada de la cámara seleccionada"""
        seleccion = listbox_guardadas.curselection()
        if not seleccion:
            return
        
        camara = camaras_guardadas[seleccion[0]]
        info = f"""INFORMACIÓN DE LA CÁMARA
{'='*40}

Nombre: {camara['nombre']}
URL: {camara['url']}
IP Local: {camara['ip_local']}
Descripción: {camara.get('descripcion', 'N/A')}
Fecha Agregada: {camara['fecha_agregada']}
Estado: {'Activa' if camara.get('activa', True) else 'Inactiva'}
Intentos de Conexión: {camara.get('intentos_conexion', 0)}
Última Conexión: {camara.get('ultima_conexion', 'Nunca')}

OPCIONES DE ACCESO REMOTO
{'='*40}

Para acceder a esta cámara desde internet, 
tienes las siguientes opciones:

1. PORT FORWARDING:
   - Configura tu router para redirigir
     el puerto de la cámara
   - Usa tu IP pública para acceso externo

2. VPN:
   - Configura una VPN en tu red
   - Accede como si estuvieras local

3. TÚNELES (ngrok, etc.):
   - Crea túneles temporales
   - No requiere configuración del router

4. SERVICIOS EN LA NUBE:
   - Algunos fabricantes ofrecen acceso
     remoto a través de sus plataformas

NOTA: El acceso remoto a cámaras debe
realizarse solo en dispositivos propios
y con fines educativos/de seguridad.
"""
        text_info.delete(1.0, tk.END)
        text_info.insert(1.0, info)
    
    def verificar_camara():
        """Verificar si la cámara seleccionada está accesible"""
        seleccion = listbox_guardadas.curselection()
        if not seleccion:
            messagebox.showinfo("Selección", "Selecciona una cámara para verificar.")
            return
        
        camara = camaras_guardadas[seleccion[0]]
        
        # Mostrar ventana de progreso
        ventana_progreso = tk.Toplevel(ventana_gestion)
        ventana_progreso.title("Verificando Acceso...")
        ventana_progreso.geometry("400x150")
        ventana_progreso.configure(bg=COLOR_FONDO)
        
        tk.Label(ventana_progreso, text="Verificando acceso a la cámara...", 
                fg=COLOR_TEXTO, bg=COLOR_FONDO, font=FUENTE_CONSOLA).pack(pady=20)
        
        progress = ttk.Progressbar(ventana_progreso, mode='indeterminate')
        progress.pack(pady=10, padx=20, fill=tk.X)
        progress.start()
        
        def verificar():
            manager = CameraManager()
            accesible = manager.verificar_acceso_remoto(camara)
            
            ventana_progreso.destroy()
            
            # Actualizar estadísticas de la cámara
            camara['intentos_conexion'] = camara.get('intentos_conexion', 0) + 1
            if accesible:
                camara['ultima_conexion'] = time.strftime("%Y-%m-%d %H:%M:%S")
                camara['activa'] = True
                messagebox.showinfo("Verificación", 
                                   f"✅ La cámara '{camara['nombre']}' está accesible.")
            else:
                camara['activa'] = False
                messagebox.showwarning("Verificación", 
                                      f"❌ La cámara '{camara['nombre']}' no está accesible.\n\n"
                                      "Posibles causas:\n"
                                      "- La cámara está apagada\n"
                                      "- Cambió de IP\n"
                                      "- Problemas de red\n"
                                      "- Credenciales cambiaron")
            
            manager.guardar_camaras()
            actualizar_lista()
            mostrar_info_camara(None)
        
        threading.Thread(target=verificar).start()
    
    def ver_camara_remota():
        """Abrir visor para la cámara seleccionada"""
        seleccion = listbox_guardadas.curselection()
        if not seleccion:
            messagebox.showinfo("Selección", "Selecciona una cámara para ver.")
            return
        
        camara = camaras_guardadas[seleccion[0]]
        abrir_visor_camara(camara['url'], f"Cámara Remota: {camara['nombre']}")
    
    def generar_acceso_remoto():
        """Generar configuraciones para acceso remoto"""
        seleccion = listbox_guardadas.curselection()
        if not seleccion:
            messagebox.showinfo("Selección", "Selecciona una cámara.")
            return
        
        camara = camaras_guardadas[seleccion[0]]
        
        # Ventana para configuración remota
        ventana_remoto = tk.Toplevel(ventana_gestion)
        ventana_remoto.title("Configuración de Acceso Remoto")
        ventana_remoto.geometry("700x500")
        ventana_remoto.configure(bg=COLOR_FONDO)
        
        tk.Label(ventana_remoto, text="🌐 CONFIGURACIÓN DE ACCESO REMOTO", 
                font=("Consolas", 16, "bold"), fg=COLOR_TEXTO, bg=COLOR_FONDO).pack(pady=10)
        
        tk.Label(ventana_remoto, text=f"Cámara: {camara['nombre']}", 
                font=FUENTE_CONSOLA, fg=COLOR_TEXTO, bg=COLOR_FONDO).pack(pady=5)
        
        text_config = scrolledtext.ScrolledText(ventana_remoto, bg="#1a1a1a", 
                                               fg=COLOR_TEXTO, font=FUENTE_CONSOLA)
        text_config.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Generar configuraciones
        url_parts = camara['url'].replace('rtsp://', '').replace('http://', '')
        if '@' in url_parts:
            creds, ip_puerto = url_parts.split('@')
            usuario, password = creds.split(':') if ':' in creds else ('', '')
            ip_puerto_parts = ip_puerto.split(':')
            ip = ip_puerto_parts[0]
            puerto = ip_puerto_parts[1].split('/')[0] if len(ip_puerto_parts) > 1 else '554'
        else:
            usuario, password = '', ''
            ip = url_parts.split(':')[0]
            puerto = '554'
        
        manager = CameraManager()
        urls_remotas = manager.generar_url_remota(ip, puerto, usuario, password)
        
        config_text = f"""CONFIGURACIÓN DE ACCESO REMOTO
{'='*50}

Cámara: {camara['nombre']}
IP Local: {camara['ip_local']}
URL Local: {camara['url']}

MÉTODOS DE ACCESO REMOTO:
{'='*50}

"""
        
        for i, metodo in enumerate(urls_remotas, 1):
            config_text += f"{i}. {metodo['tipo']}:\n"
            config_text += f"   URL: {metodo['url']}\n"
            config_text += f"   Descripción: {metodo['descripcion']}\n"
            config_text += f"   Nota: {metodo['nota']}\n\n"
        
        config_text += """INSTRUCCIONES DETALLADAS:
{'='*50}

🔧 METHOD 1: PORT FORWARDING
1. Accede a la configuración de tu router (192.168.1.1)
2. Busca "Port Forwarding" o "Virtual Servers"
3. Configura una regla:
   - Puerto externo: [puerto de tu elección]
   - IP interna: {ip_local}
   - Puerto interno: {puerto}
4. Guarda la configuración
5. Usa tu IP pública + puerto externo para acceso

🔧 METHOD 2: VPN
1. Configura OpenVPN o WireGuard en tu router
2. Instala cliente VPN en dispositivo remoto
3. Conéctate a la VPN
4. Usa la URL local normalmente

🔧 METHOD 3: NGROK TUNNEL
1. Instala ngrok: https://ngrok.com/
2. Ejecuta: ngrok tcp {puerto}
3. Usa la URL proporcionada por ngrok
4. Nota: Solo para pruebas, no permanente

⚠️  CONSIDERACIONES DE SEGURIDAD:
- Cambia credenciales por defecto
- Usa HTTPS/SSL cuando sea posible
- Configura firewall adecuadamente
- Monitorea accesos no autorizados
- Solo para dispositivos propios

📝 TUTORIAL PARA ROUTER:
1. Abre navegador web
2. Ve a 192.168.1.1 (o IP de tu router)
3. Ingresa usuario/contraseña del router
4. Busca sección "Advanced" > "Port Forwarding"
5. Añade nueva regla con los datos indicados

""".format(ip_local=camara['ip_local'], puerto=puerto)
        
        text_config.insert(1.0, config_text)
        
        def exportar_config():
            archivo = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt")]
            )
            if archivo:
                with open(archivo, 'w') as f:
                    f.write(config_text)
                messagebox.showinfo("Exportar", f"Configuración guardada en:\n{archivo}")
        
        ttk.Button(ventana_remoto, text="Exportar Configuración", 
                  command=exportar_config).pack(pady=10)
    
    def eliminar_camara():
        """Eliminar cámara seleccionada"""
        seleccion = listbox_guardadas.curselection()
        if not seleccion:
            messagebox.showinfo("Selección", "Selecciona una cámara para eliminar.")
            return
        
        camara = camaras_guardadas[seleccion[0]]
        if messagebox.askyesno("Confirmar", 
                              f"¿Eliminar la cámara '{camara['nombre']}'?"):
            del camaras_guardadas[seleccion[0]]
            CameraManager().guardar_camaras()
            actualizar_lista()
            text_info.delete(1.0, tk.END)
    
    # Eventos
    listbox_guardadas.bind('<<ListboxSelect>>', mostrar_info_camara)
    
    # Botones
    frame_botones = tk.Frame(frame_lista, bg=COLOR_FONDO)
    frame_botones.pack(fill=tk.X, pady=10)
    
    ttk.Button(frame_botones, text="Verificar Acceso", 
              command=verificar_camara).pack(side=tk.LEFT, padx=2)
    ttk.Button(frame_botones, text="Ver Cámara", 
              command=ver_camara_remota).pack(side=tk.LEFT, padx=2)
    ttk.Button(frame_botones, text="Config. Remota", 
              command=generar_acceso_remoto).pack(side=tk.LEFT, padx=2)
    ttk.Button(frame_botones, text="Eliminar", 
              command=eliminar_camara).pack(side=tk.LEFT, padx=2)
    
    # Cargar lista inicial
    actualizar_lista()

def guardar_camara_detectada():
    """Guardar una cámara detectada para acceso remoto"""
    idx = listbox_camaras.curselection()
    if not idx:
        messagebox.showinfo("Selecciona una cámara", 
                           "Debes seleccionar una cámara de la lista.")
        return
    
    camara_info = camaras_validas[idx[0]]
    
    # Ventana para guardar cámara
    ventana_guardar = tk.Toplevel()
    ventana_guardar.title("Guardar Cámara para Acceso Remoto")
    ventana_guardar.geometry("500x350")
    ventana_guardar.configure(bg=COLOR_FONDO)
    
    tk.Label(ventana_guardar, text="💾 GUARDAR CÁMARA", 
             font=("Consolas", 16, "bold"), fg=COLOR_TEXTO, bg=COLOR_FONDO).pack(pady=10)
    
    frame_form = tk.Frame(ventana_guardar, bg=COLOR_FONDO)
    frame_form.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
    
    # Formulario
    tk.Label(frame_form, text="Nombre de la cámara:", fg=COLOR_TEXTO, 
             bg=COLOR_FONDO, font=FUENTE_CONSOLA).grid(row=0, column=0, sticky='w', pady=5)
    entry_nombre = tk.Entry(frame_form, font=FUENTE_CONSOLA, bg="#1a1a1a", 
                           fg=COLOR_TEXTO, width=30)
    entry_nombre.grid(row=0, column=1, pady=5, padx=10)
    entry_nombre.insert(0, f"Cámara_{camara_info['ip']}")
    
    tk.Label(frame_form, text="URL:", fg=COLOR_TEXTO, 
             bg=COLOR_FONDO, font=FUENTE_CONSOLA).grid(row=1, column=0, sticky='w', pady=5)
    entry_url = tk.Entry(frame_form, font=FUENTE_CONSOLA, bg="#1a1a1a", 
                        fg=COLOR_TEXTO, width=30)
    entry_url.grid(row=1, column=1, pady=5, padx=10)
    entry_url.insert(0, camara_info['url'])
    
    tk.Label(frame_form, text="IP Local:", fg=COLOR_TEXTO, 
             bg=COLOR_FONDO, font=FUENTE_CONSOLA).grid(row=2, column=0, sticky='w', pady=5)
    entry_ip = tk.Entry(frame_form, font=FUENTE_CONSOLA, bg="#1a1a1a", 
                       fg=COLOR_TEXTO, width=30)
    entry_ip.grid(row=2, column=1, pady=5, padx=10)
    entry_ip.insert(0, camara_info['ip'])
    
    tk.Label(frame_form, text="Descripción:", fg=COLOR_TEXTO, 
             bg=COLOR_FONDO, font=FUENTE_CONSOLA).grid(row=3, column=0, sticky='w', pady=5)
    entry_desc = tk.Text(frame_form, font=FUENTE_CONSOLA, bg="#1a1a1a", 
                        fg=COLOR_TEXTO, width=30, height=3)
    entry_desc.grid(row=3, column=1, pady=5, padx=10)
    
    # Información adicional
    info_text = f"""Esta cámara será guardada para acceso futuro.
    
Podrás configurar acceso remoto usando:
- Port Forwarding en tu router
- VPN para acceso seguro
- Servicios de túnel (ngrok, etc.)

Una vez guardada, podrás acceder desde
cualquier lugar con la configuración adecuada."""
    
    tk.Label(frame_form, text=info_text, fg=COLOR_TEXTO, bg=COLOR_FONDO, 
             font=("Consolas", 9), justify=tk.LEFT, wraplength=400).grid(
             row=4, column=0, columnspan=2, pady=10)
    
    def guardar():
        manager = CameraManager()
        if manager.agregar_camara(
            nombre=entry_nombre.get(),
            url=entry_url.get(),
            ip_local=entry_ip.get(),
            descripcion=entry_desc.get("1.0", tk.END).strip()
        ):
            messagebox.showinfo("Guardado", 
                               f"Cámara '{entry_nombre.get()}' guardada correctamente.\n\n"
                               "Ahora puedes configurar acceso remoto desde el menú "
                               "'Gestión de Cámaras'.")
            ventana_guardar.destroy()
        else:
            messagebox.showerror("Error", "No se pudo guardar la cámara.")
    
    frame_botones = tk.Frame(frame_form, bg=COLOR_FONDO)
    frame_botones.grid(row=5, column=0, columnspan=2, pady=20)
    
    ttk.Button(frame_botones, text="Guardar", command=guardar).pack(side=tk.LEFT, padx=5)
    ttk.Button(frame_botones, text="Cancelar", 
              command=ventana_guardar.destroy).pack(side=tk.LEFT, padx=5)

def abrir_visor_camara(url, titulo="ShadowCam - Visor"):
    """Función mejorada para abrir el visor de cámara"""
    win = tk.Toplevel(app)
    win.title(titulo)
    win.geometry("660x520")
    win.configure(bg=COLOR_FONDO)
    
    # Barra superior con información
    frame_info = tk.Frame(win, bg="#1a1a1a")
    frame_info.pack(fill=tk.X, padx=10, pady=5)
    
    tk.Label(frame_info, text="🎥 CÁMARA EN VIVO", font=("Consolas", 16, "bold"), 
             fg=COLOR_TEXTO, bg="#1a1a1a").pack(pady=5)
    tk.Label(frame_info, text=url, font=("Consolas", 10), fg=COLOR_TEXTO, bg="#1a1a1a").pack()
    
    # Estado de conexión
    label_estado = tk.Label(frame_info, text="Estado: Conectando...", 
                           font=("Consolas", 10), fg="yellow", bg="#1a1a1a")
    label_estado.pack()
    
    # Contenedor para el video
    frame_video = tk.Frame(win, bg="#1a1a1a", padx=10, pady=10)
    frame_video.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    # Crear visor con manejo de errores mejorado
    class CamViewer:
        def __init__(self, parent, url, label_estado):
            self.parent = parent
            self.url = url
            self.label_estado = label_estado
            self.cap = cv2.VideoCapture(self.url)
            self.label = tk.Label(parent)
            self.label.pack(fill=tk.BOTH, expand=True)
            self.running = True
            self.connection_attempts = 0
            self.max_attempts = 3
            self.update_frame()

        def update_frame(self):
            if not self.running:
                return
            
            ret, frame = self.cap.read()
            if ret:
                # Conexión exitosa
                self.label_estado.config(text="Estado: ✅ Conectado", fg="green")
                self.connection_attempts = 0
                
                # Procesar frame
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.resize(frame, (640, 480))
                img = Image.fromarray(frame)
                imgtk = ImageTk.PhotoImage(image=img)
                self.label.imgtk = imgtk
                self.label.configure(image=imgtk)
                
                self.parent.after(30, self.update_frame)
            else:
                # Error de conexión
                self.connection_attempts += 1
                if self.connection_attempts < self.max_attempts:
                    self.label_estado.config(
                        text=f"Estado: 🔄 Reintentando... ({self.connection_attempts}/{self.max_attempts})", 
                        fg="yellow")
                    self.cap.release()
                    self.cap = cv2.VideoCapture(self.url)
                    self.parent.after(1000, self.update_frame)  # Reintentar en 1 segundo
                else:
                    self.label_estado.config(text="Estado: ❌ Sin conexión", fg="red")
                    # Mostrar mensaje de error
                    self.label.config(text="❌ No se puede conectar a la cámara\n\n"
                                           "Posibles causas:\n"
                                           "• La cámara está offline\n"
                                      "• Credenciales incorrectas\n"
                                           "• La cámara cambió de IP\n"
                                           "• Problemas de red", 
                                     font=("Consolas", 12), fg=COLOR_TEXTO, 
                                     bg="#1a1a1a", justify=tk.CENTER)

        def stop(self):
            self.running = False
            if self.cap:
                self.cap.release()

    viewer = CamViewer(frame_video, url, label_estado)
    
    # Botones de control
    frame_controles = tk.Frame(win, bg=COLOR_FONDO)
    frame_controles.pack(fill=tk.X, padx=10, pady=5)
    
    def take_screenshot():
        if viewer.cap and viewer.cap.isOpened():
            ret, frame = viewer.cap.read()
            if ret:
                filename = f"screenshot_{int(time.time())}.jpg"
                cv2.imwrite(filename, frame)
                messagebox.showinfo("Screenshot", f"Captura guardada como: {filename}")
    
    def reconnect():
        viewer.connection_attempts = 0
        viewer.cap.release()
        viewer.cap = cv2.VideoCapture(viewer.url)
        viewer.label_estado.config(text="Estado: 🔄 Reconectando...", fg="yellow")
    
    ttk.Button(frame_controles, text="📷 Captura", command=take_screenshot).pack(side=tk.LEFT, padx=5)
    ttk.Button(frame_controles, text="🔄 Reconectar", command=reconnect).pack(side=tk.LEFT, padx=5)
    ttk.Button(frame_controles, text="❌ Cerrar", 
              command=lambda: (viewer.stop(), win.destroy())).pack(side=tk.RIGHT, padx=5)
    
    win.protocol("WM_DELETE_WINDOW", lambda: (viewer.stop(), win.destroy()))

# ---------------------- CREDITS BANNER ----------------------
def mostrar_creditos():
    ventana_creditos = tk.Toplevel()
    ventana_creditos.title("Acerca de ShadowCam")
    ventana_creditos.geometry("500x300")
    ventana_creditos.configure(bg=COLOR_FONDO)
    ventana_creditos.resizable(False, False)
    
    # Borde con efecto "hacker"
    frame_borde = tk.Frame(ventana_creditos, bg=COLOR_TEXTO, padx=2, pady=2)
    frame_borde.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)
    
    frame_interior = tk.Frame(frame_borde, bg=COLOR_FONDO)
    frame_interior.pack(fill=tk.BOTH, expand=True)
    
    # Logo estilizado
    tk.Label(frame_interior, text="⚡ SHADOWCAM ⚡", 
             font=("Consolas", 24, "bold"), fg=COLOR_TEXTO, bg=COLOR_FONDO).pack(pady=10)
    
    # Texto de créditos
    creditos_texto = """
 ---------------------- ShadowCam ---------------------- 
Software para visualización de cámaras IP 
Hacking Ético Desarrollado por AndresDev. 
© 2024 - Todos los derechos reservados 
web: https://andresgonzalezdev444.github.io/
----------------------------------------------------------
VERSIÓN 2.1 - Sistema Mejorado con Acceso Remoto
----------------------------------------------------------
"""
    
    tk.Label(frame_interior, text=creditos_texto, 
             font=("Consolas", 11), fg=COLOR_TEXTO, bg=COLOR_FONDO, 
             justify=tk.LEFT).pack(pady=5)
    
    # Botón que abre el sitio web
    def abrir_web():
        webbrowser.open("https://andresgonzalezdev444.github.io/")
    
    ttk.Button(frame_interior, text="Visitar sitio web", command=abrir_web).pack(pady=10)
    ttk.Button(frame_interior, text="Cerrar", command=ventana_creditos.destroy).pack(pady=5)

# ---------------------- LOGIN ----------------------
def interfaz_login():
    login = tk.Tk()
    login.title("ShadowCam - Login")
    login.geometry("500x350")
    login.configure(bg=COLOR_FONDO)
    login.resizable(False, False)

    tk.Label(login, text="🕵️ SHADOWCAM", font=("Consolas", 22, "bold"), fg=COLOR_TEXTO, bg=COLOR_FONDO).pack(pady=10)
    tk.Label(login, text="Enhanced Ethical Camera Detection & Remote Access System v2.1", font=("Consolas", 9), fg=COLOR_TEXTO, bg=COLOR_FONDO).pack()

    # Añadir texto de créditos en la pantalla de login
    creditos = tk.Label(login, text=" ---------------------- ShadowCam ---------------------- \nDesarrollado por AndresDev. © 2024", 
                        font=("Consolas", 8), fg=COLOR_TEXTO, bg=COLOR_FONDO)
    creditos.pack(pady=5)

    frame_login = tk.Frame(login, bg=COLOR_FONDO)
    frame_login.pack(pady=30)

    tk.Label(frame_login, text="Usuario:", fg=COLOR_TEXTO, bg=COLOR_FONDO, font=FUENTE_CONSOLA).grid(row=0, column=0, sticky='e', padx=5, pady=5)
    entrada_usuario = tk.Entry(frame_login, font=FUENTE_CONSOLA, bg="#1a1a1a", fg=COLOR_TEXTO, insertbackground=COLOR_TEXTO)
    entrada_usuario.grid(row=0, column=1, padx=5)

    tk.Label(frame_login, text="Contraseña:", fg=COLOR_TEXTO, bg=COLOR_FONDO, font=FUENTE_CONSOLA).grid(row=1, column=0, sticky='e', padx=5, pady=5)
    entrada_clave = tk.Entry(frame_login, show="*", font=FUENTE_CONSOLA, bg="#1a1a1a", fg=COLOR_TEXTO, insertbackground=COLOR_TEXTO)
    entrada_clave.grid(row=1, column=1, padx=5)

    def verificar_login():
        if entrada_usuario.get() == "andresdev" and entrada_clave.get() == "andresdev":
            login.destroy()
            abrir_app()
        else:
            messagebox.showerror("Acceso denegado", "Usuario o contraseña incorrectos.")

    ttk.Style().configure("TButton", foreground="black", background="white")
    btn_login = ttk.Button(login, text="Iniciar sesión", command=verificar_login)
    btn_login.pack(pady=10)
    
    # Añadir enlace a la web
    def abrir_web():
        webbrowser.open("https://andresgonzalezdev444.github.io/")
    
    link = tk.Label(login, text="https://andresgonzalezdev444.github.io/", 
                    fg="#00aaff", bg=COLOR_FONDO, cursor="hand2", font=("Consolas", 9, "underline"))
    link.pack(side=tk.BOTTOM, pady=10)
    link.bind("<Button-1>", lambda e: abrir_web())

    login.mainloop()

# ---------------------- FUNCIONES RED ----------------------
def obtener_interfaces():
    interfaces = []
    for nombre, info in psutil.net_if_addrs().items():
        for i in info:
            if i.family == socket.AF_INET and not i.address.startswith("127."):
                interfaces.append({"nombre": nombre, "ip": i.address, "mascara": i.netmask})
    return interfaces

def calcular_red(ip):
    return str(ipaddress.ip_network(ip + "/24", strict=False))

def escanear_red(rango_red):
    paquete = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=rango_red)
    resultado = srp(paquete, timeout=2, verbose=False)[0]
    dispositivos = []
    for enviado, recibido in resultado:
        dispositivos.append({'ip': recibido.psrc, 'mac': recibido.hwsrc})
    return dispositivos

def escanear_puertos(ip, puertos=CAM_PORTS):
    abiertos = []
    for puerto in puertos:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.5)
            resultado = s.connect_ex((ip, puerto))
            if resultado == 0:
                abiertos.append(puerto)
            s.close()
        except:
            continue
    return abiertos

def escaneo_avanzado(ip):
    nm = nmap.PortScanner()
    try:
        nm.scan(ip, arguments='-sS -p 80,554,8080,8888 --open')
        info = {}
        if ip in nm.all_hosts():
            info['puertos_abiertos'] = []
            for puerto in nm[ip]['tcp']:
                if nm[ip]['tcp'][puerto]['state'] == 'open':
                    info['puertos_abiertos'].append(puerto)
            info['servicios'] = [nm[ip]['tcp'][p]['name'] for p in info['puertos_abiertos']]
            return info
        else:
            return {'puertos_abiertos': [], 'servicios': []}
    except:
        return {'puertos_abiertos': [], 'servicios': []}

# ---------------------- FUNCIONES CÁMARAS ----------------------
def construir_urls(ip, puertos):
    urls = []
    for puerto in puertos:
        for user, pwd in DEFAULT_CREDS:
            if user and pwd:
                urls.append(f"rtsp://{user}:{pwd}@{ip}:{puerto}/")
                urls.append(f"http://{user}:{pwd}@{ip}:{puerto}/video")
            else:
                urls.append(f"rtsp://{ip}:{puerto}/")
                urls.append(f"http://{ip}:{puerto}/video")
    return urls

def probar_stream(url, texto_resultados=None):
    if texto_resultados:
        texto_resultados.insert(tk.END, f"Probando: {url}\n")
        texto_resultados.see(tk.END)
        texto_resultados.update()
    
    cap = cv2.VideoCapture(url)
    if cap.isOpened():
        ret, frame = cap.read()
        cap.release()
        return ret
    return False

# ---------------------- FUNCIONES INTERFAZ ----------------------
def iniciar_escaneo():
    global resultados, camaras_validas
    seleccion = combo.current()
    if seleccion == -1:
        messagebox.showerror("Error", "Selecciona una interfaz de red.")
        return

    btn_escanear.config(state=tk.DISABLED)
    btn_exportar_csv.config(state=tk.DISABLED)
    btn_exportar_pdf.config(state=tk.DISABLED)
    btn_dashboard.config(state=tk.DISABLED)
    btn_ver_camara.config(state=tk.DISABLED)
    btn_guardar_camara.config(state=tk.DISABLED)
    texto_resultados.delete(1.0, tk.END)
    listbox_camaras.delete(0, tk.END)
    camaras_validas = []

    interfaz = interfaces[seleccion]
    red = calcular_red(interfaz["ip"])
    texto_resultados.insert(tk.END, f"🔍 Escaneando red: {red}\n")
    texto_resultados.update()

    resultados = []

    def tarea_escaneo():
        try:
            dispositivos = escanear_red(red)
            texto_resultados.insert(tk.END, f"[+] Dispositivos encontrados: {len(dispositivos)}\n\n")
            texto_resultados.update()

            for d in dispositivos:
                if var_avanzado.get():
                    info_nmap = escaneo_avanzado(d['ip'])
                    puertos = info_nmap.get('puertos_abiertos', [])
                else:
                    puertos = escanear_puertos(d['ip'])

                d['puertos_abiertos'] = puertos

                try:
                    fabricante = MacLookup().lookup(d['mac'])
                except:
                    fabricante = "Desconocido"

                d['fabricante'] = fabricante
                d['posible_camara'] = any(p in puertos for p in CAM_PORTS)

                linea = f"IP: {d['ip']}\tMAC: {d['mac']}\tFabricante: {fabricante}\tPuertos abiertos: {puertos}"
                if d['posible_camara']:
                    linea += "   📽 POSIBLE CÁMARA DETECTADA"
                    
                    # Probar conexión a las cámaras
                    urls = construir_urls(d['ip'], [p for p in puertos if p in CAM_PORTS])
                    for url in urls:
                        texto_resultados.insert(tk.END, f"\nProbando acceso a cámara: {url}\n")
                        texto_resultados.see(tk.END)
                        texto_resultados.update()
                        
                        if probar_stream(url, texto_resultados):
                            texto_resultados.insert(tk.END, f"✅ Cámara accesible en: {url}\n")
                            texto_resultados.see(tk.END)
                            texto_resultados.update()
                            
                            d['url_camara'] = url
                            camaras_validas.append({'ip': d['ip'], 'url': url})
                            listbox_camaras.insert(tk.END, f"{d['ip']} -> {url}")
                            break

                texto_resultados.insert(tk.END, linea + "\n")
                texto_resultados.see(tk.END)
                texto_resultados.update()

                resultados.append(d)
        finally:
            btn_escanear.config(state=tk.NORMAL)
            btn_exportar_csv.config(state=tk.NORMAL)
            btn_exportar_pdf.config(state=tk.NORMAL)
            btn_dashboard.config(state=tk.NORMAL)
            if camaras_validas:
                btn_ver_camara.config(state=tk.NORMAL)
                btn_guardar_camara.config(state=tk.NORMAL)

    hilo = threading.Thread(target=tarea_escaneo)
    hilo.start()

def ver_camara_seleccionada():
    idx = listbox_camaras.curselection()
    if not idx:
        messagebox.showinfo("Selecciona una cámara", "Debes seleccionar una cámara de la lista.")
        return
    
    url = camaras_validas[idx[0]]['url']
    abrir_visor_camara(url, f"ShadowCam - Visor de cámara: {url}")

def abrir_app():
    global app, combo, interfaces, btn_escanear, texto_resultados
    global btn_exportar_csv, btn_exportar_pdf, btn_dashboard, btn_ver_camara
    global var_avanzado, listbox_camaras, camaras_validas, btn_guardar_camara

    app = tk.Tk()
    app.title("ShadowCam - Enhanced Ethical Camera Detection & Remote Access System")
    app.geometry("1000x750")
    app.configure(bg=COLOR_FONDO)

    tk.Label(app, text="🕵️ SHADOWCAM", font=("Consolas", 22, "bold"), fg=COLOR_TEXTO, bg=COLOR_FONDO).pack(pady=5)
    tk.Label(app, text="Enhanced Ethical Camera Detection & Remote Access System v2.1", font=("Consolas", 10), fg=COLOR_TEXTO, bg=COLOR_FONDO).pack(pady=2)

    # Frame para el selector de interfaz y escaneo
    frame_opciones = tk.Frame(app, bg=COLOR_FONDO)
    frame_opciones.pack(fill=tk.X, padx=10, pady=5)
    
    tk.Label(frame_opciones, text="Selecciona la interfaz de red:", fg=COLOR_TEXTO, bg=COLOR_FONDO, font=FUENTE_CONSOLA).grid(row=0, column=0, padx=5, pady=5)

    interfaces = obtener_interfaces()
    nombres = [f"{i['nombre']} - {i['ip']}" for i in interfaces]

    combo = ttk.Combobox(frame_opciones, values=nombres, width=50)
    combo.grid(row=0, column=1, padx=5, pady=5)

    var_avanzado = tk.BooleanVar()
    chk_nmap = ttk.Checkbutton(frame_opciones, text="Escaneo avanzado (nmap)", variable=var_avanzado)
    chk_nmap.grid(row=0, column=2, padx=5, pady=5)

    btn_escanear = ttk.Button(frame_opciones, text="Iniciar escaneo", command=iniciar_escaneo)
    btn_escanear.grid(row=0, column=3, padx=5, pady=5)

    # Frame para los resultados y cámaras encontradas
    frame_contenido = tk.Frame(app, bg=COLOR_FONDO)
    frame_contenido.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
    
    # Panel de resultados
    frame_resultados = tk.Frame(frame_contenido, bg=COLOR_FONDO)
    frame_resultados.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    tk.Label(frame_resultados, text="Resultados del escaneo:", fg=COLOR_TEXTO, bg=COLOR_FONDO, font=FUENTE_CONSOLA).pack(anchor='w')
    texto_resultados = scrolledtext.ScrolledText(frame_resultados, height=25, width=80, bg="#1a1a1a", fg=COLOR_TEXTO, font=FUENTE_CONSOLA, insertbackground=COLOR_TEXTO)
    texto_resultados.pack(fill=tk.BOTH, expand=True, pady=5)
    
    # Panel de cámaras
    frame_camaras = tk.Frame(frame_contenido, bg=COLOR_FONDO)
    frame_camaras.pack(side=tk.RIGHT, fill=tk.Y, padx=10)
    
    tk.Label(frame_camaras, text="Cámaras detectadas:", fg=COLOR_TEXTO, bg=COLOR_FONDO, font=FUENTE_CONSOLA).pack(anchor='w')
    listbox_camaras = tk.Listbox(frame_camaras, height=15, width=40, bg="#1a1a1a", fg=COLOR_TEXTO, font=FUENTE_CONSOLA)
    listbox_camaras.pack(fill=tk.BOTH, expand=True, pady=5)
    
    btn_ver_camara = ttk.Button(frame_camaras, text="Ver cámara seleccionada", command=ver_camara_seleccionada, state=tk.DISABLED)
    btn_ver_camara.pack(pady=2, fill=tk.X)
    
    btn_guardar_camara = ttk.Button(frame_camaras, text="💾 Guardar para acceso remoto", command=guardar_camara_detectada, state=tk.DISABLED)
    btn_guardar_camara.pack(pady=2, fill=tk.X)
    
    # Botones de acciones
    frame_botones = tk.Frame(app, bg=COLOR_FONDO)
    frame_botones.pack(pady=10, padx=10, fill=tk.X)

    btn_exportar_csv = ttk.Button(frame_botones, text="Exportar a CSV", command=lambda: exportar_csv(), state=tk.DISABLED)
    btn_exportar_csv.pack(side=tk.LEFT, padx=5)

    btn_exportar_pdf = ttk.Button(frame_botones, text="Exportar a PDF", command=lambda: exportar_pdf(), state=tk.DISABLED)
    btn_exportar_pdf.pack(side=tk.LEFT, padx=5)

    btn_dashboard = ttk.Button(frame_botones, text="Mostrar Dashboard", command=lambda: mostrar_dashboard(), state=tk.DISABLED)
    btn_dashboard.pack(side=tk.LEFT, padx=5)
    
    # Nueva funcionalidad: Botón para gestión de cámaras
    btn_gestion = ttk.Button(frame_botones, text="🎥 Gestión de Cámaras", command=lambda: mostrar_gestion_camaras())
    btn_gestion.pack(side=tk.LEFT, padx=5)
    
    # Añadir botón de créditos
    btn_creditos = ttk.Button(frame_botones, text="Acerca de", command=lambda: mostrar_creditos())
    btn_creditos.pack(side=tk.RIGHT, padx=5)
    
    camaras_validas = []
    
    # Añadir barra de estado con créditos
    frame_estado = tk.Frame(app, bg="#101010", height=20)
    frame_estado.pack(side=tk.BOTTOM, fill=tk.X)
    
    tk.Label(frame_estado, text="© 2024 AndresDev - https://andresgonzalezdev444.github.io/ - ShadowCam v2.1", 
             font=("Consolas", 8), fg=COLOR_TEXTO, bg="#101010").pack(side=tk.RIGHT, padx=10)
    
    # Inicializar gestor de cámaras
    CameraManager()
    
    app.mainloop()

# ---------------------- EXPORTACIONES ----------------------
def exportar_csv():
    if not resultados:
        messagebox.showwarning("Advertencia", "No hay datos para exportar.")
        return
    archivo = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if archivo:
        df = pd.DataFrame(resultados)
        df.to_csv(archivo, index=False)
        messagebox.showinfo("Exportar CSV", f"Datos exportados a:\n{archivo}")
        
        # Añadir información de marca de agua con los créditos
        try:
            with open(archivo, 'a') as f:
                f.write("\n\n# ---------------------- ShadowCam ----------------------\n")
                f.write("# Enhanced Ethical Camera Detection & Remote Access System v2.1\n")
                f.write("# Hacking Ético Desarrollado por AndresDev.\n")
                f.write("# © 2024 - Todos los derechos reservados\n")
                f.write("# web: https://andresgonzalezdev444.github.io/\n")
                f.write("# ----------------------------------------------------------\n")
        except:
            pass

def exportar_pdf():
    if not resultados:
        messagebox.showwarning("Advertencia", "No hay datos para exportar.")
        return
    archivo = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
    if archivo:
        c = canvas.Canvas(archivo, pagesize=letter)
        ancho, alto = letter
        
        # Encabezado con logo y título
        c.setFont("Helvetica-Bold", 18)
        c.drawString(30, alto - 40, "ShadowCam v2.1 - Reporte de Análisis")
        c.setFont("Helvetica", 12)
        c.drawString(30, alto - 60, "Enhanced Ethical Camera Detection & Remote Access System")
        
        # Línea divisoria
        c.line(30, alto - 70, ancho - 30, alto - 70)
        
        # Datos del reporte
        c.setFont("Helvetica-Bold", 14)
        c.drawString(30, alto - 100, "Dispositivos escaneados:")
        
        c.setFont("Helvetica", 10)
        y = alto - 120
        for d in resultados:
            linea = f"IP: {d['ip']}  MAC: {d['mac']}  Fabricante: {d['fabricante']}  Puertos: {d['puertos_abiertos']}  Camara: {'Sí' if d['posible_camara'] else 'No'}"
            c.drawString(30, y, linea)
            y -= 15
            if y < 100:  # Asegurar espacio para el pie de página
                c.showPage()
                c.setFont("Helvetica", 10)
                y = alto - 40
        
        # Añadir pie de página con créditos
        c.setFont("Helvetica-Bold", 10)
        c.drawString(30, 60, "---------------------- ShadowCam v2.1 ----------------------")
        c.setFont("Helvetica", 9)
        c.drawString(30, 45, "Enhanced Ethical Camera Detection & Remote Access System")
        c.drawString(30, 35, "Hacking Ético Desarrollado por AndresDev.")
        c.drawString(30, 25, "© 2024 - Todos los derechos reservados")
        c.drawString(30, 15, "web: https://andresgonzalezdev444.github.io/")
        
        c.save()
        messagebox.showinfo("Exportar PDF", f"Datos exportados a:\n{archivo}")

# ---------------------- DASHBOARD ----------------------
def mostrar_dashboard():
    if not resultados:
        messagebox.showwarning("Advertencia", "No hay datos para mostrar.")
        return
    df = pd.DataFrame(resultados)
    conteo_fabricantes = df['fabricante'].value_counts()
    camaras_por_fabricante = df[df['posible_camara'] == True]['fabricante'].value_counts()

    ventana_graf = tk.Toplevel()
    ventana_graf.title("Dashboard - ShadowCam v2.1")
    ventana_graf.geometry("800x650")
    ventana_graf.configure(bg=COLOR_FONDO)

    tk.Label(ventana_graf, text="Dashboard ShadowCam v2.1", font=("Consolas", 16, "bold"), 
             fg=COLOR_TEXTO, bg=COLOR_FONDO).pack(pady=10)

    frame_graficos = tk.Frame(ventana_graf, bg=COLOR_FONDO)
    frame_graficos.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    # Gráfico de todos los dispositivos
    fig1 = plt.Figure(figsize=(5, 4), facecolor=COLOR_FONDO)
    ax1 = fig1.add_subplot(111)
    conteo_fabricantes.plot(kind='bar', ax=ax1, color='green')
    ax1.set_title('Dispositivos por Fabricante', color=COLOR_TEXTO)
    ax1.set_ylabel('Cantidad', color=COLOR_TEXTO)
    ax1.set_xlabel('Fabricante', color=COLOR_TEXTO)
    ax1.tick_params(axis='x', colors=COLOR_TEXTO, rotation=45)
    ax1.tick_params(axis='y', colors=COLOR_TEXTO)
    fig1.tight_layout()

    # Gráfico de cámaras detectadas
    fig2 = plt.Figure(figsize=(5, 4), facecolor=COLOR_FONDO)
    ax2 = fig2.add_subplot(111)
    if not camaras_por_fabricante.empty:
        camaras_por_fabricante.plot(kind='pie', ax=ax2, autopct='%1.1f%%', startangle=90, colors=['green', 'lime', 'darkgreen', 'lightgreen'])
        ax2.set_title('Cámaras por Fabricante', color=COLOR_TEXTO)
    else:
        ax2.text(0.5, 0.5, 'No se detectaron cámaras', ha='center', va='center', transform=ax2.transAxes, color=COLOR_TEXTO)
        ax2.set_title('Cámaras por Fabricante', color=COLOR_TEXTO)
    ax2.tick_params(axis='x', colors=COLOR_TEXTO)
    fig2.tight_layout()

    # Añadir gráficos a la ventana
    canvas1 = FigureCanvasTkAgg(fig1, master=frame_graficos)
    canvas1.draw()
    canvas1.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    canvas2 = FigureCanvasTkAgg(fig2, master=frame_graficos)
    canvas2.draw()
    canvas2.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
    
    # Añadir estadísticas
    frame_stats = tk.Frame(ventana_graf, bg="#101010")
    frame_stats.pack(side=tk.BOTTOM, fill=tk.X, pady=5)
    
    total_dispositivos = len(resultados)
    total_camaras = len([d for d in resultados if d.get('posible_camara', False)])
    camaras_accesibles = len(camaras_validas)
    camaras_guardadas_count = len(camaras_guardadas)
    
    stats_text = f"Dispositivos: {total_dispositivos} | Cámaras detectadas: {total_camaras} | Accesibles: {camaras_accesibles} | Guardadas: {camaras_guardadas_count}"
    tk.Label(frame_stats, text=stats_text, font=("Consolas", 10), fg=COLOR_TEXTO, bg="#101010").pack(pady=5)
    
    # Añadir panel de créditos en la parte inferior
    frame_creditos = tk.Frame(ventana_graf, bg="#101010", height=80)
    frame_creditos.pack(side=tk.BOTTOM, fill=tk.X)
    
    texto_creditos = """
 ---------------------- ShadowCam ---------------------- 
Software para visualización de cámaras IP 
Hacking Ético Desarrollado por AndresDev. 
© 2024 - Todos los derechos reservados 
web: https://andresgonzalezdev444.github.io/
----------------------------------------------------------
"""
    
    creditos_label = tk.Label(frame_creditos, text=texto_creditos, 
                         font=("Consolas", 9), fg=COLOR_TEXTO, bg="#101010",
                         justify=tk.LEFT)
    creditos_label.pack(pady=5)

# ---------------------- INICIAR APP ----------------------
if __name__ == "__main__":
    interfaz_login()

