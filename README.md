# Desktop AI Assistant

A modern voice-controlled desktop assistant built with Python and Tkinter that helps you control your computer using voice commands and provides a clean GUI for quick app launching.

## 🌟 Features

### Voice Assistant
- **Speech Recognition**: Uses Google Speech Recognition for accurate voice command processing
- **Text-to-Speech**: Responds with both male and female voice options
- **Real-time Status**: Live status updates and command history display
- **Threading**: Non-blocking voice processing that keeps the GUI responsive

### App Launcher
- **Quick Launch**: One-click access to commonly used applications
- **Icon Support**: Beautiful app icons with hover effects
- **Customizable**: Easy to add or remove applications from the launcher

### Voice Commands
- **Wikipedia Search**: `"wikipedia [topic]"` - Search and read Wikipedia articles
- **Web Browsing**: `"open youtube"`, `"open google"`
- **System Apps**: 
  - Open: `"open notepad"`, `"open calculator"`, `"open camera"`, etc.
  - Close: `"close notepad"`, `"close calculator"`, etc.
- **Screenshots**: `"take screenshot"` - Capture and save screenshots
- **Control**: `"quit"` or `"bye"` - Stop the assistant

## 🚀 Installation

### Prerequisites
- Python 3.7 or higher
- Windows OS (for Windows-specific app commands)

### Dependencies
Install required packages using pip:

```bash
pip install -r requirements.txt
```

**Required packages:**
```
tkinter
pyttsx3
SpeechRecognition
wikipedia
pyautogui
psutil
pillow
googlesearch-python
beautifulsoup4
requests
pygetwindow
```

## Run the application
python main.py
```

## 📁 Project Structure

```
simple-desktop-app/
├── src/
│   ├── ui/
│   │   ├── app_window.py      # Main GUI application
│   │   └── icons/             # App icons directory
│   │       ├── whatsapp.png
│   │       ├── notepad.png
│   │       ├── calculator.png
│   │       └── ...
├── screenshots/               # Screenshots storage
├── main.py                   # Application entry point
├── requirements.txt          # Python dependencies
└── README.md                # This file
```

## 🎯 Usage

### Starting the Assistant
1. Run the application: `python main.py`
2. Choose your preferred voice (Male/Female)
3. Test your microphone with "Check mic" button
4. Click "Start Assistant" to begin voice control

### Voice Commands Examples
```
"wikipedia artificial intelligence"
"open notepad"
"close calculator"
"take screenshot"
"open youtube"
"quit"
```

### App Launcher
- Click any app icon to launch the corresponding application
- Apps are organized in a clean grid layout
- Hover over icons for tooltips (if implemented)

## ⚙️ Configuration

### Adding New Apps
Edit the `apps` list in `app_window.py`:

```python
apps = [
    {"name": "Your App", "icon": "icons/yourapp.png", "command": lambda: os.system("your_command_here")},
    # Add more apps here
]
```

### Customizing Voice Commands
Add new voice commands in the `background_assistant_task()` method:

```python
elif 'your command' in query:
    self.message_queue.put("🔧 Executing your command...")
    # Your command logic here
```

## 🛠️ Technical Details

### Architecture
- **Threading**: Uses Python threading for non-blocking voice processing
- **Queue System**: Thread-safe message passing between background tasks and GUI
- **Polling**: 100ms polling interval for real-time GUI updates
- **Error Handling**: Comprehensive exception handling for robust operation

### Voice Processing
- **Recognition**: Google Speech Recognition API
- **Language**: English (UK) - configurable in code
- **TTS Engine**: pyttsx3 with Windows SAPI voices
- **Audio**: Uses default system microphone

## 🎨 UI Features

- **Modern Design**: Clean, flat design with intuitive colors
- **Responsive Layout**: Grid-based app launcher that adapts to screen size
- **Status Display**: Real-time command processing and system status
- **Color Coding**: Different colors for success, error, and status messages

## 🐛 Known Issues

- Requires internet connection for Google Speech Recognition
- Windows-specific app commands may not work on other OS
- Some antivirus software may flag voice recognition as suspicious

## 🔮 Future Enhancements

- [ ] Offline speech recognition support
- [ ] Custom hotkey activation
- [ ] Plugin system for extensibility
- [ ] Multi-language support
- [ ] AI chat integration
- [ ] Smart home device control
- [ ] Custom voice training


## 🙏 Acknowledgments

- Google Speech Recognition API
- Microsoft Speech API (SAPI)
- Python Tkinter community
- All open-source contributors

---

Made with ❤️ by Sandeep Ganesh # Desktop-Assistant
