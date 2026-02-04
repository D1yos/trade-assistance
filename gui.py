import customtkinter as ctk
from tkinter import messagebox
from database import Database
import logic
import parser

ctk.set_appearance_mode("dark")

BTN_STYLE = {"fg_color": "#3d3d3d", "hover_color": "#575757", "text_color": "white", "border_width": 1,
             "border_color": "#2b2b2b"}


class AutocompleteDropdown(ctk.CTkToplevel):
    def __init__(self, master, callback):
        super().__init__(master)
        self.overrideredirect(True)
        self.callback = callback
        self.listbox = ctk.CTkScrollableFrame(self, width=250, height=200, fg_color="#2b2b2b")
        self.listbox.pack(fill="both", expand=True)
        self.withdraw()

    def update_list(self, items, x, y):
        for widget in self.listbox.winfo_children(): widget.destroy()
        if not items:
            self.withdraw()
            return
        for item in items:
            btn = ctk.CTkButton(self.listbox, text=item, fg_color="transparent", anchor="w",
                                command=lambda i=item: self.callback(i))
            btn.pack(fill="x")
        self.geometry(f"+{int(x)}+{int(y)}")
        self.deiconify()
        self.lift()


class RegisterWindow(ctk.CTkToplevel):
    def __init__(self, db_instance):
        super().__init__()
        self.title("Create Account")
        self.geometry("420x480")
        self.db = db_instance
        self.attributes("-topmost", True)
        self.show_p = self.show_cp = False

        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.pack(expand=True, fill="both", padx=30, pady=20)
        ctk.CTkLabel(self.main_frame, text="Registration", font=("Arial", 20, "bold")).pack(pady=15)

        self.grid_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.grid_frame.pack()

        self.u_entry = ctk.CTkEntry(self.grid_frame, placeholder_text="Username", width=250)
        self.u_entry.grid(row=0, column=0, pady=5)
        ctk.CTkLabel(self.grid_frame, text="", width=45).grid(row=0, column=1)

        self.p_entry = ctk.CTkEntry(self.grid_frame, placeholder_text="Password", show="*", width=250)
        self.p_entry.grid(row=1, column=0, pady=5)
        ctk.CTkButton(self.grid_frame, text="👁", width=45, fg_color="transparent",
                      command=lambda: self.toggle('p')).grid(row=1, column=1, padx=5)

        self.cp_entry = ctk.CTkEntry(self.grid_frame, placeholder_text="Confirm Password", show="*", width=250)
        self.cp_entry.grid(row=2, column=0, pady=5)
        ctk.CTkButton(self.grid_frame, text="👁", width=45, fg_color="transparent",
                      command=lambda: self.toggle('cp')).grid(row=2, column=1, padx=5)

        ctk.CTkButton(self.main_frame, text="Register", command=self.do_register, width=305, **BTN_STYLE).pack(pady=25)

    def toggle(self, target):
        if target == 'p':
            self.show_p = not self.show_p
            self.p_entry.configure(show="" if self.show_p else "*")
        else:
            self.show_cp = not self.show_cp
            self.cp_entry.configure(show="" if self.show_cp else "*")

    def do_register(self):
        u, p, cp = self.u_entry.get().strip(), self.p_entry.get(), self.cp_entry.get()
        if p == cp and self.db.register_user(u, p):
            messagebox.showinfo("Success", "Account created!")
            self.destroy()
        else:
            messagebox.showerror("Error", "Check fields or user exists")


class LoginWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("PoE 2 Assistant ")
        self.geometry("420x380")
        self.db = Database()
        self.show_pass = False

        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.pack(expand=True, fill="both", padx=20, pady=20)
        ctk.CTkLabel(self.main_frame, text="Authorization", font=("Arial", 22, "bold")).pack(pady=20)

        self.grid_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.grid_frame.pack()

        self.user_e = ctk.CTkEntry(self.grid_frame, placeholder_text="Username", width=250)
        self.user_e.grid(row=0, column=0, pady=5)
        ctk.CTkLabel(self.grid_frame, text="", width=45).grid(row=0, column=1)

        self.pass_e = ctk.CTkEntry(self.grid_frame, placeholder_text="Password", show="*", width=250)
        self.pass_e.grid(row=1, column=0, pady=5)
        ctk.CTkButton(self.grid_frame, text="👁", width=45, fg_color="transparent", command=self.toggle_pass).grid(row=1,
                                                                                                                  column=1,
                                                                                                                  padx=5)

        ctk.CTkButton(self.main_frame, text="Login", command=self.login, width=305, **BTN_STYLE).pack(pady=15)
        ctk.CTkButton(self.main_frame, text="Create Account", fg_color="transparent", text_color="#aaaaaa",
                      command=lambda: RegisterWindow(self.db)).pack()

    def toggle_pass(self):
        self.show_pass = not self.show_pass
        self.pass_e.configure(show="" if self.show_pass else "*")

    def login(self):
        if self.db.check_user(self.user_e.get(), self.pass_e.get()):
            self.withdraw()
            self.quit()
        else:
            messagebox.showerror("Error", "Login failed")


class ArbitrageApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("PoE 2 Trade Assistant")
        self.geometry("1100x850")
        self.db = Database()
        self.dropdown = AutocompleteDropdown(self, self.on_item_select)
        self.active_entry = None

        ctk.CTkLabel(self, text="PoE 2 Currency Monitoring", font=("Arial", 22, "bold")).pack(pady=15)

        self.input_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.input_frame.pack(pady=10, padx=20, fill="x")
        self.item_from = ctk.CTkEntry(self.input_frame, placeholder_text="Give", width=180)
        self.item_from.grid(row=0, column=0, padx=5, pady=20)
        self.amount_n = ctk.CTkEntry(self.input_frame, placeholder_text="Qty", width=70)
        self.amount_n.grid(row=0, column=1, padx=5)
        ctk.CTkButton(self.input_frame, text="<->", width=40, command=self.reverse_inputs, **BTN_STYLE).grid(row=0,
                                                                                                             column=2,
                                                                                                             padx=5)
        self.amount_x = ctk.CTkEntry(self.input_frame, placeholder_text="Qty", width=70)
        self.amount_x.grid(row=0, column=3, padx=5)
        self.item_to = ctk.CTkEntry(self.input_frame, placeholder_text="Get", width=180)
        self.item_to.grid(row=0, column=4, padx=5)
        ctk.CTkButton(self.input_frame, text="Add Rate", command=self.add_rate, width=100, **BTN_STYLE).grid(row=0,
                                                                                                             column=5,
                                                                                                             padx=10)

        self.calc_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.calc_frame.pack(pady=15, padx=20, fill="x")
        self.calc_start = ctk.CTkEntry(self.calc_frame, placeholder_text="From", width=200)
        self.calc_start.grid(row=0, column=0, padx=10, pady=15)
        self.calc_end = ctk.CTkEntry(self.calc_frame, placeholder_text="To", width=200)
        self.calc_end.grid(row=0, column=1, padx=10)
        ctk.CTkButton(self.calc_frame, text="Find Best Route", command=self.run_calculation, **BTN_STYLE).grid(row=0,
                                                                                                               column=2,
                                                                                                               padx=10)

        for entry in [self.item_from, self.item_to, self.calc_start, self.calc_end]:
            entry.bind("<KeyRelease>", self.on_key_release)

        self.ctrl_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.ctrl_frame.pack(fill="x", padx=20)
        ctk.CTkButton(self.ctrl_frame, text="Show All", command=self.refresh_view, **BTN_STYLE).pack(side="left",
                                                                                                     padx=5,
                                                                                                     expand=True)
        ctk.CTkButton(self.ctrl_frame, text="Ninja Update", command=self.update_from_web, **BTN_STYLE).pack(side="left",
                                                                                                            padx=5,
                                                                                                            expand=True)
        ctk.CTkButton(self.ctrl_frame, text="Clear DB", command=self.clear_db, **BTN_STYLE).pack(side="left", padx=5,
                                                                                                 expand=True)

        self.result_box = ctk.CTkTextbox(self, height=400, font=("Consolas", 14))
        self.result_box.pack(pady=10, padx=20, fill="both")
        self.refresh_view()

    def on_key_release(self, event):
        entry = event.widget
        text = entry.get().strip().lower()
        if not text:
            self.dropdown.withdraw()
            return
        self.active_entry = entry
        items = set()
        for r in self.db.get_all_rates(): items.update([r[0], r[1]])
        matches = [i for i in items if text in i.lower()]
        self.dropdown.update_list(matches[:10], entry.winfo_rootx(), entry.winfo_rooty() + entry.winfo_height())

    def on_item_select(self, item):
        if self.active_entry:
            self.active_entry.delete(0, 'end')
            self.active_entry.insert(0, item)
            self.dropdown.withdraw()

    def reverse_inputs(self):
        f, t = self.item_from.get(), self.item_to.get()
        self.item_from.delete(0, 'end')
        self.item_from.insert(0, t)
        self.item_to.delete(0, 'end')
        self.item_to.insert(0, f)

    def add_rate(self):
        n = logic.clean_num(self.amount_n.get())
        x = logic.clean_num(self.amount_x.get())
        f = self.item_from.get().strip()
        t = self.item_to.get().strip()

        if n and x and f and t:
            self.db.update_rate(f, t, n, x)

            self.amount_n.delete(0, 'end')
            self.amount_x.delete(0, 'end')

            self.refresh_view()
        else:
            messagebox.showwarning("Warning", "Please fill all fields correctly")

    def run_calculation(self):
        start, end = self.calc_start.get().strip(), self.calc_end.get().strip()
        if start and end:
            res = logic.find_best_route(self.db.get_all_rates(), start, end)
            self.result_box.delete("1.0", "end")
            self.result_box.insert("end", res)

    def update_from_web(self):
        data = parser.fetch_poe_prices()
        if data:
            for f, t, n, x in data: self.db.update_rate(f, t, n, x)
            self.refresh_view()
            messagebox.showinfo("Ninja", "Done")

    def refresh_view(self):
        self.result_box.delete("1.0", "end")
        for r in self.db.get_all_rates(): self.result_box.insert("end", f"{r[0]} -> {r[1]}: {r[2]} to {r[3]}\n")

    def clear_db(self):
        if messagebox.askyesno("Clear", "Delete all?"): self.db.clear_all(); self.refresh_view()


if __name__ == "__main__":
    auth = LoginWindow()
    auth.mainloop()
    try:
        auth.destroy()
        app = ArbitrageApp()
        app.mainloop()
    except Exception:
        pass