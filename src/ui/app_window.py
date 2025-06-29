import re
from googlesearch import search
import tkinter as tk
import pyttsx3 as p
import speech_recognition as sr
import datetime
import wikipedia
import os
import psutil
import pyautogui
import random
import webbrowser
from PIL import Image, ImageTk
import threading
import queue

class AppWindow:
    def __init__(self, master):
        """
        Initialize the AppWindow class.
        
        Parameters:
        master (tk.Tk): The main window of the application.
        """
        self.k = 0  # default voice index
        self.master = master  # Set the master window
        self.running = False  # Flag to control the assistant
        
        # Create thread-safe queue for messages
        self.message_queue = queue.Queue()
        
        # Create main label
        self.label = tk.Label(
            master,
            text="Desktop Assistant - Ready",
            font=("Arial", 16, "bold"), 
            bg="#F8F9FA",
            fg="#2C3E50",
            bd=3,
            padx=10, pady=10,
            relief=tk.RAISED,
            anchor="center"
        )
        self.label.pack(pady=5)

        # Voice selection buttons frame
        button_frame = tk.Frame(master)
        button_frame.pack(pady=10)

        # Male Voice button
        self.change_button = tk.Button(
            button_frame, 
            text="Male Voice", 
            bg="#3498DB",
            fg="white",
            command=self.male_voice
        )
        self.change_button.pack(side=tk.LEFT, padx=10) 

        # Female Voice button
        self.female_button = tk.Button(
            button_frame, 
            text="Female Voice", 
            bg="#E91E63",
            fg="white",
            activebackground="#C2185B",
            command=self.female_voice
        )
        self.female_button.pack(side=tk.LEFT, padx=10) 

        # Mic check button
        self.display_button = tk.Button(
            master, 
            text="Check mic", 
            bg="#4CAF50",
            fg="white",
            command=self.display_text
        )
        self.display_button.pack(pady=15)

        # Run/Stop button
        self.run_button = tk.Button(
            master, 
            text="Start Assistant", 
            bg="#FF6B35",
            fg="white",
            command=self.toggle_assistant
        )
        self.run_button.pack(pady=5)

        # Status display area
        self.status_text = tk.Text(
            master,
            height=8,
            width=80,
            bg="#F5F5F5",
            fg="#2C3E50",
            font=("Consolas", 9),
            state=tk.DISABLED
        )
        self.status_text.pack(pady=10, padx=20, fill="both")

        # App launcher configuration
        apps = [
            {"name": "WhatsApp", "icon": "icons/whatsapp.png", "command": lambda: os.system("start whatsapp://")},
            {"name": "Planner", "icon": "icons/planner.png", "command": lambda: os.system("start outlookcal://")},
            {"name": "Notepad", "icon": "icons/notepad.png", "command": lambda: os.system("notepad.exe")},
            {"name": "Calculator", "icon": "icons/calculator.png", "command": lambda: os.system("calc.exe")},
            {"name": "Camera", "icon": "icons/camera.png", "command": lambda: os.system("start microsoft.windows.camera:")},
            {"name": "Paint", "icon": "icons/paint.png", "command": lambda: os.system("mspaint")},
            {"name": "Browser", "icon": "icons/browser.png", "command": lambda: os.system("start chrome")},
            {"name": "File Explorer", "icon": "icons/explorer.png", "command": lambda: os.system("explorer")},
            {"name": "Settings", "icon": "icons/settings.png", "command": lambda: os.system("start ms-settings:")},
            {"name": "Task Manager", "icon": "icons/taskmgr.png", "command": lambda: os.system("taskmgr")},
        ]

        # App launcher frame
        columns_per_row = 15
        app_frame = tk.Frame(master, bg="#ECEFF1", bd=1, relief=tk.SOLID)
        app_frame.pack(pady=10, padx=20, fill="both")
        self.app_icons = []

        # Create app launcher buttons
        for idx, app in enumerate(apps):
            row = idx // columns_per_row
            col = idx % columns_per_row
            app_frame.grid_rowconfigure(row, weight=1)
            try:
                # Load and resize icon
                icon_path = os.path.join(os.path.dirname(__file__), app["icon"])
                icon_path = os.path.abspath(icon_path)
                icon = Image.open(icon_path)
                icon = icon.resize((50, 50), Image.Resampling.LANCZOS)
                icon = ImageTk.PhotoImage(icon)
                self.app_icons.append(icon)
                
                # Create button with icon
                button = tk.Button(
                    app_frame, 
                    text=app["name"], 
                    image=icon, 
                    compound=tk.TOP,
                    bg="#FFFFFF",
                    fg="#2C3E50",
                    bd=1,
                    relief=tk.SOLID,
                    command=app["command"],
                    anchor="center",
                    width=80, 
                    height=80, 
                    font=("Segoe UI", 8) 
                )
                button.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
                
            except Exception as e:
                print(f"Error loading icon for {app['name']}: {e}")
                # Create button without icon
                button = tk.Button(
                    app_frame, 
                    text=app["name"],
                    bg="#FFFFFF",
                    fg="#2C3E50",
                    bd=1,
                    relief=tk.SOLID,
                    command=app["command"]
                )
                button.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

        # Start queue checker
        self.check_queue()

        # Initialize with greeting
        self.add_message("🤖 Desktop Assistant initialized")
        self.add_message("💡 Available commands: 'wikipedia [topic]', 'open [app]', 'close [app]', 'take screenshot', etc.")

    def add_message(self, message):
        """Add a message to the status display"""
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}"
        
        self.status_text.config(state=tk.NORMAL)
        self.status_text.insert(tk.END, formatted_message + "\n")
        self.status_text.see(tk.END)  # Auto-scroll to bottom
        self.status_text.config(state=tk.DISABLED)
        self.status_text.update()

    def check_queue(self):
        """Check message queue and update GUI"""
        try:
            while True:
                message = self.message_queue.get_nowait()
                if message.startswith("STATUS:"):
                    # Update main label
                    self.label.config(text=message[7:], bg="#E3F2FD", fg="#1976D2")
                elif message.startswith("ERROR:"):
                    # Error message
                    self.label.config(text=message[6:], bg="#FFEBEE", fg="#C62828")
                elif message.startswith("SUCCESS:"):
                    # Success message
                    self.label.config(text=message[8:], bg="#E8F5E8", fg="#2E7D32")
                else:
                    # Regular message
                    self.add_message(message)
        except queue.Empty:
            pass
        
        # Schedule next check
        self.master.after(100, self.check_queue)  # Check every 100ms

    def background_assistant_task(self):
        """Background thread for voice assistant"""
        self.message_queue.put("🎤 Voice Assistant Started")
        p.speak("I am Jarvis, If you want to quit me, just say bye", self.k)
        
        while self.running:
            try:
                self.message_queue.put("STATUS:🎧 Listening...")
                query = self.take().lower()
                
                if not query:
                    continue
                    
                self.message_queue.put(f"🔍 Processing: '{query}'")
                
                # Wikipedia search
                if 'wikipedia' in query:
                    self.message_queue.put("📚 Searching Wikipedia...")
                    p.speak("Searching Wikipedia", self.k)
                    query = query.replace("wikipedia", "")
                    try:
                        results = wikipedia.summary(query, sentences=2)
                        p.speak("According to Wikipedia", self.k)
                        self.message_queue.put(f"📖 Wikipedia: {results}")
                        p.speak(results, self.k)
                    except Exception as e:
                        self.message_queue.put("ERROR:Wikipedia search failed")
                        p.speak("Sorry, could not find information", self.k)
                    
                # Web browsing
                elif 'open youtube' in query:
                    self.message_queue.put("🎥 Opening YouTube...")
                    webbrowser.open("youtube.com")
                elif 'open google' in query:
                    self.message_queue.put("🔍 Opening Google...")
                    webbrowser.open("google.com")
                    
                # App controls - Open
                elif 'open whatsapp' in query:
                    self.message_queue.put("💬 Opening WhatsApp...")
                    os.system("start whatsapp://")
                elif 'open planner' in query:
                    self.message_queue.put("📅 Opening Planner...")
                    os.system("start outlookcal://")
                elif 'open notepad' in query:
                    self.message_queue.put("📝 Opening Notepad...")
                    os.system("notepad.exe")
                elif 'open calculator' in query:
                    self.message_queue.put("🔢 Opening Calculator...")
                    os.system("calc.exe")
                elif 'open camera' in query:
                    self.message_queue.put("📷 Opening Camera...")
                    os.system("start microsoft.windows.camera:")
                elif 'open paint' in query:
                    self.message_queue.put("🎨 Opening Paint...")
                    os.system("mspaint")
                elif 'open browser' in query:
                    self.message_queue.put("🌐 Opening Browser...")
                    os.system("start chrome")
                elif 'open file explorer' in query:
                    self.message_queue.put("📁 Opening File Explorer...")
                    os.system("explorer")
                elif 'open settings' in query:
                    self.message_queue.put("⚙️ Opening Settings...")
                    os.system("start ms-settings:")
                elif 'open task manager' in query:
                    self.message_queue.put("💼 Opening Task Manager...")
                    os.system("taskmgr")
                elif 'open command prompt' in query:
                    self.message_queue.put("💻 Opening Command Prompt...")
                    os.system("cmd")
                elif 'open powershell' in query:
                    self.message_queue.put("🔷 Opening PowerShell...")
                    os.system("start powershell")
                elif 'open snipping tool' in query:
                    self.message_queue.put("✂️ Opening Snipping Tool...")
                    os.system("start snippingtool")
                    
                # App controls - Close
                elif 'close whatsapp' in query:
                    self.message_queue.put("❌ Closing WhatsApp...")
                    self._close_process("whatsapp", "WhatsApp")
                elif 'close planner' in query:
                    self.message_queue.put("❌ Closing Planner...")
                    self._close_process(["msedgewebview2", "olk"], "planner")
                elif 'close notepad' in query:
                    self.message_queue.put("❌ Closing Notepad...")
                    self._close_process("notepad", "Notepad")
                elif 'close calculator' in query:
                    self.message_queue.put("❌ Closing Calculator...")
                    self._close_process("calculator", "calculator")
                elif 'close camera' in query:
                    self.message_queue.put("❌ Closing Camera...")
                    self._close_process("camera", "camera")
                elif 'close paint' in query:
                    self.message_queue.put("❌ Closing Paint...")
                    self._close_process("mspaint", "Paint")
                elif 'close browser' in query:
                    self.message_queue.put("❌ Closing Browser...")
                    self._close_process("chrome", "browser")
                elif 'close file explorer' in query:
                    self.message_queue.put("❌ Closing File Explorer...")
                    self._close_process("explorer", "File Explorer")
                elif 'close settings' in query:
                    self.message_queue.put("❌ Closing Settings...")
                    self._close_process("ms-settings", "Settings")
                elif 'close task manager' in query:
                    self.message_queue.put("❌ Closing Task Manager...")
                    self._close_process("taskmgr", "Task Manager")
                elif 'close command prompt' in query:
                    self.message_queue.put("❌ Closing Command Prompt...")
                    self._close_process("cmd", "Command Prompt")
                elif 'close powershell' in query:
                    self.message_queue.put("❌ Closing PowerShell...")
                    self._close_process("powershell", "PowerShell")
                elif 'close snipping tool' in query:
                    self.message_queue.put("❌ Closing Snipping Tool...")
                    self._close_process("snippingtool", "Snipping Tool")
                    
                # Screenshot
                elif 'screenshot' in query:
                    self.message_queue.put("📸 Taking screenshot...")
                    screenshot = pyautogui.screenshot()
                    i=0
                    screenshot.save(f"screenshots/screenshot{i}.png")
                    i+=1
                    self.message_queue.put(f"SUCCESS:Screenshot saved as 'screenshot{i}.png'")
                    p.speak("Screenshot taken", self.k)
                    
                # Quit
                elif 'bye' in query or 'quit' in query:
                    self.message_queue.put("👋 Goodbye! Stopping assistant...")
                    p.speak("Goodbye!", self.k)
                    self.running = False
                    break
                    
                # Unknown command
                elif len(query) != 0:
                    self.message_queue.put(f"❓ Unknown command: '{query}'")
                    p.speak("Sorry I am not aware of this instruction", self.k)
                    
            except Exception as e:
                self.message_queue.put(f"ERROR:Assistant error: {str(e)}")
                
        # Assistant stopped
        self.message_queue.put("STATUS:🛑 Assistant stopped")
        self.message_queue.put("Session ended. Click 'Start Assistant' to begin again.")

    def toggle_assistant(self):
        """Start or stop the voice assistant"""
        if not self.running:
            # Start assistant
            self.running = True
            self.run_button.config(text="Stop Assistant", bg="#F44336")
            
            # Start background thread
            self.worker_thread = threading.Thread(target=self.background_assistant_task)
            self.worker_thread.daemon = True
            self.worker_thread.start()
        else:
            # Stop assistant
            self.running = False
            self.run_button.config(text="Start Assistant", bg="#FF6B35")

    def male_voice(self):
        """Set voice to male"""
        engine = p.init()
        voices = engine.getProperty('voices')
        self.k = 0
        engine.setProperty('voice', voices[0].id)
        p.speak("Changed to male voice", self.k)
        self.add_message("🔊 Voice changed to male")

    def female_voice(self):
        """Set voice to female"""
        engine = p.init()
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[1].id)
        self.k = 1
        p.speak("Changed to female voice", self.k)
        self.add_message("🔊 Voice changed to female")

    def display_text(self):
        """Test microphone and display recognized speech"""
        self.add_message("🎤 Testing microphone...")
        r = sr.Recognizer()
        
        with sr.Microphone() as source:
            print("Command:...")
            audio = r.listen(source)
            
        try:
            print("Recognized")
            query = r.recognize_google(audio, language='en-uk')
            print("User said:", query)
            self.label.config(text=f"✅ Mic test: {query}", bg="#E8F5E8", fg="#2E7D32")
            self.add_message(f"✅ Microphone working. You said: '{query}'")
            return query
        except Exception as e:
            print("Please say again")
            self.label.config(text="❌ Mic test failed", bg="#FFEBEE", fg="#C62828")
            self.add_message("❌ Microphone test failed. Please try again.")
            return ""

    @staticmethod
    def wish(k):
        """Greet user based on time of day"""
        hr = int(datetime.datetime.now().hour)
        
        if hr >= 0 and hr < 12:
            p.speak("Good morning", k)
        elif hr >= 12 and hr < 16:
            p.speak("Good afternoon", k)
        elif hr >= 16 and hr < 19:
            p.speak("Good evening", k)
        else:
            p.speak("Good night", k)

    def take(self):
        """Take voice input from user"""
        r = sr.Recognizer()
        
        with sr.Microphone() as source:
            print("Command:...")
            audio = r.listen(source)
            
        try:
            print("Recognized")
            query = r.recognize_google(audio, language='en-uk')
            print("User said:", query)
            return query
        except Exception as e:
            print("Please say again")
            return ""

    def _close_process(self, process_names, app_name):
        """Helper method to close processes"""
        if isinstance(process_names, str):
            process_names = [process_names]
            
        killed = False
        for proc in psutil.process_iter(['name']):
            for process_name in process_names:
                if process_name in proc.info['name'].lower():
                    proc.kill()
                    killed = True
                    break
                    
        if killed:
            self.message_queue.put(f"SUCCESS:{app_name} closed successfully")
        else:
            self.message_queue.put(f"ERROR:No matching {app_name} process found")
            p.speak(f"No matching {app_name} process found.", self.k)

    def on_quit(self):
        """Cleanup when closing the application"""
        self.running = False
        self.message_queue.put("Session ended. Available commands: wikipedia, open/close apps, take screenshot, etc.")