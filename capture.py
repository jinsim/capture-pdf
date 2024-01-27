import time
import os
import shutil
from datetime import datetime
import pyautogui
from pynput import mouse
from PIL import ImageGrab, Image


def left_top_click(x, y, button, pressed):
    if pressed and button==mouse.Button.left:
        global left_top_x
        global left_top_y
        left_top_x = int(x)
        left_top_y = int(y)
        print(f"우측 상단 좌표 ({left_top_x}, {left_top_y})")
        return False # 조건에 맞으면 listening 멈춘다.
    return True # listening 시작

def right_bottom_click(x, y, button, pressed):
    if pressed and button==mouse.Button.left:
        global right_bottom_x
        global right_bottom_y
        right_bottom_x = int(x)
        right_bottom_y = int(y)
        print(f"좌측 하단 좌표 ({right_bottom_x}, {right_bottom_y})")
        return False # 조건에 맞으면 listening 멈춘다.
    return True # listening 시작

def listen_mouse(func):
    with mouse.Listener(on_click=func) as listener:
        listener.join()

def capture(page):
    time.sleep(3)
    for _ in range(page):
        time.sleep(0.3)
        now_time = datetime.now().strftime("%Y-%m-%d-%H-%M-%S.%f")
        img = ImageGrab.grab(bbox=(left_top_x, left_top_y, right_bottom_x, right_bottom_y))
        img.save(f"img/{now_time}.png")
        pyautogui.press('right')

def sort_images_by_filename(folder_path):
    # 이미지 파일 리스트
    image_paths = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.lower().endswith(('.png', '.jpg', '.jpeg'))]
    image_paths.sort()
    return image_paths

def images_to_pdf(image_paths, pdf_path):
    # 이미지를 RGB 로 변환 후 PDF 로 변환
    images = [Image.open(path).convert('RGB') for path in image_paths]
    images[0].save(pdf_path, save_all=True, append_images=images[1:])

def remove_imgs():
    try:
        # img 폴더와 그 내부 파일 전체 삭제
        shutil.rmtree('./img')
        print("Removed 'img' directory and its contents.")
    except OSError as e:
        print(f"Error: {e}")

    os.makedirs('./img', exist_ok=True)

    with open('./img/.gitkeep', 'w') as f:
        pass

if __name__ == "__main__":

    page = int(input("페이지 수를 입력해주세요. : "))
    ipt = input("좌표를 아시면 y를 눌러주세요. : ")

    if ipt == "y":
        left_top_x, left_top_y, right_bottom_x, right_bottom_y = map(int, input("우측 상단 x 좌표, 우측 상단 y 좌표, 좌측 하단 x 좌표, 좌측 하단 y 좌표를 순서대로 띄어쓰기로 구분하여 입력해주세요. : ").split())
    else:
        print("왼쪽 위 좌표를 클릭해주세요.")
        listen_mouse(left_top_click)
        
        print("오른쪽 아래 좌표를 클릭해주세요.")
        listen_mouse(right_bottom_click)

    capture(page)


    image_folder = 'img'
    pdf_file_path = 'pdf/output.pdf'

    sorted_images = sort_images_by_filename(image_folder)
    images_to_pdf(sorted_images, pdf_file_path)
    remove_imgs()
