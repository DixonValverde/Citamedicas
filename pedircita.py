import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime, timedelta
import calendar

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('hospital.db')
        self.create_tables()
        self.insert_initial_data()

    def create_tables(self):
        cursor = self.conn.cursor()
        
        # Tabla de Usuarios
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY,
                nombre TEXT NOT NULL,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                tipo TEXT NOT NULL
            )
        ''')
        
        # Tabla de Especialidades
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS especialidades (
                id INTEGER PRIMARY KEY,
                nombre TEXT NOT NULL
            )
        ''')
        
        # Tabla de Médicos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS medicos (
                id INTEGER PRIMARY KEY,
                nombre TEXT NOT NULL,
                especialidad_id INTEGER,
                FOREIGN KEY (especialidad_id) REFERENCES especialidades (id)
            )
        ''')
        
        # Tabla de Citas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS citas (
                id INTEGER PRIMARY KEY,
                paciente_id INTEGER,
                medico_id INTEGER,
                fecha TEXT NOT NULL,
                hora TEXT NOT NULL,
                estado TEXT NOT NULL,
                FOREIGN KEY (paciente_id) REFERENCES usuarios (id),
                FOREIGN KEY (medico_id) REFERENCES medicos (id)
            )
        ''')
        
        self.conn.commit()

    def insert_initial_data(self):
        cursor = self.conn.cursor()
        
        # Insertar usuario administrador si no existe
        cursor.execute("SELECT * FROM usuarios WHERE username = 'admin'")
        if not cursor.fetchone():
            cursor.execute('''
                INSERT INTO usuarios (nombre, username, password, tipo)
                VALUES ('Administrador', 'admin', 'admin123', 'admin')
            ''')

        # Insertar especialidades si no existen
        especialidades = ['Cardiología', 'Pediatría', 'Dermatología', 'Oftalmología']
        for esp in especialidades:
            cursor.execute("SELECT * FROM especialidades WHERE nombre = ?", (esp,))
            if not cursor.fetchone():
                cursor.execute("INSERT INTO especialidades (nombre) VALUES (?)", (esp,))

        # Insertar algunos médicos de ejemplo
        medicos = [
            ('Dr. García', 1),
            ('Dra. Rodríguez', 1),
            ('Dr. Martínez', 2),
            ('Dra. López', 3)
        ]
        for med in medicos:
            cursor.execute("SELECT * FROM medicos WHERE nombre = ?", (med[0],))
            if not cursor.fetchone():
                cursor.execute("INSERT INTO medicos (nombre, especialidad_id) VALUES (?, ?)", med)

        self.conn.commit()

# Función principal para iniciar la aplicación

class LoginWindow:
    def __init__(self, db):
        self.db = db
        self.window = tk.Tk()
        self.window.title("Sistema de Citas Médicas - Login")
        self.window.geometry("600x400")
        
        # Centrar la ventana
        self.center_window()
        
        # Crear frame principal
        main_frame = ttk.Frame(self.window, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Crear widgets
        ttk.Label(main_frame, text="Sistema de Gestión de Citas", 
                 font=('Helvetica', 12, 'bold')).grid(row=0, column=0, columnspan=2, pady=10)
        
        ttk.Label(main_frame, text="Usuario:").grid(row=1, column=0, pady=5)
        self.username = ttk.Entry(main_frame)
        self.username.grid(row=1, column=1, pady=5)
        
        ttk.Label(main_frame, text="Contraseña:").grid(row=2, column=0, pady=5)
        self.password = ttk.Entry(main_frame, show="*")
        self.password.grid(row=2, column=1, pady=5)
        
        ttk.Button(main_frame, text="Iniciar Sesión", 
                  command=self.login).grid(row=3, column=0, columnspan=2, pady=20)
        ttk.Button(main_frame, text="Registrar Paciente",
                   command=self.show_registration).grid(row=4, column=0, columnspan=2, pady=5)
        # Configurar eventos
        self.window.bind('<Return>', lambda e: self.login())
        
    def center_window(self):
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        
    def login(self):
        username = self.username.get()
        password = self.password.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Por favor complete todos los campos")
            return
        
        cursor = self.db.conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE username = ? AND password = ?", 
                      (username, password))
        user = cursor.fetchone()
        
        if user:
            self.window.destroy()
            if user[4] == 'admin':
                AdminWindow(self.db, user)
            else:
                PatientWindow(self.db, user)
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")
    def show_registration(self):
        PatientRegistrationWindow(self.db)
class PatientRegistrationWindow:
    def __init__(self, db):
        self.db = db
        self.window = tk.Toplevel()
        self.window.title("Registro de Paciente")
        self.window.geometry("400x500")
        
        main_frame = ttk.Frame(self.window, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Campos del formulario
        ttk.Label(main_frame, text="Nombre:").grid(row=0, column=0, pady=5, sticky='w')
        self.nombre = ttk.Entry(main_frame, width=30)
        self.nombre.grid(row=0, column=1, pady=5)
        
        ttk.Label(main_frame, text="Apellido:").grid(row=1, column=0, pady=5, sticky='w')
        self.apellido = ttk.Entry(main_frame, width=30)
        self.apellido.grid(row=1, column=1, pady=5)
        
        ttk.Label(main_frame, text="Correo:").grid(row=2, column=0, pady=5, sticky='w')
        self.correo = ttk.Entry(main_frame, width=30)
        self.correo.grid(row=2, column=1, pady=5)
        
        ttk.Label(main_frame, text="Dirección:").grid(row=3, column=0, pady=5, sticky='w')
        self.direccion = ttk.Entry(main_frame, width=30)
        self.direccion.grid(row=3, column=1, pady=5)
        
        ttk.Label(main_frame, text="Usuario:").grid(row=4, column=0, pady=5, sticky='w')
        self.username = ttk.Entry(main_frame, width=30)
        self.username.grid(row=4, column=1, pady=5)
        
        ttk.Label(main_frame, text="Contraseña:").grid(row=5, column=0, pady=5, sticky='w')
        self.password = ttk.Entry(main_frame, width=30, show="*")
        self.password.grid(row=5, column=1, pady=5)
        
        # Botones
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=6, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="Registrar", 
                  command=self.register_patient).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Cancelar", 
                  command=self.window.destroy).pack(side='left', padx=5)
    
    def register_patient(self):
        # Validar campos
        if not all([self.nombre.get(), self.apellido.get(), self.correo.get(), 
                   self.direccion.get(), self.username.get(), self.password.get()]):
            messagebox.showerror("Error", "Todos los campos son requeridos")
            return
        
        try:
            cursor = self.db.conn.cursor()
            
            # Verificar si el usuario ya existe
            cursor.execute("SELECT * FROM usuarios WHERE username = ?", (self.username.get(),))
            if cursor.fetchone():
                messagebox.showerror("Error", "El nombre de usuario ya existe")
                return
            
            # Insertar nuevo paciente
            cursor.execute('''
                INSERT INTO usuarios (nombre, apellido, correo, direccion, username, password, tipo)
                VALUES (?, ?, ?, ?, ?, ?, 'paciente')
            ''', (self.nombre.get(), self.apellido.get(), self.correo.get(), 
                 self.direccion.get(), self.username.get(), self.password.get()))
            
            self.db.conn.commit()
            messagebox.showinfo("Éxito", "Paciente registrado correctamente")
            self.window.destroy()
            
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error al registrar paciente: {str(e)}")

class AdminWindow:
    def __init__(self, db, user):
        self.db = db
        self.user = user
        self.window = tk.Tk()
        self.window.title("Panel de Administrador")
        self.window.geometry("1000x600")
        
        # Centrar la ventana
        self.center_window()
        
        # Crear menú principal
        self.create_menu()
        
        # Crear pestañas
        self.notebook = ttk.Notebook(self.window)
        self.notebook.pack(expand=True, fill='both', padx=10, pady=5)
        
        # Pestaña de Citas
        self.appointments_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.appointments_frame, text='Citas')
        self.setup_appointments_tab()
        
        # Pestaña de Calendario
        self.calendar_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.calendar_frame, text='Calendario')
        self.setup_calendar_tab()
        
        # Pestaña de Gestión de Médicos
        self.doctors_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.doctors_frame, text='Médicos')
        self.setup_doctors_tab()
        
    def center_window(self):
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        
    def create_menu(self):
        menubar = tk.Menu(self.window)
        self.window.config(menu=menubar)
        
        # Menú Archivo
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Archivo", menu=file_menu)
        file_menu.add_command(label="Cerrar Sesión", command=self.logout)
        file_menu.add_separator()
        file_menu.add_command(label="Salir", command=self.window.quit)
        
        # Menú Herramientas
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Herramientas", menu=tools_menu)
        tools_menu.add_command(label="Configuración", command=self.show_settings)
        
    def setup_appointments_tab(self):
        # Frame superior para filtros
        filter_frame = ttk.LabelFrame(self.appointments_frame, text="Filtros", padding="10")
        filter_frame.pack(fill='x', padx=5, pady=5)
        
        # Filtros
        ttk.Label(filter_frame, text="Fecha:").grid(row=0, column=0, padx=5)
        self.date_filter = ttk.Entry(filter_frame, width=15)
        self.date_filter.grid(row=0, column=1, padx=5)
        
        ttk.Label(filter_frame, text="Médico:").grid(row=0, column=2, padx=5)
        self.doctor_filter = ttk.Combobox(filter_frame, width=20)
        self.doctor_filter.grid(row=0, column=3, padx=5)
        
        ttk.Button(filter_frame, text="Filtrar", 
                  command=self.filter_appointments).grid(row=0, column=4, padx=5)
        ttk.Button(filter_frame, text="Limpiar Filtros", 
                  command=self.clear_filters).grid(row=0, column=5, padx=5)
        
        # Lista de citas
        self.appointments_tree = ttk.Treeview(self.appointments_frame, 
            columns=('id', 'Paciente', 'Médico', 'Especialidad', 'Fecha', 'Hora', 'Estado'),
            show='headings',
            height=20)
        
        # Configurar columnas
        self.appointments_tree.heading('id', text='ID')
        self.appointments_tree.heading('Paciente', text='Paciente')
        self.appointments_tree.heading('Médico', text='Médico')
        self.appointments_tree.heading('Especialidad', text='Especialidad')
        self.appointments_tree.heading('Fecha', text='Fecha')
        self.appointments_tree.heading('Hora', text='Hora')
        self.appointments_tree.heading('Estado', text='Estado')
        
        # Configurar anchos de columna
        self.appointments_tree.column('id', width=50)
        self.appointments_tree.column('Paciente', width=150)
        self.appointments_tree.column('Médico', width=150)
        self.appointments_tree.column('Especialidad', width=150)
        self.appointments_tree.column('Fecha', width=100)
        self.appointments_tree.column('Hora', width=100)
        self.appointments_tree.column('Estado', width=100)
        
        # Agregar scrollbar
        scrollbar = ttk.Scrollbar(self.appointments_frame, 
                                orient="vertical", 
                                command=self.appointments_tree.yview)
        self.appointments_tree.configure(yscrollcommand=scrollbar.set)
        
        self.appointments_tree.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        scrollbar.pack(side='right', fill='y', pady=5)
        
        # Botones de acción
        button_frame = ttk.Frame(self.appointments_frame)
        button_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Button(button_frame, text="Nueva Cita", 
                  command=self.new_appointment).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Editar Cita", 
                  command=self.edit_appointment).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Cancelar Cita", 
                  command=self.cancel_appointment).pack(side='left', padx=5)
        
        # Cargar datos iniciales
        self.load_appointments()
        self.load_doctors_filter()
        
    def load_doctors_filter(self):
        cursor = self.db.conn.cursor()
        cursor.execute("SELECT nombre FROM medicos ORDER BY nombre")
        doctors = [row[0] for row in cursor.fetchall()]
        self.doctor_filter['values'] = ['Todos'] + doctors
        self.doctor_filter.set('Todos')

    def setup_calendar_tab(self):
        # Implementación del calendario
        pass  # Se implementará en la siguiente parte
        
    def setup_doctors_tab(self):
        # Implementación de la gestión de médicos
        pass  # Se implementará en la siguiente parte

    def logout(self):
        self.window.destroy()
        login_window = LoginWindow(self.db)
        login_window.window.mainloop()
        
    def show_settings(self):
        messagebox.showinfo("Configuración", "Funcionalidad en desarrollo")
class AppointmentWindow:
    def __init__(self, db, parent, appointment=None):
        self.db = db
        self.parent = parent
        self.appointment = appointment
        self.window = tk.Toplevel()
        self.window.title("Nueva Cita" if not appointment else "Editar Cita")
        self.window.geometry("400x500")
        
        # Frame principal
        main_frame = ttk.Frame(self.window, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Campos del formulario
        ttk.Label(main_frame, text="Paciente:").grid(row=0, column=0, pady=5, sticky='w')
        self.patient = ttk.Combobox(main_frame, width=30)
        self.patient.grid(row=0, column=1, pady=5)
        
        ttk.Label(main_frame, text="Especialidad:").grid(row=1, column=0, pady=5, sticky='w')
        self.specialty = ttk.Combobox(main_frame, width=30)
        self.specialty.grid(row=1, column=1, pady=5)
        
        ttk.Label(main_frame, text="Médico:").grid(row=2, column=0, pady=5, sticky='w')
        self.doctor = ttk.Combobox(main_frame, width=30)
        self.doctor.grid(row=2, column=1, pady=5)
        
        ttk.Label(main_frame, text="Fecha (YYYY-MM-DD):").grid(row=3, column=0, pady=5, sticky='w')
        self.date = ttk.Entry(main_frame, width=30)
        self.date.grid(row=3, column=1, pady=5)
        
        ttk.Label(main_frame, text="Hora (HH:MM):").grid(row=4, column=0, pady=5, sticky='w')
        self.time = ttk.Entry(main_frame, width=30)
        self.time.grid(row=4, column=1, pady=5)
        
        # Botones
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="Guardar", 
                  command=self.save_appointment).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Cancelar", 
                  command=self.window.destroy).pack(side='left', padx=5)
        
        # Cargar datos
        self.load_data()
        if appointment:
            self.load_appointment_data()
        
    def load_data(self):
        cursor = self.db.conn.cursor()
        
        # Cargar pacientes
        cursor.execute("SELECT nombre FROM usuarios WHERE tipo = 'paciente'")
        self.patient['values'] = [row[0] for row in cursor.fetchall()]
        
        # Cargar especialidades
        cursor.execute("SELECT nombre FROM especialidades")
        self.specialty['values'] = [row[0] for row in cursor.fetchall()]
        
        # Configurar evento para actualizar médicos
        self.specialty.bind('<<ComboboxSelected>>', self.update_doctors)
        
    def update_doctors(self, event=None):
        specialty = self.specialty.get()
        if not specialty:
            return
            
        cursor = self.db.conn.cursor()
        cursor.execute('''
            SELECT m.nombre
            FROM medicos m
            JOIN especialidades e ON m.especialidad_id = e.id
            WHERE e.nombre = ?
        ''', (specialty,))
        
        self.doctor['values'] = [row[0] for row in cursor.fetchall()]
        
    def load_appointment_data(self):
        cursor = self.db.conn.cursor()
        cursor.execute('''
            SELECT u.nombre, e.nombre, m.nombre, c.fecha, c.hora
            FROM citas c
            JOIN usuarios u ON c.paciente_id = u.id
            JOIN medicos m ON c.medico_id = m.id
            JOIN especialidades e ON m.especialidad_id = e.id
            WHERE c.id = ?
        ''', (self.appointment[0],))
        
        data = cursor.fetchone()
        if data:
            self.patient.set(data[0])
            self.specialty.set(data[1])
            self.doctor.set(data[2])
            self.date.insert(0, data[3])
            self.time.insert(0, data[4])
            
    def validate_data(self):
        # Validar campos requeridos
        if not all([self.patient.get(), self.specialty.get(), 
                   self.doctor.get(), self.date.get(), self.time.get()]):
            messagebox.showerror("Error", "Todos los campos son requeridos")
            return False
            
        # Validar formato de fecha
        try:
            datetime.strptime(self.date.get(), '%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Error", "Formato de fecha inválido. Use YYYY-MM-DD")
            return False
            
        # Validar formato de hora
        try:
            datetime.strptime(self.time.get(), '%H:%M')
        except ValueError:
            messagebox.showerror("Error", "Formato de hora inválido. Use HH:MM")
            return False
            
        return True
        
    def save_appointment(self):
        if not self.validate_data():
            return
            
        cursor = self.db.conn.cursor()
        
        # Verificar disponibilidad
        query = '''
            SELECT COUNT(*)
            FROM citas c
            JOIN medicos m ON c.medico_id = m.id
            WHERE m.nombre = ? AND c.fecha = ? AND c.hora = ?
            AND c.estado != 'cancelada'
        '''
        params = [self.doctor.get(), self.date.get(), self.time.get()]
        
        if self.appointment:
            query += ' AND c.id != ?'
            params.append(self.appointment[0])
            
        cursor.execute(query, params)
        
        if cursor.fetchone()[0] > 0:
            messagebox.showerror("Error", "El horario seleccionado no está disponible")
            return
            
        try:
            if self.appointment:
                # Actualizar cita existente
                cursor.execute('''
                    UPDATE citas
                    SET paciente_id = (SELECT id FROM usuarios WHERE nombre = ?),
                        medico_id = (SELECT id FROM medicos WHERE nombre = ?),
                        fecha = ?,
                        hora = ?
                    WHERE id = ?
                ''', (self.patient.get(), self.doctor.get(), 
                     self.date.get(), self.time.get(), self.appointment[0]))
            else:
                # Crear nueva cita
                cursor.execute('''
                    INSERT INTO citas (paciente_id, medico_id, fecha, hora, estado)
                    VALUES (
                        (SELECT id FROM usuarios WHERE nombre = ?),
                        (SELECT id FROM medicos WHERE nombre = ?),
                        ?, ?, 'programada'
                    )
                ''', (self.patient.get(), self.doctor.get(), 
                     self.date.get(), self.time.get()))
            
            self.db.conn.commit()
            messagebox.showinfo("Éxito", "Cita guardada correctamente")
            self.parent.load_appointments()
            self.window.destroy()
            
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error al guardar la cita: {str(e)}")
class PatientWindow:
    def __init__(self, db, user):
        self.db = db
        self.user = user
        self.window = tk.Tk()
        self.window.title(f"Panel de Paciente - {user[1]}")
        self.window.geometry("800x500")
        
        # Crear notebook para pestañas
        self.notebook = ttk.Notebook(self.window)
        self.notebook.pack(expand=True, fill='both', padx=10, pady=5)
        
        # Pestaña de Mis Citas
        self.appointments_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.appointments_frame, text='Mis Citas')
        self.setup_appointments_tab()
        
        # Pestaña de Nueva Cita
        self.new_appointment_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.new_appointment_frame, text='Nueva Cita')
        self.setup_new_appointment_tab()
        
    def setup_appointments_tab(self):
        # Lista de citas del paciente
        self.appointments_tree = ttk.Treeview(self.appointments_frame,
            columns=('id', 'Médico', 'Especialidad', 'Fecha', 'Hora', 'Estado'),
            show='headings',
            height=15)
        
        # Configurar columnas
        self.appointments_tree.heading('id', text='ID')
        self.appointments_tree.heading('Médico', text='Médico')
        self.appointments_tree.heading('Especialidad', text='Especialidad')
        self.appointments_tree.heading('Fecha', text='Fecha')
        self.appointments_tree.heading('Hora', text='Hora')
        self.appointments_tree.heading('Estado', text='Estado')
        
        # Configurar anchos de columna
        self.appointments_tree.column('id', width=50)
        self.appointments_tree.column('Médico', width=150)
        self.appointments_tree.column('Especialidad', width=150)
        self.appointments_tree.column('Fecha', width=100)
        self.appointments_tree.column('Hora', width=100)
        self.appointments_tree.column('Estado', width=100)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.appointments_frame, 
                                orient="vertical", 
                                command=self.appointments_tree.yview)
        self.appointments_tree.configure(yscrollcommand=scrollbar.set)
        
        self.appointments_tree.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        scrollbar.pack(side='right', fill='y', pady=5)
        
        # Botón para cancelar cita
        ttk.Button(self.appointments_frame, text="Cancelar Cita Seleccionada", 
                  command=self.cancel_appointment).pack(pady=10)
        
        # Cargar citas
        self.load_appointments()
        
    def setup_new_appointment_tab(self):
        # Frame para el formulario
        form_frame = ttk.LabelFrame(self.new_appointment_frame, text="Nueva Cita", padding="20")
        form_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Campos del formulario
        ttk.Label(form_frame, text="Especialidad:").grid(row=0, column=0, pady=5, sticky='w')
        self.specialty = ttk.Combobox(form_frame, width=30)
        self.specialty.grid(row=0, column=1, pady=5)
        
        ttk.Label(form_frame, text="Médico:").grid(row=1, column=0, pady=5, sticky='w')
        self.doctor = ttk.Combobox(form_frame, width=30)
        self.doctor.grid(row=1, column=1, pady=5)
        
        ttk.Label(form_frame, text="Fecha (YYYY-MM-DD):").grid(row=2, column=0, pady=5, sticky='w')
        self.date = ttk.Entry(form_frame, width=30)
        self.date.grid(row=2, column=1, pady=5)
        
        ttk.Label(form_frame, text="Hora (HH:MM):").grid(row=3, column=0, pady=5, sticky='w')
        self.time = ttk.Entry(form_frame, width=30)
        self.time.grid(row=3, column=1, pady=5)
        
        # Botón para agendar
        ttk.Button(form_frame, text="Agendar Cita", 
                  command=self.schedule_appointment).grid(row=4, column=0, columnspan=2, pady=20)
        
        # Cargar datos
        self.load_specialties()
        self.specialty.bind('<<ComboboxSelected>>', self.update_doctors)
        
    def load_appointments(self):
        cursor = self.db.conn.cursor()
        cursor.execute('''
            SELECT c.id, m.nombre, e.nombre, c.fecha, c.hora, c.estado
            FROM citas c
            JOIN medicos m ON c.medico_id = m.id
            JOIN especialidades e ON m.especialidad_id = e.id
            WHERE c.paciente_id = ?
            ORDER BY c.fecha DESC, c.hora DESC
        ''', (self.user[0],))
        
        # Limpiar tabla
        for item in self.appointments_tree.get_children():
            self.appointments_tree.delete(item)
            
        # Insertar datos
        for row in cursor.fetchall():
            self.appointments_tree.insert('', 'end', values=row)
            
    def load_specialties(self):
        cursor = self.db.conn.cursor()
        cursor.execute("SELECT nombre FROM especialidades ORDER BY nombre")
        self.specialty['values'] = [row[0] for row in cursor.fetchall()]
        
    def update_doctors(self, event=None):
        specialty = self.specialty.get()
        if not specialty:
            return
            
        cursor = self.db.conn.cursor()
        cursor.execute('''
            SELECT m.nombre
            FROM medicos m
            JOIN especialidades e ON m.especialidad_id = e.id
            WHERE e.nombre = ?
        ''', (specialty,))
        
        self.doctor['values'] = [row[0] for row in cursor.fetchall()]
        
    def schedule_appointment(self):
        # Validar campos
        if not all([self.specialty.get(), self.doctor.get(), 
                   self.date.get(), self.time.get()]):
            messagebox.showerror("Error", "Todos los campos son requeridos")
            return
            
        # Validar formato de fecha y hora
        try:
            datetime.strptime(self.date.get(), '%Y-%m-%d')
            datetime.strptime(self.time.get(), '%H:%M')
        except ValueError:

            messagebox.showerror("Error", "Formato de fecha u hora inválido")
        return
# Continuación de PatientWindow
    def schedule_appointment(self):
        try:
            # Validar disponibilidad
            cursor = self.db.conn.cursor()
            cursor.execute('''
                SELECT COUNT(*)
                FROM citas c
                JOIN medicos m ON c.medico_id = m.id
                WHERE m.nombre = ? AND c.fecha = ? AND c.hora = ?
                AND c.estado != 'cancelada'
            ''', (self.doctor.get(), self.date.get(), self.time.get()))
            
            if cursor.fetchone()[0] > 0:
                messagebox.showerror("Error", "El horario seleccionado no está disponible")
                return
                
            # Crear la cita
            cursor.execute('''
                INSERT INTO citas (paciente_id, medico_id, fecha, hora, estado)
                VALUES (
                    ?,
                    (SELECT id FROM medicos WHERE nombre = ?),
                    ?, ?, 'programada'
                )
            ''', (self.user[0], self.doctor.get(), self.date.get(), self.time.get()))
            
            self.db.conn.commit()
            messagebox.showinfo("Éxito", "Cita agendada correctamente")
            
            # Limpiar campos
            self.specialty.set('')
            self.doctor.set('')
            self.date.delete(0, tk.END)
            self.time.delete(0, tk.END)
            
            # Actualizar lista de citas
            self.load_appointments()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al agendar la cita: {str(e)}")
            
    def cancel_appointment(self):
        selected_item = self.appointments_tree.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Por favor seleccione una cita para cancelar")
            return
            
        if messagebox.askyesno("Confirmar", "¿Está seguro de cancelar esta cita?"):
            try:
                appointment_id = self.appointments_tree.item(selected_item)['values'][0]
                
                cursor = self.db.conn.cursor()
                cursor.execute('''
                    UPDATE citas
                    SET estado = 'cancelada'
                    WHERE id = ? AND paciente_id = ?
                ''', (appointment_id, self.user[0]))
                
                self.db.conn.commit()
                messagebox.showinfo("Éxito", "Cita cancelada correctamente")
                self.load_appointments()
                
            except Exception as e:
                messagebox.showerror("Error", f"Error al cancelar la cita: {str(e)}")

# Función principal mejorada
def main():
    try:
        db = Database()
        # Crear un usuario de prueba si no existe
        cursor = db.conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE username = 'paciente1'")
        if not cursor.fetchone():
            cursor.execute('''
                INSERT INTO usuarios (nombre, username, password, tipo)
                VALUES ('Paciente Prueba', 'paciente1', 'pass123', 'paciente')
            ''')
            db.conn.commit()
            
        login_window = LoginWindow(db)
        login_window.window.mainloop()
    except Exception as e:
        messagebox.showerror("Error", f"Error al iniciar la aplicación: {str(e)}")



def main():
    db = Database()
    login_window = LoginWindow(db)
    login_window.window.mainloop()

if __name__ == "__main__":
    main()