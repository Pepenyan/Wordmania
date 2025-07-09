import time
import random
import os
from achievements import load_achievements, save_achievements, check_and_unlock

WORDS_FILE = "words.txt"

def load_words():
    if not os.path.exists(WORDS_FILE):
        return []
    with open(WORDS_FILE, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if "|" in line]
    return [tuple(map(str.strip, line.split("|", 1))) for line in lines[1:]]

def get_best_score():
    try:
        with open(WORDS_FILE, "r", encoding="utf-8") as f:
            return int(f.readline().strip())
    except:
        return 0

def update_best_score(score):
    with open(WORDS_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()
    lines[0] = str(score) + "\n"
    with open(WORDS_FILE, "w", encoding="utf-8") as f:
        f.writelines(lines)

def save_words(best_score, words):
    with open(WORDS_FILE, "w", encoding="utf-8") as f:
        f.write(f"{best_score}\n")
        for word, desc in words:
            f.write(f"{word} | {desc}\n")

def show_title(best_score):
    os.system('cls' if os.name == 'nt' else 'clear')
    print(r"""
 \ \        / / __ \|  __ \|  __ \|  \/  |   /\   | \ | |_   _|   /\    
  \ \  /\  / | |  | | |__) | |  | | \  / |  /  \  |  \| | | |    /  \   
   \ \/  \/ /| |  | |  _  /| |  | | |\/| | / /\ \ | . ` | | |   / /\ \  
    \  /\  / | |__| | | \ \| |__| | |  | |/ ____ \| |\  |_| |_ / ____ \ 
     \/  \/   \____/|_|  \_|_____/|_|  |_/_/    \_|_| \_|_____/_/    \_\
""")
    print(f"\nЛучший счёт: {best_score}")

def play(words, best_score):
    score = 0
    streak = 0
    mistakes = 0
    total_rounds = 0
    achievements = load_achievements()

    random.shuffle(words)

    for word, wrong_def in words:
        total_rounds += 1
        print(f"\nПодсказка: {wrong_def}")
        start_time = time.time()
        guess = input("Ваш ответ: ").strip().lower()
        time_taken = time.time() - start_time

        if guess == word.lower():
            print("Верно!")
            score += 1
            streak += 1
        else:
            print(f"Неверно! Правильный ответ: {word}")
            streak = 0
            mistakes += 1

        if score > best_score:
            best_score = score
            update_best_score(best_score)

        achievements = check_and_unlock(
            achievements, score, streak, time_taken, total_rounds, mistakes
        )
        save_achievements(achievements)

    print(f"\nИгра окончена. Ваш счёт: {score}")

def word_editor():
    best_score = get_best_score()
    words = load_words()
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("== Редактор слов (всего слов:", len(words), ") ==")
        for i, (w, d) in enumerate(words):
            print(f"{i+1}. {w} | {d}")
        print("\nВыберите действие:")
        print("1 - Добавить новое слово")
        print("2 - Удалить слово")
        print("3 - Вернуться в меню")
        choice = input(">>> ")

        if choice == "1":
            w = input("Слово: ").strip()
            d = input("Ложное описание: ").strip()
            if w and d:
                words.append((w, d))
        elif choice == "2":
            idx = input("Номер слова для удаления: ").strip()
            if idx.isdigit() and 1 <= int(idx) <= len(words):
                words.pop(int(idx)-1)
        elif choice == "3":
            break

    save_words(best_score, words)
    print("Список обновлён. Возврат в меню...")
    time.sleep(1)

def main_menu():
    best_score = get_best_score()
    while True:
        show_title(best_score)
        print("\nМеню:")
        print("1 - Играть")
        print("2 - Посмотреть достижения")
        print("3 - Редактировать список слов")
        print("4 - Выход")
        choice = input("\nВыберите: ").strip()

        if choice == "1":
            words = load_words()
            if not words:
                print("[!] Нет слов для игры. Добавьте их в редакторе.")
                input("Нажмите Enter...")
            else:
                play(words, best_score)
        elif choice == "2":
            ach = load_achievements()
            print("\n== Достижения ==")
            for key, unlocked in ach.items():
                print(f"- {key.replace('_', ' ').capitalize()}: {'Да' if unlocked else 'Нет'}")
            input("\nНажмите Enter для возврата в меню...")
        elif choice == "3":
            word_editor()
            best_score = get_best_score()
        elif choice == "4":
            print("Выход...")
            break
        else:
            print("Неверный выбор.")
            time.sleep(1)

if __name__ == "__main__":
    main_menu()
