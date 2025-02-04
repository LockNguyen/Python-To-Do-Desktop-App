from customtkinter import *

app = CTk()
app.title("Kwabs's To-Do List")
app.geometry("500x400")

# Button, callback, place()
btn_quit = CTkButton(master=app,                text="X", 
                     text_color="white",        hover_color="#FF0000",
                     border_color="#FFFFFF",    border_width=1,
                     width=28,                  corner_radius=6, 
                     command=app.quit)

# Place (abs) vs. Pack (rel)
# Place (relx/y, anchor)
btn_quit.place(relx=0.995, rely=0.01, anchor="ne") # rel=1.0 --> 100%
# Pack (side, fill, expand) (padx/y, ipadx/y)
# btn_quit.pack(side=TOP, pady=10, anchor="e")



# SKIP THIS ----------------------------------------------------------------------
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

# Create an error message label and hide it initially
# error_label = CTkLabel(master=frame, text="Error! Task cannot be empty.", text_color="red")
# error_label.grid(row=2, column=0, columnspan=2, pady=10)
# error_label.grid_remove()

def remove_taskrow(textbox, button):
    textbox.destroy()
    tasks.remove(textbox)

    button.destroy()
    buttons.remove(button)

    update_taskrow()

def update_taskrow():
    global curr_taskrow
    curr_taskrow = 2
    for i in range(len(tasks)):
        tasks[i].grid(row=curr_taskrow, column=0, padx=10, pady=10, sticky="ew")
        buttons[i].grid(row=curr_taskrow, column=1, padx=10, pady=10, sticky="ew")
        curr_taskrow += 1

def add_taskrow():
    task_name = input_field.get()
    input_field.delete(0, "end")
    # if not task_name.strip():
    #     show_error_modal()
    #     return
    
    global button_count, curr_taskrow, buttons

    new_text = CTkEntry(master=frame)
    new_text.grid(row=curr_taskrow, column=0, padx=10, pady=10, sticky="ew")
    new_text.insert(0, task_name)
    new_text.configure(state="readonly")
    tasks.append(new_text)

    new_button = CTkButton(master=frame, text=f"Task {button_count}")
    new_button.configure(command=lambda: remove_taskrow(new_text, new_button))
    new_button.grid(row=curr_taskrow, column=1, padx=10, pady=10, sticky="ew")
    buttons.append(new_button)

    button_count += 1
    curr_taskrow += 1

# def show_error_modal():
#     error_label.grid()
#     app.after(2000, error_label.grid_remove)  # Hide the error message after 2000 milliseconds (2 seconds)

buttons = []
tasks = []
curr_taskrow = 2
button_count = 1
# END SKIP ----------------------------------------------------------------------



# Grid ("best, highly responsive (4 re-sizing) & extendable (4 adding)" - author of customtkinter)
# app.grid_columnconfigure(0, weight=5)
# app.grid_rowconfigure(0, weight=5)
# app.grid_columnconfigure(1, weight=1)
# app.grid_rowconfigure(1, weight=1)

# Entry & add_button (sticky)
input_field = CTkEntry(master=frame, placeholder_text="Enter a task...")
input_field.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
add_button = CTkButton(master=frame, text="Add Task", command=add_taskrow) #, command=add_taskrow
add_button.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

# Label
lbl_todolist = CTkLabel(master=frame, text="To-do List", font=("Cabin", 20), text_color="#FFFFFF")
lbl_todolist.grid(row=0, column=0, columnspan=2, padx=10, pady=10)



# Loops forever & listens to clicks
app.mainloop()