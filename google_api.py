import os
from dotenv import load_dotenv
import google.generativeai as genai
from pathlib import Path
import tkinter as tk

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# .envファイルの読み込み
load_dotenv()

# API-KEYの設定
GOOGLE_API_KEY=os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel('gemini-1.5-flash')

picture = [{
    'mime_type': 'image/jpg',
    'data': Path('photo.jpg').read_bytes()
}]
prompt = "ここは研究室です。この部屋でだらしない場所があれば教えて下さい。また、人が何人いるか端的に教えて下さい。ただし、お姉さん口調の日本語で回答して下さい。"

response = model.generate_content(
    contents=[prompt, picture[0]]
)
# print(response.text)

# tkinterを使って大きく表示する部分
def display_text():
    root = tk.Tk()
    root.title("Response")

    # ウィンドウのサイズ
    window_width = 1900
    window_height = 1000
    
    # 画面サイズの取得
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # 位置を計算して中央に配置
    position_x = (screen_width - window_width) // 2
    position_y = (screen_height - window_height) // 2

    # ウィンドウサイズと位置の設定
    root.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

    # テキストを大きく表示
    # sudo apt install fonts-noto-cjk でインストール
    label = tk.Label(root, text=response.text, font=("Noto Sans CJK JP", 50), wraplength=1500)
    label.pack(expand=True)

    # 1分後に閉じる
    root.after(60000, root.destroy)
    root.mainloop()

display_text()
