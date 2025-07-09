import os
import random
import threading

WORDS_FILE = "words.txt"
FACTS_FILE = "fun_facts.txt"

TIME_LIMIT = 15  # секунд на ответ

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def input_with_timeout(prompt, timeout):
    answer = [None]

    def ask():
        answer[0] = input(prompt)

    thread = threading.Thread(target=ask)
    thread.daemon = True
    thread.start()

    thread.join(timeout)
    if thread.is_alive():
        print("\nВремя вышло!")
        return None
    return answer[0]

def load_words():
    if not os.path.exists(WORDS_FILE):
        with open(WORDS_FILE, "w", encoding="utf-8") as f:
            f.write("0\n")
    with open(WORDS_FILE, encoding="utf-8") as f:
        lines = f.read().strip().split("\n")
    try:
        best_score = int(lines[0])
    except:
        best_score = 0
    word_pairs = []
    for line in lines[1:]:
        if "|" in line:
            word, hint = map(str.strip, line.split("|", 1))
            word_pairs.append((word.lower(), hint))
    return best_score, word_pairs

def save_best_score(score, word_pairs):
    with open(WORDS_FILE, "w", encoding="utf-8") as f:
        f.write(str(score) + "\n")
        for w, h in word_pairs:
            f.write(f"{w} | {h}\n")

def load_facts():
    if not os.path.exists(FACTS_FILE):
        return []
    with open(FACTS_FILE, encoding="utf-8") as f:
        facts = [line.strip() for line in f if line.strip()]
    return facts

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

def print_menu():
    clear()
    print("Меню:")
    print("1. Начать игру")
    print("2. Добавить слово")
    print("3. Выйти")
    choice = input("Выберите пункт (1-3): ")
    return choice.strip()

def add_word(word_pairs):
    clear()
    print("Добавление нового слова в словарь")
    word = input("Введите новое слово (без пробелов): ").strip().lower()
    if not word or " " in word or "|" in word:
        print("Неверный формат слова.")
        input("Нажмите Enter для возврата в меню...")
        return word_pairs
    hint = input("Введите подсказку для этого слова: ").strip()
    if not hint:
        print("Подсказка не может быть пустой.")
        input("Нажмите Enter для возврата в меню...")
        return word_pairs
    word_pairs.append((word, hint))
    save_best_score(best_score, word_pairs)
    print(f"Слово '{word}' с подсказкой добавлено!")
    input("Нажмите Enter для возврата в меню...")
    return word_pairs

def play_game(best_score, word_pairs, facts):
    score = 0
    used_indices = set()
    while True:
        if len(used_indices) == len(word_pairs):
            print("Поздравляем! Вы угадали все слова.")
            break
        # Выбираем случайное слово, которое ещё не было
        idx = random.choice([i for i in range(len(word_pairs)) if i not in used_indices])
        used_indices.add(idx)
        word, hint = word_pairs[idx]
        print(f"\nПодсказка: {hint}")
        answer = input_with_timeout(f"Угадай слово (таймер {TIME_LIMIT} секунд): ", TIME_LIMIT)
        if answer is None:
            print(f"Неверно! Правильный ответ: {word}")
            score = 0
            input("Нажмите Enter для продолжения...")
            continue
        if answer.strip().lower() == word:
            score += 1
            print("Верно! +1 очко.")
            # Показать случайный забавный факт
            if facts:
                fact = random.choice(facts)
                print(f"Забавный факт: {fact}")
            else:
                print("Нет забавных фактов.")
            input("Нажмите Enter для следующего слова...")
        else:
            print(f"Неверно! Правильный ответ: {word}")
            score = 0
            input("Нажмите Enter для продолжения...")
        if score > best_score:
            best_score = score
            print(f"Новый лучший счёт: {best_score}!")
            save_best_score(best_score, word_pairs)
    print(f"Игра окончена. Ваш счёт: {score}")
    input("Нажмите Enter для возврата в меню...")
    return best_score

if __name__ == "__main__":
    best_score, word_pairs = load_words()
    facts = load_facts()
    while True:
        print_title(best_score)
        choice = print_menu()
        if choice == "1":
            best_score = play_game(best_score, word_pairs, facts)
        elif choice == "2":
            word_pairs = add_word(word_pairs)
        elif choice == "3":
            print("Спасибо за игру!")
            break
        else:
            print("Некорректный ввод. Попробуйте снова.")
            input("Нажмите Enter...")