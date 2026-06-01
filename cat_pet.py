import tkinter as tk
import os
from PIL import Image, ImageTk

class CatPet:
    def __init__(self, root):
        self.root = root
        self.root.title("猫咪桌面宠物")

        # 设置窗口置顶、透明和无边框
        self.root.attributes("-topmost", True)
        self.root.attributes("-transparentcolor", "#000001")
        self.root.overrideredirect(True)

        # 初始化位置（桌面右上角）
        screen_width = self.root.winfo_screenwidth()
        self.x = screen_width - 160
        self.y = 0

        # 设置窗口大小
        self.root.geometry("160x180")

        # 主画布（透明背景）
        self.canvas = tk.Canvas(self.root, width=160, height=180, bg="#000001", highlightthickness=0)
        self.canvas.pack()

        # 猫咪图片列表
        self.cat_images = ["猫1.png", "猫2.png", "猫3.png"]
        self.current_cat_index = 0
        self.cat_photo = None

        # 加载猫咪图片
        self.load_cat_image()

        # 右键菜单
        self.menu = tk.Menu(self.root, tearoff=0)
        self.menu.add_command(label="退出", command=self.close_app)
        self.canvas.bind("<Button-3>", self.show_menu)

        # 拖拽状态
        self.dragging = False
        self.drag_start = (0, 0)
        self.click_pos = (0, 0)

        # 绑定鼠标事件
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

        # 开始主循环
        self.main_loop()

    def load_cat_image(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.canvas.delete("all")

        cat_image_path = os.path.join(script_dir, self.cat_images[self.current_cat_index])

        try:
            if os.path.exists(cat_image_path):
                img = Image.open(cat_image_path).convert('RGB')
                img = img.resize((160, 160), Image.LANCZOS)

                # 将近白像素（RGB 均 > 248）替换为透明色 #000001
                datas = list(img.getdata())
                bg_color = (0, 0, 1)
                new_data = [bg_color if p[0] == 255 and p[1] == 255 and p[2] == 255 else p for p in datas]
                img.putdata(new_data)

                self.cat_photo = ImageTk.PhotoImage(img)
                self.canvas.create_image(80, 90, image=self.cat_photo)
                self.canvas.image = self.cat_photo
            else:
                self.canvas.create_text(80, 90,
                                      text=f"找不到图片\n{self.cat_images[self.current_cat_index]}",
                                      font=("Arial", 10), fill="white")
        except Exception as e:
            print(f"图片加载失败: {e}")
            self.cat_ascii = """     /\\_/\\  \n    ( ^.^ ) \n     > ^ <"""
            self.canvas.create_text(80, 90, text=self.cat_ascii, font=("Courier", 14), fill="#FF8C00")

    def switch_cat(self):
        self.current_cat_index = (self.current_cat_index + 1) % len(self.cat_images)
        self.load_cat_image()

    def close_app(self):
        self.root.destroy()

    def show_menu(self, event):
        self.menu.post(event.x_root, event.y_root)

    def main_loop(self):
        self.root.geometry(f"+{int(self.x)}+{int(self.y)}")
        self.root.after(50, self.main_loop)

    def on_click(self, event):
        self.dragging = True
        self.drag_start = (event.x, event.y)
        self.click_pos = (event.x, event.y)

    def on_drag(self, event):
        if self.dragging:
            delta_x = event.x - self.drag_start[0]
            delta_y = event.y - self.drag_start[1]
            self.x += delta_x
            self.y += delta_y
            self.drag_start = (event.x, event.y)

    def on_release(self, event):
        if self.dragging:
            dx = event.x - self.click_pos[0]
            dy = event.y - self.click_pos[1]
            dist = (dx * dx + dy * dy) ** 0.5
            if dist < 5:
                self.switch_cat()
        self.dragging = False

if __name__ == "__main__":
    root = tk.Tk()
    app = CatPet(root)
    root.mainloop()
