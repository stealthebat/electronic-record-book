from tkinter import ttk

import customtkinter as ctk
from .table_window import TableWindow
from .functions_window import FunctionsWindow
from PIL import Image


class MainWindow(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()
        self.geometry("1100x700")
        self.resizable(False, False)
        self.title("Электронная зачетная книжка")
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("dark-blue")
        self.scrollable_frame = ctk.CTkScrollableFrame(self, orientation="vertical", width=1100, fg_color="white",
                                                       label_text="Результаты запросов", label_fg_color="white",
                                                       label_text_color='black')
        self.scrollable_frame.pack()
        self.scrollable_frame.place(x=1100, y=0)
        self.queries_results_label = ctk.CTkLabel(self, text="")

        self.draw_widgets()

    def open_student_groups(self) -> None:
        window: TableWindow = TableWindow(self, "student_groups", self.queries_results_label)

    def open_departments(self) -> None:
        window: TableWindow = TableWindow(self, "departments", self.queries_results_label)

    def open_classrooms(self) -> None:
        window: TableWindow = TableWindow(self, "classrooms", self.queries_results_label)

    def open_subjects(self) -> None:
        window: TableWindow = TableWindow(self, "subjects", self.queries_results_label)

    def open_teachers(self) -> None:
        window: TableWindow = TableWindow(self, "teachers", self.queries_results_label)

    def open_students(self) -> None:
        window: TableWindow = TableWindow(self, "students", self.queries_results_label)

    def open_exams(self) -> None:
        window: TableWindow = TableWindow(self, "exams", self.queries_results_label)

    def open_functions(self) -> None:
        window: FunctionsWindow = FunctionsWindow(self, "Functions and procedures", self.queries_results_label)

    def open_results(self) -> None:
        results_window = ctk.CTkToplevel()
        results_window.geometry(f"{100+self.queries_results_label.winfo_reqwidth()}x"
                                f"{20+self.queries_results_label.winfo_reqheight()}")
        results_window.title("Результаты последних запросов")

        result_label = ctk.CTkLabel(results_window, text=self.queries_results_label.cget("text"))
        result_label.pack()

        results_window.grab_set()
        results_window.focus_set()
        results_window.wait_window()

    def draw_widgets(self) -> None:
        scheme_img = ctk.CTkImage(Image.open("./assets/main.png"), size=(1100, 700))
        scheme_label = ctk.CTkLabel(self, image=scheme_img, text="")
        scheme_label.pack(expand=1)
        scheme_label.place(x=0, y=0)

        student_groups_button = ctk.CTkButton(
            self,
            text="Groups",
            text_color='black',
            font=("Helvetica", 17, 'bold'),
            command=self.open_student_groups,
            width=230,
            height=36,
            fg_color="lightblue",
            bg_color="lightblue",
            hover_color='lightblue3'
        )
        student_groups_button.place(x=821, y=22)

        departments_button = ctk.CTkButton(
            self,
            text="Departments",
            text_color='black',
            font=("Helvetica", 17, 'bold'),
            command=self.open_departments,
            width=230,
            height=36,
            fg_color="lightblue",
            bg_color="lightblue",
            hover_color='lightblue3'
        )
        departments_button.place(x=39, y=327)

        classrooms_button = ctk.CTkButton(
            self,
            text="Classrooms",
            text_color='black',
            font=("Helvetica", 17, 'bold'),
            command=self.open_classrooms,
            width=230,
            height=36,
            fg_color="lightblue",
            bg_color="lightblue",
            hover_color='lightblue3'

        )
        classrooms_button.place(x=682, y=326)

        subjects_button = ctk.CTkButton(
            self,
            text="Subjects",
            text_color='black',
            font=("Helvetica", 17, 'bold'),
            command=self.open_subjects,
            width=230,
            height=36,
            fg_color="lightblue",
            bg_color="lightblue",
            hover_color='lightblue3'
        )
        subjects_button.place(x=39, y=500)

        teachers_button = ctk.CTkButton(
            self,
            text="Teachers",
            text_color='black',
            font=("Helvetica", 17, 'bold'),
            command=self.open_teachers,
            width=231,
            height=36,
            fg_color="lightblue",
            bg_color="lightblue",
            hover_color='lightblue3'
        )
        teachers_button.place(x=212, y=22)

        students_button = ctk.CTkButton(
            self,
            text="Students",
            text_color='black',
            font=("Helvetica", 17, 'bold'),
            command=self.open_students,
            width=230,
            height=36,
            fg_color="lightblue",
            bg_color="lightblue",
            hover_color='lightblue3'
        )
        students_button.place(x=532, y=22)

        exams_button = ctk.CTkButton(
            self,
            text="Exams",
            text_color='black',
            font=("Helvetica", 17, 'bold'),
            command=self.open_exams,
            width=230,
            height=36,
            fg_color="lightblue",
            bg_color="lightblue",
            hover_color='lightblue3'
        )
        exams_button.place(x=387, y=326)

        functions_button = ctk.CTkButton(
            self,
            text="Functions and procedures",
            command=self.open_functions,
            text_color="black",
            font=("Helvetica", 14, 'bold'),
            fg_color="lightblue",
            bg_color="white",
            hover_color='lightblue3'
        )
        functions_button.place(x=0, y=0)

        last_results_button = ctk.CTkButton(
            self,
            text="Last results",
            command=self.open_results,
            text_color="black",
            font=("Helvetica", 14, 'bold'),
            fg_color="lightblue",
            bg_color="white",
            hover_color='lightblue3'
        )
        last_results_button.place(x=0, y=50)

    def run_app(self) -> None:
        self.mainloop()
