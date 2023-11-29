import customtkinter
import customtkinter as ctk
import tkinter
from tkinter import ttk
from database.db import Database, add_text_to_label
from functions.funcs import is_float


class TableWindow(ctk.CTk):
    def __init__(self, parent: ctk.CTk, title: str, queries_results_label) -> None:
        super().__init__()

        self.title = title
        self.db_obj = Database()
        self.root = ctk.CTkToplevel(parent)
        self.root.title(title)
        self.root.resizable(False, False)
        customtkinter.set_appearance_mode("light")
        customtkinter.set_default_color_theme("green")
        self.queries_results_label = queries_results_label
        self.draw_widgets()
        self.grab_focus()

    def set_style(self):
        # Styles tables
        self.style = ttk.Style()
        self.style.theme_use("default")
        self.style.configure(
            "Treeview.Heading",
            background="lightblue",
            foreground="black",
            font=('Arial', 13, 'bold')
        )
        self.style.configure(
            "Treeview",
            foreground="black",
            background="white",
            font=('Arial', 10, 'bold')
        )
        # Tab style
        self.style2 = ttk.Style()
        self.style2.theme_use("default")
        self.style2.configure(
            "TNotebook",
            background="white",
            tabposition="sw"
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

    def insert_data_into_db(self) -> None:
        data = []
        keys = self.columns
        for entry in self.entries:
            if entry.get().isdigit():
                data.append(int(entry.get()))
            elif is_float(entry.get()):
                data.append(float(entry.get()))
            else:
                data.append(entry.get())
        data = str(tuple(data))
        keys = str(tuple(keys)).replace("'", "")
        add_text_to_label(self.db_obj.insert_data(self.title, data, keys), self.queries_results_label)
        self.root.destroy()

    def delete_data_from_db(self) -> None:
        key = self.key_find
        value = self.entry_delete.get()
        if value.isdigit():
            value = int(value)
            add_text_to_label(self.db_obj.delete_data(self.title, key, value), self.queries_results_label)
        else:
            add_text_to_label("The ID can only be an integer, enter the value again", self.queries_results_label)
        self.root.destroy()

    def get_new_data(self) -> None:
        data = []
        for entry in self.entries:
            if entry.get().isdigit():
                data.append(int(entry.get()))
            elif is_float(entry.get()):
                data.append(float(entry.get()))
            else:
                data.append(entry.get())
        data.insert(0, self.id)
        add_text_to_label(self.db_obj.update_the_data_in_the_table(self.columns, data, self.title),
                          self.queries_results_label)
        self.root.destroy()

    def update_table_row(self):
        self.values = tuple(self.db_obj.get_row(self.title, self.columns[0], self.entry_update.get())[0].values())
        self.id = self.values[0]
        if hasattr(self, 'frame_update') and isinstance(self.frame_update, ctk.CTkFrame):
            self.frame_update.destroy()

        self.frame_update = ctk.CTkFrame(self.tab_update, fg_color="white")
        self.entries = []
        for i in range(len(self.columns)):
            # Row
            frame_row = ctk.CTkFrame(self.frame_update, fg_color="white")
            # Content
            label_update = ctk.CTkLabel(frame_row, text=self.columns[i], width=100)
            if i == 0:
                entry_update = ctk.CTkLabel(frame_row, fg_color="white", text=self.values[i])
            else:
                entry_update = ctk.CTkEntry(frame_row, fg_color="white")
                entry_update.insert(0, self.values[i])
                self.entries.append(entry_update)
            # Placement
            label_update.grid(row=i, column=0, padx=(0, 50), sticky="w")
            entry_update.grid(row=i, column=1, sticky="ew")
            frame_row.pack(pady=5)
        frame_row = ctk.CTkFrame(self.frame_update, fg_color="white")

        accept_button = ctk.CTkButton(frame_row, text="Accept", text_color="black", command=self.get_new_data,
                                      bg_color="lightblue", fg_color='lightblue', hover_color='lightblue3')
        accept_button.pack()
        frame_row.pack(pady=5)
        self.frame_update.pack(pady=5)

    def draw_widgets(self) -> None:
        self.set_style()
        # Tabs
        tab_control = ttk.Notebook(self.root)
        tab_table = ctk.CTkFrame(tab_control, fg_color="white")
        tab_insertion = ctk.CTkFrame(tab_control, fg_color="white")
        tab_delete = ctk.CTkFrame(tab_control, fg_color="white")
        self.tab_update = ctk.CTkFrame(tab_control, fg_color="white")
        tab_control.add(tab_table, text="Table")
        tab_control.add(tab_insertion, text="Insert")
        tab_control.add(tab_delete, text="Delete")
        tab_control.add(self.tab_update, text="Update")
        tab_control.pack(expand=1)

        # Getting db data
        data = self.db_obj.get_table(self.title)
        self.columns = list(data[0].keys())

        # Db table
        self.tree = ttk.Treeview(master=tab_table, columns=self.columns, show="headings")
        for col in self.columns:
            self.tree.heading(col, text=col)
        for line in data:
            self.tree.insert("", tkinter.END, values=list(line.values()))
        self.tree.pack(fill=tkinter.BOTH, expand=1)

        # Insert tab
        self.frame_insert = ctk.CTkFrame(tab_insertion, fg_color="white")
        self.entries = []
        for i in range(len(self.columns)):
            # Row
            frame_row = ctk.CTkFrame(self.frame_insert, fg_color="white")
            # Content
            label_insert = ctk.CTkLabel(frame_row, text=self.columns[i], width=100)
            entry_insert = ctk.CTkEntry(frame_row, fg_color="white")
            self.entries.append(entry_insert)
            # Placement
            label_insert.grid(row=i, column=0, padx=(0, 50), sticky="w")
            entry_insert.grid(row=i, column=1, sticky="ew")
            frame_row.pack(pady=5)
        frame_row = ctk.CTkFrame(self.frame_insert, fg_color="white")
        accept_button = ctk.CTkButton(frame_row, text="Accept", command=self.insert_data_into_db, text_color="black",
                                      bg_color="lightblue", fg_color='lightblue', hover_color='lightblue3')
        accept_button.pack()
        frame_row.pack(pady=5)
        self.frame_insert.pack(pady=5)

        # Delete tab
        self.frame_delete = ctk.CTkFrame(tab_delete, fg_color="white")
        self.key_find = self.columns[0]
        frame_row = ctk.CTkFrame(self.frame_delete, fg_color="white")
        label_delete = ctk.CTkLabel(frame_row, text=self.key_find)
        self.entry_delete = ctk.CTkEntry(frame_row, fg_color="white")
        label_delete.grid(row=0, column=0, padx=15)
        self.entry_delete.grid(row=0, column=1, padx=15)
        frame_row.pack(pady=5)
        frame_row = ctk.CTkFrame(self.frame_delete, fg_color="white")
        delete_button = ctk.CTkButton(frame_row, text="Accept", command=self.delete_data_from_db, text_color="black",
                                      bg_color="lightblue", fg_color='lightblue', hover_color='lightblue3')
        delete_button.pack()
        frame_row.pack(pady=5)
        self.frame_delete.pack(pady=5)

        # Update tab
        self.frame_update = ctk.CTkFrame(self.tab_update, fg_color="white")
        frame_row = ctk.CTkFrame(self.frame_update, fg_color="white")
        label_update = ctk.CTkLabel(frame_row, text=self.columns[0])
        self.entry_update = ctk.CTkEntry(frame_row, fg_color="white")
        label_update.grid(row=0, column=0, padx=15)
        self.entry_update.grid(row=0, column=1, padx=15)
        frame_row.pack(pady=5)
        frame_row = ctk.CTkFrame(self.frame_update, fg_color="white")
        update_button = ctk.CTkButton(frame_row, text="Update", text_color="black", command=self.update_table_row,
                                      bg_color="lightblue", fg_color='lightblue', hover_color='lightblue3')
        update_button.pack()
        frame_row.pack(pady=5)
        self.frame_update.pack(pady=5)

    def grab_focus(self) -> None:
        self.root.grab_set()
        self.root.focus_set()
        self.root.wait_window()
