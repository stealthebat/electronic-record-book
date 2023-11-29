import customtkinter
import customtkinter as ctk
import tkinter
from tkinter import ttk
from database.db import Database, add_text_to_label


class FunctionsWindow(ctk.CTk):
    def __init__(self, parent, title, queries_results_label):
        super().__init__()
        self.title = title
        self.db_obj = Database()
        self.root = ctk.CTkToplevel(parent)
        self.root.geometry("1300x250")
        self.root.title(title)
        self.root.resizable(False, False)
        ctk.set_appearance_mode("light")

        self.queries_results_label = queries_results_label
        self.draw_widgets()
        self.grab_focus()

    def set_styles(self):
        # Styles tables
        self.style = ttk.Style()
        self.style.theme_use("default")
        self.style.configure(
            "Treeview.Heading",
            background="lightblue",
            foreground="black",
            font=('Times New Roman', 13, 'bold')
        )
        self.style.configure(
            "Treeview",
            foreground="black",
            background="white",
            font=('Times New Roman', 13, 'bold')
        )
        # Tab style
        self.style2 = ttk.Style()
        self.style2.theme_use("default")
        self.style2.configure(
            "TNotebook",
            background="white",
            tabposition="nw"
        )
        self.style2.configure(
            "TNotebook.Tab",
            background="lightblue",
            foreground="black",
            font=('Arial', 10, 'bold')
        )
        self.style2.map(
            "TNotebook.Tab",
            background=[("selected", "lightblue3")],
        )

    def get_department_by_subject(self) -> None:
        subject_name = self.subject_name.get()
        subject_department = list(self.db_obj.call_func_get_department_by_subject(subject_name)[0].values())[0]
        if subject_department is not None:
            self.department_result.set(f"Предмет {subject_name} относится к кафедре {subject_department}.")
        else:
            self.department_result.set(f"Предмета {subject_name} не существует")

    def get_student_average_grade(self) -> None:
        student_name = self.student_name.get()
        print(self.db_obj.call_func_get_student_average_grade(student_name))
        student_avg_grade = list(self.db_obj.call_func_get_student_average_grade(student_name)[0].values())[0]
        if student_avg_grade is not None:
            self.avg_grade.set(f"Студент {student_name} имеет средний балл {student_avg_grade}")
        elif self.db_obj.check_student(student_name):
            self.avg_grade.set(f"Студент {student_name} не сдавал ни один экзамен")
        else:
            self.avg_grade.set(f"Студент {student_name} не обучается в вузе")

    def draw_widgets(self) -> None:
        # Styles exec
        self.set_styles()
        # Tabs
        tab_control = ttk.Notebook(self.root)
        tab_exams_count_per_classroom = ctk.CTkFrame(tab_control, fg_color="white")
        tab_youngest_students = ctk.CTkFrame(tab_control, fg_color="white")
        tab_department_by_subject = ctk.CTkFrame(tab_control, fg_color="white")
        tab_student_average_grade = ctk.CTkFrame(tab_control, fg_color="white")
        tab_control.add(tab_exams_count_per_classroom, text="Количество проведенных экзаменов по аудиториям")
        tab_control.add(tab_youngest_students, text="Самые молодые студенты")
        tab_control.add(tab_department_by_subject, text="Получить кафедру по названию дисциплины")
        tab_control.add(tab_student_average_grade, text="Получить среднюю оценку студента")
        tab_control.pack(expand=1, fill="both")

        # Exams count per classroom
        active_count_data = self.db_obj.call_proc_get_exams_count_per_classroom()
        active_count_data_keys = list(active_count_data[0].keys())
        tree = ttk.Treeview(master=tab_exams_count_per_classroom, columns=active_count_data_keys, show="headings")
        for col in active_count_data_keys:
            tree.heading(col, text=col)
        for line in active_count_data:
            tree.insert("", tkinter.END, values=list(line.values()))
        tree.pack(fill=tkinter.BOTH, expand=1)

        # Youngest students
        active_count_data = self.db_obj.call_proc_get_youngest_students()
        active_count_data_keys = list(active_count_data[0].keys())
        tree = ttk.Treeview(master=tab_youngest_students, columns=active_count_data_keys, show="headings")
        for col in active_count_data_keys:
            tree.heading(col, text=col)
        for line in active_count_data:
            tree.insert("", tkinter.END, values=list(line.values()))
        tree.pack(fill=tkinter.BOTH, expand=1)

        # Department by subject name
        department_by_subject_frame = ctk.CTkFrame(tab_department_by_subject, fg_color="white")
        # Result label
        self.department_result = tkinter.StringVar()
        department_label = ctk.CTkLabel(department_by_subject_frame, textvariable=self.department_result,
                                        fg_color="white")
        department_label.pack(pady=10)
        # Row
        row_subject = ctk.CTkFrame(department_by_subject_frame, fg_color="white")
        label_subject = ctk.CTkLabel(row_subject, text="Название дисциплины", fg_color="white")
        self.subject_name = ctk.CTkEntry(row_subject, width=300)
        label_subject.grid(row=0, column=0, padx=15)
        self.subject_name.grid(row=0, column=1, padx=15)
        row_subject.pack(pady=5)
        # Button
        subject_btn = ctk.CTkButton(department_by_subject_frame, text="Accept", command=self.get_department_by_subject,
                                    bg_color="lightblue", fg_color='lightblue', hover_color='lightblue3',
                                    text_color='black')
        subject_btn.pack(pady=5)
        department_by_subject_frame.pack()

        # Average grade of student
        student_average_grade_frame = ctk.CTkFrame(tab_student_average_grade, fg_color="white")
        # Result label
        self.avg_grade = tkinter.StringVar()
        avg_grade_label = ctk.CTkLabel(student_average_grade_frame, textvariable=self.avg_grade,
                                       fg_color="white")
        avg_grade_label.pack(pady=10)
        # Row
        row_student = ctk.CTkFrame(student_average_grade_frame, fg_color="white")
        label_student = ctk.CTkLabel(row_student, text="ФИО студента", fg_color="white")
        self.student_name = ctk.CTkEntry(row_student, width=300)
        label_student.grid(row=0, column=0, padx=15)
        self.student_name.grid(row=0, column=1, padx=15)
        row_student.pack(pady=5)
        # Button
        student_btn = ctk.CTkButton(student_average_grade_frame, text="Accept", command=self.get_student_average_grade,
                                    bg_color="lightblue", fg_color='lightblue', hover_color='lightblue3',
                                    text_color='black')
        student_btn.pack(pady=5)
        student_average_grade_frame.pack()

    def grab_focus(self) -> None:
        self.root.grab_set()
        self.root.focus_set()
        self.root.wait_window()
