import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import simpledialog
import pandas as pd

class FacturaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Generador de Facturas")

        # Datos de la empresa y cliente
        self.datos_empresa = {'Nombre': '', 'Direccion': '', 'Telefono': '', 'Email': ''}
        self.datos_cliente = {'Nombre': '', 'Direccion': '', 'Telefono': '', 'Email': ''}

        # Inicializar DataFrames para segmentos de la factura
        self.segmentos = {
            'Materiales': pd.DataFrame(columns=['Linea', 'Descripción', 'Unidad', 'Precio Unitario', 'Cantidad', 'Total']),
            'Mano de Obra': pd.DataFrame(columns=['Linea', 'Descripción', 'Unidad', 'Precio Unitario', 'Cantidad', 'Total']),
            'Equipos': pd.DataFrame(columns=['Linea', 'Descripción', 'Unidad', 'Precio Unitario', 'Cantidad', 'Total']),
            'Transporte': pd.DataFrame(columns=['Linea', 'Descripción', 'Unidad', 'Precio Unitario', 'Cantidad', 'Total'])
        }

        # Crear pestañas
        self.tabControl = ttk.Notebook(root)
        self.tab1 = ttk.Frame(self.tabControl)
        self.tab2 = ttk.Frame(self.tabControl)

        # Agregar pestañas
        self.tabControl.add(self.tab1, text='Datos')
        self.tabControl.add(self.tab2, text='Factura')

        self.tabControl.pack(expand=1, fill="both")

        # Configurar pestaña de datos
        self.configurar_tab_datos()

        # Configurar pestaña de factura
        self.configurar_tab_factura()

    def configurar_tab_datos(self):
        # Crear un Canvas para la pestaña de Datos
        canvas_datos = tk.Canvas(self.tab1)
        canvas_datos.pack(side="left", fill="both", expand=True)

        # Agregar un Scrollbar al Canvas
        scrollbar_datos = ttk.Scrollbar(self.tab1, orient="vertical", command=canvas_datos.yview)
        scrollbar_datos.pack(side="right", fill="y")

        # Configurar el Scrollbar para que interactúe con el Canvas
        canvas_datos.configure(yscrollcommand=scrollbar_datos.set)

        # Crear un nuevo Frame para contener los widgets
        frame_datos = ttk.Frame(canvas_datos)
        canvas_datos.create_window((0, 0), window=frame_datos, anchor="nw")

        # Configurar etiquetas y campos de entrada para datos de empresa y cliente
        ttk.Label(frame_datos, text="Datos de la Empresa").grid(column=0, row=0, columnspan=2, pady=10)
        self.crear_campos(frame_datos, self.datos_empresa, row_start=1)

        ttk.Label(frame_datos, text="Datos del Cliente").grid(column=0, row=5, columnspan=2, pady=10)
        self.crear_campos(frame_datos, self.datos_cliente, row_start=6)

        ttk.Button(frame_datos, text="Guardar Datos", command=self.guardar_datos).grid(column=1, row=11, pady=10)

        # Configurar el evento de desplazamiento
        frame_datos.bind("<Configure>", lambda event, canvas=canvas_datos: self.on_frame_configure(canvas))

    def configurar_tab_factura(self):
        #Obtener dimensiones de la pantalla
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        # Crear un Canvas para la pestaña de Factura
        canvas_factura = tk.Canvas(self.tab2)
        canvas_factura.pack(side="left", fill="both", expand=True)
        canvas_factura.configure(width=screen_width-100, height=screen_height-300)

        # Agregar un Scrollbar al Canvas
        scrollbar_factura = ttk.Scrollbar(self.tab2, orient="vertical", command=canvas_factura.yview)
        scrollbar_factura.pack(side="right", fill="y",expand=True)

        # Configurar el Scrollbar para que interactúe con el Canvas
        canvas_factura.configure(yscrollcommand=scrollbar_factura.set)

        # Crear un nuevo Frame para contener los widgets
        frame_factura = ttk.Frame(canvas_factura)
        #frame_factura.configure(width=2000, height=2000)
        canvas_factura.create_window((0, 0), window=frame_factura, anchor="nw")
        

        # Crear un nuevo Frame para contener las tablas
        self.tablas_frame = ttk.Frame(frame_factura)
        
        self.tablas_frame.pack(pady=10,padx=screen_height-400)

        # Configurar pestañas para cada segmento de la factura
        for segmento in self.segmentos.keys():
            frame_tab = ttk.Frame(self.tablas_frame)
            frame_tab.pack(pady=10, padx=10)

            ttk.Label(frame_tab, text=segmento).pack(pady=5)

            # Crear Frame para la tabla
            frame_tabla = ttk.Frame(frame_tab)
            frame_tabla.pack(pady=10)

            # Crear tabla usando Treeview con barras de desplazamiento
            tree = ttk.Treeview(frame_tabla, columns=('Linea', 'Descripción', 'Unidad', 'Precio Unitario', 'Cantidad', 'Total'), show='headings')
            tree.heading('Linea', text='Linea')
            tree.heading('Descripción', text='Descripción')
            tree.heading('Unidad', text='Unidad')
            tree.heading('Precio Unitario', text='Precio Unitario')
            tree.heading('Cantidad', text='Cantidad')
            tree.heading('Total', text='Total')

            tree.column('Linea', width=50, anchor='center')
            tree.column('Descripción', width=150, anchor='center')
            tree.column('Unidad', width=100, anchor='center')
            tree.column('Precio Unitario', width=100, anchor='center')
            tree.column('Cantidad', width=100, anchor='center')
            tree.column('Total', width=100, anchor='center')

            yscrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=tree.yview)
            yscrollbar.pack(side='right', fill='y')
            tree.configure(yscrollcommand=yscrollbar.set)

            tree.pack()

            # Configurar botones para agregar, eliminar y modificar filas
            ttk.Button(frame_tab, text="Agregar Fila", command=lambda t=tree: self.agregar_fila(t)).pack(side='left', padx=5)
            ttk.Button(frame_tab, text="Eliminar Fila", command=lambda t=tree: self.eliminar_fila(t)).pack(side='left', padx=5)
            ttk.Button(frame_tab, text="Modificar Fila", command=lambda t=tree: self.modificar_fila(t)).pack(side='left', padx=5)

            # Agregar datos al Treeview
            for i, row in self.segmentos[segmento].iterrows():
                tree.insert('', 'end', values=row.tolist())

        # Botón para agregar nueva tabla
        ttk.Button(frame_factura, text="Agregar Tabla", command=self.agregar_tabla).pack(pady=10)

        # Botón para calcular totales y guardar factura
        ttk.Button(frame_factura, text="Calcular Totales y Guardar", command=self.calcular_totales_guardar).pack(pady=10)

        # Configurar el evento de desplazamiento
        frame_factura.bind("<Configure>", lambda event, canvas=canvas_factura: self.on_frame_configure(canvas))
        

    def crear_campos(self, frame, data_dict, row_start):
        for i, (campo, valor) in enumerate(data_dict.items()):
            ttk.Label(frame, text=f"{campo}:").grid(column=0, row=row_start + i, pady=5)
            data_dict[campo] = tk.StringVar()
            ttk.Entry(frame, textvariable=data_dict[campo]).grid(column=1, row=row_start + i, pady=5)

    def guardar_datos(self):
        # Función para guardar datos de empresa y cliente
        print("Datos guardados")

    def calcular_totales_guardar(self):
        # Función para calcular totales y guardar la factura
        totales = {}
        for segmento, df in self.segmentos.items():
            totales[segmento] = self.calcular_subtotal(df)

        total_final = sum(totales.values())

        # Mostrar resultados
        messagebox.showinfo("Totales Calculados", "\n".join([f"{segmento}: {subtotal}" for segmento, subtotal in totales.items()] +
                                                              [f"\nTotal Final: {total_final}"]))

    def calcular_subtotal(self, df):
        # Calcular subtotal para un DataFrame dado
        return df['Total'].sum()

    def on_frame_configure(self, canvas):
        # Ajustar el área desplazable para coincidir con el tamaño del contenido
        canvas.configure(scrollregion=canvas.bbox("all"))

    def agregar_fila(self, tree):
        # Función para agregar una nueva fila
        nueva_linea = len(tree.get_children()) + 1
        tree.insert('', 'end', values=[nueva_linea, '', '', 0, 0, 0])

    def eliminar_fila(self, tree):
        # Función para eliminar la fila seleccionada
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Por favor, selecciona una fila para eliminar.")
        else:
            tree.delete(selected_item)

    def modificar_fila(self, tree):
        # Función para modificar la fila seleccionada
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Por favor, selecciona una fila para modificar.")
        else:
            # Obtener los valores actuales de la fila seleccionada
            valores_actuales = tree.item(selected_item, 'values')

            # Crear una ventana emergente para la modificación
            modificar_ventana = tk.Toplevel(self.root)
            modificar_ventana.title("Modificar Fila")

            # Crear etiquetas y campos de entrada para la modificación
            etiquetas = ['Descripción', 'Unidad', 'Precio Unitario', 'Cantidad']
            valores_modificar = [tk.StringVar(value=val) for val in valores_actuales[1:-1]]

            for i, etiqueta in enumerate(etiquetas):
                ttk.Label(modificar_ventana, text=f"{etiqueta}:").grid(column=0, row=i, pady=5)
                ttk.Entry(modificar_ventana, textvariable=valores_modificar[i]).grid(column=1, row=i, pady=5)

            # Función para aplicar la modificación
            def aplicar_modificacion():
                nuevos_valores = [val.get() for val in valores_modificar]
                nuevos_valores = [val if val != '' else 0 for val in nuevos_valores]
                nuevos_valores = [valores_actuales[0]] + nuevos_valores + [float(nuevos_valores[2]) * float(nuevos_valores[3])]

                tree.item(selected_item, values=nuevos_valores)
                modificar_ventana.destroy()

            ttk.Button(modificar_ventana, text="Aplicar Modificación", command=aplicar_modificacion).grid(column=1, row=4, pady=10)

    def agregar_tabla(self):
        # Función para agregar una nueva tabla
        nuevo_nombre_tabla = simpledialog.askstring("Agregar Tabla", "Ingrese el nombre de la nueva tabla:")
        if nuevo_nombre_tabla:
            self.segmentos[nuevo_nombre_tabla] = pd.DataFrame(columns=['Linea', 'Descripción', 'Unidad', 'Precio Unitario', 'Cantidad', 'Total'])
            ttk.Label(self.tablas_frame, text=nuevo_nombre_tabla).pack(pady=10)
            self.crear_tabla(self.tablas_frame, self.segmentos[nuevo_nombre_tabla])

    def crear_tabla(self, tab, df):
        # Crear Frame para la tabla
        frame_tabla = ttk.Frame(tab)
        frame_tabla.pack(pady=10)

        # Crear tabla usando Treeview con barras de desplazamiento
        tree = ttk.Treeview(frame_tabla, columns=('Linea', 'Descripción', 'Unidad', 'Precio Unitario', 'Cantidad', 'Total'), show='headings')
        tree.heading('Linea', text='Linea')
        tree.heading('Descripción', text='Descripción')
        tree.heading('Unidad', text='Unidad')
        tree.heading('Precio Unitario', text='Precio Unitario')
        tree.heading('Cantidad', text='Cantidad')
        tree.heading('Total', text='Total')

        tree.column('Linea', width=50, anchor='center')
        tree.column('Descripción', width=150, anchor='center')
        tree.column('Unidad', width=100, anchor='center')
        tree.column('Precio Unitario', width=100, anchor='center')
        tree.column('Cantidad', width=100, anchor='center')
        tree.column('Total', width=100, anchor='center')

        yscrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=tree.yview)
        yscrollbar.pack(side='right', fill='y')
        tree.configure(yscrollcommand=yscrollbar.set)

        tree.pack()

        # Configurar botones para agregar, eliminar y modificar filas
        ttk.Button(frame_tabla, text="Agregar Fila", command=lambda: self.agregar_fila(tree)).pack(side='left', padx=5)
        ttk.Button(frame_tabla, text="Eliminar Fila", command=lambda: self.eliminar_fila(tree)).pack(side='left', padx=5)
        ttk.Button(frame_tabla, text="Modificar Fila", command=lambda: self.modificar_fila(tree)).pack(side='left', padx=5)

        # Agregar datos al Treeview
        for i, row in df.iterrows():
            tree.insert('', 'end', values=row.tolist())

# Inicializar la aplicación
root = tk.Tk()
app = FacturaApp(root)
root.mainloop()

