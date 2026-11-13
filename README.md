# Windows Chat Messenger

A beginner-friendly WhatsApp-inspired **local desktop demo** made with Python and Tkinter.

## Requirements
- Windows 10 or Windows 11
- Python 3.10 or newer
- VS Code (recommended, optional)

Tkinter is normally included with the standard Windows Python installer. No internet connection or third-party package is needed to run this project.

## Run the project

1. Download the ZIP file and extract it. Do not run the project from inside the ZIP.
2. Open the extracted `windows-chat-messenger` folder.
3. Open a terminal in this folder (in VS Code: Terminal -> New Terminal).
4. Check Python:

   ```powershell
   py --version
   ```

5. Start the application:

   ```powershell
   py app.py
   ```

6. The Windows messenger window will open. Select a contact, type a message, and press **Send** (or Enter).

If the `py` command is unavailable but `python` works, use:

```powershell
python app.py
```

## Features
- Sample contact list
- Search contacts
- Select a conversation
- Send and display text messages with timestamps
- Save chat history in `chats.json`
- Delete a conversation after confirmation
- Reject empty messages

## Files
- `app.py` - main Tkinter desktop application
- `chats.json` - local contacts and chat history
- `requirements.txt` - dependency note

## Stop / close
Close the application window normally. Chat history is saved to `chats.json` when a message is sent.

## Important limitation
This is an educational local prototype. It does not connect to WhatsApp, other computers, or the internet. Messages are stored only on this computer. Do not use it for private or sensitive messages.

## Troubleshooting
- **Python is not recognised:** install Python from python.org and enable the option to add Python to PATH, or try `py app.py`.
- **No module named tkinter:** rerun the official Python installer and ensure Tcl/Tk support is installed.
- **Window does not open:** run `py app.py` in the terminal and read the error message shown there.
- **Chat history is missing:** keep `chats.json` in the same folder as `app.py` and make sure the folder is writable.
