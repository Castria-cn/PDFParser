import re
import os
import pdfplumber
from pattern.Pattern import Pattern
from structure.ContentTree import ContentTree

class PDFParser:
    def __init__(self, filepath: str) -> None:
        self.filepath = filepath
        self.reader = pdfplumber.open(filepath)
        self.page_num = len(self.reader.pages)
        self.pages = self.reader.pages
        self.patterns = [pattern() for pattern in Pattern.subpatterns]
    
    def _first_title(self, content: str):
        """
        给定 content, 返回其中出现的第一个标题对应的下标(start, end)以及对应的模式对象 pattern, 左闭右开.
        若无法找到下标, 返回(None, None, None).
        """
        rstart = len(content)
        for pattern in self.patterns:
            match = re.search(pattern.mode(), content)
            if match:
                start, end = match.start(), match.end()
                if start < rstart:
                    rstart, rend, rpattern = start, end, pattern
        if rstart != len(content):
            return rstart, rend, rpattern
        return None, None, None

    def _next_title(self, content: str, title_id: str, pattern: Pattern, offset: int=0):
        """
        给定content， 找到title_id在其中对应的下一个同级标题。如:
        _next_title('2. xxx...', '1.', pattern) -> (0, 2)
        若无法找到下标, 返回(None, None).
        """
        next_title = pattern.next_title(title_id)
        if type(next_title) == str:
            start = content.find(next_title)
        elif type(next_title) == list:
            indices = [content.find(title) for title in next_title]
            start = len(content)
            for idx in indices:
                if idx >= 0 and idx < start:
                    start = idx
        if start == -1 or start == len(content):
            return None, None
        end = start + len(next_title)
        return (start + offset, end + offset)

    def _parse_str(self, content: str, title_id: str='') -> ContentTree:
        root = ContentTree(title_id)
        
        start, end, pattern = self._first_title(content)
        if start == None:
            root.contents.append(content.strip())
            return root

        # parse paragraph beginning
        beginning = content[:start].strip()
        if len(beginning):
            beginning = self._parse_str(beginning)
            root.contents.append(beginning)
        
        # parse subparagraphs
        while start != None:
            tid = content[start: end]
            rest = content[end:]
            next_start, next_end = self._next_title(rest, tid, pattern, offset=end)
            if next_start != None:
                subparagraph = self._parse_str(content[end: next_start], title_id=content[start: end])
                root.contents.append(subparagraph)
            else:
                subparagraph = self._parse_str(content[end:], title_id=content[start: end])
                root.contents.append(subparagraph)
            start, end = next_start, next_end

        return root
    def postprocess(self, root: ContentTree):
        if len(root.contents) == 1 and type(root.contents[0]) == str and len(root.title_id) == 0:
            return root.contents[0]
        for i in range(len(root.contents)):
            if type(root.contents[i]) == str:
                continue
            root.contents[i] = self.postprocess(root.contents[i])
        
        return root
    def parse(self, start=0, end=-1) -> ContentTree:
        """
        解析 [start, end] 页.
        :param start: 起始页，从0开始.
        :param end: 终止页，若end=-1, 则为最后一页.
        """
        assert end == -1 or start <= end
        end = (self.page_num - 1) if end == -1 else end

        content = '\n'.join([page.extract_text() for page in self.pages[start:end+1]])
        print(content)

        result = self._parse_str(content, title_id='root')

        result = self.postprocess(result)

        return result

if __name__ == '__main__':
    parser = PDFParser('./data/sample2.pdf')
    root = parser.parse(end=0)
    root.show()