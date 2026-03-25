# KeyStroke Sentinel - Secure Keyboard Activity Visualizer

A **safe, educational Tkinter-based keyboard activity visualizer** that helps users understand how keyboard events work in real-time.  
It captures and displays **Pressed**, **Held**, and **Released** key events **only inside the app’s own typing area**, making it ideal for **learning, demonstrations, and cyber security awareness**.

> **Important:** This project is designed for **ethical, educational, and authorized use only**. It **does not monitor other applications or the operating system globally**.

---

## Features

- **Safe Keyboard Event Monitoring**
  - Tracks keys **only within the application’s text box**
  - No system-wide or background capture

- **Live Event Visualization**
  - Displays:
    - `Pressed`
    - `Held`
    - `Released`

- **Automatic Logging**
  - Saves readable key activity to:
    - `logs.txt`
  - Saves structured event data to:
    - `logs.json`

- **Session Summary Export**
  - Exports summary information to:
    - `summary.json`

- **Interactive GUI**
  - Start Logging
  - Stop Logging
  - Clear Logs
  - View Saved Logs
  - Export Summary
  - Exit

- **Real-Time Stats**
  - Shows current logging status
  - Displays total number of key events captured

---

## Technologies Used

- **Python 3**
- **Tkinter**
- **JSON**
- **File Handling**

---

## Project Structure

```bash
KeyStroke-Sentinel/
│
├── keylogger.py        # Main application
├── logs.txt            # Human-readable saved keystrokes
├── logs.json           # Structured keyboard event logs
├── summary.json        # Session summary report
└── README.md           # Project documentation
```

## How to Run
### 1. Clone the repository
```bash
git clone https://github.com/your-username/your-repository-name.git
cd your-repository-name
```
### 2. Run the Python file
```bash
python keylogger.py
```
- Make sure Python 3 is installed on your system.

## How It Works
- Launch the application.
- Click Start Logging.
- Type inside the input box provided in the GUI.
### The app will:
- Show live keyboard events
- Save logs automatically
- Click Stop Logging to stop monitoring.
### Use:
- View Saved Logs to inspect saved content
- Export Summary to save session details
- Output Files
- logs.txt

- Stores typed content in a human-readable format.

### Example:
```bash
hello world
logs.json
```
- Stores keyboard activity in structured JSON format.

### Example:
```bash
[
    {
        "Pressed": "h"
    },
    {
        "Held": "h"
    },
    {
        "Released": "h"
    }
]
```
- summary.json

### Stores a session summary.

### Example:
```bash
{
    "total_events": 18,
    "session_duration_seconds": 12.45,
    "last_key": "d",
    "all_keys": "hello world"
}
```
---

## Use Cases
- Python GUI practice
- Keyboard event handling demonstration
- Cyber security awareness presentations
- Educational workshops
- Mini project / internship submission

## Safety & Ethical Notice

### This application is intentionally built as a safe educational demo:

- It does not capture keyboard input outside the application
- It does not run silently in the background
- It is intended only for learning, testing, and demonstration

### Please do not modify or use this type of concept for:
- unauthorized monitoring
- privacy invasion
- credential capture
- surveillance without consent

### Use responsibly and ethically.

## Future Enhancements

### Possible upgrades for future versions:

- Dark mode UI
- Typing speed analytics
- Graph-based session reports
- Timestamped event logging
- Export to CSV / PDF
- Search and filter logs
- Improved dashboard design
  ---
## Author

### Indrasen Singh
### B.Tech CSE Student | Web Developer | ML & AI Enthusiast | Creative Coder

## License

- This project is intended for educational use.
- You may customize it for learning and demonstration purposes.
