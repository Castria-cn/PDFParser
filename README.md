# 安装
```bash
pip install -r requirements.txt
```
# 使用
`PDFParser.py`:
```python
parser = PDFParser('./data/sample.pdf')
root = parser.parse() # 返回一个structure.ContentTree.ContentTree对象
root.show() # 可视化
```
## ContentTree
类有两个属性：`title_id`和`contents`.`title_id`是该段落的标号(`1.`、`二、`等)；`contents`是一个`list`,每个元素或者是递归的`ContentTree`对象，或者是表示该段落为最小段落的`str`.
## 规则扩充
为`pattern.Pattern.Pattern`增加子类即可。子类需要重写两个方法`mode`和`next_title`:
```python
@abstractmethod
def mode(self) -> str:
    """
    应当返回该模式的正则字符串。如r'\d\.'
    """
    pass 

@abstractmethod
def next_title(self, title: str) -> str:
    """
    应当返回该模式下，给定 title 时的下一个标题。可以以 str 形式或 List[str]形式返回，
    如next_title('1.') -> '2.' 或 next_title('1.') -> ['2.', '2．'] (对应英文实心点和中文实心点)
    """
    pass
```