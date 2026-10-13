from html.parser import HTMLParser

with open("chapter3.html", "r", encoding="utf-8") as f:
    content = f.read()

VOID_TAGS = {"img", "br", "hr", "link", "meta", "input", "source", "area", "base", "col", "embed", "param", "track", "wbr"}

class FullHTMLValidator(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack = []
        self.errors = []
    def handle_starttag(self, tag, attrs):
        if tag.lower() in VOID_TAGS:
            return
        attrs_dict = dict(attrs)
        cls = attrs_dict.get("class", "")
        id_ = attrs_dict.get("id", "")
        info = f"{tag}" + (f".{cls}" if cls else "") + (f"#{id_}" if id_ else "")
        self.stack.append((tag, info, self.getpos()))
    def handle_endtag(self, tag):
        if tag.lower() in VOID_TAGS:
            return
        if not self.stack:
            self.errors.append(f"Unexpected end tag </{tag}> at line {self.getpos()[0]}")
            return
        for idx in range(len(self.stack)-1, -1, -1):
            if self.stack[idx][0] == tag:
                for unclosed in self.stack[idx+1:]:
                    self.errors.append(f"Unclosed <{unclosed[1]}> from line {unclosed[2][0]} before </{tag}> at line {self.getpos()[0]}")
                self.stack = self.stack[:idx]
                return
        self.errors.append(f"Unmatched end tag </{tag}> at line {self.getpos()[0]}")

val = FullHTMLValidator()
val.feed(content)

print(f"Total remaining unclosed tags: {len(val.stack)}")
for tag in val.stack:
    print(f"  Unclosed: {tag[1]} at line {tag[2][0]}")

print(f"Total tag errors: {len(val.errors)}")
for err in val.errors:
    print(f"  Error: {err}")
