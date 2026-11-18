"""Render the short presenter guide. Requires ReportLab and Liberation Sans."""
from html import escape
from pathlib import Path
import re

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, KeepTogether

ROOT = Path(__file__).resolve().parents[1]
FONT_LOCATIONS = [Path('/usr/share/fonts/liberation-sans-fonts'),
                  Path('/usr/share/fonts/truetype/liberation2'),
                  Path('/usr/share/fonts/truetype/liberation')]
FONT_DIR = next((p for p in FONT_LOCATIONS if (p/'LiberationSans-Regular.ttf').exists()), None)
if FONT_DIR is None:
    raise SystemExit('Installer les polices Liberation Sans pour générer la fiche.')
for name, file in [('Guide', 'LiberationSans-Regular.ttf'), ('GuideBold', 'LiberationSans-Bold.ttf'),
                   ('GuideItalic', 'LiberationSans-Italic.ttf')]:
    pdfmetrics.registerFont(TTFont(name, str(FONT_DIR/file)))
pdfmetrics.registerFontFamily('Guide', normal='Guide', bold='GuideBold', italic='GuideItalic', boldItalic='GuideBold')

INK = colors.HexColor('#20262c')
MUTED = colors.HexColor('#53616c')
RED = colors.HexColor('#b52127')
LINK = colors.HexColor('#175d87')
STYLES = {
    'title': ParagraphStyle('title', fontName='GuideBold', fontSize=26, leading=29, textColor=INK, spaceAfter=15),
    'section': ParagraphStyle('section', fontName='GuideBold', fontSize=20, leading=25, textColor=INK, spaceAfter=13, keepWithNext=True),
    'subsection': ParagraphStyle('subsection', fontName='GuideBold', fontSize=12, leading=16, textColor=RED, spaceBefore=9, spaceAfter=5, keepWithNext=True),
    'body': ParagraphStyle('body', fontName='Guide', fontSize=10.5, leading=14.4, textColor=INK, spaceAfter=7, alignment=TA_LEFT),
    'bullet': ParagraphStyle('bullet', fontName='Guide', fontSize=10.5, leading=14.4, textColor=INK, leftIndent=10, firstLineIndent=-10, spaceAfter=6),
    'quote': ParagraphStyle('quote', fontName='Guide', fontSize=11, leading=16, textColor=INK, backColor=colors.HexColor('#f2f4f5'), borderPadding=12, spaceBefore=11, spaceAfter=15, leftIndent=12, rightIndent=12),
    'source': ParagraphStyle('source', fontName='Guide', fontSize=8.4, leading=11.5, textColor=MUTED, spaceBefore=7, spaceAfter=5),
}


def inline(text):
    text = escape(text)
    text = re.sub(r'\[([^\]]+)\]\((https?://[^)]+)\)',
                  lambda m: f'<link href="{m[2]}" color="{LINK.hexval()}">{m[1]}</link>', text)
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'`([^`]+)`', r'<font name="Guide">\1</font>', text)
    return text


def footer(canvas, doc):
    canvas.saveState()
    width, height = A4
    canvas.setFillColor(RED)
    canvas.rect(42, height-29, 30, 3, fill=1, stroke=0)
    canvas.setFillColor(MUTED)
    canvas.setFont('Guide', 8)
    canvas.drawString(80, height-28, 'OPENSHIFT AI 3.5  |  FICHE DE PRÉSENTATION')
    canvas.setStrokeColor(colors.HexColor('#d6dde1'))
    canvas.line(42, 35, width-42, 35)
    canvas.drawString(42, 22, 'Documentation officielle 3.5 et vérifications du 18 novembre 2026')
    canvas.drawRightString(width-42, 22, f'{doc.page} / 5')
    canvas.restoreState()


def main():
    source = ROOT/'docs/PRESENTER-OPENSHIFT-AI-3.5.md'
    destination = ROOT/'output/pdf/guide-presentation-openshift-ai-3.5.pdf'
    destination.parent.mkdir(parents=True, exist_ok=True)
    document = SimpleDocTemplate(str(destination), pagesize=A4, rightMargin=42, leftMargin=42,
                                 topMargin=49, bottomMargin=48,
                                 title='Présenter OpenShift AI 3.5 en 20 minutes',
                                 author='Démonstrations OpenShift AI', pageCompression=1)
    story = []
    pages = source.read_text().split('<!-- pagebreak -->')
    for number, page in enumerate(pages):
        if number:
            story.append(PageBreak())
        for block in re.split(r'\n\s*\n', page.strip()):
            if block.startswith('# '):
                style, text = 'title', block[2:]
            elif block.startswith('## '):
                style, text = 'section', block[3:]
            elif block.startswith('### '):
                style, text = 'subsection', block[4:]
            elif block.startswith('> '):
                style, text = 'quote', block[2:]
            elif block.startswith('- '):
                for line in block.splitlines():
                    story.append(Paragraph('• ' + inline(line[2:]), STYLES['bullet']))
                continue
            else:
                style = 'source' if block.startswith(('Références :', 'Les clics suivent')) else 'body'
                text = block
            story.append(Paragraph(inline(text.replace('\n', ' ')), STYLES[style]))
        story.append(Spacer(1, 1))
    document.build(story, onFirstPage=footer, onLaterPages=footer)
    print(destination)


if __name__ == '__main__':
    main()
