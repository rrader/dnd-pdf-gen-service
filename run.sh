name=$1
python converter.py ${name}
python fill_pdf.py ${name}
pdftk Interactive_DnD_4.0_Character_Sheet.pdf fill_form data.fdf output ${name}.pdf flatten
python gen.py ${name}
