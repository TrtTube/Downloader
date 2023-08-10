import youtube_dl
import tkinter
from tkinter import filedialog
import tkinter.ttk 
import tkinter.messagebox 
import sqlite3
import ffmpeg
import os
import subprocess
import customtkinter
from CTkMessagebox import CTkMessagebox
from CTkTable import *
import datetime
import time
from tkinter.filedialog import askopenfilename

class Veritabani:

    def __init__(self):
        self.dbConnection = sqlite3.connect("arsivdb")
        self.dbCursor = self.dbConnection.cursor()
        self.dbCursor.execute("CREATE TABLE IF NOT EXISTS arsiv_table (id INTEGER PRIMARY KEY AUTOINCREMENT, link text, kalite text, baslik text, size text, sure text, time text)") # süre , id

    def __del__(self):
        self.dbCursor.close()
        self.dbConnection.close()

    def Giris(self, link, kalite, baslik, size, sure, time):
        self.dbCursor.execute("INSERT INTO arsiv_table (link, kalite, baslik, size, sure, time) VALUES (?, ?, ?, ?, ?, ?)", (link, kalite, baslik, size , sure, time))
        self.dbConnection.commit()

    def Görüntüle(self):
        self.dbCursor.execute("SELECT * FROM arsiv_table")
        records = self.dbCursor.fetchall() #fetchall metoduyla bütün verileri records adlı değişkene atadık
        return records

class Values:
    def Validate(self, link):

        if str(link).count("https://") == 0:
            return "link"
        else:
            return "SUCCESS"

class HomePage(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        
        # configure window
        self.title("xFirması")
        self.geometry(f"{1100}x{580}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)
        self.SidebarOlustur()

    def SidebarOlustur(self):
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=5, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Main", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, text="Download", command=self.download_menu)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, text="Arşiv", command=self.Görüntüle)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, text="Quit", command=self.destroy)
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)
        self.sidebar_button_4 = customtkinter.CTkButton(self.sidebar_frame, text="Convert", command=self.donustur_menu)
        self.sidebar_button_4.grid(row=4, column=0, padx=20, pady=10)

        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Tema", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="Ölçek", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))


    def Görüntüle(self):
        self.IcerikTemizle()
        self.SidebarOlustur()

        self.veritabani = Veritabani()
        self.data = self.veritabani.Görüntüle()

        self.title("Database")

        self.name_label = customtkinter.CTkLabel(self.sidebar_frame, text="          DB          ", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.name_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.dbConnection = sqlite3.connect("arsivdb")
        self.dbCursor = self.dbConnection.cursor()
        self.dbCursor.execute("CREATE TABLE IF NOT EXISTS arsiv_table (id INTEGER PRIMARY KEY AUTOINCREMENT, link text, kalite text, baslik text, size text, sure text, time text)") # süre , id

        self.dbCursor.execute("SELECT * FROM arsiv_table")
        results = self.dbCursor.fetchall()
        self.dbConnection.close()
        self.baslik = customtkinter.CTkLabel(self, text="HISTORY", font=customtkinter.CTkFont(size=20, weight="normal"))
        self.baslik.grid(row=0, column=1, padx=0, pady=(0, 0))

        table = CTkTable(self, row=5, column=6, values=results)
  
        liste=["ID","LINK","QUALITY","BASLIK","SIZE","DURATION","TIME"]
        table.add_row(index=0,values=liste)
        table.grid(row=1, column=1, padx=(20, 20), pady=(20, 20), sticky="nsew")

        self.dbConnection.close()
            
    def download_menu(self):
        self.IcerikTemizle()
        self.SidebarOlustur()
           
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Downloader", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.entry = customtkinter.CTkEntry(self, placeholder_text="Paste Url")
        self.entry.grid(row=3, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.main_button_1 = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"),text="Search" ,command=self.Search)
        self.main_button_1.grid(row=3, column=2, padx=(20, 20), pady=(20, 0), sticky="nsew")

        self.output_directory_entry = customtkinter.CTkEntry(self, placeholder_text="Select Folder")
        self.output_directory_entry.grid(row=4, column=1, padx=(20, 0), pady=(20, 5), sticky="nsew")

        self.main_button_2 = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"),text="Select",command=self.select_output_directory)
        self.main_button_2.grid(row=4, column=2, padx=(20, 20), pady=(20, 5), sticky="nsew")


    def select_output_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.output_directory_entry.delete(0, tkinter.END)
            self.output_directory_entry.insert(tkinter.END, directory)

    def download_file(self):
        self.values = Values()
        self.veritabani = Veritabani()
        self.test = self.values.Validate(self.entry.get())
        print(self.entry.get())
        current_time = datetime.datetime.now()
        formatted_time = current_time.strftime("%d-%m-%Y-%H-%M-%S")

        video_link = self.sozluk[self.optionmenu_1.get()]
        print(video_link)
        self.output_directory = self.output_directory_entry.get()
        
        try:
            ydl_opts = {
                'outtmpl': os.path.join(self.output_directory, f'{formatted_time}.%(ext)s'),
                'progress_hooks': [self.update_progress]
            }
            
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                if self.test == "SUCCESS":
                    info_dict = ydl.extract_info(video_link, download=False)  # Video bilgilerini al
                    resulation = [i['format_id'] for i in info_dict['formats']]
                    title = info_dict.get('title', None)
                    sure = info_dict.get('duration', None)
                    size=0
                    print (sure)
                    print(resulation)

                    ydl.download([video_link])
                    tkinter.messagebox.showinfo("download complate", "indirme başladı")

                else:
                    self.valueErrorMessage = "Invalid input in field " + self.test
                    tkinter.messagebox.showerror("Value Error", self.valueErrorMessage)
                
                if title is not None:
                    # Dosya yolunu oluştur
                    self.file_name = formatted_time + ".mp4"
                    tkinter.messagebox.showinfo("Dosya yolu", self.file_name)

                else:
                    tkinter.messagebox.showinfo("Hata", "Dosya adı alınamadı.")
        except:
            tkinter.messagebox.showinfo("error", "indirme başarılı")
        self.veritabani.Giris(video_link, self.optionmenu_1.get(), title, size, sure, formatted_time)
        CTkMessagebox(title= "SUCCESS", message="veritabanına ekleme işlemi başarılı" , option_1="Tamam") 
    
    def update_progress(self, data):
        if data['status'] == 'downloading':
            self.slider_progressbar_frame = customtkinter.CTkFrame(self, fg_color="transparent")
            self.slider_progressbar_frame.grid(row=1, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
            self.slider_progressbar_frame.grid_columnconfigure(0, weight=1)
            self.slider_progressbar_frame.grid_rowconfigure(4, weight=1)
            
            self.progressbar_1 = customtkinter.CTkProgressBar(self.slider_progressbar_frame)
            self.progressbar_1.grid(row=1, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
            self.slider_progressbar_frame['maximum'] = data['total_bytes']
            self.slider_progressbar_frame['value'] = data['downloaded_bytes']
            self.progressbar_1.set(data['downloaded_bytes'])

    def Search(self):
        self.values = Values()
        self.veritabani = Veritabani()
        self.test = self.values.Validate(self.entry.get())
        try:
            with youtube_dl.YoutubeDL() as ydl:
                if self.test == "SUCCESS":
                    info_dict = ydl.extract_info(self.entry.get(), download=False)  # Video bilgilerini al
                    print (info_dict)
                    resulation = [i['format_id'] for i in info_dict['formats']]
                    links = [format['url'] for format in info_dict['formats']]
                    self.sozluk={}
                    for i in range(len(links)):
                        self.sozluk[resulation[i]]=links[i]

                    print(resulation)
                    print(links)
                    print(self.sozluk)

                else:
                    self.valueErrorMessage = "Invalid input in field " + self.test
                    tkinter.messagebox.showerror("Value Error", self.valueErrorMessage)
                
        except:
            tkinter.messagebox.showinfo("error", "indirme başarılı")

        self.tabview = customtkinter.CTkTabview(self, width=250)
        self.tabview.grid(row=0, column=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.tabview.add("Format")
        self.tabview.tab("Format").grid_columnconfigure(0, weight=1)  

        self.optionmenu_1 = customtkinter.CTkOptionMenu(self.tabview.tab("Format"), dynamic_resizing=False,values=resulation)
        self.optionmenu_1.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.download_button = customtkinter.CTkButton(self.tabview.tab("Format"), text="İndir",command=self.download_file)
        self.download_button.grid(row=2, column=0, padx=20, pady=(10, 10))

        print(self.optionmenu_1.get())
        CTkMessagebox(title= "info", message="tercihler kaydedildi\n Quality : {}\n" .format(self.optionmenu_1.get()), option_1="Tamam") 

    def destroy(self):
        msg = CTkMessagebox(title="Çıkış?", message="Çıkış yapmak istediğinize emin misiniz?",icon="question", option_1="Hayır", option_3="Evet")
        response = msg.get()
    
        if response=="Evet":
            tkinter.Tk.destroy(self)  
        else:
            print("Çıkış için 'Evet' e tıkla!")

    def donustur_menu(self):
        self.IcerikTemizle()
        self.SidebarOlustur()

        self.convert_directory = customtkinter.CTkEntry(self, placeholder_text="Select Folder")
        self.convert_directory.grid(row=4, column=1, padx=(20, 0), pady=(20, 5), sticky="nsew")

        self.main_button_2 = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"),text="Select",command=self.dosya)
        self.main_button_2.grid(row=4, column=2, padx=(20, 20), pady=(20, 5), sticky="nsew")
        self.main_button_1 = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"),text="convert",command=self.convert)
        self.main_button_1.grid(row=3, column=2, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.tabview = customtkinter.CTkTabview(self, width=250)
        self.tabview.grid(row=0, column=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.tabview.add("Format")
        self.tabview.tab("Format").grid_columnconfigure(0, weight=1)  

        self.optionmenu_1 = customtkinter.CTkOptionMenu(self.tabview.tab("Format"), dynamic_resizing=False,
                                                        values=["mp4", "avi", "wmv", "mkv", "mp3"])
        self.optionmenu_1.grid(row=0, column=0, padx=20, pady=(20, 10))

    def dosya(self):
        directory = askopenfilename()
        if directory:
            self.convert_directory.delete(0, tkinter.END)
            self.convert_directory.insert(tkinter.END, directory)

    def convert(self):
        input_file=self.convert_directory.get()
        format=self.optionmenu_1.get()
        output_file=filedialog.asksaveasfilename(defaultextension=f'.{format}', filetypes=[(f'{format.upper()} Dosyaları', f'.{format}')])
        if format=="mp3":
            command = ['ffmpeg', '-i', input_file, '-vn', '-ar', '44100', '-ac', '2', '-b:a', '192k', output_file]
        else:
            command = f'ffmpeg -i "{input_file}" -c:v libx264 -c:a aac -strict experimental "{output_file}"'
        try:
            # subprocess modülü ile komutu çalıştır
            subprocess.run(command, check=True)
            print("Dönüşüm tamamlandı!")
        except subprocess.CalledProcessError as e:
            print("Dönüşüm hatası:", e)

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)
    def IcerikTemizle(self):
        for widget in self.winfo_children():
            widget.destroy()

        self.SidebarOlustur()

if __name__ == "__main__":
    homePage = HomePage()
    homePage.mainloop()
