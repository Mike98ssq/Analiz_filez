import customtkinter as ctk
from gui import AnalyticsApp

if __name__ == "__main__":
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("dark-blue")
    root = ctk.CTk()
    app = AnalyticsApp(root)
    root.mainloop()