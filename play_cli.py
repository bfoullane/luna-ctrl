from engine import *


def main():
    level = input("Level (junior/commander/expert): ") or "commander"
    s = new_game(level=level, seed=None)
    while not s["over"]:
        print(f"\nDAY {s['day']}  P{s['power']} O{s['oxygen']} S{s['shield']} F{s['food']} Sci{s['science']}")
        print("Actions:", available(s))
        acts = input("Pick 2 actions (space-separated): ").split()
        choices = []
        for ev in start_day(s):
            e = EVENTS[ev]
            print(f"\n{e['title']} - {e['text']}")
            print("Choices:", list(e["options"]))
            choices.append(input("Choice: "))
        for line in play_day(s, acts, choices):
            print("  *", line)
    print("WON" if s["won"] else "LOST", "science:", s["science"])


if __name__ == "__main__":
    main()