import random
import keyboard
import time
import os
import sys

DICT_FILE = "dictionary.txt"

def load_dictionary(filename=DICT_FILE):
    if not os.path.exists(filename):
        print(f"Dictionary file '{filename}' not found. No replacements will be made.")
        return {}

    word_map = {}
    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            
            word, replacements = line.split("=", 1)
            word = word.strip().lower()
            replacements = [r.strip() for r in replacements.split(",") if r.strip()]
            
            if word and replacements:
                word_map[word] = replacements
    return word_map


class Obfuscator:
    def __init__(self):
        self.word_map = load_dictionary()
        self.word_end_keys = {"space", "enter", "tab"}
        self.delay = 0.02
        self.replace_chance = 0.8
        self.active = True
        self.current_word = []
        self.setup_controls()
        self.show_welcome()

    def setup_controls(self):
        try:
            keyboard.unhook_all_hotkeys()
        except:
            pass
            
        time.sleep(0.05)
        keyboard.add_hotkey("f12", self.toggle)
        keyboard.add_hotkey("ctrl+up", self.increase_chance)
        keyboard.add_hotkey("ctrl+down", self.decrease_chance)

    def show_welcome(self):
        print("\n=== Moros Obfuscator ===")
        print("F12 - Toggle on/off")
        print("Ctrl+Up/Down - Change replacement chance")
        print("\nListening for input... (Ctrl+C to exit)")
        self.update_status()

    def update_status(self):
        sys.stdout.write("\r" + " " * 80 + "\r")
        status = "on" if self.active else "off"
        chance = int(self.replace_chance * 100)
        sys.stdout.write(f"Status: {status} | Replacement chance: {chance}%")
        sys.stdout.flush()

    def toggle(self):
        self.active = not self.active
        self.update_status()

    def increase_chance(self):
        self.replace_chance = min(1.0, round(self.replace_chance + 0.1, 2))
        self.update_status()

    def decrease_chance(self):
        self.replace_chance = max(0.0, round(self.replace_chance - 0.1, 2))
        self.update_status()

    def run(self):
        keyboard.hook(self.handle_key)
        try:
            keyboard.wait()
        except KeyboardInterrupt:
            print("\n[EXIT] Moros Obfuscator stopped.")

    def handle_key(self, event):
        if not self.active or event.event_type != "down":
            return

        key = event.name

        if key in self.word_end_keys:
            word = "".join(self.current_word)
            word_lower = word.lower()
            
            if (word and word_lower in self.word_map 
                and random.random() < self.replace_chance):
                
                keyboard.send("backspace")
                time.sleep(self.delay)

                for _ in range(len(self.current_word)):
                    keyboard.send("backspace")
                    time.sleep(self.delay)

                new_word = random.choice(self.word_map[word_lower])
                keyboard.write(new_word, delay=self.delay)

                if key == "space":
                    keyboard.write(" ", delay=self.delay)
                elif key == "enter":
                    keyboard.send("enter")
                elif key == "tab":
                    keyboard.send("tab")

            self.current_word.clear()
            return

        if key == "backspace":
            if self.current_word:
                self.current_word.pop()
            return

        if len(key) == 1 and key.isprintable():
            self.current_word.append(key)


if __name__ == "__main__":
    Obfuscator().run()
