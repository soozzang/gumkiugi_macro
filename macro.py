import pyautogui
import pyperclip
import time
import re

# 1. 채팅(강화 결과) 좌표 (강화 성공 기준으로 잡히는 좌표여야함)
OUTPUT_X = 1010
OUTPUT_Y = 660

# 2. 채팅입력창 좌표
INPUT_X = 1200
INPUT_Y = 1050

# 3. 목표 레벨
TARGET_LEVEL = 18

def get_last_message():
    pyautogui.click(x=OUTPUT_X, y=OUTPUT_Y)

    pyautogui.hotkey('command', 'a')
    time.sleep(0.05)
    pyautogui.hotkey('command', 'c')
    time.sleep(0.05)

    full_text = pyperclip.paste()
    if full_text:
        first_line = full_text.split('\n')[0]
        return first_line.strip()
    else:
        return ""


def parse_game_state(message):
    if "강화 파괴" in message:
        return "fail", 0

    success_match = re.search(r'\+(\d+)\s*→\s*\+(\d+)', message)
    if success_match:
        new_level = int(success_match.group(2))
        return "success", new_level

    if "강화 유지" in message:
        maintain_match = re.search(r'\[\+(\d+)\]', message)
        if maintain_match:
            current_level = int(maintain_match.group(1))
            return "maintain", current_level

    return "unknown", None


def perform_enhance():
    pyautogui.click(x=INPUT_X, y=INPUT_Y)
    time.sleep(0.1)

    pyperclip.copy('/강화')
    pyautogui.hotkey('command', 'v')
    time.sleep(0.1)

    pyautogui.press('enter')

    time.sleep(0.2)

    pyautogui.press('enter')


def main():
    time.sleep(3)

    while True:
        perform_enhance()

        time.sleep(5)

        log = get_last_message()
        status, level = parse_game_state(log)

        if status == 'fail':
            current_level = 0
        else:
            current_level = level

        if current_level is not None and current_level >= TARGET_LEVEL:
            break

if __name__ == "__main__":
    pyautogui.FAILSAFE = True
    main()