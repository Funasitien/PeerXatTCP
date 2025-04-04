import socket
import threading
from config import IP, PORT, PSEUDO, COULEUR, THEME
from data import ASCII_ART
from color import color, theme
import curses
import sys
import signal

class ChatClient:
    def __init__(self):
        self.host = IP
        self.port = PORT
        self.pseudo = PSEUDO
        self.color_code = getattr(color, COULEUR, color.reset)
        self.theme = getattr(theme, THEME, theme.classic)
        self.messages = []
        self.input_buffer = ""
        self.running = True
        self.new_message_event = threading.Event()
        signal.signal(signal.SIGINT, self.handle_exit)

    def receive_messages(self, sock):
        """Run in a background thread; only update the message list and signal a refresh."""
        while self.running:
            try:
                data = sock.recv(1024)
                if not data:
                    break
                # Append new message and signal a refresh
                self.messages.append(data.decode('utf-8'))
                self.new_message_event.set()
            except Exception as e:
                self.messages.append(f"[Erreur de réception] {e}")
                self.new_message_event.set()
                break

    
    def handle_exit(self, sig=None, frame=None):
        self.running = False
        curses.endwin()
        print(color.red + "\nFermeture du client." + color.k)
        sys.exit(0)

    def draw(self, stdscr):
        """Redraw the entire UI using curses without causing a flash of black."""
        # Instead of clear(), use erase() so that our background setting persists.
        stdscr.erase()
        height, width = stdscr.getmaxyx()
        start_y = 0
        
        for i, line in enumerate(ASCII_ART):
            stdscr.addstr(i, (width - len(line)) // 2, line)

        # Chat messages area
        chat_start = start_y + len(ASCII_ART) + 1
        max_chat_lines = height - chat_start - 2
        recent_messages = self.messages[-max_chat_lines:]
        for idx, msg in enumerate(recent_messages):
            try:
                # Default attribute if no ANSI code found.
                color_attr = self.theme[0]
                # Check for an ANSI color code at the beginning of the message.
                for ansi_code, curses_attr in self.color_pairs.items():
                    if msg.startswith(ansi_code):
                        color_attr = curses_attr
                        # Remove the ANSI code and the reset code from the username.
                        msg = msg.replace(ansi_code, "", 1)
                        msg = msg.replace(color.reset, "", 1)
                        break
                username, sep, text = msg.partition(":")
                stdscr.addstr(chat_start + idx, 1, username + ":", color_attr)
                stdscr.addstr(text, self.theme[0])
            except curses.error:
                try:
                    stdscr.addstr(chat_start + idx, 1, msg[:width - 2], self.theme_default)
                except curses.error:
                    pass

        # Input prompt at the bottom
        prompt = "Vous: "
        stdscr.addstr(height - 1, 0, prompt + self.input_buffer[:width - len(prompt) - 1])

        stdscr.refresh()

    def run(self, stdscr):
        # Initialize curses color support and set a theme background if desired.
        curses.start_color()
        # Example: set color pair 1 to white text on blue background.
        curses.init_pair(1, self.theme[0], self.theme[1])
        stdscr.bkgd(' ', curses.color_pair(1))
        stdscr.erase()
        stdscr.refresh()

        # Setup socket connection
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client.connect((self.host, self.port))
        except Exception as e:
            stdscr.addstr(0, 0, f"Connexion échouée: {e}")
            stdscr.refresh()
            stdscr.getch()
            return

        # Send username with color formatting
        uname = self.color_code + self.pseudo + color.reset
        client.send(uname.encode('utf-8'))

        # Start the background thread for receiving messages.
        thread = threading.Thread(target=self.receive_messages, args=(client,), daemon=True)
        thread.start()

        self.color_pairs = {}
        ansi_to_color = {
            "\033[94m": curses.COLOR_BLUE,
            "\033[96m": curses.COLOR_CYAN,
            "\033[92m": curses.COLOR_GREEN,
            "\033[93m": curses.COLOR_YELLOW,
            "\033[91m": curses.COLOR_RED,
        }
        pair_number = 2
        for ansi_code, curses_color in ansi_to_color.items():
            curses.init_pair(pair_number, curses_color, curses.COLOR_BLUE)
            self.color_pairs[ansi_code] = curses.color_pair(pair_number)
            pair_number += 1
        
        curses.curs_set(1)
        stdscr.nodelay(True)
        stdscr.timeout(100)  # Wait 100ms for input
        self.draw(stdscr)

        while self.running:
            # Only redraw if a new message was received or on key input
            if self.new_message_event.is_set():
                self.draw(stdscr)
                self.new_message_event.clear()

            try:
                key = stdscr.getch()
            except:
                key = -1

            if key == -1:
                continue
            elif key in (curses.KEY_ENTER, 10, 13):
                if self.input_buffer.strip():
                    text = self.input_buffer.strip()
                    if text.lower() == "exit":
                        self.handle_exit()
                    try:
                        msg = f"{self.pseudo}: {text}"
                        client.send(msg.encode('utf-8'))
                    except Exception as e:
                        self.messages.append(f"[Erreur d'envoi] {e}")
                        self.new_message_event.set()
                    self.input_buffer = ""
                    self.draw(stdscr)
            elif key in (curses.KEY_BACKSPACE, 127, 8):
                self.input_buffer = self.input_buffer[:-1]
                self.draw(stdscr)
            elif 32 <= key <= 126:
                self.input_buffer += chr(key)
                self.draw(stdscr)

        client.close()

    def start(self):
        curses.wrapper(self.run)

if __name__ == "__main__":
    ChatClient().start()