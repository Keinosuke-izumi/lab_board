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
prompt = "ここは研究室です。この部屋でだらしない場所があれば教えて下さい。また、なんでもいいので変な人がいれば指摘して下さい。ただし、150字以内でキズナアイ口調の日本語で回答して下さい。"

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

    # フォントサイズを調整する関数
    def adjust_font_size():
        current_font_size = 50
        while True:
            label.config(font=("Noto Sans CJK JP", current_font_size))
            label.update_idletasks()
            if label.winfo_height() <= window_height and label.winfo_width() <= window_width:
                break
            current_font_size -= 2  # 少しずつフォントサイズを小さく調整
            if current_font_size < 10:  # フォントサイズの下限を設定
                break
    
    # テキスト表示後にフォントサイズを調整
    root.after(100, adjust_font_size)

    # 1分後に閉じる
    root.after(60000, root.destroy)
    root.mainloop()

if __name__ == "__main__":
    display_text()