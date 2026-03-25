import tkinter as tk
from tkinter import ttk, messagebox
import json
import time
import os

# ----------------------------------------------------------------------
# Constants
# ----------------------------------------------------------------------
TXT_FILE = "logs.txt"
JSON_FILE = "logs.json"
SUMMARY_FILE = "summary.json"

# ----------------------------------------------------------------------
# Main Application Class
# ----------------------------------------------------------------------
class KeyloggerApp:
    """
    A safe educational keylogger demo.
    Logs keystrokes from a designated text widget and saves them to files.
    """

    def __init__(self, root):
        self.root = root
        self.root.title("KeyStroke Sentinel - Secure Keyboard Activity Visualizer")
        self.root.geometry("620x650")
        self.root.configure(bg="lightgreen")

        # Data structures
        self.key_list = []          # list of key events (for JSON)
        self.key_strokes = ""       # concatenated readable text (for TXT)
        self.held_flag = False      # flag to track press/hold status
        self.last_pressed_key = None
        self.start_time = None
        self.logging_active = False

        # Initialize files
        self._initialize_files()

        # Build GUI
        self._create_widgets()

        # Bind key events to the input text widget
        self.input_box.bind("<KeyPress>", self.on_press)
        self.input_box.bind("<KeyRelease>", self.on_release)

    # ------------------------------------------------------------------
    # File Handling Methods
    # ------------------------------------------------------------------
    def _initialize_files(self):
        """Create empty files if they do not exist."""
        if not os.path.exists(TXT_FILE):
            with open(TXT_FILE, "w", encoding="utf-8") as f:
                f.write("")

        if not os.path.exists(JSON_FILE):
            with open(JSON_FILE, "w", encoding="utf-8") as f:
                json.dump([], f, indent=4)

        if not os.path.exists(SUMMARY_FILE):
            with open(SUMMARY_FILE, "w", encoding="utf-8") as f:
                json.dump({}, f, indent=4)

    def _update_txt_file(self):
        """Write current key_strokes to the text file."""
        with open(TXT_FILE, "w", encoding="utf-8") as f:
            f.write(self.key_strokes.strip())

    def _update_json_file(self):
        """Write current key_list to the JSON file."""
        with open(JSON_FILE, "w", encoding="utf-8") as f:
            json.dump(self.key_list, f, indent=4)

    def _update_summary_file(self):
        """Write a summary of the current session to the JSON summary file."""
        duration = round(time.time() - self.start_time, 2) if self.start_time else 0
        summary = {
            "total_events": len(self.key_list),
            "session_duration_seconds": duration,
            "last_key": self.last_pressed_key,
            "all_keys": self.key_strokes.strip()
        }
        with open(SUMMARY_FILE, "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=4)

    def _update_all_files(self):
        """Convenience method to update all three files."""
        self._update_txt_file()
        self._update_json_file()
        self._update_summary_file()

    # ------------------------------------------------------------------
    # UI Helper Methods
    # ------------------------------------------------------------------
    def _add_output(self, text):
        """Append a line to the output text widget and scroll to the end."""
        self.output_box.insert(tk.END, text + "\n")
        self.output_box.see(tk.END)

    def _update_stats(self):
        """Update the status label with the current number of key events."""
        total_keys = len(self.key_list)
        self.stats_var.set(f"Keys Logged: {total_keys}")

    # ------------------------------------------------------------------
    # Event Handlers (Key Press / Release)
    # ------------------------------------------------------------------
    def on_press(self, event):
        """Handle key press events (only when logging is active)."""
        if not self.logging_active:
            return

        key = event.keysym
        self.last_pressed_key = key

        # Record press/hold events
        if not self.held_flag:
            self.key_list.append({"Pressed": key})
            self._add_output(f"[Pressed] {key}")
            self.held_flag = True
        else:
            self.key_list.append({"Held": key})
            self._add_output(f"[Held] {key}")

        # Build readable text log
        if len(key) == 1:
            self.key_strokes += key
        elif key == "space":
            self.key_strokes += " "
        elif key == "Return":
            self.key_strokes += "\n"
        elif key == "Tab":
            self.key_strokes += "\t"
        else:
            self.key_strokes += f" <{key}> "

        # Update files and UI
        self._update_all_files()
        self._update_stats()

    def on_release(self, event):
        """Handle key release events (only when logging is active)."""
        if not self.logging_active:
            return

        key = event.keysym
        self.key_list.append({"Released": key})
        self._add_output(f"[Released] {key}")

        if self.held_flag:
            self.held_flag = False

        self._update_all_files()
        self._update_stats()

    # ------------------------------------------------------------------
    # Button Commands
    # ------------------------------------------------------------------
    def start_logging(self):
        """Start capturing keystrokes."""
        if self.logging_active:
            self._add_output("[!] Logging already active.")
            return

        self.logging_active = True
        self.start_time = time.time()

        self.status_var.set("Status: Logging Active")
        self._add_output("[+] Logging started successfully!")
        self._add_output(f"[!] Saving key logs in '{JSON_FILE}' and '{TXT_FILE}'")
        self._add_output("[*] Type inside the input box below...")
        self.input_box.focus_set()

    def stop_logging(self):
        """Stop capturing keystrokes."""
        if not self.logging_active:
            self._add_output("[!] Logging is not active.")
            return

        self.logging_active = False
        self.status_var.set("Status: Logging Stopped")
        self._update_summary_file()
        self._add_output("[!] Logging stopped.")

    def clear_logs(self):
        """Clear all recorded data and reset the UI."""
        self.key_list = []
        self.key_strokes = ""
        self.held_flag = False
        self.last_pressed_key = None
        self.start_time = None
        self.logging_active = False

        self._update_all_files()
        self.output_box.delete("1.0", tk.END)
        self.input_box.delete("1.0", tk.END)

        self.stats_var.set("Keys Logged: 0")
        self.status_var.set("Status: Idle")
        self._add_output("[*] Logs cleared successfully.")

    def export_summary(self):
        """Force an update of the summary file."""
        self._update_summary_file()
        self._add_output(f"[+] Summary exported to '{SUMMARY_FILE}'")

    def view_saved_logs(self):
        """Display the contents of logs.txt and logs.json in the output area."""
        self._add_output("\n========== SAVED logs.txt ==========")
        try:
            with open(TXT_FILE, "r", encoding="utf-8") as f:
                txt_data = f.read().strip()
                self._add_output(txt_data if txt_data else "(logs.txt is empty)")
        except Exception as e:
            self._add_output(f"Error reading logs.txt: {e}")

        self._add_output("========== SAVED logs.json ==========")
        try:
            with open(JSON_FILE, "r", encoding="utf-8") as f:
                json_data = json.load(f)
                self._add_output(json.dumps(json_data, indent=4))
        except Exception as e:
            self._add_output(f"Error reading logs.json: {e}")

    def exit_app(self):
        """Close the application."""
        self.root.destroy()

    # ------------------------------------------------------------------
    # GUI Construction
    # ------------------------------------------------------------------
    def _create_widgets(self):
        """Create and arrange all GUI elements."""
        # Header
        header = tk.Label(
            self.root,
            text="KeyStroke Sentinel - Secure Keyboard Activity Visualizer",
            font=('Verdana', 15, 'bold'),
            bg="lightgreen"
        )
        header.pack(pady=12)

        # Status line
        self.status_var = tk.StringVar(value="Status: Idle")
        status_label = tk.Label(
            self.root,
            textvariable=self.status_var,
            font=('Arial', 11, 'bold'),
            bg="lightgreen",
            fg="blue"
        )
        status_label.pack()

        # Stats line
        self.stats_var = tk.StringVar(value="Keys Logged: 0")
        stats_label = tk.Label(
            self.root,
            textvariable=self.stats_var,
            font=('Arial', 11),
            bg="lightgreen"
        )
        stats_label.pack(pady=5)

        # Input area label
        input_label = tk.Label(
            self.root,
            text="Type Here (Only this box is monitored):",
            font=('Arial', 11, 'bold'),
            bg="lightgreen"
        )
        input_label.pack(pady=6)

        # Text widget for user input
        self.input_box = tk.Text(self.root, height=7, width=65, font=("Consolas", 11))
        self.input_box.pack(pady=6)

        # Output area label
        output_label = tk.Label(
            self.root,
            text="Live Key Events:",
            font=('Arial', 11, 'bold'),
            bg="lightgreen"
        )
        output_label.pack(pady=6)

        # Text widget for logging output
        self.output_box = tk.Text(
            self.root,
            height=18,
            width=72,
            font=("Consolas", 10),
            bg="white",
            fg="black"
        )
        self.output_box.pack(pady=6)

        # Button frame
        btn_frame = tk.Frame(self.root, bg="lightgreen")
        btn_frame.pack(pady=12)

        # Row 0 buttons
        tk.Button(
            btn_frame, text="Start Logging", command=self.start_logging, width=16,
            bg="green", fg="white"
        ).grid(row=0, column=0, padx=6, pady=6)

        tk.Button(
            btn_frame, text="Stop Logging", command=self.stop_logging, width=16,
            bg="red", fg="white"
        ).grid(row=0, column=1, padx=6, pady=6)

        tk.Button(
            btn_frame, text="Clear Logs", command=self.clear_logs, width=16,
            bg="orange", fg="black"
        ).grid(row=0, column=2, padx=6, pady=6)

        # Row 1 buttons
        tk.Button(
            btn_frame, text="Export Summary", command=self.export_summary, width=16,
            bg="blue", fg="white"
        ).grid(row=1, column=0, padx=6, pady=6)

        tk.Button(
            btn_frame, text="View Saved Logs", command=self.view_saved_logs, width=16,
            bg="purple", fg="white"
        ).grid(row=1, column=1, padx=6, pady=6)

        tk.Button(
            btn_frame, text="Exit", command=self.exit_app, width=16,
            bg="black", fg="white"
        ).grid(row=1, column=2, padx=6, pady=6)


# ----------------------------------------------------------------------
# Run the Application
# ----------------------------------------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = KeyloggerApp(root)
    root.mainloop()