import os
import random
import sys

WORDS_FILE = "words.txt"

def get_local_path(filename):
    """Возвращает путь к файлу рядом с .py или .exe"""
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS if hasattr(sys, '_MEIPASS') else os.path.dirname(sys.executable)
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, filename)

def load_words_and_score(filename):
    path = get_local_path(filename)
    if not os.path.exists(path):
        print(f"Файл {filename} не найден.")
        sys.exit(1)

    with open(path, encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    try:
        best_score = int(lines[0])
    except ValueError:
        best_score = 0

    word_lines = lines[1:]
    words = []
    for line in word_lines:
        if '|' in line:
            word, hint = map(str.strip, line.split('|', 1))
            words.append((word.lower(), hint))

    return best_score, words

def save_best_score(filename, score):
    path = get_local_path(filename)
    with open(path, encoding="utf-8") as f:
        lines = f.readlines()

    lines = [str(score) + "\n"] + lines[1:]  # обновляем первую строку
    with open(path, "w", encoding="utf-8") as f:
        f.writelines(lines)

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_title(best_score):
    clear()
    print(r"""
 \ \        / / __ \|  __ \|  __ \|  \/  |   /\   | \ | |_   _|   /\    
  \ \  /\  / | |  | | |__) | |  | | \  / |  /  \  |  \| | | |    /  \   
   \ \/  \/ /| |  | |  _  /| |  | | |\/| | / /\ \ | . ` | | |   / /\ \  
    \  /\  / | |__| | | \ \| |__| | |  | |/ ____ \| |\  |_| |_ / ____ \ 
     \/  \/   \____/|_|  \_|_____/|_|  |_/_/    \_|_| \_|_____/_/    \_\
""")
    print(f"Лучший счёт: {best_score}")
    print("\nНажмите Enter, чтобы начать игру...")
    input()

def play_game(word_list, best_score):
    score = 0
    try:
        while True:
            clear()
            print("ВОРДМАНИЯ — УГАДАЙ СЛОВО")
            print(f"Счёт: {score}   |   Лучший: {best_score}")
            word, hint = random.choice(word_list)
            print("\nПодсказка:", hint)
            guess = input("\nТвой ответ: ").strip().lower()

            if guess == word:
                print("\nПравильно!")
                score += 1
                if score > best_score:
                    best_score = score
                    save_best_score(WORDS_FILE, best_score)
            else:
                print(f"\nНеправильно. Правильный ответ: {word}")
                score = 0

            input("\nНажмите Enter, чтобы продолжить...")
    except KeyboardInterrupt:
        print("\nВыход из игры. Спасибо за игру!")

if __name__ == "__main__":
    best_score, words = load_words_and_score(WORDS_FILE)
    if not words:
        print("Файл words.txt пуст или некорректен.")
        sys.exit(1)

    print_title(best_score)
    play_game(words, best_score)
