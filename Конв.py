import os
import re
import fitz  
from PIL import Image, ImageStat
from io import BytesIO
from PyPDF2 import PdfWriter, PdfReader
def is_image_blank(pil_image, threshold=13):
    grayscale = pil_image.convert("L")
    stat = ImageStat.Stat(grayscale)
    return stat.stddev[0] < threshold
def get_sorted_pdf_files():
    pdfs = [f for f in os.listdir('.') if f.lower().endswith('.pdf')]
    def extract_num(name):
        m = re.match(r'(\d+)\.pdf$', name)
        return int(m.group(1)) if m else float('inf')
    return sorted(pdfs, key=extract_num)
def merge(output='документ.pdf'):
    writer = PdfWriter()
    pdf_files = get_sorted_pdf_files()

    for pdf_file in pdf_files:
        doc = fitz.open(pdf_file)
        print(f"Обработка {pdf_file} с {doc.page_count} страницами")

        reader = PdfReader(pdf_file) 

        for i in range(doc.page_count):
            page = doc.load_page(i)
            
            pix = page.get_pixmap()
            img = Image.open(BytesIO(pix.tobytes(output="png")))

            if is_image_blank(img):
                print(f" - Пропуск страницы {i+1}")
                continue

            
            writer.add_page(reader.pages[i])

    with open(output, 'wb') as f_out:
        writer.write(f_out)

    print(f"Все! Сохранено как {output}, нашмите на Enter чтобы закрыть")
    input()
print("Конвертрон версия 1.2  И.А.А  Я.М.М. и  А.А.Р.  2025")
merge()
