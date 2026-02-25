import tkinter as tk

class Node234:
    def __init__(self, leaf=True):
        self.leaf = leaf
        self.keys = []
        self.child = []

class Tree234:
    def __init__(self):
        self.root = Node234()

    def insert(self, key):
        if key in self._get_all_keys(self.root): return
        if len(self.root.keys) == 3:
            new_root = Node234(False)
            new_root.child.append(self.root)
            self._split_child(new_root, 0)
            self.root = new_root
        self._insert_non_full(self.root, key)

    def _split_child(self, parent, i):
        node = parent.child[i]
        new_node = Node234(node.leaf)
        parent.keys.insert(i, node.keys[1])
        parent.child.insert(i + 1, new_node)
        new_node.keys = [node.keys[2]]
        node.keys = [node.keys[0]]
        if not node.leaf:
            new_node.child = node.child[2:]
            node.child = node.child[:2]

    def _insert_non_full(self, node, key):
        i = len(node.keys) - 1
        if node.leaf:
            node.keys.append(None)
            while i >= 0 and key < node.keys[i]:
                node.keys[i+1] = node.keys[i]
                i -= 1
            node.keys[i+1] = key
        else:
            while i >= 0 and key < node.keys[i]: i -= 1
            i += 1
            if len(node.child[i].keys) == 3:
                self._split_child(node, i)
                if key > node.keys[i]: i += 1
            self._insert_non_full(node.child[i], key)

    def delete(self, key):
        if key not in self._get_all_keys(self.root): return
        self._delete_recursive(self.root, key)
        if len(self.root.keys) == 0 and not self.root.leaf:
            self.root = self.root.child[0]

    def _delete_recursive(self, node, key):
        i = 0
        while i < len(node.keys) and key > node.keys[i]: i += 1
        if i < len(node.keys) and node.keys[i] == key:
            if node.leaf:
                node.keys.pop(i) 
            else:
                self._delete_from_internal(node, i)
        elif not node.leaf:
            if len(node.child[i].keys) < 2:
                self._prepare_child(node, i)
                if i > len(node.keys): i = len(node.keys)
                elif i < len(node.keys) and key > node.keys[i]: i += 1
            self._delete_recursive(node.child[i], key)

    def _delete_from_internal(self, node, i):
        key = node.keys[i]
        if len(node.child[i].keys) >= 2:
            pred = self._get_pred(node.child[i])
            node.keys[i] = pred
            self._delete_recursive(node.child[i], pred)
        elif len(node.child[i+1].keys) >= 2:
            succ = self._get_succ(node.child[i+1])
            node.keys[i] = succ
            self._delete_recursive(node.child[i+1], succ)
        else:
            self._merge(node, i)
            self._delete_recursive(node.child[i], key)

    def _prepare_child(self, parent, i):
        if i > 0 and len(parent.child[i-1].keys) >= 2:
            child, sib = parent.child[i], parent.child[i-1]
            child.keys.insert(0, parent.keys[i-1])
            parent.keys[i-1] = sib.keys.pop()
            if not child.leaf: child.child.insert(0, sib.child.pop())
        elif i < len(parent.child)-1 and len(parent.child[i+1].keys) >= 2:
            child, sib = parent.child[i], parent.child[i+1]
            child.keys.append(parent.keys[i])
            parent.keys[i] = sib.keys.pop(0)
            if not child.leaf: child.child.append(sib.child.pop(0))
        else:
            if i < len(parent.keys): self._merge(parent, i)
            else: self._merge(parent, i-1)

    def _merge(self, parent, i):
        left, right = parent.child[i], parent.child[i+1]
        mid_key = parent.keys.pop(i)
        left.keys.extend([mid_key] + right.keys)
        if not left.leaf: left.child.extend(right.child)
        parent.child.pop(i+1)

    def _get_pred(self, node):
        while not node.leaf: node = node.child[-1]
        return node.keys[-1]

    def _get_succ(self, node):
        while not node.leaf: node = node.child[0]
        return node.keys[0]

    def _get_all_keys(self, node):
        res = list(node.keys)
        for c in node.child: res.extend(self._get_all_keys(c))
        return res
-
class App234:
    def __init__(self, win):
        self.tree = Tree234()
        win.title("2-3-4 Tree Fixed")
        self.canvas = tk.Canvas(win, width=1000, height=450, bg="white")
        self.canvas.pack()
        f = tk.Frame(win); f.pack()
        self.e = tk.Entry(f, width=10); self.e.pack(side=tk.LEFT, padx=10)
        tk.Button(f, text="Thêm", command=self.add, bg="green", fg="white").pack(side=tk.LEFT)
        tk.Button(f, text="Xóa", command=self.remove, bg="red", fg="white").pack(side=tk.LEFT, padx=5)

    def draw(self, node, x, y, dx):
        if node:
            w = len(node.keys) * 40
            self.canvas.create_rectangle(x-w/2, y-15, x+w/2, y+15, fill="#34495e")
            for i, k in enumerate(node.keys):
                self.canvas.create_text(x-w/2 + i*40 + 20, y, text=str(k), fill="white")
            if not node.leaf:
                for i, child in enumerate(node.child):
                    cx = x - dx + (i * (2*dx) / (len(node.child)-1))
                    self.canvas.create_line(x, y+15, cx, y+50)
                    self.draw(child, cx, y+50, dx/2.2)

    def add(self):
        try:
            self.tree.insert(int(self.e.get()))
            self.update_c()
        except: pass

    def remove(self):
        try:
            self.tree.delete(int(self.e.get()))
            self.update_c()
        except: pass

    def update_c(self):
        self.canvas.delete("all")
        self.draw(self.tree.root, 500, 40, 300)
        self.e.delete(0, 'end')

if __name__ == "__main__":
    root = tk.Tk()
    App234(root)
    root.mainloop()

# swon