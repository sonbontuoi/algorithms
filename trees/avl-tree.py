import tkinter as tk

class AVLNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1

class AVLTree:
    def get_height(self, node):
        return node.height if node else 0

    def get_balance(self, node):
        return self.get_height(node.left) - self.get_height(node.right) if node else 0

    def rotate_right(self, y):
        print(f"-> Đang xoay phải tại {y.key}")
        x = y.left
        T2 = x.right
        x.right = y
        y.left = T2
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        x.height = 1 + max(self.get_height(x.left), self.get_height(x.right))
        return x

    def rotate_left(self, x):
        print(f"-> Đang xoay trái tại {x.key}")
        y = x.right
        T2 = y.left
        y.left = x
        x.right = T2
        x.height = 1 + max(self.get_height(x.left), self.get_height(x.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        return y

    def insert(self, root, key):
        if not root: return AVLNode(key)
        if key < root.key:
            root.left = self.insert(root.left, key)
        else:
            root.right = self.insert(root.right, key)

        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))
        balance = self.get_balance(root)

        if balance > 1 and key < root.left.key: return self.rotate_right(root)
        if balance < -1 and key > root.right.key: return self.rotate_left(root)
        if balance > 1 and key > root.left.key:
            root.left = self.rotate_left(root.left)
            return self.rotate_right(root)
        if balance < -1 and key < root.right.key:
            root.right = self.rotate_right(root.right)
            return self.rotate_left(root)
        return root

    def get_min_value_node(self, node):
        if node is None or node.left is None: return node
        return self.get_min_value_node(node.left)

    def delete(self, root, key):
        if not root: return root
        if key < root.key:
            root.left = self.delete(root.left, key)
        elif key > root.key:
            root.right = self.delete(root.right, key)
        else:
            if root.left is None:
                temp = root.right
                root = None
                return temp
            elif root.right is None:
                temp = root.left
                root = None
                return temp
            temp = self.get_min_value_node(root.right)
            root.key = temp.key
            root.right = self.delete(root.right, temp.key)

        if root is None: return root

        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))

        balance = self.get_balance(root)

        if balance > 1 and self.get_balance(root.left) >= 0:
            return self.rotate_right(root)

        if balance > 1 and self.get_balance(root.left) < 0:
            root.left = self.rotate_left(root.left)
            return self.rotate_right(root)

        if balance < -1 and self.get_balance(root.right) <= 0:
            return self.rotate_left(root)

        if balance < -1 and self.get_balance(root.right) > 0:
            root.right = self.rotate_right(root.right)
            return self.rotate_left(root)
        
        return root

class AVLApp:
    def __init__(self, master):
        self.tree = AVLTree()
        self.root_node = None
        self.master = master
        self.master.title("AVL Tree Interactive")
        
        self.canvas = tk.Canvas(master, width=800, height=500, bg="white")
        self.canvas.pack()

        frame = tk.Frame(master)
        frame.pack(pady=10)

        self.entry = tk.Entry(frame)
        self.entry.pack(side=tk.LEFT, padx=5)

        tk.Button(frame, text="Thêm", command=self.add, bg="green", fg="white").pack(side=tk.LEFT)
        tk.Button(frame, text="Xóa", command=self.remove, bg="red", fg="white").pack(side=tk.LEFT, padx=5)

    def draw(self, node, x, y, step):
        if node:
            if node.left:
                self.canvas.create_line(x, y, x - step, y + 60)
                self.draw(node.left, x - step, y + 60, step / 2)
            if node.right:
                self.canvas.create_line(x, y, x + step, y + 60)
                self.draw(node.right, x + step, y + 60, step / 2)
            self.canvas.create_oval(x-20, y-20, x+20, y+20, fill="lightblue")
            self.canvas.create_text(x, y, text=str(node.key))

    def refresh(self):
        self.canvas.delete("all")
        self.draw(self.root_node, 400, 50, 200)

    def add(self):
        val = int(self.entry.get())
        self.root_node = self.tree.insert(self.root_node, val)
        self.refresh()

    def remove(self):
        val = int(self.entry.get())
        self.root_node = self.tree.delete(self.root_node, val)
        self.refresh()

if __name__ == "__main__":
    root = tk.Tk()
    app = AVLApp(root)
    root.mainloop()


# swon