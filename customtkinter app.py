from customtkinter import *

app = CTk()
app.title("Kwabs's To-Do List")
app.geometry("500x400")

btn_quit = CTkButton(master=app, text="X", text_color="white", width=28, corner_radius=6, hover_color="#FF0000", border_width=1, border_color="#FFFFFF", command=app.quit)
btn_quit.place(relx=0.995, rely=0.01, anchor="ne") # rel=1.0 --> 100%

lbl_todolist = CTkLabel(master=app, text="To-do List", font=("Cabin", 20), text_color="#FFCC70", bg_color="#FF0000", fg_color="#FFFFFF")


# Configure the grid to expand
app.grid_columnconfigure(0, weight=1)
app.grid_rowconfigure(0, weight=1)

# Create a frame to hold the to-do list
frame = CTkScrollableFrame(master=app, fg_color="#8D6F3A", border_color="#FFCC70", border_width=2)
frame.grid(row=0, column=0, padx=30, pady=30, sticky="nsew")

# Configure the frame's grid to expand
frame.grid_columnconfigure(0, weight=3)
frame.grid_rowconfigure(0, weight=3)
frame.grid_columnconfigure(1, weight=1)
frame.grid_rowconfigure(1, weight=1)

def remove_taskrow(textbox, button):
    textbox.destroy()
    tasks.remove(textbox)

    button.destroy()
    buttons.remove(button)

    update_taskrow()

def update_taskrow():
    global curr_taskrow
    curr_taskrow = 1
    for i in range(len(tasks)):
        tasks[i].grid(row=i+1, column=0, padx=10, pady=10)
        buttons[i].grid(row=curr_taskrow, column=1, padx=10, pady=10)
        curr_taskrow += 1

def add_taskrow():
    global button_count, curr_taskrow, buttons

    new_text = CTkEntry(master=frame)
    new_text.grid(row=curr_taskrow, column=0, padx=10, pady=10) #, sticky="nsew"
    task_name = input_field.get()
    input_field.delete(0, "end")
    new_text.insert(0, task_name)
    new_text.configure(state="readonly")
    tasks.append(new_text)

    new_button = CTkButton(master=frame, text=f"Task {button_count}")
    new_button.configure(command=lambda: remove_taskrow(new_text, new_button))
    new_button.grid(row=curr_taskrow, column=1, padx=10, pady=10)
    buttons.append(new_button)

    button_count += 1
    curr_taskrow += 1

buttons = []
tasks = []
curr_taskrow = 1
button_count = 1

input_field = CTkEntry(master=frame, placeholder_text="Enter a task...")
input_field.grid(row=0, column=0, padx=10, pady=10)
add_button = CTkButton(master=frame, text="Add Task", command=add_taskrow)
add_button.grid(row=0, column=1, padx=10, pady=10)



# # Create a label
# label = CTkLabel(app, text="Hello, CustomTkinter!")
# label.pack(pady=20)

# # Create a button
# button = CTkButton(app, text="Click Me")
# button.pack(pady=10)

# Loops forever & listens to clicks
app.mainloop()