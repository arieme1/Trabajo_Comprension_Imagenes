import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageOps
import pywt, os
import numpy as np

class Wavelet_compressor:
    def __init__(self, root):
        self.root = root
        self.root.title("Compresor WAVELETS de imágenes")
        self.root.geometry("800x600+10+10")

        self.is_original_image   = False
        self.is_compressed_image = False

        # Título de la aplicación
        self.title_text = tk.Label(master = self.root, text = "Compresor WAVELETS de imágenes", font = ("Consolas", 25))
        self.title_text.pack(pady = 5)

        # Canvas para mostrar las imágenes
        self.frm_w = 700
        self.frm_h = 400
        self.frm_canvas = tk.Frame(master = self.root, width = self.frm_w, height = self.frm_h)
        self.frm_canvas.pack()
        self.canvas = tk.Canvas(master = self.frm_canvas, width = self.frm_w, height = self.frm_h, background = "white")
        self.canvas.pack(pady = 5)

        # Cargar imagen por defecto
        self.original_image_path = "default.jpg"
        self.load_image(self.original_image_path)
        self.update_image(image_type = "original")

        # Paneles de botones
        self.frm_master_buttons = tk.Frame(master = self.root)
        self.frm_master_buttons.pack()
        self.frm_img_buttons = tk.Frame(master = self.frm_master_buttons, relief = tk.RAISED, width = 400, height = 400, borderwidth = 2)
        self.frm_img_buttons.grid(row = 0, column = 0, padx = 10, pady = 2)
        self.frm_cmpr_buttons = tk.Frame(master = self.frm_master_buttons, relief = tk.RAISED, width = 400, height = 400, borderwidth = 2)
        self.frm_cmpr_buttons.grid(row = 0, column = 1, padx = 10, pady = 2)

        # Títulos de los paneles de botones
        self.frm_img_buttons_text = tk.Label(master = self.frm_img_buttons, text = "Opciones de imagen", font = ("Consolas", 12))
        self.frm_img_buttons_text.grid(row = 0, column = 0, columnspan = 2)
        self.frm_cmpr_buttons_text = tk.Label(master = self.frm_cmpr_buttons, text = "Control de la compresión", font = ("Consolas", 12))
        self.frm_cmpr_buttons_text.grid(row = 0, column = 0, columnspan = 4)

        # Botón de cargar imagen
        self.load_button = tk.Button(master = self.frm_img_buttons, text = "Cargar imagen", command = self.on_load_image_button_click)
        self.load_button.grid(row = 1, column = 0, padx = 1, pady = 2)

        # Label de imagen cargada
        self.image_dir_text = tk.Label(master = self.frm_img_buttons, text = self.original_image_path, background = "white", relief = tk.SUNKEN)
        self.image_dir_text.grid(row = 1, column = 1, padx = 1, pady = 2)

        # Botón para corregir orientación
        self.rotate_button = tk.Button(master = self.frm_img_buttons, text = "Corregir rotación", command = self.on_rotate_button_click)
        self.rotate_button.grid(row = 2, column = 0, columnspan = 2, padx = 1, pady = 2)

        # Botón para corregir orientación
        self.save_button = tk.Button(master = self.frm_img_buttons, text = "Guardar imagen", command = self.on_save_button_click)
        self.save_button.grid(row = 3, column = 0, columnspan = 2, padx = 1, pady = 2)

        # Label de la familia
        self.family_text = tk.Label(master = self.frm_cmpr_buttons, text = "Familia:")
        self.family_text.grid(row = 1, column = 0, padx = 1, pady = 2)

        # Dropdown para seleccionar familia
        family_options = pywt.families(short = True)
        self.family = tk.StringVar(master = self.frm_cmpr_buttons)
        self.family.set(family_options[0])
        self.family_dropdown = tk.OptionMenu(self.frm_cmpr_buttons, self.family, *family_options, command = self.on_family_dropdown_change)
        self.family_dropdown.grid(row = 1, column = 1, padx = 1, pady = 2)

        # Label de la wavelet
        self.wavelet_text = tk.Label(master = self.frm_cmpr_buttons, text = "Wavelet:")
        self.wavelet_text.grid(row = 1, column = 2, padx = 1, pady = 2)

        # Dropdown para seleccionar wavelet
        wavelet_options = pywt.wavelist(family = self.family.get())
        self.wavelet = tk.StringVar(master = self.frm_cmpr_buttons)
        self.wavelet.set(wavelet_options[0])
        self.wavelet_dropdown = tk.OptionMenu(self.frm_cmpr_buttons, self.wavelet, *wavelet_options)
        self.wavelet_dropdown.grid(row = 1, column = 3, padx = 1, pady = 2)

        # Label del threshold
        self.threshold_text = tk.Label(master = self.frm_cmpr_buttons, text = "Threshold")
        self.threshold_text.grid(row = 2, column = 0, padx = 1, pady = 2)

        # Input numérico del threshold
        self.threshold = tk.StringVar(master = self.frm_cmpr_buttons)
        self.threshold.set("200")
        self.threshold_spinbox = tk.Spinbox(master = self.frm_cmpr_buttons, width = 10, from_ = 1, to = 500, textvariable = self.threshold)
        self.threshold_spinbox.grid(row = 2, column = 1, padx = 1, pady = 2)

        # Botón de comprimir imagen
        self.compress_button = tk.Button(master = self.frm_cmpr_buttons, text = "Comprimir imagen", command = self.on_compress_button_click)
        self.compress_button.grid(row = 3, column = 0, columnspan = 4, padx = 1, pady = 2)
    
    def on_load_image_button_click(self):
        image_path = filedialog.askopenfilename(title = "Seleccionar imagen", filetypes = [("Archivos de imagen", "*.png;*.jpg;*.jpeg;*.gif;gorila")])
        if image_path:
            self.load_image(image_path)
            self.update_image(image_type = "original")

    def load_image(self, image_path, rotate = False):
        image_obj = Image.open(image_path)
        img_array = np.array(image_obj)
        if rotate:
            img_array = np.fliplr(np.transpose(img_array, (1, 0, 2)))
            image_obj = Image.fromarray(img_array)
        image_obj = image_obj.resize((int(self.frm_w / 2), self.frm_h), Image.LANCZOS) # CALCULAR RESIZE PARA MANTENER PROPORCIONES
        image_obj = ImageTk.PhotoImage(image_obj)
        self.original_image_path  = image_path
        self.original_image_array = img_array
        self.original_image       = image_obj
        self.is_original_image = True

    def on_rotate_button_click(self):
        if self.is_original_image:
            self.load_image(self.original_image_path, rotate = True)
            self.update_image(image_type = "original")

    def update_image(self, image_type):
        if image_type == "original":
            if self.is_original_image:
                self.canvas.create_image(0, 0, anchor = tk.NW, image = self.original_image)
            else:
                messagebox.showerror('Error', 'dev_Error: cannot display the original image.')
        elif image_type == "compressed":
            if self.is_compressed_image:
                self.canvas.create_image(int(self.frm_w / 2), 0, anchor = tk.NW, image = self.compressed_image)
            else:
                messagebox.showerror('Error', 'dev_Error: cannot display the compressed image.')
        else:
            messagebox.showerror('Error', f'dev_Error: opción <<{image_type}>> de image_type no implementada.')
        return self
    
    def on_save_button_click(self, output_format = ".jpg"):
        if self.is_compressed_image:
            output_image_path = filedialog.asksaveasfile(defaultextension = "jpg")
            if output_image_path:
                last_period_index = output_image_path.name.rfind('.')
                if last_period_index == -1 or last_period_index < output_image_path.name.rfind('/'):
                    output_image_path = output_image_path.name + output_format
                else:
                    current_extension = output_image_path.name[last_period_index + 0:]
                    if current_extension != output_format:
                        output_image_path = output_image_path.name[:last_period_index] + output_format
                    else:
                        output_image_path = output_image_path.name
                compressed_image_uint8 = np.clip(self.compressed_image_array, 0, 255).astype(np.uint8)
                img_to_save = Image.fromarray(compressed_image_uint8)
                try:
                    img_to_save.save(output_image_path)
                except KeyError as e:
                    messagebox.showwarning('Error', f'No es posible guardar la imagen en {output_image_path}: {e}.')
                except IOError as e:
                    messagebox.showwarning('Error', f'No es posible guardar la imagen en {output_image_path}: {e}.')
                else:
                    answer = messagebox.askyesno('Imagen guardada', 'La imagen se ha guardado correctamente.\n¿Quiere guardar el fichero de metadatos de la compresión?')
                    if answer:
                        original_size = os.path.getsize(self.original_image_path) / 1024 # kB
                        compressed_size = os.path.getsize(output_image_path) / 1024 # kB
                        compression_perc = ((original_size - compressed_size) / original_size) * 100
                        last_period_index = output_image_path.rfind('.')
                        metadata_path = output_image_path[:last_period_index] + '.txt'
                        metadata = f"MetaDatos de la compresión de la imagen: {self.original_image_path}\n\n" +\
                            f" - Imagen comprimida: {output_image_path}\n" +\
                            f" - Familia de wavelets: {self.used_config['f']}\n" +\
                            f" - Wavelet: {self.used_config['w']}\n" +\
                            f" - Threshold: {self.used_config['t']}\n\n" +\
                            f" - Tamaño de la imagen original: {original_size} kB\n" +\
                            f" - Tamaño de la imagen comprimida: {compressed_size} kB\n" +\
                            f" - Porcentaje de compresión: {round(compression_perc)} %\n"
                        with open(metadata_path, "w") as f:
                            f.write(metadata)
                    messagebox.showinfo('Guardado completado', 'Los resultados se han guardado correctamente.')
            else:
                messagebox.showwarning('Error', 'El directorio seleccionado no es válido.')
        else:
            messagebox.showwarning("Error", 'Debe crear una imagen comprimida para poder guardarla.')

    def on_family_dropdown_change(self, *args):
        self.wavelet.set('')
        self.wavelet_dropdown['menu'].delete(0, 'end')
        wavelet_options = pywt.wavelist(family = self.family.get(), kind = 'discrete')
        for option in wavelet_options:
            self.wavelet_dropdown['menu'].add_command(label = option, command=tk._setit(self.wavelet, option))
        self.wavelet.set(wavelet_options[0])

    def on_compress_button_click(self):
        status = self.compress_image()
        if status:
            self.update_image(image_type = "compressed")

    def compress_image(self, default_threshold = 200):
        wavelet = self.wavelet.get()
        try:
            threshold = float(self.threshold.get())
        except ValueError as e:
            messagebox.showwarning("Error", str(e))
            threshold = default_threshold
            self.threshold.set(str(threshold))
        else:
            if threshold <= 0 or threshold > 500:
                messagebox.showwarning("Error", 'El threshold debe ser positivo y menor que 500.')
                threshold = default_threshold
                self.threshold.set(str(threshold))
        self.used_config = {'f': self.family.get(), 'w': wavelet, 't': threshold}
        img_array = self.original_image_array
        r, g, b = img_array[:, :, 0], img_array[:, :, 1], img_array[:, :, 2]

        # Aplicar wavelet en cada canal y hallar coeficientes
        def apply_wavelet(channel, wavelet):
            try:
                coeffs = pywt.dwt2(channel, wavelet)
            except ValueError as e:
                messagebox.showwarning("Error", str(e))
                coeffs = False
            else:
                cA, (cH, cV, cD) = coeffs
            return coeffs

        # Coeficientes R, G y B
        r_coeffs = apply_wavelet(r, wavelet)
        g_coeffs = apply_wavelet(g, wavelet)
        b_coeffs = apply_wavelet(b, wavelet)

        if all((r_coeffs, g_coeffs, b_coeffs)):
            cA, (cH, cV, cD) = r_coeffs
            r_coeffs = cA, cH, cV, cD
            cA, (cH, cV, cD) = g_coeffs
            g_coeffs = cA, cH, cV, cD
            cA, (cH, cV, cD) = b_coeffs
            b_coeffs = cA, cH, cV, cD
        else:
            return False

        # Meter threshold en coeficientes para la compresión
        r_coeffs_compressed = [pywt.threshold(i, value = threshold, mode = 'garrote') for i in r_coeffs]
        g_coeffs_compressed = [pywt.threshold(i, value = threshold, mode = 'garrote') for i in g_coeffs]
        b_coeffs_compressed = [pywt.threshold(i, value = threshold, mode = 'garrote') for i in b_coeffs]

        # Reconstrucción de canales tras la compresión
        def reconstruct_channel(cA, cH, cV, cD, wavelet_type):
            coeffs = (cA, (cH, cV, cD))
            reconstructed_channel = pywt.idwt2(coeffs, wavelet_type)
            return reconstructed_channel

        reconstructed_r = reconstruct_channel(*r_coeffs_compressed, wavelet)
        reconstructed_g = reconstruct_channel(*g_coeffs_compressed, wavelet)
        reconstructed_b = reconstruct_channel(*b_coeffs_compressed, wavelet)

        # Reconstrucción de la imagen a partir de los canales
        reconstructed_image_array = np.stack((reconstructed_r, reconstructed_g, reconstructed_b), axis=-1)
        reconstructed_image_array = np.clip(reconstructed_image_array, 0, 255).astype(np.uint8)
        reconstructed_image = Image.fromarray(reconstructed_image_array)
        reconstructed_image = reconstructed_image.resize((int(self.frm_w / 2), self.frm_h), Image.LANCZOS) # CALCULAR RESIZE PARA MANTENER PROPORCIONES
        self.compressed_image_array = reconstructed_image_array
        self.compressed_image = ImageTk.PhotoImage(reconstructed_image)
        self.is_compressed_image = True
        return True

if __name__ == "__main__":
    root = tk.Tk()
    app = Wavelet_compressor(root)
    root.mainloop()
