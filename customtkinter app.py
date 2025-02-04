from customtkinter import *

app = CTk()
app.title("Kwabs's To-Do List")
app.geometry("500x400")

btn_quit = CTkButton(master=app, text="Click Me", corner_radius=6, hover_color="#0096FF", border_width=1, border_color="#FFFFFF", command=app.quit)
btn_quit.place(relx=0.5, rely=0.5, anchor="center") # rel=1.0 --> 100%

lbl_todolist = CTkLabel(master=app, text="To-do List", font=("Cabin", 20), text_color="#FFCC70", bg_color="#FF0000", fg_color="#FFFFFF")

button_count = 1
button_row = 0

def add_button():
    global button_count, button_row
    new_button = CTkButton(master=app, text=f"Button {button_count}")
    new_button.grid(row=button_row, column=0, padx=10, pady=10)
    button_count += 1
    button_row += 1

add_button = CTkButton(master=app, text="Add Button", command=add_button)
add_button.grid(row=button_row, column=0, padx=10, pady=10)
button_row += 1

# Create a label
label = CTkLabel(app, text="Hello, CustomTkinter!")
label.pack(pady=20)

# Create a button
button = CTkButton(app, text="Click Me")
button.pack(pady=10)

# Loops forever & listens to clicks
app.mainloop()