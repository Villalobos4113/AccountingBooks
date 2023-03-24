from Accounting.classes.account_movement import AccountMovement
from Accounting.classes.policy import Policy
from Accounting.classes.exercise import Exercise

from Accounting.settings import database_path

from tkinter import messagebox
import customtkinter as ctk
import pickle


def read_file() -> list[Exercise]:
    print("\nOpening database")
    try:
        with open(database_path + "/database.pickle", "rb") as f:
            lst = pickle.load(f)
            print("  lst[Exercise] loaded correctly from database.\n")
    except Exception:
        lst = []
        print("  database couldn't be opened\n")

    return lst


# === MAIN CLASS ===

class Accounting(ctk.CTk):

    def __init__(self, company_name: str):
        super().__init__()

        self.company_name = company_name
        self.exercises = read_file()

        self.geometry("1050x750")
        self.title(self.company_name + " Accounting APP")
        self.minsize(750, 450)

        self.protocol("WM_DELETE_WINDOW", self.save)

        self.title = ctk.CTkLabel(self, text=self.company_name, font=ctk.CTkFont(size=30, weight="bold"))
        self.title.pack(padx=10, pady=(40, 20))

        exercises_frame = Exercises(self, exercises=self.exercises, company_name=self.company_name)
        exercises_frame.pack(padx=20, pady=20)

        print("\nAccounting created successfully:")
        print("  company name: ", self.company_name)
        print("  exercises: ", self.exercises, "\n")

    def save(self):
        with open(database_path + "/database.pickle", "wb") as f:
            pickle.dump(self.exercises, f)
            print("\nDatabase saved successfully\n")
        self.destroy()


# === EXERCISES FRAME ===

class Exercises(ctk.CTkFrame):

    def __init__(self, *args, exercises: list[Exercise], company_name: str, **kwargs):
        super().__init__(*args, **kwargs)

        self.exercises = exercises
        self.company_name = company_name
        self.window = args[0]

        self.header = ctk.CTkLabel(self, text="Exercises", font=ctk.CTkFont(size=25, weight="bold"))
        self.header.grid(row=0, column=0, pady=10)

        # == New Exercise Frame ==

        self.new_exercise_frame = ctk.CTkFrame(self)
        self.new_exercise_frame.grid(row=1, column=0, pady=10)

        self.new_exercise_header = ctk.CTkLabel(self.new_exercise_frame, text="New Exercise", font=ctk.CTkFont(size=20, weight="bold"))
        self.new_exercise_header.grid(row=0, column=0, pady=10, columnspan=2)

        self.name_new_exercise_entry = ctk.CTkEntry(self.new_exercise_frame, placeholder_text="Name New Exercise", width=500)
        self.name_new_exercise_entry.grid(row=1, column=0, padx=20, pady=10)

        self.button_new_exercise = ctk.CTkButton(self.new_exercise_frame, text="New Exercise", command=self.show_new_exercise_book)
        self.button_new_exercise.grid(row=1, column=1, padx=20, pady=10)

        # == Exercises Frame ==

        if len(self.exercises) > 0:
            self.exercises_frame = ctk.CTkScrollableFrame(self, height=400)
            self.exercises_frame.grid(row=2, column=0, sticky="nsew")

            self.exercises_header = ctk.CTkLabel(self.exercises_frame, text="Exercises", font=ctk.CTkFont(size=20, weight="bold"))
            self.exercises_header.grid(row=0, column=0, pady=20, columnspan=4)

            row = 1
            column = 0

            for exercise in self.exercises:
                if column >= 4:
                    row += 1
                    column = 0

                exercise_button = ctk.CTkButton(self.exercises_frame, text=exercise.name, command=lambda this_exercise=exercise: self.show_exercise_book(exercise=this_exercise))
                exercise_button.grid(row=row, column=column, padx=19, pady=15)

                column += 1

            while row == 1 and column < 4:
                fill_button = ctk.CTkButton(self.exercises_frame, text="", bg_color="transparent", fg_color="transparent", hover=False)
                fill_button.grid(row=row, column=column, padx=19, pady=15)

                column += 1

        print("\nExercises created successfully:")
        print("  company name: ", self.company_name)
        print("  exercises: ", self.exercises)
        print("  window: ", self.window)

    def show_exercise_book(self, exercise: Exercise):
        exercise_book_frame = ExerciseBook(self.window, exercise=exercise, exercises=self.exercises, company_name=self.company_name, window=self.window)
        self.destroy()
        exercise_book_frame.pack(padx=20, pady=20)

    def show_new_exercise_book(self):
        if self.name_new_exercise_entry.get() == "":
            messagebox.showwarning(title="Name Entry", message="Name entry is empty")
        else:
            for exercise in self.exercises:
                if exercise.name == self.name_new_exercise_entry.get():
                    messagebox.showwarning("New Exercise", message="New Exercise's name already exists.")
                    return

            self.exercises.append(Exercise(self.company_name, self.name_new_exercise_entry.get()))
            exercise_book_frame = ExerciseBook(self.window, exercise=self.exercises[-1], exercises=self.exercises, company_name=self.company_name, window=self.window)
            self.destroy()
            exercise_book_frame.pack(padx=20, pady=20)


# === EXERCISE FRAME ===

class ExerciseBook(ctk.CTkFrame):
    def __init__(self, *args, exercise: Exercise, exercises: list[Exercise], company_name: str, window, **kwargs):
        super().__init__(*args, **kwargs)

        self.actual_frame = None
        self.exercise = exercise
        self.exercises = exercises
        self.company_name = company_name
        self.window = window
        self.actual_frame: ctk.CTkFrame

        self.header = ctk.CTkLabel(self, text=self.exercise.name, font=ctk.CTkFont(size=25, weight="bold"))
        self.header.grid(row=0, column=0, pady=20, columnspan=4)

        self.add_account_button = ctk.CTkButton(self, text="Add Account", command=self.add_account)
        self.add_account_button.grid(row=1, column=0, padx=19, pady=15)

        self.add_policy_button = ctk.CTkButton(self, text="Add Policy", command=self.add_policy)
        self.add_policy_button.grid(row=1, column=1, padx=19, pady=15)

        self.see_exercise_button = ctk.CTkButton(self, text="See Exercise", command=self.see_exercise)
        self.see_exercise_button.grid(row=1, column=2, padx=19, pady=15)

        self.exit_button = ctk.CTkButton(self, text="Exit", command=self.exit)
        self.exit_button.grid(row=1, column=3, padx=19, pady=15)

        print("\nExerciseBook created successfully:")
        print("  company name: ", self.company_name)
        print("  exercise: ", self.exercise.name)
        print("  exercises: ", self.exercises)
        print("  window: ", self.window, "\n")

    def add_policy(self):
        add_policy_frame = AddPolicy(self, exercise=self.exercise)

        if self.actual_frame is not None:
            self.actual_frame.destroy()

        self.actual_frame = add_policy_frame
        self.actual_frame.grid(row=2, column=0, padx=20, pady=20, columnspan=4)

    def add_account(self):
        add_account_frame = AddAccount(self, exercise=self.exercise)

        if self.actual_frame is not None:
            self.actual_frame.destroy()

        self.actual_frame = add_account_frame
        self.actual_frame.grid(row=2, column=0, padx=20, pady=20, columnspan=4)

    def see_exercise(self):
        see_exercise_frame = SeeExercise(self, exercise=self.exercise)

        if self.actual_frame is not None:
            self.actual_frame.destroy()

        self.actual_frame = see_exercise_frame
        self.actual_frame.grid(row=2, column=0, padx=20, pady=20, columnspan=4)

    def exit(self):
        exercises_frame = Exercises(self.window, exercises=self.exercises, company_name=self.company_name)
        self.destroy()
        exercises_frame.pack(padx=20, pady=20)


class AddPolicy(ctk.CTkFrame):

    def __init__(self, *args, exercise: Exercise, **kwargs):
        super().__init__(*args, **kwargs)

        self.exercise = exercise

        self.header = ctk.CTkLabel(self, text="Add Policy", font=ctk.CTkFont(size=20, weight="bold"))
        self.header.grid(row=0, column=0, pady=20, columnspan=8)

        self.invoice_label = ctk.CTkLabel(self, text="Invoice:", font=ctk.CTkFont(size=15, weight="bold"))
        self.invoice_label.grid(row=1, column=0, pady=15, padx=15)

        self.invoice = ctk.CTkLabel(self, text=str(exercise.next_policy_invoice()), justify="left")
        self.invoice.grid(row=1, column=1, pady=15, padx=15)

        self.description_label = ctk.CTkLabel(self, text="Description:", font=ctk.CTkFont(size=15, weight="bold"))
        self.description_label.grid(row=2, column=0, padx=15, pady=15, columnspan=2)

        self.description_entry = ctk.CTkEntry(self, width=400)
        self.description_entry.grid(row=2, column=2, padx=15, pady=15, columnspan=6)

        self.credit_label = ctk.CTkLabel(self, text="Credit:", font=ctk.CTkFont(size=15, weight="bold"))
        self.credit_label.grid(row=3, column=0, padx=15, pady=15, columnspan=2)

        self.credit_entry = ctk.CTkEntry(self, width=125, placeholder_text="$")
        self.credit_entry.grid(row=3, column=2, padx=15, pady=15, columnspan=2)

        self.credit_account_label = ctk.CTkLabel(self, text="Account:", font=ctk.CTkFont(size=15, weight="bold"))
        self.credit_account_label.grid(row=3, column=4, padx=15, pady=15, columnspan=2)

        self.credit_account_entry = ctk.CTkComboBox(self, values=exercise.get_all_accounts(), width=125, variable="")
        self.credit_account_entry.grid(row=3, column=6, padx=15, pady=15, columnspan=2)

        self.debit_label = ctk.CTkLabel(self, text="Debit:", font=ctk.CTkFont(size=15, weight="bold"))
        self.debit_label.grid(row=4, column=0, padx=15, pady=15, columnspan=2)

        self.debit_entry = ctk.CTkEntry(self, width=125, placeholder_text="$")
        self.debit_entry.grid(row=4, column=2, padx=15, pady=15, columnspan=2)

        self.debit_account_label = ctk.CTkLabel(self, text="Account:", font=ctk.CTkFont(size=15, weight="bold"))
        self.debit_account_label.grid(row=4, column=4, padx=15, pady=15, columnspan=2)

        self.debit_account_entry = ctk.CTkComboBox(self, values=exercise.get_all_accounts(), width=125, variable="")
        self.debit_account_entry.grid(row=4, column=6, padx=15, pady=15, columnspan=2)

        self.add_policy_button = ctk.CTkButton(self, text="Add Policy", width=500, command=self.add_policy)
        self.add_policy_button.grid(row=5, column=0, columnspan=8, padx=20, pady=(30, 30))

        print("\nAddPolicy created successfully:")
        print("  exercise: ", self.exercise.name, "\n")

    def add_policy(self):
        try:
            if self.description_entry.get() == "":
                print()
                raise Exception("Description entry is empty.")

            if self.credit_entry.get() == "":
                raise Exception("Credit balance entry is empty.")
            else:
                try:
                    if float(self.credit_entry.get()) < 0:
                        raise Exception("Credit balance entry can not be negative.")
                except Exception:
                    raise Exception("Credit balance entry is not a valid number.")

            if self.debit_entry.get() == "":
                raise Exception("Debit balance entry is empty.")
            else:
                try:
                    if float(self.debit_entry.get()) < 0:
                        raise Exception("Debit balance entry can not be negative.")
                except Exception:
                    raise Exception("Debit balance entry is not a valid number.")

            if self.credit_account_entry.get() == "":
                raise Exception("Credit Account entry is empty.")
            elif not self.credit_account_entry.get().isnumeric():
                raise Exception("Credit Account entry is not numeric (0-9).")
            elif len(self.credit_account_entry.get()) != 6:
                raise Exception("Credit Account entry must have 6 digits.")

            if self.debit_account_entry.get() == "":
                raise Exception("Debit Account entry is empty.")
            elif not self.debit_account_entry.get().isnumeric():
                raise Exception("Debit Account entry is not numeric (0-9).")
            elif len(self.debit_account_entry.get()) != 6:
                raise Exception("Debit Account entry must have 6 digits.")

            policy = Policy(self.exercise.next_policy_invoice(), self.description_entry.get())

            policy.credit = AccountMovement(int(self.credit_account_entry.get()), float(self.credit_entry.get()), "c")
            policy.debit = AccountMovement(int(self.debit_account_entry.get()), float(self.debit_entry.get()), "d")

            self.exercise.policies = policy

            self.description_entry.delete(0, len(self.description_entry.get()))
            self.credit_entry.delete(0, len(self.credit_entry.get()))
            self.debit_entry.delete(0, len(self.debit_entry.get()))
            self.credit_account_entry.set("")
            self.debit_account_entry.set("")

            messagebox.showinfo(title="Success", message="Policy added successfully.")
            print("Policy added successfully: ", policy, "\n")

        except Exception as e:
            messagebox.showwarning(title="Add Policy Warning", message=str(e))


class AddAccount(ctk.CTkFrame):

    def __init__(self, *args, exercise: Exercise, **kwargs):
        super().__init__(*args, **kwargs)

        self.exercise = exercise

        self.header = ctk.CTkLabel(self, text="Add Account", font=ctk.CTkFont(size=20, weight="bold"))
        self.header.grid(row=0, column=0, pady=20, columnspan=8)

        self.account_id_label = ctk.CTkLabel(self, text="Account ID:", font=ctk.CTkFont(size=15, weight="bold"))
        self.account_id_label.grid(row=1, column=0, padx=15, pady=15, columnspan=2)

        self.account_id_entry = ctk.CTkEntry(self, width=400)
        self.account_id_entry.grid(row=1, column=2, padx=15, pady=15, columnspan=6)

        self.name_label = ctk.CTkLabel(self, text="Name:", font=ctk.CTkFont(size=15, weight="bold"))
        self.name_label.grid(row=2, column=0, padx=15, pady=15, columnspan=2)

        self.name_entry = ctk.CTkEntry(self, width=400)
        self.name_entry.grid(row=2, column=2, padx=15, pady=15, columnspan=6)

        self.add_account_button = ctk.CTkButton(self, text="Add Account", width=500, command=self.add_account)
        self.add_account_button.grid(row=3, column=0, columnspan=8, padx=20, pady=(30, 30))

        print("\nAddAccount created successfully:")
        print("  exercise: ", self.exercise.name, "\n")

    def add_account(self):
        try:
            if self.account_id_entry.get() == "":
                raise Exception("Account ID entry is empty.")
            elif not self.account_id_entry.get().isnumeric():
                raise Exception("Account ID entry is not numeric (0-9).")
            elif len(self.account_id_entry.get()) != 6:
                raise Exception("Account ID entry must have 6 digits.")

            if self.name_entry.get() == "":
                raise Exception("Name entry is empty.")

            self.exercise.add_account(int(self.account_id_entry.get()), self.name_entry.get())

            self.account_id_entry.delete(0, len(self.account_id_entry.get()))
            self.name_entry.delete(0, len(self.name_entry.get()))

            messagebox.showinfo(title="Success", message="Account added successfully")
            print("\nAccount added successfully: ", self.exercise.get_all_accounts()[-1], "\n")

        except Exception as e:
            messagebox.showwarning(title="Add Account Warning", message=str(e))


class SeeExercise(ctk.CTkFrame):

    def __init__(self, *args, exercise: Exercise, **kwargs):
        super().__init__(*args, **kwargs)

        self.exercise = exercise

        self.header = ctk.CTkLabel(self, text="See Exercise", font=ctk.CTkFont(size=20, weight="bold"))
        self.header.grid(row=0, column=0, pady=20)

        self.str_exercise = ctk.CTkTextbox(self, width=600, height=300)
        self.str_exercise.grid(row=1, column=0, pady=20, padx=20)

        self.str_exercise.insert("0.0", exercise)
        self.str_exercise.configure(state="disabled")