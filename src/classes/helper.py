from os.path import join, dirname, abspath, exists, isfile
from os import mkdir, remove, walk
from tkinter import Toplevel, Tk, PhotoImage
from classes.Widgets import Widgets
from __main__ import __file__ as main_file

class Helper:
    @staticmethod
    def get_notepads_directory(**kwargs):
        _path = dirname(abspath(main_file))

        path = join(_path, "notepads") if "imported" not in kwargs else join(_path, "notepads", "imported")

        if not exists(path):
            mkdir(path)

        return path

    @staticmethod
    def get_notepad_path(name: str, **kwargs):
        file = join(Helper.get_notepads_directory(**kwargs), name) + ".txt"

        if kwargs.get("imported"):
            file = Helper.get_imported_file_path(name)

        return file

    @staticmethod
    def get_notepad_path_raw(name: str, **kwargs):
        file_path = join(Helper.get_notepads_directory(**kwargs), name) + ".txt"

        return file_path

    @staticmethod
    def add_notepad(name: str, file_path: str = None, **kwargs) -> bool:
        path = ""

        if file_path:
            file_name = file_path.split("/")[-1].split(".")[0]
            path = Helper.get_notepad_path_raw(file_name, **kwargs)
        else:
            path = Helper.get_notepad_path_raw(name, **kwargs)

        if exists(path):
            return False

        if name:
            with open(path, "w"):
                pass
        else:
            with open(path, "w") as f:
                f.write(file_path)

        return True

    @staticmethod
    def delete_notepad(name: str, file_path: str = None) -> bool | str:
        path = Helper.get_notepad_path(name)

        if file_path:
            path = file_path
        try:
            if not exists(path):
                if exists(Helper.get_notepad_path(name, imported=True)):
                    path = Helper.get_notepad_path(name, imported=True)
                else:
                    return False
        except:
            return False

        try:
            remove(path)
        except OSError:
            return "perm"

        return True

    @staticmethod
    def get_notepads() -> list[str]:
        directory = Helper.get_notepads_directory()
        dirs = walk(directory)

        def check_file(_file):
            notepad_dir = isfile(join(directory, _file))
            imported = isfile(join(directory, "imported", _file))

            return notepad_dir or imported

        def check_type(_file):
            return file.endswith(".txt") and _file != "__password__.txt"

        files = []

        for r, d, f in dirs:
            for file in f:
                if file != "__password__.txt" and check_file(file) and check_type(file):
                    files.append(file)

        return files

    @staticmethod
    def show_error(error_message: str, root: Tk):
        X_COORD = root.winfo_rootx() - 12
        Y_COORD = 150

        top_error = Helper.setup_top(None, "Error", geometry=f"300x100+{X_COORD}+{Y_COORD}", withdraw=False)

        top_error.bind("<Escape>", lambda e: top_error.destroy())
        top_error.bind("<Return>", lambda e: top_error.destroy())

        error_label = Widgets.create_label(top_error, text=error_message)
        error_label.pack()

        okay_button = Widgets.create_button(top_error, text="okay", width=20, command=top_error.destroy)
        okay_button.place(relx=0.5, rely=0.5, anchor="center")
        okay_button.focus_force()

        return top_error

    @staticmethod
    def confirmation(title: str, message: str, cb: callable, root: Tk):
        X_COORD = root.winfo_rootx() - 12
        Y_COORD = 150

        top_confirm = Helper.setup_top(None, title, geometry=f"300x100+{X_COORD}+{Y_COORD}", withdraw=False)

        top_confirm.bind("<Escape>", lambda e: top_confirm.destroy())

        confirm_label = Widgets.create_label(top_confirm, text=message)
        confirm_label.pack()

        def confirm(*_):
            cb()
            top_confirm.destroy()

        top_confirm.bind("<Return>", confirm)

        confirm_button = Widgets.create_button(top_confirm, text="confirm", width=20, command=confirm)
        confirm_button.place(relx=0.7, rely=0.5, anchor="center")
        confirm_button.focus_force()

        exit_button = Widgets.create_button(top_confirm, text="cancel", width=20, command=top_confirm.destroy)
        exit_button.place(relx=0.3, rely=0.5, anchor="center")

    @staticmethod
    def setup_top(parent: Tk | None, title: str, **kwargs):
        if "withdraw" not in kwargs:
            parent.withdraw()

        top = Toplevel(parent)
        top.title(title)

        if "geometry" in kwargs:
            top.geometry(kwargs["geometry"])
        else:
            X_COORD = parent.winfo_rootx() - 12
            Y_COORD = 150
            top.geometry(f"300x100+{X_COORD}+{Y_COORD}")

        if "resizable" in kwargs:
            top.resizable(width=False, height=False)
        top.config(bg="#25292e")

        icon = PhotoImage(file=join(dirname(main_file), "assets\\notepad+.png"))
        top.iconphoto(False, icon)

        def destroy():
            top.destroy()

            if parent is not None:
                parent.destroy()

        if "protocol" not in kwargs:
            top.protocol("WM_DELETE_WINDOW", destroy)

        return top

    @staticmethod
    def get_imported_file_path(name: str):
        file_path = join(Helper.get_notepads_directory(imported=True), name) + ".txt"

        if not exists(file_path):
            return None

        with open(file_path, "r") as f:
            return f.read()

    @staticmethod
    def get_imported_file_content(name: str):
        path = Helper.get_imported_file_path(name)

        if not exists(path):
            return False

        with open(path, "r") as f:
            return f.read()
