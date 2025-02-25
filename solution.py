from customtkinter import CTk, CTkButton, CTkEntry, CTkLabel, CTkScrollableFrame, CTkTabview, CTkTextbox
import requests
import pyrebase


class ToDoApp:
    """A modern To-Do List application with themes, colors, animations, and drag-and-drop functionality."""

    def __init__(self):
        """
        It's like a Constructor in C++!
        Define class variables to be used ANYwhere within the class here.

        """
        self.app = CTk()
        self.app.title("Kwabs's To-Do List")
        self.app.geometry("600x500")

        # Task storage
        self.tasks = []
        self.task_buttons = [] # Buttons to remove tasks
        self.dragging_index = None  # Track which task is being dragged

        firebase_config = {
            "apiKey": "AIzaSyBTK_bxSrB4Ob-UiqUK-ZScWN6iJQmHRqY",
            "authDomain": "sdc-to-do.firebaseapp.com",
            "projectId": "sdc-to-do",
            "storageBucket": "sdc-to-do.firebasestorage.app",
            "messagingSenderId": "946654441691",
            "appId": "1:946654441691:web:7e84b748493a6321021cfe",
            "databaseURL": "https://sdc-to-do-default-rtdb.firebaseio.com/"
        }
        
        firebase = pyrebase.initialize_app(firebase_config)

        self.auth_service = firebase.auth()
        self.db_service = firebase.database()

        self.user = None
        self.uid = None

        # Create UI components
        self.show_login_ui()

    def show_login_ui(self):
        self.username_label = CTkLabel(master=self.app, text="🧑 Username",
            font=("Cabin", 22, "bold"), text_color="#FFCC70")
        self.password_label = CTkLabel(master=self.app, text="🔑 Password",
            font=("Cabin", 22, "bold"), text_color="#FFCC70")
        self.username_input = CTkEntry(master=self.app, placeholder_text="Enter your email...", width=250)
        self.password_input = CTkEntry(master=self.app, width=250)
        self.login_button = CTkButton(
            master=self.app, text="Login ➜", text_color="white",
            width=30, height=30, corner_radius=6,
            fg_color="#2E2E2E", hover_color="#FF0000",
            border_color="#FFCC70", border_width=1,
            command=self.login
        )
        self.signup_button = CTkButton(
            master=self.app, text="Sign Up ➜", text_color="white",
            width=30, height=30, corner_radius=6,
            fg_color="#2E2E2E", hover_color="#FF0000",
            border_color="#FFCC70", border_width=1,
            command=self.signup
        )

        self.username_label.pack(pady=10, padx=10)
        self.username_input.pack(pady=10, padx=10)
        self.password_label.pack(pady=10, padx=10)
        self.password_input.pack(pady=10, padx=10)
        self.login_button.pack(pady=10, padx=10)
        self.signup_button.pack(pady=10, padx=10)

    def destroy_login_ui(self):
        self.username_label.destroy()
        self.username_input.destroy()
        self.password_label.destroy()
        self.password_input.destroy()
        self.login_button.destroy()
        self.signup_button.destroy()

    def login(self):
        username = self.username_input.get().strip()
        self.username_input.delete(0, "end")
        password = self.password_input.get().strip()
        self.password_input.delete(0, "end")

        if username == "" or password == "":
            self.show_error_modal()
            return
        
        try:
            self.user = self.auth_service.sign_in_with_email_and_password(username, password)
        except:
            self.user = None
            self.show_error_modal()
            return

        if "error" in self.user:
            self.user = None
            self.show_error_modal()
            return
        
        if "idToken" in self.user:
            indexOfAt = self.user['email'].index("@")
            self.uid = self.user['email'][:indexOfAt] # [0, index)

            self.destroy_login_ui()
            self.create_ui()
            self.load_tasks_from_firebase()

    def signup(self):
        pass

    def create_ui(self):
        # Create tabviews
        self.tabs = CTkTabview(master=self.app,
                               width=1920, height=1080, # 1920x1080: The tab shrinks responsively, but doesn't expand. Therefore, give it the max resolution of the entire screen.
                               corner_radius=6, anchor="n")
        self.tabs.pack(pady=10, padx=10, fill='both',)

        # Create tabs
        self.tab_1 = self.tabs.add("To Do List")
        self.tab_2 = self.tabs.add("Cat Facts")

        """Set up the UI layout and widgets with styling."""
        # Quit button (top-right corner)
        quit_button = CTkButton(
            master=self.app, text="❌", text_color="white",
            width=30, height=30, corner_radius=6,
            fg_color="#2E2E2E", hover_color="#FF0000",
            border_color="#FFCC70", border_width=1,
            command=self.app.quit
        )
        quit_button.place(relx=0.98, rely=0.02, anchor="ne")

        # Configure layout responsiveness
        self.tab_1.grid_columnconfigure(0, weight=1)
        self.tab_1.grid_rowconfigure(0, weight=1)
            # ^ In the app screen, create a grid (or "table") that has 1 row & 1 column.
            #   Basically a big square that fills the whole screen.

        # On the app screen, create a scrollable frame (will put the to-do list inside)
        self.frame = CTkScrollableFrame(
            master=self.tab_1, fg_color="#2E2E2E",
            border_color="#FFCC70", border_width=2,
        )
        self.frame.grid(row=0, column=0, padx=30, pady=20, sticky="nsew")

        # Configure layout responsiveness
        self.frame.grid_columnconfigure(0, weight=3)
        self.frame.grid_columnconfigure(1, weight=1)
            # ^ In the frame, create a grid (or "table") that has 2 columns.
            #   LEFT (column 0) = task title; RIGHT (column 1) = remove button.

        # Title Label
        lbl_todolist = CTkLabel(
            master=self.frame, text="📌 Kwab's To-do List",
            font=("Cabin", 22, "bold"), text_color="#FFCC70"
        )
        lbl_todolist.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        # Input field for new tasks
        self.input_field = CTkEntry(master=self.frame, placeholder_text="Enter a task...", width=250)
        self.input_field.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
            # ^ sticky="ew" tells the input field to expand to touch East & West walls of its box in the grid.
            # ^ Try removing "sticky" to see what happens!
        self.input_field.bind("<Return>", lambda event: self.add_task())

        # Add Task button
        add_button = CTkButton(
            master=self.frame, text="➕ Add Task",
            command=self.add_task, corner_radius=6
        )
        add_button.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        # Error message label (initially hidden)
        self.error_label = CTkEntry(master=self.frame, text_color="red", width=200)
        self.error_label.insert(0, "⚠️ Error! Task cannot be empty.")
        self.error_label.configure(state="readonly")

        # Generate Meme button
        fact_button = CTkButton(master=self.tab_2, text="Get Cat Fact", command=self.get_cat_fact)
        fact_button.pack(pady=10)

        self.fact_text = CTkTextbox(master=self.tab_2)
        self.fact_text.configure(state='disabled')
        self.fact_text.pack(padx=30, pady=20, fill="both")

    def show_error_modal(self):
        # MEDIUM CHALLENGE: Implement the show_error_modal() function here!
        #   1. Display the modal
        #   2. Make sure it's on top
        #   3. Hide the error message after 2000 milliseconds (2 seconds)
        return
    
    def add_to_db(self, data: str):
        task_id = self.db_service.child("tasks").child(self.uid).push(data, self.user['idToken'])
        return task_id
    
    def remove_from_db(self, task_id: str):
        self.db_service.child("tasks").child(self.uid).child(task_id).remove()
        return

    def add_task(self):
        """Add a new task to the list."""
        task_text = self.input_field.get().strip()
        self.input_field.delete(0, "end")

        if task_text == "":
            self.show_error_modal()
            return
        
        # Add to Firebase Realtime database first.
        # If works, continue. If not, don't add.
        task_id = self.add_to_db(task_text)
        task_id = task_id["name"]
        print(f"Added task! task_id: {task_id}")

        # Create task entry (readonly)
        task_entry = CTkEntry(master=self.frame, width=250)
        task_entry.insert(0, task_text)
        task_entry.configure(state="readonly")

        # Create remove button
        remove_button = CTkButton(
            master=self.frame, text="❌ Remove",
            command=lambda: self.remove_task(task_id)
        )        

        # ADVANCED: Enable drag-and-drop
        task_entry.bind("<Button-1>", lambda event: self.start_drag(task_entry)) # Right button clicked
        task_entry.bind("<B1-Motion>", self.drag_task)          # Right button clicked & moving
        task_entry.bind("<ButtonRelease-1>", self.drop_task)    # Right button released

        # Add to storage
        self.tasks.append((task_id, task_entry))
        self.task_buttons.append(remove_button)

        self.display_tasks()

    def remove_task(self, task_id: str):
        """Remove a task from the list."""

        for i in range(len(self.tasks)):
            id, task_entry = self.tasks[i]
            print(id, task_id)

            if id == task_id:
                self.remove_from_db(task_id)
                self.tasks.pop(i)
                remove_button = self.task_buttons.pop(i)

                task_entry.destroy()
                remove_button.destroy()
                self.display_tasks()

                break

        return

    def display_tasks(self):
        """Re-display the tasks on the screen to maintain proper layout."""
        for i in range(len(self.tasks)):
            task_id, task_entry = self.tasks[i]
            button = self.task_buttons[i]
            task_entry.grid(row=i+2, column=0, padx=10, pady=10, sticky="ew")  # 0th & 1st rows are for the title & input field
            button.grid(row=i+2, column=1, padx=10, pady=10, sticky="ew")

    def load_tasks_from_firebase(self):
        db_tasks = self.db_service.child("tasks").child(self.uid).get().each()

        for task in db_tasks:

            task_id = task.key()
            task_text = task.val()

            # print(f"Loaded task! ID: {task_id}, {type(task_id)}")

            # Create task entry (readonly)
            task_entry = CTkEntry(master=self.frame, width=250)
            task_entry.insert(0, task_text)
            task_entry.configure(state="readonly")

            # Create remove button
            remove_button = CTkButton(
                master=self.frame, text="❌ Remove",
                command=lambda t_id=task_id: self.remove_task(t_id) # t_id=task_id captures the task_id value now, so remove_task can reference that, instead of the constantly-changing task_id value.
            )
            
            self.tasks.append((task_id, task_entry))
            self.task_buttons.append(remove_button)

            self.display_tasks() 

    def get_cat_fact(self):
        # API endpoint URL
        url = 'https://catfact.ninja/fact'

        try:
            # Make a GET request to the API endpoint using requests.get()
            response = requests.get(url)

            if response.status_code == 200:
                cat_fact = response.json()

                self.fact_text.configure(state='normal')
                self.fact_text.delete("0.0", "end")
                self.fact_text.insert("0.0", cat_fact["fact"])
                self.fact_text.configure(state='disabled')
            else:
                print('Error:', response.status_code)
                return None
        except requests.exceptions.RequestException as e:
            print('Error:', e)
            return None

    def start_drag(self, task_entry):
        """ADVANCED: Begin dragging a task."""
        self.dragging_index = self.tasks.index(task_entry)
        task_entry.configure(fg_color="#FFD700")  # Highlight the task being dragged

    def drag_task(self, event):
        """ADVANCED: Move a task while dragging."""
        if self.dragging_index is None:
            return

        y_position = event.y_root - self.frame.winfo_rooty()  # Get position within the frame
            # ^ y_from_frame's_top_to_mouse = y_from_screen's_top_to_mouse - y_from_screen's_top_to_frame's_top

        # Determine new index based on Y position
        for i, task in enumerate(self.tasks):
            if task.winfo_y() > y_position:
                # Swap positions
                self.tasks.insert(i, self.tasks.pop(self.dragging_index))
                self.task_buttons.insert(i, self.task_buttons.pop(self.dragging_index))
                self.dragging_index = i
                self.display_tasks()
                break

    def drop_task(self, event):
        """ADVANCED: Drop a task after dragging."""
        if self.dragging_index is not None:
            self.tasks[self.dragging_index].configure(fg_color="#2E2E2E")  # Reset color
        self.dragging_index = None

    def run(self):
        """Run the application event loop."""
        self.app.mainloop()


if __name__ == "__main__":
    """This is the driver code. Program execution starts here."""
    my_app = ToDoApp() # Create an instance (will call __init__())
    my_app.run() # Run that instance
