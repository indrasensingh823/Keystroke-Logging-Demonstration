import tkinter as tk

class KeyloggerApp:
    """A minimal Tkinter application window for a keylogger project."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Keylogger Project")
        self.root.geometry("150x200")
        
        # Optional: Add a simple label to demonstrate the window content
        label = tk.Label(
            self.root,
            text="Keylogger App",
            font=('Arial', 12, 'bold')
        )
        label.pack(pady=20)
        
        # You can add more widgets here later
        
    def run(self):
        """Start the Tkinter main loop."""
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = KeyloggerApp(root)
    app.run()