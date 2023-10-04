
from tkinter import Tk, Canvas, Button, Label, Entry, Text, filedialog
from PIL import Image, ImageTk, ImageDraw
import random
import csv

def create_gradient_image(width, height, color1, color2):
    base = Image.new('RGB', (width, height), color1)
    top = Image.new('RGB', (width, height), color2)
    mask = Image.new('L', (width, height))
    mask_data = []
    for y in range(height):
        mask_data.extend([int(255 * (y / height))] * width)
    mask.putdata(mask_data)
    base.paste(top, (0, 0), mask)
    return ImageTk.PhotoImage(base)

def convert_seconds_to_time(total_seconds):
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    return hours, minutes, seconds

def run_simulation(n, k, total_cook_count):
    total_time = 0
    remaining_cook_count = total_cook_count
    while remaining_cook_count > 0:
        if random.randint(1, 100) <= k:
            remaining_cook_count -= 10
            total_time += n
        else:
            remaining_cook_count -= 1
            total_time += n
    return total_time

def calculate_time():
    try:
        n = float(entry_n.get())
        k = float(entry_k.get())
        total_cook_count = int(entry_count.get())
    except ValueError:
        text_result.config(state='normal')
        text_result.delete(1.0, 'end')
        text_result.insert('end', "잘못된 입력입니다. 숫자를 입력해주세요.")
        text_result.config(state='disabled')
        return

    simulation_count = 100
    total_simulation_time = 0
    for _ in range(simulation_count):
        total_simulation_time += run_simulation(n, k, total_cook_count)

    average_time = total_simulation_time / simulation_count
    hours, minutes, seconds = convert_seconds_to_time(int(average_time))
    result_text = f"예상되는 평균 요리 시간은 {hours}시간 {minutes}분 {seconds}초입니다."
    
    text_result.config(state='normal')
    text_result.delete(1.0, 'end')
    text_result.insert('end', result_text)
    text_result.config(state='disabled')

def save_result():
    file_path = filedialog.asksaveasfilename(defaultextension=".text")
    if not file_path:
        return
    result_text = text_result.get(1.0, 'end').strip()
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(result_text)

root = Tk()
root.title("요리 시간 계산기")
root.geometry("400x400")

# 배경색을 어두운 황금색과 투명도가 높은 검은색의 그라데이션으로 설정
background_img = create_gradient_image(400, 400, '#96774c','#a58451')
background_label = Label(root, image=background_img)
background_label.place(relwidth=1, relheight=1)


label_n = Label(root, text="1회 요리에 걸리는 시간(초):", bg='#FFD700', fg='black')
label_n.pack(pady=5)
entry_n = Entry(root)
entry_n.pack(pady=5)

label_k = Label(root, text="10회 요리를 할 확률(%):", bg='#FFD700', fg='black')
label_k.pack(pady=5)
entry_k = Entry(root)
entry_k.pack(pady=5)

label_count = Label(root, text="총 요리 횟수:", bg='#FFD700', fg='black')
label_count.pack(pady=5)
entry_count = Entry(root)
entry_count.pack(pady=5)

button_img = create_gradient_image(100, 30, '#333333', '#666666')
button_calculate = Button(root, text="시간 계산", command=calculate_time, image=button_img, compound='center', bg='#333333', fg='white')
button_calculate.pack(pady=5)

button_save = Button(root, text="결과 저장", command=save_result, image=button_img, compound='center', bg='#333333', fg='white')
button_save.pack(pady=5)

text_result = Text(root, height=5, width=50, state='disabled', bg='white')
text_result.pack(pady=5)

root.mainloop()
