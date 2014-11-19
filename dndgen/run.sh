name=$1
python dndgen/converter.py ${name}
python dndgen/fill_pdf.py ${name}
pdftk dndgen/Interactive_DnD_4.0_Character_Sheet.pdf fill_form dndgen/data.fdf output dndgen/${name}.pdf flatten
python dndgen/gen.py ${name}
