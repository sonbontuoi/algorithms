import tkinter as tk
from tkinter import messagebox

class BTreeNode:
    def __init__(self, leaf=False):
        self.leaf = leaf
        self.keys = []
        self.child = []

class BTree:
    def __init__(self, t):
        self.root = BTreeNode(True)
        self.t = t 

    def insert(self, k):
        root = self.root
        if len(root.keys) == (2 * self.t) - 1:
            temp = BTreeNode()
            self.root = temp
            temp.child.insert(0, root)
            self.split_child(temp, 0)
            self.insert_non_full(temp, k)
        else:
            self.insert_non_full(root, k)

    def insert_non_full(self, x, k):
        i = len(x.keys) - 1
        if x.leaf:
            x.keys.append(None)
            while i >= 0 and k < x.keys[i]:
                x.keys[i + 1] = x.keys[i]
                i -= 1
            x.keys[i + 1] = k
        else:
            while i >= 0 and k < x.keys[i]:
                i -= 1
            i += 1
            if len(x.child[i].keys) == (2 * self.t) - 1:
                self.split_child(x, i)
                if k > x.keys[i]:
                    i += 1
            self.insert_non_full(x.child[i], k)

    def split_child(self, x, i):
        t = self.t
        y = x.child[i]
        z = BTreeNode(y.leaf)
        x.child.insert(i + 1, z)
        x.keys.insert(i, y.keys[t - 1])
        z.keys = y.keys[t: (2 * t) - 1]
        y.keys = y.keys[0: t - 1]
        if not y.leaf:
            z.child = y.child[t: 2 * t]
            y.child = y.child[0: t]

    def delete(self, x, k):
        t = self.t
        i = 0
        while i < len(x.keys) and k > x.keys[i]:
            i += 1
        if i < len(x.keys) and x.keys[i] == k:
            if x.leaf:
                x.keys.pop(i)
            else:
                self.delete_internal_node(x, k, i)
        elif not x.leaf:
            self.delete_from_child(x, i, k)

    def delete_internal_node(self, x, k, i):
        t = self.t
        if len(x.child[i].keys) >= t:
            pre = self.get_predecessor(x.child[i])
            x.keys[i] = pre
            self.delete(x.child[i], pre)
        elif len(x.child[i+1].keys) >= t:
            suc = self.get_successor(x.child[i+1])
            x.keys[i] = suc
            self.delete(x.child[i+1], suc)
        else:
            self.merge(x, i)
            self.delete(x.child[i], k)

    def delete_from_child(self, x, i, k):
        t = self.t
        if len(x.child[i].keys) < t:
            if i != 0 and len(x.child[i-1].keys) >= t:
                self.borrow_from_prev(x, i)
            elif i != len(x.child) - 1 and len(x.child[i+1].keys) >= t:
                self.borrow_from_next(x, i)
            else:
                if i != len(x.child) - 1: self.merge(x, i)
                else: self.merge(x, i - 1); i -= 1
        self.delete(x.child[i], k)

    def borrow_from_prev(self, x, i):
        child = x.child[i]
        sibling = x.child[i-1]
        child.keys.insert(0, x.keys[i-1])
        x.keys[i-1] = sibling.keys.pop()
        if not child.leaf:
            child.child.insert(0, sibling.child.pop())

    def borrow_from_next(self, x, i):
        child = x.child[i]
        sibling = x.child[i+1]
        child.keys.append(x.keys[i])
        x.keys[i] = sibling.keys.pop(0)
        if not child.leaf:
            child.child.append(sibling.child.pop(0))

    def merge(self, x, i):
        child = x.child[i]
        sibling = x.child[i+1]
        child.keys.append(x.keys.pop(i))
        child.keys.extend(sibling.keys)
        if not child.leaf:
            child.child.extend(sibling.child)
        x.child.pop(i+1)
        if x == self.root and not x.keys:
            self.root = child

    def get_predecessor(self, x):
        while not x.leaf: x = x.child[-1]
        return x.keys[-1]

    def get_successor(self, x):
        while not x.leaf: x = x.child[0]
        return x.keys[0]

class BTreeApp:
    def __init__(self, master):
        self.tree = BTree(t=3)
        self.canvas = tk.Canvas(master, width=1000, height=500, bg="white")
        self.canvas.pack()
        f = tk.Frame(master); f.pack()
        self.e = tk.Entry(f); self.e.pack(side=tk.LEFT)
        tk.Button(f, text="Thêm", command=self.add).pack(side=tk.LEFT)
        tk.Button(f, text="Xóa", command=self.remove).pack(side=tk.LEFT)

    def draw(self, node, x, y, step):
        if node:
            w = len(node.keys) * 30
            self.canvas.create_rectangle(x-w/2, y-15, x+w/2, y+15, fill="#ffeaa7")
            for i, k in enumerate(node.keys):
                self.canvas.create_text(x-w/2 + i*30 + 15, y, text=str(k))
                if i < len(node.keys) - 1:
                    self.canvas.create_line(x-w/2 + (i+1)*30, y-15, x-w/2 + (i+1)*30, y+15)
            
            if not node.leaf:
                num_child = len(node.child)
                for i, child in enumerate(node.child):
                    cx = x - step/2 + (i * step / (num_child-1 if num_child>1 else 1))
                    self.canvas.create_line(x, y+15, cx, y+60)
                    self.draw(child, cx, y+60, step/2.5)

    def add(self):
        self.tree.insert(int(self.e.get())); self.update()
    def remove(self):
        self.tree.delete(self.tree.root, int(self.e.get())); self.update()
    def update(self):
        self.canvas.delete("all"); self.draw(self.tree.root, 500, 40, 450); self.e.delete(0, 'end')

if __name__ == "__main__":
    root = tk.Tk(); BTreeApp(root); root.mainloop()

# swon