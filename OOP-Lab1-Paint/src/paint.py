import os
import json
import time

# Класс Canvas
class Canvas:
    def __init__(self, width=80, height=18):  # Изменено height с 24 на 18
        self.width = width
        self.height = height
        self.grid = [['.' for _ in range(width)] for _ in range(height)]
        self.shapes = []
        self.next_id = 1
        self.background_char = '.'

    def add_shape(self, shape):
        shape.id = self.next_id
        self.next_id += 1
        self.shapes.append(shape)

    def remove_shape(self, shape_id):
        self.shapes = [s for s in self.shapes if s.id != shape_id]

    def render(self):
        self.grid = [['.' for _ in range(self.width)] for _ in range(self.height)]
        for shape in self.shapes:
            if isinstance(shape, Circle):
                self.draw_circle(shape.x, shape.y, shape.radius, shape.char, shape.fill_char)
            elif isinstance(shape, Line):
                self.draw_line(shape.x1, shape.y1, shape.x2, shape.y2, shape.char)
            elif isinstance(shape, Rectangle):
                self.draw_rectangle(shape.x1, shape.y1, shape.x2, shape.y2, shape.char, shape.fill_char)

    def draw_circle(self, x, y, radius, char, fill_char=None):
        if fill_char:
            for dy in range(-radius, radius + 1):
                for dx in range(-radius, radius + 1):
                    if dx * dx + dy * dy <= radius * radius:
                        px, py = x + dx, y + dy
                        if 0 <= px < self.width and 0 <= py < self.height:
                            self.grid[py][px] = fill_char
        x_pos = radius
        y_pos = 0
        err = 0
        while x_pos >= y_pos:
            for dx, dy in [(x_pos, y_pos), (-x_pos, y_pos), (x_pos, -y_pos), (-x_pos, -y_pos),
                           (y_pos, x_pos), (-y_pos, x_pos), (y_pos, -x_pos), (-y_pos, -x_pos)]:
                px, py = x + dx, y + dy
                if 0 <= px < self.width and 0 <= py < self.height:
                    self.grid[py][px] = char
            y_pos += 1
            err += 1 + 2 * y_pos
            if 2 * (err - x_pos) + 1 > 0:
                x_pos -= 1
                err += 1 - 2 * x_pos

    def draw_line(self, x1, y1, x2, y2, char):
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy
        while True:
            if 0 <= x1 < self.width and 0 <= y1 < self.height:
                self.grid[y1][x1] = char
            if x1 == x2 and y1 == y2:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x1 += sx
            if e2 < dx:
                err += dx
                y1 += sy

    def draw_rectangle(self, x1, y1, x2, y2, border_char, fill_char):
        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                if x == x1 or x == x2 or y == y1 or y == y2:
                    if 0 <= x < self.width and 0 <= y < self.height:
                        self.grid[y][x] = border_char
                elif fill_char:
                    if 0 <= x < self.width and 0 <= y < self.height:
                        self.grid[y][x] = fill_char

    def print_grid(self):
        col_nums = [' '] * (self.width + 3)
        for i in range(0, self.width, 10):
            num_str = str(i)
            col_nums[i + 3] = num_str[0]
            if i >= 10:
                col_nums[i + 4] = num_str[1]
        col_nums[-2] = '7'
        col_nums[-1] = '9'
        print(''.join(col_nums))
        for y in range(self.height):
            print(f'{y:2d} ', end='')
            print(''.join(self.grid[y]))
        print(f"Canvas size: {self.width}x{self.height}")

    def save(self, filename):
        if not filename.endswith('.json'):
            filename += '.json'
        with open(filename, 'w') as f:
            json.dump([shape.to_dict() for shape in self.shapes], f)

    def load(self, filename):
        try:
            if not filename.endswith('.json'):
                filename += '.json'
            with open(filename, 'r') as f:
                data = json.load(f)
                if not isinstance(data, list):
                    raise ValueError("File content must be a list of shapes.")
                if not data:
                    self.shapes = []
                    self.next_id = 1
                    return
                self.shapes = []
                self.next_id = 1
                for shape_data in data:
                    shape = Shape.from_dict(shape_data)
                    self.add_shape(shape)
        except FileNotFoundError:
            raise FileNotFoundError(f"Error: File '{filename}' not found. Please check the filename.")
        except json.JSONDecodeError:
            raise ValueError(f"Error: File '{filename}' contains invalid JSON. Please check the file content.")
        except Exception as e:
            raise Exception(f"Error: Failed to load file '{filename}'. Reason: {str(e)}")

    def list_shapes(self):
        return [f"{s.id}: {s}" for s in self.shapes]

# Абстрактный класс Shape
class Shape:
    def __init__(self, char='*'):
        self.id = None
        self.char = char

    def move(self, dx, dy):
        raise NotImplementedError

    def to_dict(self):
        raise NotImplementedError

    @staticmethod
    def from_dict(data):
        shape = None
        if data['type'] == 'Circle':
            shape = Circle.from_dict(data)
        elif data['type'] == 'Line':
            shape = Line.from_dict(data)
        elif data['type'] == 'Rectangle':
            shape = Rectangle.from_dict(data)
        else:
            raise ValueError(f"Unknown shape type: {data['type']}")
        return shape

    def __str__(self):
        raise NotImplementedError

# Класс Circle
class Circle(Shape):
    def __init__(self, x, y, radius, char='*', fill_char=None):
        super().__init__(char)
        self.x = x
        self.y = y
        self.radius = radius
        self.fill_char = fill_char

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def set_background(self, fill_char):
        self.fill_char = fill_char

    def to_dict(self):
        return {'type': 'Circle', 'x': self.x, 'y': self.y, 'radius': self.radius, 'char': self.char, 'fill_char': self.fill_char}

    @staticmethod
    def from_dict(data):
        return Circle(data['x'], data['y'], data['radius'], data['char'], data.get('fill_char'))

    def __str__(self):
        return f"Circle at ({self.x},{self.y}) with radius={self.radius} and char='{self.char}' and fill='{self.fill_char}'"

# Класс Line
class Line(Shape):
    def __init__(self, x1, y1, x2, y2, char='-'):
        super().__init__(char)
        self.x1, self.y1 = x1, y1
        self.x2, self.y2 = x2, y2

    def move(self, dx, dy):
        self.x1 += dx
        self.y1 += dy
        self.x2 += dx
        self.y2 += dy

    def to_dict(self):
        return {'type': 'Line', 'x1': self.x1, 'y1': self.y1, 'x2': self.x2, 'y2': self.y2, 'char': self.char}

    @staticmethod
    def from_dict(data):
        return Line(data['x1'], data['y1'], data['x2'], data['y2'], data['char'])

    def __str__(self):
        return f"Line from ({self.x1},{self.y1}) to ({self.x2},{self.y2}) with char='{self.char}'"

# Класс Rectangle
class Rectangle(Shape):
    def __init__(self, x1, y1, x2, y2, border_char='*', fill_char=None):
        super().__init__(border_char)
        self.x1, self.y1 = min(x1, x2), min(y1, y2)
        self.x2, self.y2 = max(x1, x2), max(y1, y2)
        self.fill_char = fill_char

    def move(self, dx, dy):
        self.x1 += dx
        self.y1 += dy
        self.x2 += dx
        self.y2 += dy

    def set_background(self, fill_char):
        self.fill_char = fill_char

    def to_dict(self):
        return {'type': 'Rectangle', 'x1': self.x1, 'y1': self.y1, 'x2': self.x2, 'y2': self.y2,
                'border_char': self.char, 'fill_char': self.fill_char}

    @staticmethod
    def from_dict(data):
        return Rectangle(data['x1'], data['y1'], data['x2'], data['y2'], data['border_char'], data.get('fill_char'))

    def __str__(self):
        return f"Rectangle from ({self.x1},{self.y1}) to ({self.x2},{self.y2}) with border='{self.char}' and fill='{self.fill_char}'"

# Абстрактный класс Command
class Command:
    def execute(self):
        raise NotImplementedError

    def undo(self):
        raise NotImplementedError

# Команда AddShapeCommand
class AddShapeCommand(Command):
    def __init__(self, canvas, shape):
        self.canvas = canvas
        self.shape = shape

    def execute(self):
        self.canvas.add_shape(self.shape)

    def undo(self):
        self.canvas.remove_shape(self.shape.id)

# Команда RemoveShapeCommand
class RemoveShapeCommand(Command):
    def __init__(self, canvas, shape_id):
        self.canvas = canvas
        self.shape_id = shape_id
        self.shape = next((s for s in canvas.shapes if s.id == shape_id), None)
        self.index = canvas.shapes.index(self.shape) if self.shape else None

    def execute(self):
        if self.shape:
            self.canvas.shapes.pop(self.index)

    def undo(self):
        if self.shape:
            self.canvas.shapes.insert(self.index, self.shape)

# Команда MoveShapeCommand
class MoveShapeCommand(Command):
    def __init__(self, shape, dx, dy):
        self.shape = shape
        self.dx = dx
        self.dy = dy

    def execute(self):
        self.shape.move(self.dx, self.dy)

    def undo(self):
        self.shape.move(-self.dx, -self.dy)

# Команда SetBackgroundCommand
class SetBackgroundCommand(Command):
    def __init__(self, shape, new_fill_char):
        self.shape = shape
        self.new_fill_char = new_fill_char
        self.old_fill_char = shape.fill_char if hasattr(shape, 'fill_char') else None

    def execute(self):
        if hasattr(self.shape, 'set_background'):
            self.shape.set_background(self.new_fill_char)

    def undo(self):
        if hasattr(self.shape, 'set_background'):
            self.shape.set_background(self.old_fill_char)

# Команда SetCharCommand
class SetCharCommand(Command):
    def __init__(self, shape, new_char):
        self.shape = shape
        self.new_char = new_char
        self.old_char = shape.char

    def execute(self):
        self.shape.char = self.new_char

    def undo(self):
        self.shape.char = self.old_char

# Класс PaintApp
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