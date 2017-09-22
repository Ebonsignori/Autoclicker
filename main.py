import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
import pyautogui as pag
import winsound as ws
from autoclickmate import move_2_mouse


class ImageNotFoundEx(Exception):
    """ Custom Exception for returning screenshot that can't be found """
    def __init__(self, screenShotArguments):
        Exception.__init__(self, screenShotArguments)
        self.screenShotArguments = screenShotArguments


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.images = list()
        self.regions = dict()
        self.pack()
        self.create_widgets()

    def create_widgets(self):

        self.headings_frame = tk.Frame()
        self.headings_frame.pack(side="top", fill="x", expand="true")
        self.options_heading = ttk.Label(self.headings_frame, justify="left", width=7, text="Options", font="TkDefaultFont 12 bold")
        self.options_heading.pack(side="left")
        self.hover_for_details_heading = ttk.Label(self.headings_frame, justify="left", width=18, text="*Hover for Details*", font="TkDefaultFont 8", foreground="blue")
        self.hover_for_details_heading.pack(side="left")
        self.selections_heading = ttk.Label(self.headings_frame, justify="right", width=14, text="Select An Option", font="TkDefaultFont 12 bold")
        self.selections_heading.pack(side="right")

        self.num_of_options_frame = tk.Frame()
        self.num_of_options_frame.pack(fill="x", expand="true")

        self.num_of_img_label_default_text = "How many screenshots to alternate between?"
        self.num_of_img_options_label = ttk.Label(self.num_of_options_frame, justify="left", width=55, text=self.num_of_img_label_default_text, font="TkDefaultFont 8")
        self.num_of_img_options_label.default = self.num_of_img_label_default_text
        self.num_of_img_options_label.pack(side="left", padx=2, pady=2)

        self.num_of_img_options = [1, 2, 3]
        self.num_of_img_dropdown = ttk.Combobox(self.num_of_options_frame)
        self.num_of_img_dropdown["values"] = self.num_of_img_options
        self.num_of_img_dropdown["justify"] = "center"
        self.num_of_img_dropdown["width"] = "5"
        self.num_of_img_dropdown.pack(side="right", padx=2, pady=2)
        self.num_of_img_dropdown.bind("<<ComboboxSelected>>", lambda x: self.run_img_alt_btn.configure(state="normal"))

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
        self.iterations_label.tooltip = "Alternate between screenshots \"X\" times"
        self.iterations_label.default = self.iterations_label_default_text
        self.iterations_label.pack(side="left", padx=2, pady=2)

        self.iterations_options = ["1", "2", "3", "5", "10", "25", "50", "100", "1000", "inf."]
        self.iterations_options_dropdown = ttk.Combobox(self.iterations_frame)
        self.iterations_options_dropdown["values"] = self.iterations_options
        self.iterations_options_dropdown["justify"] = "center"
        self.iterations_options_dropdown["width"] = "5"
        self.iterations_options_dropdown.pack(side="right", padx=2, pady=2)

        self.buttons_frame = tk.Frame()
        self.buttons_frame.pack(fill="x", expand="true")

        self.run_img_alt_btn = ttk.Button(self.buttons_frame, width=25, text="Select screenshots", command=self.get_images, state="disabled")
        self.run_img_alt_btn.pack(side="left", padx=20, pady=2)

        self.locate_confirm_btn = ttk.Button(self.buttons_frame, width=25, text="Confirm Images", command=self.BeginLocating, state="disabled")
        self.locate_confirm_btn.pack(side="right", padx=20, pady=2)

        self.status_frame = tk.Frame()
        self.status_frame.pack(fill="x", expand="true")

        self.begin_btn = ttk.Button(self.status_frame, width=25, text="RUN", command=self.BeginAutoClick, state="disabled")
        self.begin_btn.pack(side="top", ipady=4)
        self.status_label = ttk.Label(self.status_frame, width="max-width", text="No Screenshots Selected", justify="center", font="TkDefaultFont 10 bold")
        self.status_label.pack(side="bottom")

        for widget in (self.num_of_img_options_label, self.indp_options_label, self.iterations_label):
            widget.bind("<Enter>", self.tooltip_mouse_enter)
            widget.bind("<Leave>", self.tooltip_mouse_leave)

    def tooltip_mouse_enter(self, event):
        tooltip_label = getattr(event.widget, "tooltip", "")
        event.widget.configure(text=tooltip_label, font="TkDefaultFont 8", cursor="question_arrow", foreground="blue")

    def tooltip_mouse_leave(self, event):
        default_label = getattr(event.widget, "default", "")
        event.widget.configure(text=default_label, font="TkDefaultFont 8", foreground="black")

    def EnableSelection(self):
        self.run_img_alt_btn.configure(state="normal")

    def get_images(self):
        self.num_of_imgs = int(self.num_of_img_dropdown.get())
        del self.images[:]
        for img in range(self.num_of_imgs):
            self.images.append(filedialog.askopenfilename())
        self.locate_confirm_btn.configure(state="normal")
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
        self.i = 0
        for img in self.images:
            self.i = self.i + 1
            try:
                l, t, w, h = pag.locateOnScreen(img, minSearchTime=5)
                w = w + 5
                h = h + 5
                self.regions[img] = {l, t, w, h}
                self.status_label.configure(text="Found" + img)
            except Exception as e:
                raise(ImageNotFoundEx("Image #" + str(self.i) + " " + img))
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
        ws.PlaySound("sounds/correct_2.wav", ws.SND_FILENAME)

    def BeginAutoClick(self):
        self.iterations = self.indp_options_dropdown.get()
        if self.num_of_imgs is 2 and None not in self.regions:
            self.status_label.configure(text="You clicking is being automated, cheers mate")
            if self.num_of_imgs is 1:
                print(self.images[0], self.regions[self.images[0]])
                # autoclick
            if self.num_of_imgs is 2:
            for i in self.iterations:
                print(self.images[0], self.regions[self.images[0]], self.images[1], self.regions[self.images[1]])
                # move_2_mouse(self.images[0], self.regions[self.images[0]], self.images[1], self.regions[self.images[1]])
            if self.num_of_imgs is 3:

root = tk.Tk()
app = Application(master=root)
app.master.title("Auto[Click]Mate")
app.master.maxsize(400, 500)
app.mainloop()
