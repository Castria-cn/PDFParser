import tkinter as tk
from tkinter import ttk

DISPLAY_CHAR = 4

class ContentTree:
    tmp_id = 0
    details = {}
    """
    文档结构节点对象。
    title_id: 该节点的标题编号，如 '1.1'
    contents: List, 其元素或者为str(叶节点), 或者为ContentTree对象。
    """
    def __init__(self, title_id: str=''):
        """
        :param title_id: 该段内容的标题编号, 如 '1.1'
        """
        self.title_id = title_id
        self.contents = []
    def add(self, content):
        self.contents.append(content)
    
    def _insert(self, tree: ttk.Treeview, father: int):
        for item in self.contents:
            ContentTree.tmp_id += 1
            if type(item) == str:
                tree.insert(str(father), 'end', str(ContentTree.tmp_id), text=f'{item[:DISPLAY_CHAR]}...')
            elif type(item) == ContentTree:
                tree.insert(str(father), 'end', str(ContentTree.tmp_id), text=item.title_id)
                item._insert(tree, self.tmp_id)
    
    def show(self):
        ContentTree.tmp_id = 0
        root = tk.Tk()
        tree = ttk.Treeview(root)
        tree.insert('', 'end', '0', text='root')        
        self._insert(tree, 0)
        tree.pack()
        root.mainloop()