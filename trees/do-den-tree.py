import tkinter as tk
from tkinter import messagebox

class RBNode:
    def __init__(self, data, color="RED"):
        self.data = data
        self.color = color
        self.left = None
        self.right = None
        self.parent = None

class RedBlackTree:
    def __init__(self):
        self.NIL = RBNode(0, color="BLACK")
        self.root = self.NIL

    def rotate_left(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.NIL:
            y.left.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def rotate_right(self, x):
        y = x.left
        x.left = y.right
        if y.right != self.NIL:
            y.right.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

    def insert(self, key):
        new_node = RBNode(key)
        new_node.left = self.NIL
        new_node.right = self.NIL
        y = None
        x = self.root
        while x != self.NIL:
            y = x
            if new_node.data < x.data: x = x.left
            else: x = x.right
        new_node.parent = y
        if y is None: self.root = new_node
        elif new_node.data < y.data: y.left = new_node
        else: y.right = new_node
        new_node.color = "RED"
        self.fix_insert(new_node)

    def fix_insert(self, k):
        while k.parent and k.parent.color == "RED":
            if k.parent == k.parent.parent.left:
                u = k.parent.parent.right
                if u.color == "RED":
                    u.color = "BLACK"; k.parent.color = "BLACK"
                    k.parent.parent.color = "RED"; k = k.parent.parent
                else:
                    if k == k.parent.right:
                        k = k.parent; self.rotate_left(k)
                    k.parent.color = "BLACK"; k.parent.parent.color = "RED"
                    self.rotate_right(k.parent.parent)
            else:
                u = k.parent.parent.left
                if u.color == "RED":
                    u.color = "BLACK"; k.parent.color = "BLACK"
                    k.parent.parent.color = "RED"; k = k.parent.parent
                else:
                    if k == k.parent.left:
                        k = k.parent; self.rotate_right(k)
                    k.parent.color = "BLACK"; k.parent.parent.color = "RED"
                    self.rotate_left(k.parent.parent)
            if k == self.root: break
        self.root.color = "BLACK"

    def delete_node(self, data):
        self.delete_node_helper(self.root, data)

    def delete_node_helper(self, node, key):
        z = self.NIL
        while node != self.NIL:
            if node.data == key: z = node
            if node.data <= key: node = node.right
            else: node = node.left

        if z == self.NIL: return 

        y = z
        y_original_color = y.color
        if z.left == self.NIL:
            x = z.right
            self.rb_transplant(z, z.right)
        elif z.right == self.NIL:
            x = z.left
            self.rb_transplant(z, z.left)
        else:
            y = self.minimum(z.right)
            y_original_color = y.color
            x = y.right
            if y.parent == z: x.parent = y
            else:
                self.rb_transplant(y, y.right)
                y.right = z.right
                y.right.parent = y
            self.rb_transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color
        if y_original_color == "BLACK":
            self.fix_delete(x)

    def rb_transplant(self, u, v):
        if u.parent is None: self.root = v
        elif u == u.parent.left: u.parent.left = v
        else: u.parent.right = v
        v.parent = u.parent

    def fix_delete(self, x):
        while x != self.root and x.color == "BLACK":
            if x == x.parent.left:
                s = x.parent.right
                if s.color == "RED":
                    s.color = "BLACK"; x.parent.color = "RED"
                    self.rotate_left(x.parent); s = x.parent.right
                if s.left.color == "BLACK" and s.right.color == "BLACK":
                    s.color = "RED"; x = x.parent
                else:
                    if s.right.color == "BLACK":
                        s.left.color = "BLACK"; s.color = "RED"
                        self.rotate_right(s); s = x.parent.right
                    s.color = x.parent.color; x.parent.color = "BLACK"
                    s.right.color = "BLACK"; self.rotate_left(x.parent)
                    x = self.root
            else:
                s = x.parent.left
                if s.color == "RED":
                    s.color = "BLACK"; x.parent.color = "RED"
                    self.rotate_right(x.parent); s = x.parent.left
                if s.right.color == "BLACK" and s.left.color == "BLACK":
                    s.color = "RED"; x = x.parent
                else:
                    if s.left.color == "BLACK":
                        s.right.color = "BLACK"; s.color = "RED"
                        self.rotate_left(s); s = x.parent.left
                    s.color = x.parent.color; x.parent.color = "BLACK"
                    s.left.color = "BLACK"; self.rotate_right(x.parent)
                    x = self.root
        x.color = "BLACK"

    def minimum(self, node):
        while node.left != self.NIL: node = node.left
        return node

class App:
    def __init__(self, root):
        self.tree = RedBlackTree()
        self.root = root
        self.root.title("Red-Black Tree Full (Insert/Delete)")
        self.canvas = tk.Canvas(root, width=900, height=500, bg="#2c3e50")
        self.canvas.pack(pady=10)
        
        f = tk.Frame(root)
        f.pack()
        self.entry = tk.Entry(f, width=10, font=('Arial', 14))
        self.entry.pack(side=tk.LEFT, padx=10)
        
        tk.Button(f, text="Thêm", bg="green", fg="white", command=self.add).pack(side=tk.LEFT, padx=2)
        tk.Button(f, text="Xóa", bg="red", fg="white", command=self.delete).pack(side=tk.LEFT, padx=2)

    def draw(self, node, x, y, x_off):
        if node != self.tree.NIL:
            if node.left != self.tree.NIL:
                self.canvas.create_line(x, y, x-x_off, y+60, fill="white")
                self.draw(node.left, x-x_off, y+60, x_off/1.7)
            if node.right != self.tree.NIL:
                self.canvas.create_line(x, y, x+x_off, y+60, fill="white")
                self.draw(node.right, x+x_off, y+60, x_off/1.7)
            c = "#ff4757" if node.color == "RED" else "#000000"
            self.canvas.create_oval(x-18, y-18, x+18, y+18, fill=c, outline="white")
            self.canvas.create_text(x, y, text=str(node.data), fill="white")

    def add(self):
        self.tree.insert(int(self.entry.get()))
        self.update()

    def delete(self):
        self.tree.delete_node(int(self.entry.get()))
        self.update()

    def update(self):
        self.canvas.delete("all")
        self.draw(self.tree.root, 450, 40, 220)
        self.entry.delete(0, tk.END)

if __name__ == "__main__":
    r = tk.Tk()
    App(r)
    r.mainloop()

# swon