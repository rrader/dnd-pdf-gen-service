import json
import os
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4, landscape, portrait
from reportlab.lib.units import cm, mm, inch, pica
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle, BaseDocTemplate, Frame, \
    PageTemplate, KeepTogether, flowables
from reportlab.lib import colors
import sys
try:
    from dndgen.converter import POWERS, get_power_info, get_weapon_info
except ImportError:
    from converter import POWERS, get_power_info, get_weapon_info


def gen(data, output):
    style = getSampleStyleSheet()
    headlineStyle = style["Heading2"]
    simple_paragraph = style["Normal"]
    # simple_paragraph.spaceAfter = inch * .04
    simple_paragraph.borderPadding = inch * .02
    simple_paragraph.alignment = TA_JUSTIFY
    highlighted_paragraph = simple_paragraph.clone("Highlighted")
    highlighted_paragraph.backColor = colors.toColor("#CCFF99")
    highlighted_paragraph.spaceAfter = inch * .02

    highlighted_paragraph2 = simple_paragraph.clone("Highlighted2")
    highlighted_paragraph2.backColor = colors.toColor("#CC9999")
    highlighted_paragraph2.spaceBefore = inch * .02

    powerHeader = style["Normal"].clone("PowerHeader")
    powerHeader.alignment = TA_JUSTIFY
    powerHeader.borderPadding = inch * .02
    powerHeader.textColor = colors.white
    # powerHeader.fontName = "Helvetica-Bold"
    powerHeader.fontSize = 9
    atwillHeader = powerHeader.clone("atWillHeader")
    atwillHeader.backColor = colors.toColor("#649769")

    encounterHeader = powerHeader.clone("encounterHeader")
    encounterHeader.backColor = colors.toColor("#981332")

    dailyHeader = powerHeader.clone("dailyHeader")
    dailyHeader.backColor = colors.toColor("#4C4C4E")

    utilityHeader = powerHeader.clone("utilityHeader")
    utilityHeader.backColor = colors.toColor("#336699")
    all_blocks = []
    # for i in range(5):
    #     headline = Paragraph("Hello world %d" % i, headlineStyle)
    #     blocks.append(headline)
    #     text = Paragraph(
    #         "I’ve added a content-disposition header. Instead of attachment, as you normally put into content-disposition, I’ve specified that the file should be displayed normally (which on some browsers will still be as an attachment if they don’t have the capability to inline-view PDF files). But by giving it a filename, if they do save the PDF they should get that as the default filename for the file.",
    #         paraStyle)
    #     blocks.append(text)
    tp_info = {
        'at-will': {
            'style': atwillHeader
        },
        'encounter': {
            'style': encounterHeader
        },
        'daily': {
            'style': dailyHeader
        },
        'utility': {
            'style': utilityHeader
        }
    }
    for tp_item in ['at-will', 'encounter', 'daily', 'utility']:
        for item in filter(None, data[tp_item]):
            tp = tp_item
            if tp == 'utility':
                if not item[0]:
                    continue
                tp = item[1]
                item = item[0]
            blocks = []
            blocks.append(flowables.HRFlowable(color=colors.black, spaceBefore=0, spaceAfter=2, width="100%", thickness=2))
            info = get_power_info(item)
            info['c'] = data
            info['attack_val'] = data.get(info["attack"].lower()+"_attack") or ["[no]", "[no]"]
            text = Paragraph("<b>{name}</b><br />{title}".format(**info), tp_info[tp_item]['style'])
            blocks.append(text)
            text = Paragraph(
                        """<u>{tp}</u><br />
                        <b>{action} Action</b> --- <b>Range:</b> {range}<br />
                        <b>Target:</b> {target}<br />
                        """.format(tp=tp.capitalize(), **info), simple_paragraph)
            blocks.append(text)
            if info['is_weapon'] == "yes":
                if info["attack"] != "trigger":
                    text = Paragraph("""
                                     <b>Attack:</b> {attack} vs. {vs} [{attack_val[0]}] =<br/>= {attack_val[1]}
                                     """.format(**info), highlighted_paragraph)
                    blocks.append(text)
                weapons = [w[0].strip() for w in data["Attacks"] if w[0] and get_weapon_info(w[0])["range"] in info["range"].split(';')]
                for weapon in weapons:
                    d = get_weapon_info(weapon)
                    d.update(info)
                    hit = info["hit"].format(**d)
                    text = Paragraph(
                                    """
                                    <b>Hit w/ {weapon}:</b> {hit}
                                    """.format(weapon=weapon, hit=hit), highlighted_paragraph2)
                    blocks.append(text)
                if info["hit_comment"]:
                    text = Paragraph(info["hit_comment"].format(**info), highlighted_paragraph2)
                    blocks.append(text)
                if not weapons:
                    hit = info["hit"].format(**info)
                    text = Paragraph(
                                    """
                                    <b>Hit:</b> {hit}
                                    """.format(hit=hit), highlighted_paragraph2)
                    blocks.append(text)
            if info["comment"]:
                text = Paragraph(info["comment"].format(**info), simple_paragraph)
                blocks.append(text)
            blocks.append(flowables.HRFlowable(color=colors.black, spaceBefore=0, spaceAfter=2, width="100%", thickness=2))
            blocks.append(flowables.HRFlowable(color=colors.white, spaceBefore=0, spaceAfter=0, width="100%", thickness=3))
            block = KeepTogether(blocks)
            block.style = highlighted_paragraph2
            all_blocks.append(block)

    doc = BaseDocTemplate(output, pagesize=portrait(A4),
                          leftMargin=1.5*cm, rightMargin=1.5*cm,
                          topMargin=1.5*cm, bottomMargin=1.5*cm)
    frame_count = 2
    frame_width = doc.width / frame_count
    frame_height = doc.height - .05 * inch
    frames = []

    for frame in range(frame_count):
        left_margin = doc.leftMargin + frame * frame_width
        column = Frame(left_margin, doc.bottomMargin, frame_width, frame_height)
        frames.append(column)

    template = PageTemplate(frames=frames)
    doc.addPageTemplates(template)
    doc.build(all_blocks)


if __name__ == "__main__":
    data = json.load(open(os.path.join("dndgen/Characters", sys.argv[1]+'.json')))
    gen(data, "dndgen/" + sys.argv[1] + "_Powers.pdf")
