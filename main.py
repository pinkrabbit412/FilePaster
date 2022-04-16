# Python default packages
import os
import sys
import getpass
import threading
import time
import datetime
import shutil
import configparser

# tkinter / GUI
import tkinter
import tkinter.font
from tkinter import messagebox
import PIL.Image
import PIL.ImageTk

# Setting program info
programIcon = "./resources/prograbbitIcon.ico"
programVersion = "v1.0.1.dev220416A"


class UserCanceledError(Exception): # 사용자 정의 에러
    pass


class Program:
    # Setting directory variable
    config = configparser.ConfigParser(interpolation=None)
    config.read("./config.ini")
    section = config.sections()
    original_directory = str(config["Config"]["to_copy"])
    target_directory = str(config["Config"]["paste_to"])
    if "%userprofile%" in target_directory:
        target_directory = target_directory.replace("%userprofile%", ("C:\\Users\\" + getpass.getuser()))

    @staticmethod
    def TaskCompleted(target_directory):
        messagebox.showinfo("Task Completed!", "Task completed.\nOpening target directory...")
        os.startfile(target_directory)
        return

    @staticmethod
    def TaskTerminated():
        messagebox.showerror("Task Terminated!", "Task terminated by user input.")
        return

    def __init__(self):
        # 0. Initialize tkinter window / Read the directory setting from ./config.ini
        self.window = tkinter.Tk()

    def enableButton(self):
        self.continue_anination_loop = False
        self.window.start_button.config(state="normal")
        self.window.start_button.configure(image=self.window.start_button_image)
        return

    def disableButton(self):
        self.window.start_button.config(state=tkinter.DISABLED)
        self.window.start_button.configure(image=self.window.start_button_deactivated_image)
        time.sleep(1)
        while True:
            if not self.continue_anination_loop: break;
            self.window.start_button.configure(image=self.window.start_button_deactivated_image1)
            time.sleep(1)
            if not self.continue_anination_loop: break;
            self.window.start_button.configure(image=self.window.start_button_deactivated_image2)
            time.sleep(1)
            if not self.continue_anination_loop: break;
            self.window.start_button.configure(image=self.window.start_button_deactivated_image3)
            time.sleep(1)
            if not self.continue_anination_loop: break;
            self.window.start_button.configure(image=self.window.start_button_deactivated_image4)
            time.sleep(2)
        return

    def startCopyThread(self):
        # The long long work...
        self.continue_anination_loop = True
        remove_question = messagebox.askyesno("Trying to start tasks",
                                              "Start Copy-and-Paste task to the target directory?")
        if remove_question:
            try:
                if os.path.isdir(self.target_directory):
                    remove_confirm = messagebox.askyesno("Directory already exists",
                                                         "Directory or file already exists.\nBackup at near directory and continue?")
                    if remove_confirm:
                        today_datetime = datetime.datetime.now().strftime("%Y.%m.%d. %H %M' %S''")
                        shutil.copytree(self.target_directory,
                                        (self.target_directory + " - Backupd at " + today_datetime))
                    else:
                        raise UserCanceledError()
                shutil.rmtree(self.target_directory, ignore_errors=True)
                shutil.copytree(self.original_directory, self.target_directory)
                self.TaskCompleted(self.target_directory)
            except PermissionError:
                messagebox.showerror("Task Terminated!",
                                     "Task terminated due to the file permission error.\nInsufficient permission.")
            except UserCanceledError:
                messagebox.showinfo("Task cancelled successfully",
                                    "Task cancelled successfully.\nNothing has been changed.")
        else:
            messagebox.showinfo("Task cancelled successfully",
                                "Task cancelled successfully.\nNothing has been changed.")
        self.enableButton()
        return

    def startCopy(self):
        # Setting thread and start it
        continue_anination_loop = True
        button_animation_thread = threading.Thread(target=self.disableButton)
        copy_thread = threading.Thread(target=self.startCopyThread)
        button_animation_thread.start()
        copy_thread.start()
        return

    def Main(self):
        # 1. Program Initialize
        self.window.iconbitmap(programIcon)
        self.window.title("prograbbit™ FilePaster")
        self.window.resizable(False, False)
        self.window.geometry("960x600")
        font_malgun_gothic_12 = tkinter.font.Font(family="맑은 고딕", size=12)

        # 2. Program Background
        background_image_data = PIL.Image.open("./resources/background_image.jpg")
        background_image = PIL.ImageTk.PhotoImage(background_image_data)
        background_image_label = tkinter.Label(self.window, image=background_image)
        background_image_label.image = background_image
        background_image_label.place(x=0, y=0, width=960, height=600)

        # 3. Display directory
        original_directory_for_display = self.original_directory.replace("\\", "/")
        original_directory_display = tkinter.Label(self.window, text=original_directory_for_display, background="white",
                                                   font=font_malgun_gothic_12)
        original_directory_display.place(x=85, y=224)
        target_directory_for_display = self.target_directory.replace("\\", "/")
        target_directory_display = tkinter.Label(self.window, text=target_directory_for_display, background="white",
                                                 font=font_malgun_gothic_12)
        target_directory_display.place(x=85, y=345)

        # Copy start button
        start_button_image_data = PIL.Image.open("./resources/copy_start_button.png")
        self.window.start_button_image = PIL.ImageTk.PhotoImage(start_button_image_data)

        start_button_deactivated_image_data = PIL.Image.open("./resources/copy_start_button_deactivated.png")
        self.window.start_button_deactivated_image = PIL.ImageTk.PhotoImage(start_button_deactivated_image_data)

        start_button_deactivated_image1_data = PIL.Image.open("./resources/copy_start_button_deactivated1.png")
        self.window.start_button_deactivated_image1 = PIL.ImageTk.PhotoImage(start_button_deactivated_image1_data)

        start_button_deactivated_image2_data = PIL.Image.open("./resources/copy_start_button_deactivated2.png")
        self.window.start_button_deactivated_image2 = PIL.ImageTk.PhotoImage(start_button_deactivated_image2_data)

        start_button_deactivated_image3_data = PIL.Image.open("./resources/copy_start_button_deactivated3.png")
        self.window.start_button_deactivated_image3 = PIL.ImageTk.PhotoImage(start_button_deactivated_image3_data)

        start_button_deactivated_image4_data = PIL.Image.open("./resources/copy_start_button_deactivated4.png")
        self.window.start_button_deactivated_image4 = PIL.ImageTk.PhotoImage(start_button_deactivated_image4_data)

        self.window.start_button = tkinter.Button(self.window, relief=tkinter.FLAT,
                                                  image=self.window.start_button_image, command=self.startCopy)
        self.window.start_button.place(x=319, y=435, width=300, height=60)

        self.window.mainloop()


if __name__ == '__main__':
    program = Program()
    program.Main()
