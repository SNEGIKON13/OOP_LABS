import os
import time
from canvas import Canvas
from shapes.circle import Circle
from shapes.line import Line
from shapes.rectangle import Rectangle
from commands import AddShapeCommand, RemoveShapeCommand, MoveShapeCommand, SetBackgroundCommand, SetCharCommand

class PaintApp:
    def __init__(self):
        self.canvas = Canvas(width=80, height=18)  # Изменено height с 24 на 18
        self.undo_stack = []
        self.redo_stack = []
        self.messages = []

    def add_message(self, message):
        self.messages.append(message)
        if len(self.messages) > 5:
            self.messages.pop(0)

    def display_messages(self):
        print("\nMessages:")
        if not self.messages:
            print("No messages.")
        else:
            for msg in self.messages:
                print(msg)

    def execute_command(self, command):
        command.execute()
        self.undo_stack.append(command)
        self.redo_stack.clear()
        self.canvas.render()

    def undo(self):
        if self.undo_stack:
            command = self.undo_stack.pop()
            command.undo()
            self.redo_stack.append(command)
            self.canvas.render()
            self.add_message("Undo performed successfully.")
        else:
            self.add_message("Nothing to undo. The undo stack is empty.")

    def redo(self):
        if self.redo_stack:
            command = self.redo_stack.pop()
            command.execute()
            self.undo_stack.append(command)
            self.canvas.render()
            self.add_message("Redo performed successfully.")
        else:
            self.add_message("Nothing to redo. The redo stack is empty.")

    def validate_int(self, value, min_val, max_val, prompt):
        try:
            val = int(value)
            if min_val <= val <= max_val:
                return val
            else:
                self.add_message(f"Error: {prompt} must be between {min_val} and {max_val}. You entered: {value}")
                return None
        except ValueError:
            self.add_message(f"Error: {prompt} must be a valid integer. You entered: {value}")
            return None

    def validate_char(self, value, prompt, allow_empty=False):
        if not value.strip() and allow_empty:
            return None
        if not value.strip():
            self.add_message(f"Error: {prompt} cannot be empty.")
            return None
        if len(value) == 1:
            return value
        self.add_message(f"Error: {prompt} must be a single character. You entered: '{value}'")
        return False

    def run(self):
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            self.canvas.render()
            self.canvas.print_grid()
            print("\nShapes:")
            if not self.canvas.shapes:
                print("No shapes on canvas.")
            for s in self.canvas.list_shapes():
                print(s)
            self.display_messages()
            print("\nMenu:")
            print("1. Draw circle")
            print("2. Draw line")
            print("3. Draw rectangle")
            print("4. Erase shape")
            print("5. Move shape")
            print("6. Set background")
            print("7. Set shape character")
            print("8. Save")
            print("9. Load")
            print("10. Undo")
            print("11. Redo")
            print("0. Exit")
            choice = input("Enter choice: ").strip()
            if not choice:
                self.add_message("Error: Choice cannot be empty. Please select a menu option.")
                time.sleep(1)
                continue

            if choice == '0':
                self.add_message("Exiting the application. Goodbye!")
                self.display_messages()
                break
            elif choice == '1':
                x = self.validate_int(input("Enter x (0-79): "), 0, 79, "X coordinate")
                if x is None: continue
                y = self.validate_int(input("Enter y (0-17): "), 0, 17, "Y coordinate")  # Изменено с 0-23 на 0-17
                if y is None: continue
                radius = self.validate_int(input("Enter radius (0-10): "), 0, 10, "Radius")
                if radius is None: continue
                char = self.validate_char(input("Enter char (default '*'): ") or '*', "Character", allow_empty=True)
                if char is False: continue
                fill_char_input = input("Enter fill char (optional, default None): ").strip()
                fill_char = self.validate_char(fill_char_input, "Fill character", allow_empty=True) if fill_char_input else None
                if fill_char is False: continue
                shape = Circle(x, y, radius, char, fill_char)
                self.execute_command(AddShapeCommand(self.canvas, shape))
                self.add_message("Circle added successfully.")
            elif choice == '2':
                x1 = self.validate_int(input("Enter x1 (0-79): "), 0, 79, "X1 coordinate")
                if x1 is None: continue
                y1 = self.validate_int(input("Enter y1 (0-17): "), 0, 17, "Y1 coordinate")  # Изменено с 0-23 на 0-17
                if y1 is None: continue
                x2 = self.validate_int(input("Enter x2 (0-79): "), 0, 79, "X2 coordinate")
                if x2 is None: continue
                y2 = self.validate_int(input("Enter y2 (0-17): "), 0, 17, "Y2 coordinate")  # Изменено с 0-23 на 0-17
                if y2 is None: continue
                char = self.validate_char(input("Enter char (default '-'): ") or '-', "Character", allow_empty=True)
                if char is False: continue
                shape = Line(x1, y1, x2, y2, char)
                self.execute_command(AddShapeCommand(self.canvas, shape))
                self.add_message("Line added successfully.")
            elif choice == '3':
                x1 = self.validate_int(input("Enter x1 (0-79): "), 0, 79, "X1 coordinate")
                if x1 is None: continue
                y1 = self.validate_int(input("Enter y1 (0-17): "), 0, 17, "Y1 coordinate")  # Изменено с 0-23 на 0-17
                if y1 is None: continue
                x2 = self.validate_int(input("Enter x2 (0-79): "), 0, 79, "X2 coordinate")
                if x2 is None: continue
                y2 = self.validate_int(input("Enter y2 (0-17): "), 0, 17, "Y2 coordinate")  # Изменено с 0-23 на 0-17
                if y2 is None: continue
                border_char = self.validate_char(input("Enter border char (default '*'): ") or '*', "Border character", allow_empty=True)
                if border_char is False: continue
                fill_char_input = input("Enter fill char (optional, default None): ").strip()
                fill_char = self.validate_char(fill_char_input, "Fill character", allow_empty=True) if fill_char_input else None
                if fill_char is False: continue
                shape = Rectangle(x1, y1, x2, y2, border_char, fill_char)
                self.execute_command(AddShapeCommand(self.canvas, shape))
                self.add_message("Rectangle added successfully.")
            elif choice == '4':
                if not self.canvas.shapes:
                    self.add_message("Error: No shapes to erase. Please add a shape first.")
                    continue
                shape_id = self.validate_int(input("Enter shape ID to erase: "), 1, self.canvas.next_id - 1, "Shape ID")
                if shape_id is None: continue
                if not any(s.id == shape_id for s in self.canvas.shapes):
                    self.add_message("Error: Shape ID not found. Please check the list of shapes.")
                    continue
                self.execute_command(RemoveShapeCommand(self.canvas, shape_id))
                self.add_message(f"Shape with ID {shape_id} erased successfully.")
            elif choice == '5':
                if not self.canvas.shapes:
                    self.add_message("Error: No shapes to move. Please add a shape first.")
                    continue
                shape_id = self.validate_int(input("Enter shape ID to move: "), 1, self.canvas.next_id - 1, "Shape ID")
                if shape_id is None: continue
                if not any(s.id == shape_id for s in self.canvas.shapes):
                    self.add_message("Error: Shape ID not found. Please check the list of shapes.")
                    continue
                dx = self.validate_int(input("Enter dx: "), -79, 79, "X displacement")
                if dx is None: continue
                dy = self.validate_int(input("Enter dy: "), -17, 17, "Y displacement")  # Изменено с -23, 23 на -17, 17
                if dy is None: continue
                shape = next((s for s in self.canvas.shapes if s.id == shape_id), None)
                self.execute_command(MoveShapeCommand(shape, dx, dy))
                self.add_message(f"Shape with ID {shape_id} moved successfully by dx={dx}, dy={dy}.")
            elif choice == '6':
                if not self.canvas.shapes:
                    self.add_message("Error: No shapes to set background for. Please add a shape first.")
                    continue
                shape_id = self.validate_int(input("Enter shape ID to set background: "), 1, self.canvas.next_id - 1, "Shape ID")
                if shape_id is None: continue
                if not any(s.id == shape_id for s in self.canvas.shapes):
                    self.add_message("Error: Shape ID not found. Please check the list of shapes.")
                    continue
                shape = next((s for s in self.canvas.shapes if s.id == shape_id), None)
                if not isinstance(shape, (Rectangle, Circle)):
                    self.add_message("Error: Only rectangles and circles support background fill.")
                    continue
                fill_char = self.validate_char(input("Enter fill char: "), "Fill character", allow_empty=False)
                if fill_char is None: continue
                if fill_char is False: continue
                self.execute_command(SetBackgroundCommand(shape, fill_char))
                self.add_message(f"Background for shape with ID {shape_id} set to '{fill_char}' successfully.")
            elif choice == '7':
                if not self.canvas.shapes:
                    self.add_message("Error: No shapes to set character for. Please add a shape first.")
                    continue
                shape_id = self.validate_int(input("Enter shape ID to set character: "), 1, self.canvas.next_id - 1, "Shape ID")
                if shape_id is None: continue
                if not any(s.id == shape_id for s in self.canvas.shapes):
                    self.add_message("Error: Shape ID not found. Please check the list of shapes.")
                    continue
                shape = next((s for s in self.canvas.shapes if s.id == shape_id), None)
                new_char_input = input("Enter new character: ").strip()
                new_char = self.validate_char(new_char_input, "New character", allow_empty=False)
                if new_char is None or new_char is False: continue
                self.execute_command(SetCharCommand(shape, new_char))
                self.add_message(f"Character for shape with ID {shape_id} set to '{new_char}' successfully.")
            elif choice == '8':
                filename = input("Enter filename to save: ").strip()
                if not filename:
                    self.add_message("Error: Filename cannot be empty. Please provide a valid filename.")
                    continue
                if not filename.isalnum():
                    self.add_message("Error: Filename should contain only alphanumeric characters for safety.")
                    continue
                self.canvas.save(filename)
                self.add_message(f"Canvas saved to {filename}.json successfully.")
            elif choice == '9':
                filename = input("Enter filename to load: ").strip()
                if not filename:
                    self.add_message("Error: Filename cannot be empty. Please provide a valid filename.")
                    continue
                if not filename.isalnum():
                    self.add_message("Error: Filename should contain only alphanumeric characters for safety.")
                    continue
                try:
                    self.canvas.load(filename)
                    self.canvas.render()
                    self.add_message(f"Canvas loaded from {filename}.json successfully.")
                except FileNotFoundError as e:
                    self.add_message(str(e))
                except ValueError as e:
                    self.add_message(str(e))
                except Exception as e:
                    self.add_message(str(e))
            elif choice == '10':
                self.undo()
            elif choice == '11':
                self.redo()
            else:
                self.add_message(f"Error: Invalid choice '{choice}'. Please select a valid menu option (0-11).")
            time.sleep(1)

# Запуск приложения
if __name__ == "__main__":
    app = PaintApp()
    app.run()