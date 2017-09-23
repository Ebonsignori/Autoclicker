import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
import pyautogui as pag
import winsound as ws
from pynput import keyboard
import time


class ImageNotFoundEx(Exception):
    """ Custom Exception for returning screenshot that can't be found """
    def __init__(self, screenShotArguments):
        Exception.__init__(self, screenShotArguments)
        self.screenShotArguments = screenShotArguments


class MyListener(keyboard.Listener):
    def __init__(self):
        super(MyListener, self).__init__(self.on_press, self.on_release)
        self.key_pressed = None

    def on_press(self, key):
        self.key_pressed = key

    def on_release(self, key):
        self.key_pressed = key


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.images = list()
        self.regions = dict()
        self.play_sounds = True
        self.pack()
        self.create_widgets()
        self.listener = MyListener()
        self.listener.start()

    def create_widgets(self):
        self.headings_frame = tk.Frame()
        self.headings_frame.pack(side="top", fill="x", expand="true")

        self.options_heading = ttk.Label(self.headings_frame, justify="left", width=10, text="Parameters", font="TkDefaultFont 12 bold")
        self.options_heading.pack(side="left")
        self.hover_for_details_heading = ttk.Label(self.headings_frame, justify="left", width=18, text="*Hover for Details*", font="TkDefaultFont 8", foreground="blue")
        self.hover_for_details_heading.pack(side="left")
        self.selections_heading = ttk.Label(self.headings_frame, justify="right", width=8, text="Selection", font="TkDefaultFont 12 bold")
        self.selections_heading.pack(side="right")

        self.num_of_options_frame = tk.Frame()
        self.num_of_options_frame.pack(fill="x", expand="true")

        self.top_options_sep = ttk.Separator(self.num_of_options_frame, orient="horizontal")
        self.top_options_sep.pack(side="top", fill="x", expand="true", pady=5)

        self.num_of_img_label_default_text = "How many screenshots to alternate between?"
        self.num_of_img_options_label = ttk.Label(self.num_of_options_frame, justify="left", width=55, text=self.num_of_img_label_default_text, font="TkDefaultFont 8")
        self.num_of_img_options_label.default = self.num_of_img_label_default_text
        self.num_of_img_options_label.tooltip = "Program cycles through provided screenshots."
        self.num_of_img_options_label.pack(side="left", padx=2, pady=2)

        self.num_of_img_options = [1, 2, 3, 4, 5, 6, 7, 8]
        self.num_of_img_dropdown = ttk.Combobox(self.num_of_options_frame)
        self.num_of_img_dropdown["values"] = self.num_of_img_options
        self.num_of_img_dropdown["justify"] = "center"
        self.num_of_img_dropdown["width"] = "5"
        self.num_of_img_dropdown.pack(side="right", padx=2, pady=2)
        self.num_of_img_dropdown.bind("<<ComboboxSelected>>", lambda x: self.select_screenshots_btn.configure(state="normal"))

        self.num_of_clicks_frame = tk.Frame()
        self.num_of_clicks_frame.pack(fill="x", expand="true")

        self.num_of_clicks_label_default_text = "How many clicks at each screenshot?"
        self.num_of_clicks_label = ttk.Label(self.num_of_clicks_frame, justify="left", text=self.num_of_clicks_label_default_text, width=55, font="TkDefaultFont 8")
        self.num_of_clicks_label.default = self.num_of_clicks_label_default_text
        self.num_of_clicks_label.tooltip = "1, 2, 5, 25, or -1 for infinite clicks."
        self.num_of_clicks_label.pack(side="left", padx=2, pady=2)

        self.num_of_clicks_entry = ttk.Entry(self.num_of_clicks_frame, width=8, font="TkDefaultFont 8", justify="center")
        self.num_of_clicks_entry.insert(0, "-1 for inf.")
        self.num_of_clicks_entry.pack(side="right", padx=2, pady=2)
        self.num_of_clicks_entry.bind("<Button-1>", self.ClearText)

        self.clicks__interval_frame = tk.Frame()
        self.clicks__interval_frame.pack(fill="x", expand="true")

        self.clicks_interval_default_text = "Seconds Between Each Click?"
        self.clicks_interval_label = ttk.Label(self.clicks__interval_frame, text=self.clicks_interval_default_text, justify="left", width=55, font="TkDefaultFont 8")
        self.clicks_interval_label.default = self.clicks_interval_default_text  
        self.clicks_interval_label.tooltip = "If you have more than one click. \".5\" for half a second."
        self.clicks_interval_label.pack(side="left", padx=2, pady=2)

        self.clicks_interal_entry = ttk.Entry(self.clicks__interval_frame, width=8, font="TkDefaultFont 8", justify="center")
        self.clicks_interal_entry.insert(0, "-1 for inf.")
        self.clicks_interal_entry.pack(side="right", padx=2, pady=2)
        self.clicks_interal_entry.bind("<Button-1>", self.ClearText)

        self.indp_options_frame = tk.Frame()
        self.indp_options_frame.pack(fill="x", expand="true")

        self.indp_options_label_default_text = "Are images independent of one another?"
        self.indp_options_label = ttk.Label(self.indp_options_frame, justify="left", width=55, text=self.indp_options_label_default_text, font="TkDefaultFont 8")
        self.indp_options_label.tooltip = "Does the first need to be clicked in order for the second to appear?"
        self.indp_options_label.default = self.indp_options_label_default_text
        self.indp_options_label.pack(side="left", padx=2, pady=2)

        self.indp_options = ["Yes", "No"]
        self.indp_options_dropdown = ttk.Combobox(self.indp_options_frame)
        self.indp_options_dropdown["values"] = self.indp_options
        self.indp_options_dropdown["justify"] = "center"
        self.indp_options_dropdown["width"] = "5"
        self.indp_options_dropdown.pack(side="right", padx=2, pady=2)

        self.iterations_frame = tk.Frame()
        self.iterations_frame.pack(fill="x", expand="true")

        self.iterations_label_default_text = "Loop for?"
        self.iterations_label = ttk.Label(self.iterations_frame, justify="left", width=55, text=self.iterations_label_default_text, font="TkDefaultFont 8")
        self.iterations_label.tooltip = "Alternate between screenshots \"X\" times. -1 for infinite loop"
        self.iterations_label.default = self.iterations_label_default_text
        self.iterations_label.pack(side="left", padx=2, pady=2)

        self.iterations_entry = ttk.Entry(self.iterations_frame, width=8, font="TkDefaultFont 8", justify="center")
        self.iterations_entry.insert(0, "-1 for inf.")
        self.iterations_entry.pack(side="right", padx=2, pady=2)
        self.iterations_entry.bind("<Button-1>", self.ClearText)

        self.buttons_frame = tk.Frame()
        self.buttons_frame.pack(fill="x", expand="true")

        self.bottom_options_sep = ttk.Separator(self.buttons_frame, orient="horizontal")
        self.bottom_options_sep.pack(side="top", fill="x", expand="true", pady=5)

        self.select_screenshots_btn = ttk.Button(self.buttons_frame, width=25, text="Select Screenshot(s)", command=self.get_images, state="disabled")
        self.select_screenshots_btn.pack(side="left", padx=20, pady=4)

        self.bottom_options_vert_sep = ttk.Separator(self.buttons_frame, orient="vertical")
        self.bottom_options_vert_sep.pack(side="left", fill="y", expand="true")

        self.locate_confirm_btn = ttk.Button(self.buttons_frame, width=25, text="Find Selection On Screen", command=self.BeginLocating, state="disabled")
        self.locate_confirm_btn.pack(side="right", padx=20, pady=4)

        self.run_frame = tk.Frame()
        self.run_frame.pack(fill="x")

        self.begin_btn = ttk.Button(self.run_frame, width=25, text="RUN", command=self.BeginAutoClick, state="disabled")
        self.begin_btn.pack(ipady=4, ipadx=4, pady=3, padx=3)
        
        self.run_frame_sep = ttk.Separator(self.run_frame, orient="horizontal")
        self.run_frame_sep.pack(fill="x", expand="true", pady=3)

        self.configs_frame = tk.Frame()
        self.configs_frame.pack(fill="x", expand="true", pady=3)

        self.configs_label = ttk.Label(self.configs_frame, text="Configurations", font="TkDefaultFont 10 bold")
        self.configs_label.pack(side="top", )

        self.single_config_btn = ttk.Button(self.configs_frame, width=20, text="Single Screenshot", command=self.single_config)
        self.single_config_btn.pack(side="left", padx=2)
       
        self.save_btn = ttk.Button(self.configs_frame, width=20, text="Save Config", command=self.save_config)
        self.save_btn.pack(side="left", padx=2)

        self.load_btn = ttk.Button(self.configs_frame, width=20, text="Load Config", command=self.load_config)
        self.load_btn.pack(side="left", padx=2)

        self.status_frame = tk.Frame()
        self.status_frame.pack(fill="x", expand="true", pady=5)

        self.status_frame_sep = ttk.Separator(self.status_frame, orient="horizontal")
        self.status_frame_sep.pack(fill="x", expand="true", pady=5)

        self.status_label = ttk.Label(self.status_frame, width="max-width", text="No Screenshots Selected", justify="center", font="TkDefaultFont 10 italic")
        self.status_label.pack(side="bottom")

        for widget in (self.num_of_img_options_label, self.indp_options_label, self.iterations_label, self.num_of_clicks_label, self.clicks_interval_label):
            widget.bind("<Enter>", self.tooltip_mouse_enter)
            widget.bind("<Leave>", self.tooltip_mouse_leave)

    def status(self, msg):
        self.status_label.configure(text=msg)

    def single_config(self):
        self.num_of_img_dropdown.set(1)
        self.select_screenshots_btn.configure(state="normal")

        self.num_of_clicks_entry.delete(0, 9999)
        self.num_of_clicks_entry.insert(0, "-1")

        self.clicks_interal_entry.delete(0, 9999)
        self.clicks_interal_entry.insert(0, "-1")

        self.indp_options_dropdown.set("Yes")

        self.iterations_entry.delete(0, 9999)
        self.iterations_entry.insert(0, "1")

        self.status("Single screenshot config loaded. Select an image.")

    def save_config(self):
        save_loc = filedialog.asksaveasfilename(title="Choose where to save your config file", defaultextension=".txt", filetypes=((".txt files", "*.txt"), ("all files", "*.*")))
        self.num_of_imgs = int(self.num_of_img_dropdown.get())
        self.clicks = int(self.num_of_clicks_entry.get())
        self.interval = int(float(self.clicks_interal_entry.get()))
        self.independence = str(self.indp_options_dropdown.get())
        self.iterations = int(self.iterations_entry.get())

        save_file = open(save_loc, "w")
        for var in self.num_of_imgs, self.clicks, self.interval, self.independence, self.iterations:
            save_file.write(str(var) + "*")

        if len(self.images) > 0:
            save_file.write(str(len(self.images)) + "*")
            for img in self.images:
                save_file.write(str(img) + "*")
                if len(self.regions) > 0:
                    save_file.write(str(self.regions[img]))
                else:
                    save_file.write("0")
        else:
            save_file.write("0")
        save_file.close()

        if self.play_sounds is True:
            ws.PlaySound("sounds/correct_2.wav", ws.SND_FILENAME)
        self.status("File saved succesfully. \n If you move image files it will break.")

    def load_config(self):
        save_loc = filedialog.askopenfilename(title="Choose where to save your config file", defaultextension=".txt", filetypes=((".txt files", "*.txt"), ("all files", "*.*")))
        save_file = open(save_loc, "r")
        save_data = list()
        for line in save_file:
            save_data = line.split("*")

        self.num_of_imgs = int(save_data[0])
        self.num_of_img_dropdown.set(str(save_data[0]))

        self.num_of_clicks_entry.delete(0, 9999)
        self.num_of_clicks_entry.insert(0, str(save_data[1]))

        self.clicks_interal_entry.delete(0, 9999)
        self.clicks_interal_entry.insert(0, str(save_data[2]))

        self.indp_options_dropdown.set(str(save_data[3]))

        self.iterations_entry.delete(0, 9999)
        self.iterations_entry.insert(0, str(save_data[4]))

        num_of_saved_imgs = int(save_data[5])
        previous_saved_vars = 6
        del self.images[:]
        self.regions.clear()
        i = 0
        while i < (2 * num_of_saved_imgs):
            img = str(save_data[previous_saved_vars + i])
            self.images.append(img)
            self.regions[save_data[previous_saved_vars + i]] = save_data[previous_saved_vars + i + 1]
            i += 2

        self.locate_confirm_btn["state"] = "normal"
        self.select_screenshots_btn["state"] = "normal"

        if self.play_sounds is True:
            ws.PlaySound("sounds/correct_2.wav", ws.SND_FILENAME)
        self.status("Configuration Loaded Succesfully. \n Press RUN.")

    def tooltip_mouse_enter(self, event):
        tooltip_label = getattr(event.widget, "tooltip", "")
        event.widget.configure(text=tooltip_label, font="TkDefaultFont 8", cursor="question_arrow", foreground="blue")

    def tooltip_mouse_leave(self, event):
        default_label = getattr(event.widget, "default", "")
        event.widget.configure(text=default_label, font="TkDefaultFont 8", foreground="black")

    def ClearText(self, event):
        event.widget.delete(0, 9999)

    def get_images(self):
        self.num_of_imgs = int(self.num_of_img_dropdown.get())
        del self.images[:]
        for i in range(self.num_of_imgs):
            self.images.append(filedialog.askopenfilename(title="Select Image #" + str(i + 1), defaultextension=".txt", filetypes=(("Image Files", "*.png;*.jpeg;*.jpg"), ("all files", "*.*"))))
        self.locate_confirm_btn.configure(state="normal")
        if "" in self.images:
            self.status_label.configure(text="Please Select " + str(self.num_of_imgs) + " screenshots.")
        self.status_label.configure(text="Screenshots Selected")

    def ImageNotFoundPopup(self, msg):
        self.status_label.configure(text="Screenshot(s) Not On Screen")
        popup = tk.Tk()
        popup.wm_title("Image Not Found!")
        label = ttk.Label(popup, justify="center", text=msg + "Please make sure the screenshot you selected is visible on your primary monitor before running.")
        label.pack(side="top", fill="x", pady=10)
        B1 = ttk.Button(popup, text="Okay", command=popup.destroy)
        B1.pack()
        popup.mainloop()

    def TraceImageRegion(self):
        i = 0
        for img in self.images:
            i = i + 1
            try:
                l, t, w, h = pag.locateOnScreen(img, minSearchTime=5)
                w = w + 5
                h = h + 5
                self.regions[img] = [l, t, w, h]
                self.status_label.configure(text="Found" + img)
            except Exception as e:
                raise(ImageNotFoundEx("Image #" + str(i) + " " + img))
        self.status_label.configure(text="Screenshots Located Successully \n Click *RUN* to begin automat[E]ion.")

    def BeginLocating(self):
        self.status_label.configure(text="Searching for images on screen...")
        try:
            self.TraceImageRegion()
        except ImageNotFoundEx as inf:
            ws.PlaySound("sounds/bad_beep_1.wav", ws.SND_FILENAME)
            self.ImageNotFoundPopup("Unable to locate: \"{0}\" on your screen. \n".format(inf.args[0]))
            return
        self.begin_btn.configure(state="normal", style="green/black.TButton")
        self.status_label.configure(text="Screenshots Located Successully \n Click *RUN* to begin automat[E]ion.")
        if self.play_sounds is True:
            ws.PlaySound("sounds/correct_2.wav", ws.SND_FILENAME)

    def stop(self):
        self.status_label.configure(text="Looping Cancelled.")

    def BeginAutoClick(self):
        self.listener.key_pressed = keyboard.Key.alt
        self.iterations = int(self.iterations_entry.get())
        self.clicks = int(self.num_of_clicks_entry.get())
        self.interval = int(float(self.clicks_interal_entry.get())*1000)
        self.status_label.configure(text="Your clicking is being automated, cheers mate")
        for i in range(self.iterations):
            for j in range(self.num_of_imgs):
                self.time_taken = time.time()

                if self.listener.key_pressed is "Key.esc":
                    self.status_label.configure(text="Looping Cancelled.")
                    return

                try:
                    x, y = pag.locateCenterOnScreen(self.images[j], region=self.regions[self.images[j]])
                except TypeError as te:
                    if self.listener.key_pressed is keyboard.Key.esc:
                            self.stop
                            return
                    pag.moveTo(1, 1)
                    try:
                        if self.listener.key_pressed is keyboard.Key.esc:
                            self.stop
                            return
                        x, y = pag.locateCenterOnScreen(self.images[j], region=self.regions[self.images[j]], minSearchTime=5)
                    except TypeError as te:
                        ws.PlaySound("sounds/bad_beep_1.wav", ws.SND_FILENAME)
                        self.ImageNotFoundPopup("Unable to locate: \"{0}\" on your screen. \n".format(self.images[j]))
                
                pag.moveTo(x, y, .3)
        
                if self.clicks is -1:
                    self.interval /= 1000
                    while True:
                        if self.listener.key_pressed is keyboard.Key.esc:
                            self.stop
                            return
                        if self.interval < 0:
                            pag.click()
                        else:
                            time.sleep(self.interval)
                            pag.click()
                else:
                    for k in range(self.clicks):
                        if self.listener.key_pressed is keyboard.Key.esc:
                            self.stop
                            return
                        root.after(self.interval, pag.click())

                self.time_taken = time.time() - self.time_taken

                self.status_label.configure(text="Time Taken For Image #" + str(j) + ": " + str(round(self.time_taken, 2)) + "seconds")

        self.status_label.configure(text="Looping Completed.")
        ws.PlaySound("sounds/correct_1.wav", ws.SND_FILENAME)


if __name__ == "__main__":
    root = tk.Tk()
    app = Application(master=root)
    app.master.title("Auto[Click]Mate")
    app.master.maxsize(400, 500)
    root.iconbitmap("./img/icon.ico")
    app.mainloop()
