# LivePython

Easily start building small networked games in Python using asyncio and pygame.

---

## ✦ Overview ✦

LivePython provides a ready-to-use foundation for creating multiplayer or networked applications. It combines rendering, networking, logging, and environment setup into a minimal starting point so you can focus on building your game or app logic.

---

## ✦ Features ✦

- Preconfigured `client.py` and `server.py`
  - Initializes pygame window
  - Sets up asyncio-based networking
- Modular `system/` folder
  - Networking
  - Process management
  - Custom launcher
- Automatic logging
  - Stored in the `log/` folder
- One-click startup
  - `client.bat` and `server.bat`
- Structured configuration
  - Located in `config/`
- Asset management
  - Located in `assets/`

---

## ✦ Project Structure ✦

```text
LivePython/
│
├── client.py
├── server.py
├── client.bat
├── server.bat
│
├── system/
│ ├── networking.py
│ ├── processes.py
│ └── launcher.bat
│
├── config/
│ ├── app_config.json
│ ├── client_config.json
│ └── server_config.json
│
├── assets/
├── log/
└── requirements.txt
```


---

## ✦ How It Works ✦

### ⟪ Setup Flow Begins ⟫

1. The launcher script:
   - Locates the most suitable Python executable
   - Creates a virtual environment if one does not exist
   - Installs dependencies from:
     - `systems/requirements.txt`
     - root `requirements.txt`

2. Dependencies include:
   - `asyncio`
   - `pygame-ce`
   - `msgpack`

3. All setup actions are logged automatically.

### ⟪ Setup Flow Ends ⟫

---

### ⟪ Runtime Flow Begins ⟫

1. `client.bat` or `server.bat` is executed  
2. Launcher runs the target script using `pythonw.exe` (no console window)  
3. The application:
   - Initializes logging
   - Starts networking
   - Opens a pygame window

4. Logs are written to:
   - `log/client_log.txt`
   - `log/server_log.txt`

### ⟪ Runtime Flow Ends ⟫

---

## ✦ Systems ✦

### ⟪ Processes System Begins ⟫

- Handles application IDs  
- Captures and logs Python exceptions  
- Integrates with logging system  

### ⟪ Processes System Ends ⟫

---

### ⟪ Networking System Begins ⟫

- Asyncio-based communication  
- Uses msgpack for serialization  
- Integrated into both client and server  

### ⟪ Networking System Ends ⟫

---

## ✦ Configuration ✦

Located in the `config/` folder:

- `app_config.json` → General application settings  
- `server_config.json` → Server-specific configuration  
- `client_config.json` → Client connection settings  

The host may be either the host name or ip-address.

> ⚠️ Remember: The client configuration must be updated before connecting to another machine on your network.

---

## ✦ Logging ✦

- All logs are stored in the `log/` directory  
- Separate logs for client and server  
- Includes setup, runtime events, and errors  
- Additional notes are provided inside the folder  

---

## ✦ Purpose ✦

This repository is intended as a **starter framework** for building more complex networked games and applications.

It removes the repetitive setup involved in:
- Environment configuration  
- Networking boilerplate  
- Logging infrastructure  

---

## ✦ License ✦

MIT License

This project serves as a reusable base under the name **LivePython**.