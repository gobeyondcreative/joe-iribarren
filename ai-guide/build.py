from pathlib import Path
import markdown
p = Path(__file__).parent
body = markdown.markdown((p / 'content.md').read_text())
(p / 'index.html').write_text((p / 'template.html').read_text().replace('{{ content }}', body))
print('Built ai-guide/index.html')
