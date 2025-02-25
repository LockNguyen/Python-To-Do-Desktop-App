from customtkinter import CTk, CTkButton, CTkEntry, CTkLabel, CTkScrollableFrame


"""A modern To-Do List application with themes, colors, animations, and drag-and-drop functionality."""

# Using global variables instead of class variables (yuck!)
app = CTk()
app.title("Kwabs's To-Do List")
app.geometry("600x500")

# Task storage
tasks = []
task_buttons = [] # Buttons to remove tasks
dragging_index = None  # Track which task is being dragged


def create_ui():
    """Set up the UI layout and widgets with styling."""
    global quit_button, frame, lbl_todolist, input_field, add_button, error_label
    # Quit button (top-right corner)
    quit_button = CTkButton(
        master=app, text="❌", text_color="white",
        width=30, height=30, corner_radius=6,
        fg_color="#2E2E2E", hover_color="#FF0000",
        border_color="#FFCC70", border_width=1,
        command=app.quit
    )
    quit_button.place(relx=0.98, rely=0.02, anchor="ne")

    # On the app screen, create a scrollable frame (will put the to-do list inside)
    frame = CTkScrollableFrame(
        master=app, fg_color="#2E2E2E",
        border_color="#FFCC70", border_width=2
    )
    frame.grid(row=0, column=0, padx=30, pady=60, sticky="nsew")

    # Configure layout responsiveness
    app.grid_columnconfigure(0, weight=1)
    app.grid_rowconfigure(0, weight=1)
        # ^ In the app screen, create a grid (or "table") that has 1 row & 1 column.
        #   Basically a big square that fills the whole screen.
    frame.grid_columnconfigure(0, weight=3)
    frame.grid_columnconfigure(1, weight=1)
        # ^ In the frame, create a grid (or "table") that has 2 columns.
        #   LEFT (column 0) = task title; RIGHT (column 1) = remove button.

    # Title Label
    lbl_todolist = CTkLabel(
        master=frame, text="📌 Kwab's To-do List",
        font=("Cabin", 22, "bold"), text_color="#FFCC70"
    )
    lbl_todolist.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

    # Input field for new tasks
    input_field = CTkEntry(master=frame, placeholder_text="Enter a task...", width=250)
    input_field.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        # ^ sticky="ew" tells the input field to expand to touch East & West walls of its box in the grid.
        # ^ Try removing "sticky" to see what happens!
    
    # MEDIUM CHALLENGE: Enable pressing the <ENTER> key to create a new task

    # Add Task button
    add_button = CTkButton(
        master=frame, text="➕ Add Task",
        command=add_task, corner_radius=6
    )
    add_button.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

    # Error message label (initially hidden)
    error_label = CTkEntry(master=frame, text_color="red", width=200)
    error_label.insert(0, "⚠️ Error! Task cannot be empty.")
    error_label.configure(state="readonly")

def show_error_modal():
    # EASY CHALLENGE: Implement the show_error_modal() function here!
    #   1. Display the modal
    #   2. Make sure it's on top
    #   3. Hide the error message after 2000 milliseconds (2 seconds)
    return

def add_task():
    """Add a new task to the list."""
    task_text = input_field.get().strip()
    input_field.delete(0, "end")

    # EASY CHALLENGE: 
    # If task_text is empty string:
    #   1. Call show_error_modal() function
    #   2. Return (stop executing)

    # Create task entry (readonly)
    task_entry = CTkEntry(master=frame, width=250)
    task_entry.insert(0, task_text)
    task_entry.configure(state="readonly")

    # Create remove button
    remove_button = CTkButton(
        master=frame, text="❌ Remove",
        command=lambda: remove_task(task_entry, remove_button)
    )        

    # ADVANCED: Enable drag-and-drop
    task_entry.bind("<Button-1>", lambda event: start_drag(task_entry)) # Right button clicked
    task_entry.bind("<B1-Motion>", drag_task)          # Right button clicked & moving
    task_entry.bind("<ButtonRelease-1>", drop_task)    # Right button released

    # Add to storage
    tasks.append(task_entry)
    task_buttons.append(remove_button)

    reorder_tasks()

def remove_task(task_entry, remove_button):
    """Remove a task from the list."""
    if task_entry in tasks:
        index = tasks.index(task_entry)
        tasks.pop(index)
        task_buttons.pop(index)

    task_entry.destroy()
    remove_button.destroy()
    reorder_tasks()

def reorder_tasks():
    """Re-display the tasks on the screen to maintain proper layout."""
    for idx, (task, button) in enumerate(zip(tasks, task_buttons), start=2):
        task.grid(row=idx, column=0, padx=10, pady=10, sticky="ew")
        button.grid(row=idx, column=1, padx=10, pady=10, sticky="ew")

def start_drag(task_entry):
    """ADVANCED: Begin dragging a task."""
    global dragging_index
    dragging_index = tasks.index(task_entry)
    task_entry.configure(fg_color="#FFD700")  # Highlight the task being dragged

def drag_task(event):
    """ADVANCED: Move a task while dragging."""
    global dragging_index
    if dragging_index is None:
        return

    y_position = event.y_root - frame.winfo_rooty()  # Get position within the frame
        # ^ y_from_frame's_top_to_mouse = y_from_screen's_top_to_mouse - y_from_screen's_top_to_frame's_top

    # Determine new index based on Y position
    for i, task in enumerate(tasks):
        if task.winfo_y() > y_position:
            # Swap positions
            tasks.insert(i, tasks.pop(dragging_index))
            task_buttons.insert(i, task_buttons.pop(dragging_index))
            dragging_index = i
            reorder_tasks()
            break

def drop_task(event):
    """ADVANCED: Drop a task after dragging."""
    global dragging_index
    if dragging_index is not None:
        tasks[dragging_index].configure(fg_color="#2E2E2E")  # Reset color
    dragging_index = None

def run():
    """Run the application event loop."""
    create_ui()
    app.mainloop()


if __name__ == "__main__":
    """This is the driver code. Program execution starts here."""
    run() # Run that instance
