import tkinter as tk

def on_button_click():
    text_field.insert(tk.END, "нажал\n")
def on_clear_click():
    text_field.delete(1.0, tk.END)
root = tk.Tk()
#root.title("Простое приложение")
root.geometry("400x400")
# Кнопки можно разместить друг под другом
button1 = tk.Button(root, text="Нажать", command=on_button_click)
button1.pack(pady=10)
button2 = tk.Button(root, text="Очистить", command=on_clear_click)
button2.pack(pady=10)
text_field = tk.Text(root, height=10, width=40)
text_field.pack()
root.mainloop()
