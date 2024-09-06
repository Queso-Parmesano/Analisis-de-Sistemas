import mysql.connector
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import DateEntry
from ttkwidgets.autocomplete import AutocompleteCombobox

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="paintball"
)
cursor = conn.cursor()

def limpiar_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def mostrar_promociones(frame):
    ttk.Label(frame, text="Promociones Disponibles", font=("Arial", 12, "bold")).pack(pady=10)
    
    cursor.execute("SELECT * FROM promos")
    promos = cursor.fetchall()
    
    for promo in promos:
        promo_text = f"Promo ID: {promo[0]}\nBalas Extras: {promo[2]}\nPrecio: ${promo[3]}"
        promo_frame = ttk.Frame(frame, padding="10 5")
        ttk.Label(promo_frame, text=promo_text, justify=tk.LEFT).pack()
        promo_frame.pack(pady=5, fill=tk.X, expand=True)

def mostrar_agregar_reserva():
    limpiar_frame(contenido_frame)

    cursor.execute("SELECT id FROM sucursales")
    sucursales_ids = [str(row[0]) for row in cursor.fetchall()]

    cursor.execute("SELECT id FROM promos")
    promos_ids = [str(row[0]) for row in cursor.fetchall()]

    #form

    formulario_frame = ttk.Frame(contenido_frame, padding="10 10")
    formulario_frame.grid(row=0, column=0, sticky="nsew")
    
    ttk.Label(formulario_frame, text="Sucursal ID").grid(row=0, column=0, padx=10, pady=10, sticky="w")
    ttk.Label(formulario_frame, text="Promo ID").grid(row=1, column=0, padx=10, pady=10, sticky="w")
    ttk.Label(formulario_frame, text="Cancha").grid(row=2, column=0, padx=10, pady=10, sticky="w")
    ttk.Label(formulario_frame, text="Fecha").grid(row=3, column=0, padx=10, pady=10, sticky="w")
    ttk.Label(formulario_frame, text="Hora Inicio\n(HH:MM:SS)").grid(row=4, column=0, padx=10, pady=10, sticky="w")
    ttk.Label(formulario_frame, text="Hora Final\n(HH:MM:SS)").grid(row=5, column=0, padx=10, pady=10, sticky="w")
    ttk.Label(formulario_frame, text="Balas Extras").grid(row=6, column=0, padx=10, pady=10, sticky="w")

    sucursal_id = AutocompleteCombobox(formulario_frame, completevalues=sucursales_ids)
    promo_id = AutocompleteCombobox(formulario_frame, completevalues=promos_ids)
    cancha = ttk.Entry(formulario_frame)
    
    # date entry
    fecha = DateEntry(formulario_frame, date_pattern='yyyy-mm-dd', width=12, background='darkblue', foreground='white', borderwidth=2)

    hora_inicio = ttk.Entry(formulario_frame)
    hora_final = ttk.Entry(formulario_frame)

    balas_extras = ttk.Entry(formulario_frame)

    sucursal_id.grid(row=0, column=1, padx=10, pady=10)
    promo_id.grid(row=1, column=1, padx=10, pady=10)
    cancha.grid(row=2, column=1, padx=10, pady=10)
    fecha.grid(row=3, column=1, padx=10, pady=10)
    hora_inicio.grid(row=4, column=1, padx=10, pady=10)
    hora_final.grid(row=5, column=1, padx=10, pady=10)
    balas_extras.grid(row=6, column=1, padx=10, pady=10)

    def guardar_reserva():
        precio = 100  # precio base
        if promo_id.get():
            cursor.execute("SELECT precio_agregado FROM promos WHERE id = %s", (promo_id.get(),))
            promo_precio = cursor.fetchone()[0]
            precio += promo_precio
        
        query = '''INSERT INTO reservas (sucursal_id, promo_id, cancha, fecha, hora_inicio, hora_final, balas_extras, precio_total)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'''
        valores = (sucursal_id.get(), promo_id.get(), cancha.get(), fecha.get(), hora_inicio.get(), hora_final.get(), balas_extras.get(), precio)
        cursor.execute(query, valores)
        conn.commit()
        messagebox.showinfo("Éxito", "Reserva agregada correctamente")
        mostrar_agregar_reserva()

    ttk.Button(formulario_frame, text="Agregar Reserva", command=guardar_reserva).grid(row=7, column=1, pady=10)

    # Mostrar promociones en la derecha
    promociones_frame = ttk.Frame(contenido_frame, padding="10 10")
    promociones_frame.grid(row=0, column=1, sticky="nsew")
    mostrar_promociones(promociones_frame)

def mostrar_agregar_promo():
    limpiar_frame(contenido_frame)

    formulario_frame = ttk.Frame(contenido_frame, padding="10 10")
    formulario_frame.grid(row=0, column=0, sticky="nsew")

    ttk.Label(formulario_frame, text="Descripcion de Promo").grid(row=0, column=0, padx=10, pady=10, sticky="w")
    ttk.Label(formulario_frame, text="Balas Extras").grid(row=1, column=0, padx=10, pady=10, sticky="w")
    ttk.Label(formulario_frame, text="Precio Agregado").grid(row=2, column=0, padx=10, pady=10, sticky="w")

    descripcion_promo = ttk.Entry(formulario_frame)
    balas_extras = ttk.Entry(formulario_frame)
    precio_agregado = ttk.Entry(formulario_frame)

    descripcion_promo.grid(row=0, column=1, padx=10, pady=10)
    balas_extras.grid(row=1, column=1, padx=10, pady=10)
    precio_agregado.grid(row=2, column=1, padx=10, pady=10)

    def guardar_promo():
        query = "INSERT INTO promos (descripcion, balas_extras, precio_agregado) VALUES (%s, %s, %s)"
        valores = (descripcion_promo.get(), balas_extras.get(), precio_agregado.get())
        cursor.execute(query, valores)
        conn.commit()
        messagebox.showinfo("Éxito", "Promoción agregada correctamente")
        mostrar_agregar_promo()

    ttk.Button(formulario_frame, text="Agregar Promo", command=guardar_promo).grid(row=3, column=1, pady=10)

def mostrar_ver_reservas():
    limpiar_frame(contenido_frame)
    
    canvas = tk.Canvas(contenido_frame)
    scrollbar_y = ttk.Scrollbar(contenido_frame, orient="vertical", command=canvas.yview)
    scrollbar_x = ttk.Scrollbar(contenido_frame, orient="horizontal", command=canvas.xview)
    scrollable_frame = ttk.Frame(canvas)
    
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

    cursor.execute("SELECT * FROM reservas")
    reservas = cursor.fetchall()
    
    for idx, reserva in enumerate(reservas, 1):
        reserva_text = f"Reserva: {reserva[0]}\nSucursal ID: {reserva[1]}\nPromo ID: {reserva[2]}\nCancha: {reserva[3]}\nFecha: {reserva[4]}\nHora Inicio: {reserva[5]}\nHora Final: {reserva[6]}\nBalas Extras: {reserva[7]}\nPrecio Total: ${reserva[8]}"
        reserva_frame = ttk.Frame(scrollable_frame, padding="10 5", relief="ridge", borderwidth=2)
        ttk.Label(reserva_frame, text=reserva_text, justify=tk.LEFT).pack()
        reserva_frame.pack(pady=5, fill=tk.X, expand=True)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar_y.pack(side="right", fill="y")
    scrollbar_x.pack(side="bottom", fill="x")

def mostrar_eliminar_reserva():
    limpiar_frame(contenido_frame)
    
    cursor.execute("SELECT id FROM reservas")
    reservas_ids = [str(row[0]) for row in cursor.fetchall()]
    
    formulario_frame = ttk.Frame(contenido_frame, padding="10 10")
    formulario_frame.grid(row=0, column=0, sticky="nsew")
    ttk.Label(formulario_frame, text="Reserva ID").grid(row=0, column=0, padx=10, pady=10, sticky="w")
    reserva_id = AutocompleteCombobox(formulario_frame, completevalues=reservas_ids)
    reserva_id.grid(row=0, column=1, padx=10, pady=10)
    
    def eliminar_reserva():
        cursor.execute(f'DELETE FROM reservas WHERE id = {reserva_id.get()}')
        conn.commit()
        messagebox.showinfo("Éxito", "Reserva eliminada correctamente")
        mostrar_eliminar_reserva()

    ttk.Button(formulario_frame, text="Eliminar Reserva", command=eliminar_reserva).grid(row=1, column=1, pady=10)


#conf

root = tk.Tk()
root.title("Gestión de Paintball")
root.geometry("700x500")
root.configure(bg="#7f7f7f")

navegacion_frame = ttk.Frame(root, padding="15 10")
navegacion_frame.pack(side=tk.LEFT, fill=tk.Y)

contenido_frame = ttk.Frame(root, padding="20 10")
contenido_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

btn_agregar_reserva = ttk.Button(navegacion_frame, text="Agregar Reserva", command=mostrar_agregar_reserva)
btn_agregar_reserva.pack(fill=tk.X, pady=10)

btn_agregar_promo = ttk.Button(navegacion_frame, text="Agregar Promo", command=mostrar_agregar_promo)
btn_agregar_promo.pack(fill=tk.X, pady=10)

btn_ver_reservas = ttk.Button(navegacion_frame, text="Ver Reservas", command=mostrar_ver_reservas)
btn_ver_reservas.pack(fill=tk.X, pady=10)

btn_eliminar_reserva = ttk.Button(navegacion_frame, text="Eliminar Reserva", command=mostrar_eliminar_reserva)
btn_eliminar_reserva.pack(fill=tk.X, pady=10)

root.mainloop()
