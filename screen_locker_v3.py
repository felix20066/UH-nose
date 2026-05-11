"""
╔══════════════════════════════════════════════════════════════╗
║         SCREEN LOCKER EDUCATIVO  v3.0  —  Windows            ║
║  Auto-instala dependencias · Multi-monitor · Anti-evasión    ║
╚══════════════════════════════════════════════════════════════╝
  Ejecutar COMO ADMINISTRADOR para máxima seguridad.
  python screen_locker.py  /  doble clic en screen_locker.pyw
"""

# ═══════════════════════════════════════════════════════════════
#  SECCIÓN 0 — BOOTSTRAP: auto-instalar dependencias
# ═══════════════════════════════════════════════════════════════
import sys, os, subprocess, threading, time, json, ctypes

REQUIRED = {"keyboard": "keyboard", "psutil": "psutil"}

def _check_admin():
    """Devuelve True si el proceso corre como Administrador."""
    try:
        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except Exception:
        return False

def _elevar():
    """Relanza el script con privilegios de Administrador."""
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable,
        " ".join([f'"{a}"' for a in sys.argv]), None, 1
    )
    sys.exit(0)

def _instalar_paquetes(faltantes, splash=None, lbl=None):
    for pkg in faltantes:
        if lbl:
            lbl.config(text=f"📦  Instalando {pkg}…")
            if splash: splash.update()
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", pkg,
             "--quiet", "--disable-pip-version-check"],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )

def _bootstrap():
    """Comprueba e instala lo que falte. Si hay algo que instalar,
    muestra una mini-ventana de progreso y reinicia el proceso."""
    faltantes = []
    for mod, pkg in REQUIRED.items():
        try:
            __import__(mod)
        except ImportError:
            faltantes.append(pkg)

    if not faltantes:
        return   # Todo listo, continúa normalmente

    # Mostrar splash de instalación
    import tkinter as tk
    splash = tk.Tk()
    splash.title("Iniciando Screen Locker…")
    splash.configure(bg="#0a1628")
    splash.resizable(False, False)
    splash.attributes("-topmost", True)
    w, h = 380, 160
    sx = splash.winfo_screenwidth()  // 2 - w // 2
    sy = splash.winfo_screenheight() // 2 - h // 2
    splash.geometry(f"{w}x{h}+{sx}+{sy}")
    splash.overrideredirect(True)

    tk.Label(splash, text="🔒  Screen Locker Educativo",
             font=("Segoe UI", 13, "bold"),
             bg="#0a1628", fg="#e8f0fe").pack(pady=(22, 6))
    lbl = tk.Label(splash, text="Verificando dependencias…",
                   font=("Segoe UI", 10), bg="#0a1628", fg="#6d8fb5")
    lbl.pack(pady=4)
    bar_frame = tk.Frame(splash, bg="#1e4080", height=4, width=300)
    bar_frame.pack(pady=8)
    bar = tk.Frame(bar_frame, bg="#3b9eda", height=4, width=0)
    bar.place(x=0, y=0, height=4)
    splash.update()

    total = len(faltantes)
    for i, pkg in enumerate(faltantes):
        lbl.config(text=f"📦  Instalando {pkg}…")
        splash.update()
        subprocess.call(
            [sys.executable, "-m", "pip", "install", pkg,
             "--quiet", "--disable-pip-version-check"],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        bar.config(width=int(300 * (i + 1) / total))
        splash.update()

    lbl.config(text="✓  Listo. Iniciando…", fg="#4caf7d")
    bar.config(width=300)
    splash.update()
    splash.after(800, splash.destroy)
    splash.mainloop()

    # Reiniciar para que los imports funcionen
    os.execv(sys.executable, [sys.executable] + sys.argv)

_bootstrap()

# ═══════════════════════════════════════════════════════════════
#  SECCIÓN 1 — IMPORTS (ya garantizados)
# ═══════════════════════════════════════════════════════════════
import tkinter as tk
import keyboard
import psutil
import ctypes.wintypes

# ═══════════════════════════════════════════════════════════════
#  SECCIÓN 2 — CONFIGURACIÓN
# ═══════════════════════════════════════════════════════════════
CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "locker_config.json")

DEFAULTS = {
    "institucion" : "Institución Educativa",
    "subtitulo"   : "Entorno de aprendizaje controlado",
    "pin_alumno"  : "1234",
    "pin_admin"   : "9999",
    "max_intentos": 5,
    "bloqueo_seg" : 45,
    "mensaje"     : "¡Concéntrate · Aprende · Crece! 📚",
}

def cfg_load():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                DEFAULTS.update(json.load(f))
        except Exception:
            pass

def cfg_save():
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump({k: DEFAULTS[k] for k in
                   ("institucion","subtitulo","pin_alumno",
                    "pin_admin","mensaje","max_intentos","bloqueo_seg")},
                  f, indent=2, ensure_ascii=False)

# ═══════════════════════════════════════════════════════════════
#  SECCIÓN 3 — PALETA
# ═══════════════════════════════════════════════════════════════
C = {
    "bg"        : "#08111e",
    "panel"     : "#0c1c30",
    "card"      : "#0f2440",
    "card2"     : "#162e50",
    "border"    : "#1a3d6b",
    "border2"   : "#2455a0",
    "accent"    : "#2d8fd4",
    "accent_d"  : "#1a6fa8",
    "green"     : "#4caf7d",
    "red"       : "#e05252",
    "yellow"    : "#e8c44b",
    "text"      : "#e0eeff",
    "muted"     : "#5a7fa8",
    "muted2"    : "#2a4560",
    "key"       : "#0d1f38",
    "key_h"     : "#152d50",
    "key_a"     : "#0a1828",
    "enter"     : "#0a2d52",
    "enter_h"   : "#123e6e",
    "dot_empty" : "#1a3d6b",
    "dot_full"  : "#2d8fd4",
    "dot_err"   : "#e05252",
    "dot_ok"    : "#4caf7d",
}

DIAS  = ["Lunes","Martes","Miércoles","Jueves","Viernes","Sábado","Domingo"]
MESES = ["enero","febrero","marzo","abril","mayo","junio",
         "julio","agosto","septiembre","octubre","noviembre","diciembre"]

# ═══════════════════════════════════════════════════════════════
#  SECCIÓN 4 — ANTI-EVASIÓN: utilidades Windows
# ═══════════════════════════════════════════════════════════════
user32   = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

# IDs arbitrarios para hotkeys globales
_HOTKEY_IDS = list(range(0xBF00, 0xBF20))

# VK codes de teclas a bloquear via keyboard lib
BLOCKED_VK_NAMES = [
    "windows", "left windows", "right windows",
    "alt+tab", "alt+f4", "ctrl+esc",
    "ctrl+shift+esc",         # Task Manager
    "ctrl+alt+delete",
    "win+d", "win+e", "win+r", "win+l",
    "win+m", "win+x",
]

def _ocultar_taskbar(ocultar: bool):
    """Oculta/muestra la barra de tareas de Windows."""
    try:
        hwnd = user32.FindWindowW("Shell_TrayWnd", None)
        hwnd_b = user32.FindWindowW("Shell_SecondaryTrayWnd", None)
        cmd = 0 if ocultar else 5   # SW_HIDE / SW_SHOW
        if hwnd:   user32.ShowWindow(hwnd,   cmd)
        if hwnd_b: user32.ShowWindow(hwnd_b, cmd)
    except Exception:
        pass

def _registrar_hotkeys_globales():
    """Consume Win+D, Win+R, Win+L, Win+E etc. a nivel de sistema."""
    MOD_WIN  = 0x0008
    MOD_ALT  = 0x0001
    MOD_CTRL = 0x0002
    hotkeys = [
        (MOD_WIN,            0x44),  # Win+D  (mostrar escritorio)
        (MOD_WIN,            0x52),  # Win+R  (ejecutar)
        (MOD_WIN,            0x4C),  # Win+L  (bloquear Windows)
        (MOD_WIN,            0x45),  # Win+E  (explorador)
        (MOD_WIN,            0x4D),  # Win+M  (minimizar todo)
        (MOD_WIN,            0x58),  # Win+X  (menú inicio)
        (MOD_WIN,            0x49),  # Win+I  (configuración)
        (MOD_WIN,            0x53),  # Win+S  (búsqueda)
        (MOD_WIN,            0x50),  # Win+P  (proyectar)
        (MOD_ALT,            0x73),  # Alt+F4
        (MOD_CTRL|MOD_ALT,   0x2E),  # Ctrl+Alt+Del (parcial)
    ]
    for i, (mod, vk) in enumerate(hotkeys):
        try:
            user32.RegisterHotKey(None, _HOTKEY_IDS[i], mod, vk)
        except Exception:
            pass

def _desregistrar_hotkeys():
    for hid in _HOTKEY_IDS:
        try: user32.UnregisterHotKey(None, hid)
        except Exception: pass

# Procesos a vigilar y terminar si aparecen
PROC_BLOQUEADOS = {
    "taskmgr.exe", "procexp.exe", "procexp64.exe",
    "cmd.exe", "powershell.exe", "powershell_ise.exe",
    "regedit.exe", "taskkill.exe", "mmc.exe",
    "resmon.exe", "perfmon.exe",
}

# ═══════════════════════════════════════════════════════════════
#  SECCIÓN 5 — CLASE PRINCIPAL
# ═══════════════════════════════════════════════════════════════
class ScreenLocker:

    def __init__(self):
        cfg_load()

        self.entrada    = ""
        self.intentos   = 0
        self.bloqueado  = False
        self.countdown  = 0
        self._alive     = True
        self._overlays  = []   # ventanas en monitores extra

        self.root = tk.Tk()
        self._setup_window()
        self._build_ui()
        self._start_clock()

        # Seguridad
        self._ocultar_taskbar(True)
        self._instalar_keyboard_hooks()
        self._registrar_hotkeys()
        self._iniciar_watchdog()
        self._iniciar_refocus()
        self._crear_overlays()

        self.root.mainloop()

    # ──────────────────────────────────────────────────────────
    #  VENTANA
    # ──────────────────────────────────────────────────────────
    def _setup_window(self):
        r = self.root
        r.title("")
        r.configure(bg=C["bg"])
        r.attributes("-fullscreen",    True)
        r.attributes("-topmost",       True)
        r.attributes("-alpha",         1.0)
        r.overrideredirect(True)       # Sin borde ni barra de título
        r.protocol("WM_DELETE_WINDOW", lambda: None)

        for s in ("<Alt-F4>","<Escape>","<Alt-Tab>",
                  "<Control-Escape>","<super>","<Meta_L>","<Meta_R>"):
            r.bind(s, lambda e: "break")

        r.focus_force()
        r.grab_set()   # Captura todos los eventos de ventana

    # ──────────────────────────────────────────────────────────
    #  OVERLAYS PARA MONITORES EXTRA
    # ──────────────────────────────────────────────────────────
    def _crear_overlays(self):
        """Crea ventanas negras en todos los monitores adicionales."""
        try:
            import tkinter as tk
            monitors = self._get_monitors()
            primary_w = self.root.winfo_screenwidth()
            primary_h = self.root.winfo_screenheight()
            for mon in monitors:
                x, y, w, h = mon
                if x == 0 and y == 0 and w == primary_w and h == primary_h:
                    continue  # Saltar el monitor principal
                ov = tk.Toplevel(self.root)
                ov.configure(bg="black")
                ov.attributes("-fullscreen",  True)
                ov.attributes("-topmost",     True)
                ov.overrideredirect(True)
                ov.geometry(f"{w}x{h}+{x}+{y}")
                ov.protocol("WM_DELETE_WINDOW", lambda: None)
                for s in ("<Alt-F4>","<Escape>"):
                    ov.bind(s, lambda e: "break")
                self._overlays.append(ov)
        except Exception:
            pass

    def _get_monitors(self):
        """Devuelve lista de (x,y,w,h) de todos los monitores."""
        monitors = []
        try:
            MONITORENUMPROC = ctypes.WINFUNCTYPE(
                ctypes.c_bool, ctypes.c_ulong, ctypes.c_ulong,
                ctypes.POINTER(ctypes.wintypes.RECT), ctypes.c_double)
            def cb(hmon, hdc, rect, data):
                r = rect.contents
                monitors.append((r.left, r.top, r.right-r.left, r.bottom-r.top))
                return True
            user32.EnumDisplayMonitors(None, None, MONITORENUMPROC(cb), 0)
        except Exception:
            monitors = [(0, 0, self.root.winfo_screenwidth(),
                         self.root.winfo_screenheight())]
        return monitors

    # ──────────────────────────────────────────────────────────
    #  UI
    # ──────────────────────────────────────────────────────────
    def _build_ui(self):
        r  = self.root
        sw = r.winfo_screenwidth()
        sh = r.winfo_screenheight()

        # Fondo con canvas
        self.canvas = tk.Canvas(r, bg=C["bg"], highlightthickness=0)
        self.canvas.place(x=0, y=0, width=sw, height=sh)
        self._draw_bg(sw, sh)

        # Frame central
        center = tk.Frame(r, bg=C["bg"])
        center.place(relx=0.5, rely=0.5, anchor="center")

        self._build_header(center)
        self._build_clock(center)
        self._build_card(center)
        self._build_footer(center)

        # Barra de estado discreta (esquina inf. derecha)
        self.lbl_admin_hint = tk.Label(
            r, text="PIN docente: admin",
            font=("Segoe UI", 8), bg=C["bg"], fg=C["muted2"]
        )
        self.lbl_admin_hint.place(relx=0.99, rely=0.99, anchor="se")

        r.bind("<Key>", self._on_key)

    def _draw_bg(self, w, h):
        c = self.canvas
        # Cuadrícula sutil
        for x in range(0, w, 56):
            c.create_line(x, 0, x, h, fill="#0e1e30", width=1)
        for y in range(0, h, 56):
            c.create_line(0, y, w, y, fill="#0e1e30", width=1)
        # Manchas de luz
        c.create_oval(-250, -200, 500, 380, fill="#0b1e35", outline="")
        c.create_oval(w-450, h-320, w+220, h+200, fill="#0b1e35", outline="")
        # Línea de acento superior
        c.create_rectangle(0, 0, w, 3, fill=C["border2"], outline="")

    def _build_header(self, parent):
        f = tk.Frame(parent, bg=C["bg"])
        f.pack(pady=(0, 14))
        tk.Label(f, text="🏫", font=("Segoe UI Emoji", 18),
                 bg=C["bg"]).pack(side="left", padx=(0,10))
        right = tk.Frame(f, bg=C["bg"])
        right.pack(side="left")
        tk.Label(right, text=DEFAULTS["institucion"],
                 font=("Segoe UI", 12, "bold"),
                 bg=C["bg"], fg=C["text"]).pack(anchor="w")
        tk.Label(right, text=DEFAULTS["subtitulo"],
                 font=("Segoe UI", 9),
                 bg=C["bg"], fg=C["muted"]).pack(anchor="w")

    def _build_clock(self, parent):
        f = tk.Frame(parent, bg=C["bg"])
        f.pack(pady=(0, 18))
        self.lbl_hora = tk.Label(f, text="00:00",
                                  font=("Consolas", 82, "bold"),
                                  bg=C["bg"], fg=C["text"])
        self.lbl_hora.pack()
        self.lbl_fecha = tk.Label(f, text="",
                                   font=("Segoe UI", 12),
                                   bg=C["bg"], fg=C["muted"])
        self.lbl_fecha.pack()

    def _build_card(self, parent):
        outer = tk.Frame(parent, bg=C["border2"], padx=1, pady=1)
        outer.pack()
        card = tk.Frame(outer, bg=C["card"], padx=38, pady=28)
        card.pack()
        self._card = card

        self.lbl_lock = tk.Label(card, text="🔒",
                                  font=("Segoe UI Emoji", 30), bg=C["card"])
        self.lbl_lock.pack(pady=(0, 6))

        tk.Label(card, text="Ingresa tu PIN para continuar",
                 font=("Segoe UI", 10), bg=C["card"], fg=C["muted"]).pack(pady=(0,16))

        # Dots
        df = tk.Frame(card, bg=C["card"])
        df.pack(pady=(0,18))
        self.dots = []
        for _ in range(4):
            d = tk.Label(df, text="○", font=("Segoe UI", 28),
                         bg=C["card"], fg=C["dot_empty"], width=2)
            d.pack(side="left", padx=7)
            self.dots.append(d)

        # Numpad
        pf = tk.Frame(card, bg=C["card"])
        pf.pack()
        layout = [["1","2","3"],["4","5","6"],
                  ["7","8","9"],["⌫","0","✓"]]
        for ri, row in enumerate(layout):
            for ci, v in enumerate(row):
                self._make_key(pf, v, ri, ci)

        self.lbl_estado = tk.Label(card, text="",
                                    font=("Segoe UI", 10),
                                    bg=C["card"], fg=C["red"],
                                    wraplength=290, justify="center")
        self.lbl_estado.pack(pady=(12,0))

    def _make_key(self, parent, val, row, col):
        es_ok  = (val == "✓")
        es_del = (val == "⌫")
        bg_n   = C["enter"]   if es_ok else C["key"]
        bg_h   = C["enter_h"] if es_ok else C["key_h"]
        fg     = (C["accent"] if es_ok else
                  C["muted"]  if es_del else C["text"])
        bdr    = C["border2"] if es_ok else C["border"]

        wrapper = tk.Frame(parent, bg=bdr, padx=1, pady=1)
        wrapper.grid(row=row, column=col, padx=5, pady=5)
        inner = tk.Label(wrapper, text=val, width=5, height=2,
                         bg=bg_n, fg=fg, cursor="hand2",
                         font=("Segoe UI", 15,
                               "bold" if es_ok else "normal"))
        inner.pack()
        inner.bind("<Enter>",         lambda e, b=inner, h=bg_h: b.config(bg=h))
        inner.bind("<Leave>",         lambda e, b=inner, n=bg_n: b.config(bg=n))
        inner.bind("<ButtonPress-1>", lambda e, b=inner: b.config(bg=C["key_a"]))
        inner.bind("<Button-1>",      lambda e, v=val:   self._tecla(v))

    def _build_footer(self, parent):
        f = tk.Frame(parent, bg=C["bg"])
        f.pack(pady=(14, 0))
        self.lbl_msg = tk.Label(f, text=DEFAULTS["mensaje"],
                                 font=("Segoe UI", 10, "italic"),
                                 bg=C["bg"], fg=C["muted2"])
        self.lbl_msg.pack()

    # ──────────────────────────────────────────────────────────
    #  RELOJ
    # ──────────────────────────────────────────────────────────
    def _start_clock(self):
        self._tick()

    def _tick(self):
        if not self._alive:
            return
        t = time.localtime()
        self.lbl_hora.config(text=time.strftime("%H:%M", t))
        self.lbl_fecha.config(
            text=f"{DIAS[t.tm_wday]}, {t.tm_mday} de "
                 f"{MESES[t.tm_mon-1]} de {t.tm_year}")
        self.root.after(1000, self._tick)

    # ──────────────────────────────────────────────────────────
    #  LÓGICA PIN
    # ──────────────────────────────────────────────────────────
    def _tecla(self, val):
        if self.bloqueado:
            return
        if val == "⌫":
            self.entrada = self.entrada[:-1]
            self._dots()
        elif val == "✓":
            self._verificar()
        elif len(self.entrada) < 4:
            self.entrada += val
            self._dots()
            if len(self.entrada) == 4:
                self.root.after(200, self._verificar)

    def _on_key(self, event):
        if self.bloqueado:
            return "break"
        k = event.keysym
        if k in "0123456789" and len(self.entrada) < 4:
            self.entrada += k
            self._dots()
            if len(self.entrada) == 4:
                self.root.after(200, self._verificar)
        elif k == "BackSpace":
            self.entrada = self.entrada[:-1]
            self._dots()
        elif k in ("Return", "KP_Enter"):
            self._verificar()
        return "break"

    def _dots(self, estado=None):
        for i, d in enumerate(self.dots):
            if estado == "error":
                d.config(text="●", fg=C["dot_err"])
            elif estado == "ok":
                d.config(text="●", fg=C["dot_ok"])
            elif i < len(self.entrada):
                d.config(text="●", fg=C["dot_full"])
            else:
                d.config(text="○", fg=C["dot_empty"])

    def _verificar(self):
        es_alu   = self.entrada == DEFAULTS["pin_alumno"]
        es_admin = self.entrada == DEFAULTS["pin_admin"]

        if es_alu or es_admin:
            self._dots("ok")
            self.lbl_lock.config(text="🔓")
            self.lbl_estado.config(
                text="✓ Acceso de docente." if es_admin else "✓ PIN correcto.",
                fg=C["green"])
            if es_admin:
                self.root.after(500, self._panel_admin)
            else:
                self.root.after(600, self._desbloquear)
        else:
            self.intentos += 1
            self._dots("error")
            rest = DEFAULTS["max_intentos"] - self.intentos
            if rest <= 0:
                self.bloqueado = True
                self.lbl_estado.config(
                    text=f"⛔ Demasiados intentos — espera {DEFAULTS['bloqueo_seg']}s",
                    fg=C["red"])
                self.root.after(700, self._reset_entrada)
                self._iniciar_bloqueo()
            else:
                color = C["yellow"] if rest <= 2 else C["red"]
                self.lbl_estado.config(
                    text=f"PIN incorrecto — {rest} intento{'s' if rest!=1 else ''} restante{'s' if rest!=1 else ''}",
                    fg=color)
                self.root.after(700, self._reset_entrada)

    def _reset_entrada(self):
        self.entrada = ""
        self._dots()

    def _iniciar_bloqueo(self):
        self.countdown = DEFAULTS["bloqueo_seg"]
        self._bloqueo_tick()

    def _bloqueo_tick(self):
        if self.countdown > 0:
            self.lbl_estado.config(
                text=f"⛔ Bloqueado — {self.countdown}s restante{'s' if self.countdown!=1 else ''}",
                fg=C["red"])
            self.countdown -= 1
            self.root.after(1000, self._bloqueo_tick)
        else:
            self.bloqueado = False
            self.intentos  = 0
            self._reset_entrada()
            self.lbl_estado.config(text="")

    # ──────────────────────────────────────────────────────────
    #  PANEL ADMIN
    # ──────────────────────────────────────────────────────────
    def _panel_admin(self):
        win = tk.Toplevel(self.root)
        win.title("Panel Docente")
        win.configure(bg=C["panel"])
        win.attributes("-topmost", True)
        win.resizable(False, False)
        ww, wh = 440, 520
        sx = self.root.winfo_screenwidth()  // 2 - ww // 2
        sy = self.root.winfo_screenheight() // 2 - wh // 2
        win.geometry(f"{ww}x{wh}+{sx}+{sy}")
        win.protocol("WM_DELETE_WINDOW", lambda: self._cerrar_panel(win))
        win.grab_set()

        def L(p, t, sz=10, bold=False, fg=None, **kw):
            return tk.Label(p, text=t,
                            font=("Segoe UI", sz, "bold" if bold else "normal"),
                            bg=C["panel"], fg=fg or C["text"], **kw)

        def campo(p, show=None, val=""):
            e = tk.Entry(p, font=("Consolas", 14),
                         bg=C["card2"], fg=C["text"],
                         insertbackground=C["accent"],
                         relief="flat", bd=0,
                         highlightbackground=C["border2"],
                         highlightthickness=1,
                         show=show)
            e.insert(0, val)
            return e

        def boton(p, txt, cmd, color=None, width=26):
            return tk.Button(p, text=txt, command=cmd, width=width,
                             font=("Segoe UI", 10, "bold"),
                             bg=color or C["accent_d"], fg=C["text"],
                             activebackground=C["accent"],
                             activeforeground=C["text"],
                             relief="flat", bd=0, cursor="hand2",
                             pady=9)

        # Encabezado
        L(win, "⚙️  Panel de Administración Docente", 13, bold=True).pack(pady=(22,2))
        L(win, "Configuración del Screen Locker", fg=C["muted"]).pack()
        tk.Frame(win, bg=C["border"], height=1).pack(fill="x", padx=24, pady=14)

        # PINs
        L(win, "CAMBIAR PINs", 9, fg=C["muted"]).pack(anchor="w", padx=28)
        for lbl_txt, key in [("PIN de alumnos", "pin_alumno"),
                              ("PIN de docente", "pin_admin")]:
            r = tk.Frame(win, bg=C["panel"])
            r.pack(fill="x", padx=28, pady=5)
            L(r, lbl_txt, fg=C["muted"]).pack(anchor="w")
            e = campo(r, show="●", val=DEFAULTS[key])
            e.pack(fill="x", ipady=7, pady=(3,0))
            if key == "pin_alumno": self._e_pa = e
            else:                   self._e_pd = e

        tk.Frame(win, bg=C["border"], height=1).pack(fill="x", padx=24, pady=12)

        # Mensaje
        L(win, "MENSAJE EN PANTALLA", 9, fg=C["muted"]).pack(anchor="w", padx=28)
        rf = tk.Frame(win, bg=C["panel"])
        rf.pack(fill="x", padx=28, pady=5)
        self._e_msg2 = campo(rf, val=DEFAULTS["mensaje"])
        self._e_msg2.pack(fill="x", ipady=7, pady=(3,0))

        tk.Frame(win, bg=C["border"], height=1).pack(fill="x", padx=24, pady=12)

        # Feedback
        self._lbl_fb = L(win, "", fg=C["green"])
        self._lbl_fb.pack(pady=(0,8))

        def guardar():
            pa  = self._e_pa.get().strip()
            pd  = self._e_pd.get().strip()
            msg = self._e_msg2.get().strip()
            if not pa.isdigit() or len(pa) != 4:
                self._lbl_fb.config(text="⚠ PIN alumnos: 4 dígitos", fg=C["red"]); return
            if not pd.isdigit() or len(pd) != 4:
                self._lbl_fb.config(text="⚠ PIN docente: 4 dígitos", fg=C["red"]); return
            if pa == pd:
                self._lbl_fb.config(text="⚠ Los PINs no pueden ser iguales", fg=C["red"]); return
            DEFAULTS["pin_alumno"] = pa
            DEFAULTS["pin_admin"]  = pd
            DEFAULTS["mensaje"]    = msg
            cfg_save()
            self.lbl_msg.config(text=msg)
            self._lbl_fb.config(text="✓ Guardado correctamente", fg=C["green"])

        # Botones
        bf = tk.Frame(win, bg=C["panel"])
        bf.pack(padx=28, fill="x")
        boton(bf, "💾  Guardar cambios",     guardar).pack(fill="x", pady=3)
        boton(bf, "🖥  Desbloquear escritorio",
              lambda: [win.destroy(), self._desbloquear()],
              color="#1e5c30").pack(fill="x", pady=3)
        boton(bf, "🔄  Volver a bloquear",
              lambda: self._cerrar_panel(win),
              color="#5c1c1c").pack(fill="x", pady=3)

    def _cerrar_panel(self, win):
        win.destroy()
        self._reset_para_relockear()

    def _reset_para_relockear(self):
        self.entrada    = ""
        self.intentos   = 0
        self.bloqueado  = False
        self._dots()
        self.lbl_lock.config(text="🔒")
        self.lbl_estado.config(text="")
        self.root.attributes("-topmost", True)
        self.root.grab_set()
        self.root.focus_force()

    # ──────────────────────────────────────────────────────────
    #  DESBLOQUEO
    # ──────────────────────────────────────────────────────────
    def _desbloquear(self):
        self._alive = False
        self._cleanup_security()
        try:
            for ov in self._overlays:
                ov.destroy()
            self.root.destroy()
        except Exception:
            pass

    # ──────────────────────────────────────────────────────────
    #  SEGURIDAD: keyboard hooks
    # ──────────────────────────────────────────────────────────
    def _instalar_keyboard_hooks(self):
        """Bloquea combinaciones peligrosas con la librería keyboard."""
        try:
            bloqueadas = [
                "windows", "left windows", "right windows",
                "win+d", "win+e", "win+r", "win+l", "win+m",
                "win+x", "win+i", "win+s", "win+p",
                "alt+f4", "alt+tab", "ctrl+esc",
                "ctrl+shift+esc", "ctrl+alt+delete",
                "ctrl+alt+del",
            ]
            for combo in bloqueadas:
                try:
                    keyboard.block_key(combo)
                except Exception:
                    pass
            # Suprimir todas las teclas Win
            keyboard.add_hotkey("windows", lambda: None, suppress=True)
            keyboard.add_hotkey("left windows", lambda: None, suppress=True)
            keyboard.add_hotkey("right windows", lambda: None, suppress=True)
        except Exception as e:
            print(f"[keyboard] {e}")

    def _registrar_hotkeys(self):
        try:
            _registrar_hotkeys_globales()
            # Hilo para consumir mensajes de hotkey registradas
            threading.Thread(target=self._hotkey_pump, daemon=True).start()
        except Exception:
            pass

    def _hotkey_pump(self):
        msg = ctypes.wintypes.MSG()
        while self._alive:
            try:
                if user32.PeekMessageW(ctypes.byref(msg), None, 0, 0, 1):
                    pass   # Consumir el mensaje sin procesarlo
            except Exception:
                pass
            time.sleep(0.01)

    # ──────────────────────────────────────────────────────────
    #  SEGURIDAD: watchdog de procesos
    # ──────────────────────────────────────────────────────────
    def _iniciar_watchdog(self):
        threading.Thread(target=self._watchdog, daemon=True).start()

    def _watchdog(self):
        """Mata procesos que podrían usarse para escapar el lock."""
        while self._alive:
            try:
                for proc in psutil.process_iter(["name", "pid"]):
                    nombre = (proc.info["name"] or "").lower()
                    if nombre in PROC_BLOQUEADOS:
                        try:
                            proc.kill()
                        except Exception:
                            pass
            except Exception:
                pass
            time.sleep(1.5)

    # ──────────────────────────────────────────────────────────
    #  SEGURIDAD: re-foco constante
    # ──────────────────────────────────────────────────────────
    def _iniciar_refocus(self):
        self._refocus()

    def _refocus(self):
        if not self._alive:
            return
        try:
            self.root.attributes("-topmost", True)
            self.root.lift()
            self.root.focus_force()
            for ov in self._overlays:
                ov.attributes("-topmost", True)
                ov.lift()
        except Exception:
            pass
        self.root.after(400, self._refocus)

    # ──────────────────────────────────────────────────────────
    #  LIMPIEZA AL DESBLOQUEAR
    # ──────────────────────────────────────────────────────────
    def _cleanup_security(self):
        try: keyboard.unhook_all()
        except Exception: pass
        try: _desregistrar_hotkeys()
        except Exception: pass
        try: _ocultar_taskbar(False)
        except Exception: pass

    def _ocultar_taskbar(self, hide: bool):
        _ocultar_taskbar(hide)


# ═══════════════════════════════════════════════════════════════
#  ENTRY POINT
# ═══════════════════════════════════════════════════════════════
if __name__ == "__main__":
    # Ocultar ventana de consola
    if sys.platform == "win32":
        try:
            ctypes.windll.user32.ShowWindow(
                ctypes.windll.kernel32.GetConsoleWindow(), 0)
        except Exception:
            pass

    # Si no es admin, solicitar elevación
    if sys.platform == "win32" and not _check_admin():
        resp = ctypes.windll.user32.MessageBoxW(
            None,
            "Este programa requiere privilegios de Administrador para "
            "máxima seguridad.\n\n"
            "¿Deseas relanzarlo como Administrador?\n\n"
            "(Si pulsas No, se ejecutará con seguridad reducida.)",
            "Screen Locker Educativo",
            0x04 | 0x30   # MB_YESNO | MB_ICONWARNING
        )
        if resp == 6:   # IDYES
            _elevar()
            # _elevar() llama sys.exit(), no llega aquí

    ScreenLocker()
