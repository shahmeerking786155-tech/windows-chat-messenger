import json
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from pathlib import Path

DATA_FILE = Path(__file__).with_name("chats.json")
DEFAULT_CONTACTS = ["Ayesha", "Ali", "Ahmed", "Sara", "Usman", "Fatima"]

class ChatMessenger:
    def __init__(self, root):
        self.root = root
        self.root.title("Windows Chat Messenger")
        self.root.geometry("1000x650")
        self.root.minsize(780, 520)
        self.root.configure(bg="#f0f2f5")
        self.selected_contact = None
        self.search_var = tk.StringVar()
        self.message_var = tk.StringVar()
        self.data = self.load_chats()

        self.setup_style()
        self.build_ui()
        self.refresh_contacts()

    def load_chats(self):
        if not DATA_FILE.exists():
            data = {"contacts": DEFAULT_CONTACTS, "chats": {name: [] for name in DEFAULT_CONTACTS}}
            self.write_data(data)
            return data
        try:
            with DATA_FILE.open("r", encoding="utf-8") as file:
                data = json.load(file)
            data.setdefault("contacts", DEFAULT_CONTACTS)
            data.setdefault("chats", {})
            for name in data["contacts"]:
                data["chats"].setdefault(name, [])
            return data
        except (json.JSONDecodeError, OSError):
            messagebox.showwarning("Chat data", "chats.json could not be read. A fresh chat file will be created.")
            data = {"contacts": DEFAULT_CONTACTS, "chats": {name: [] for name in DEFAULT_CONTACTS}}
            self.write_data(data)
            return data

    def write_data(self, data=None):
        if data is None:
            data = self.data
        with DATA_FILE.open("w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    def setup_style(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("Treeview", font=("Segoe UI", 10), rowheight=38,
                        background="white", fieldbackground="white")
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))

    def build_ui(self):
        header = tk.Frame(self.root, bg="#075e54", height=64)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text="  Windows Chat Messenger", bg="#075e54", fg="white",
                 font=("Segoe UI", 18, "bold")).pack(side="left", padx=12)
        tk.Label(header, text="LOCAL DEMO", bg="#128c7e", fg="white",
                 font=("Segoe UI", 9, "bold"), padx=10, pady=5).pack(side="right", padx=18, pady=15)

        main = tk.Frame(self.root, bg="#f0f2f5")
        main.pack(fill="both", expand=True, padx=14, pady=14)

        sidebar = tk.Frame(main, bg="white", width=280)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        tk.Label(sidebar, text="Chats", bg="white", fg="#111b21",
                 font=("Segoe UI", 17, "bold")).pack(anchor="w", padx=16, pady=(16, 10))
        search = tk.Entry(sidebar, textvariable=self.search_var, font=("Segoe UI", 10),
                          relief="flat", bg="#f0f2f5")
        search.pack(fill="x", padx=14, ipady=9)
        search.insert(0, "")
        self.search_var.trace_add("write", lambda *_: self.refresh_contacts())

        self.contact_list = tk.Listbox(sidebar, font=("Segoe UI", 11), bd=0,
                                       highlightthickness=0, activestyle="none",
                                       selectbackground="#d9fdd3", selectforeground="#111b21")
        self.contact_list.pack(fill="both", expand=True, padx=8, pady=12)
        self.contact_list.bind("<<ListboxSelect>>", self.on_contact_select)

        right = tk.Frame(main, bg="#efeae2")
        right.pack(side="left", fill="both", expand=True, padx=(12, 0))

        self.chat_header = tk.Frame(right, bg="#f0f2f5", height=62)
        self.chat_header.pack(fill="x")
        self.chat_header.pack_propagate(False)
        self.contact_title = tk.Label(self.chat_header, text="Select a contact",
                                      bg="#f0f2f5", fg="#111b21", font=("Segoe UI", 13, "bold"))
        self.contact_title.pack(side="left", padx=18, pady=18)
        tk.Button(self.chat_header, text="Delete chat", command=self.delete_chat,
                  bg="#ffffff", fg="#b42318", relief="flat", padx=12, pady=7,
                  font=("Segoe UI", 9, "bold"), cursor="hand2").pack(side="right", padx=12, pady=12)

        conversation = tk.Frame(right, bg="#efeae2")
        conversation.pack(fill="both", expand=True)
        self.messages = tk.Text(conversation, wrap="word", state="disabled", bd=0,
                               bg="#efeae2", font=("Segoe UI", 11), padx=18, pady=16,
                               spacing1=4, spacing3=10)
        self.messages.pack(side="left", fill="both", expand=True)
        scrollbar = ttk.Scrollbar(conversation, command=self.messages.yview)
        scrollbar.pack(side="right", fill="y")
        self.messages.configure(yscrollcommand=scrollbar.set)
        self.messages.tag_configure("sent", justify="right", foreground="#075e54",
                                    lmargin1=100, lmargin2=100, rmargin=12,
                                    spacing1=8, spacing3=3)
        self.messages.tag_configure("time", justify="right", foreground="#667781",
                                    font=("Segoe UI", 8), rmargin=12, spacing3=8)
        self.messages.tag_configure("received", justify="left", foreground="#202c33",
                                    lmargin1=12, lmargin2=12, rmargin=100,
                                    spacing1=8, spacing3=3)
        self.messages.tag_configure("received_time", justify="left", foreground="#667781",
                                    font=("Segoe UI", 8), lmargin1=12, spacing3=8)

        composer = tk.Frame(right, bg="#f0f2f5", padx=10, pady=10)
        composer.pack(fill="x")
        self.message_entry = tk.Entry(composer, textvariable=self.message_var,
                                      font=("Segoe UI", 11), relief="flat")
        self.message_entry.pack(side="left", fill="x", expand=True, ipady=12, padx=(0, 8))
        self.message_entry.bind("<Return>", lambda event: self.send_message())
        tk.Button(composer, text="Send", command=self.send_message,
                  bg="#075e54", fg="white", activebackground="#128c7e",
                  activeforeground="white", relief="flat", padx=22, pady=10,
                  font=("Segoe UI", 10, "bold"), cursor="hand2").pack(side="right")

        self.show_welcome()

    def show_welcome(self):
        self.messages.configure(state="normal")
        self.messages.delete("1.0", "end")
        self.messages.insert("end", "Welcome to Windows Chat Messenger\n\n", "received")
        self.messages.insert("end", "Choose a contact from the left panel to open a conversation.", "received")
        self.messages.configure(state="disabled")

    def refresh_contacts(self):
        query = self.search_var.get().strip().lower()
        self.visible_contacts = [name for name in self.data["contacts"] if query in name.lower()]
        self.contact_list.delete(0, "end")
        for name in self.visible_contacts:
            self.contact_list.insert("end", "   " + name)
        if self.selected_contact in self.visible_contacts:
            index = self.visible_contacts.index(self.selected_contact)
            self.contact_list.selection_set(index)

    def on_contact_select(self, _event=None):
        selection = self.contact_list.curselection()
        if not selection:
            return
        self.selected_contact = self.visible_contacts[selection[0]]
        self.contact_title.config(text=self.selected_contact)
        self.refresh_messages()

    def refresh_messages(self):
        self.messages.configure(state="normal")
        self.messages.delete("1.0", "end")
        chat = self.data["chats"].get(self.selected_contact, [])
        if not chat:
            self.messages.insert("end", "No messages yet. Say hello!\n", "received")
        for item in chat:
            if item.get("sender") == "You":
                self.messages.insert("end", "You: " + item.get("text", "") + "\n", "sent")
                self.messages.insert("end", item.get("time", "") + "\n", "time")
            else:
                self.messages.insert("end", self.selected_contact + ": " + item.get("text", "") + "\n", "received")
                self.messages.insert("end", item.get("time", "") + "\n", "received_time")
        self.messages.configure(state="disabled")
        self.messages.see("end")

    def send_message(self):
        if not self.selected_contact:
            messagebox.showinfo("Select contact", "Please select a contact first.")
            return
        text = self.message_var.get().strip()
        if not text:
            messagebox.showwarning("Empty message", "Please type a message before sending.")
            return
        timestamp = datetime.now().strftime("%I:%M %p")
        self.data["chats"].setdefault(self.selected_contact, []).append(
            {"sender": "You", "text": text, "time": timestamp}
        )
        self.write_data()
        self.message_var.set("")
        self.refresh_messages()
        self.message_entry.focus_set()

    def delete_chat(self):
        if not self.selected_contact:
            messagebox.showinfo("Select contact", "Please select a contact first.")
            return
        if messagebox.askyesno("Delete conversation",
                               f"Delete the conversation with {self.selected_contact}?"):
            self.data["chats"][self.selected_contact] = []
            self.write_data()
            self.refresh_messages()

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatMessenger(root)
    root.mainloop()
