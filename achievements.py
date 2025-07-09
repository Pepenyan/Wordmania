import os
import json

ACHIEVEMENTS_FILE = "achievements.json"

DEFAULT_ACHIEVEMENTS = {
    "first_win": False,
    "five_in_a_row": False,
    "ten_in_a_row": False,
    "fast_answer": False,
    "no_mistakes": False,
    "played_10_rounds": False
}

def load_achievements():
    if not os.path.exists(ACHIEVEMENTS_FILE):
        save_achievements(DEFAULT_ACHIEVEMENTS)
        return DEFAULT_ACHIEVEMENTS.copy()
    with open(ACHIEVEMENTS_FILE, "r", encoding="utf-8") as file:
        return json.load(file)

def save_achievements(achievements):
    with open(ACHIEVEMENTS_FILE, "w", encoding="utf-8") as file:
        json.dump(achievements, file, indent=2, ensure_ascii=False)

def check_and_unlock(achievements, score, streak, time_taken, total_rounds, mistakes):
    unlocked = []

    if score >= 1 and not achievements["first_win"]:
        achievements["first_win"] = True
        unlocked.append("Первый успех — угадал первое слово!")

    if streak >= 5 and not achievements["five_in_a_row"]:
        achievements["five_in_a_row"] = True
        unlocked.append("Начинающий мастер — 5 слов подряд!")

    if streak >= 10 and not achievements["ten_in_a_row"]:
        achievements["ten_in_a_row"] = True
        unlocked.append("Эксперт — 10 подряд!")

    if time_taken < 5 and not achievements["fast_answer"]:
        achievements["fast_answer"] = True
        unlocked.append("Молниеносный — угадал за 5 секунд!")

    if total_rounds >= 10 and not achievements["played_10_rounds"]:
        achievements["played_10_rounds"] = True
        unlocked.append("Упорный — сыграл 10 раундов!")

    if mistakes == 0 and total_rounds >= 10 and not achievements["no_mistakes"]:
        achievements["no_mistakes"] = True
        unlocked.append("Идеальный — ни одной ошибки за 10 раундов!")

    if unlocked:
        print("\n=== Новые достижения! ===")
        for msg in unlocked:
            print("✔", msg)
        print("=========================\n")

    return achievements