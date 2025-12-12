from pypdf import PdfReader


def pdf_to_text_file(file_path, output_path):
    reader = PdfReader(file_path)
    with open(output_path, "w", encoding="utf-8") as output_file:
        for page in reader.pages:
            text = page.extract_text()
            if text:
                output_file.write(text)
    print("Text successfully saved to", output_path)


#pdf_to_text_file("PDF/ManCalledOve.pdf", "B2_C1/ManCalledOve.txt")
#pdf_to_text_file("PDF/CatchingFire.pdf", "B1_B2/CatchingFire.txt")
#pdf_to_text_file("PDF/Mockingjay.pdf", "B1_B2/Mockingjay.txt")
pdf_to_text_file("PDF/HarryPotter3.pdf", "B1_B2/HarryPotter3.txt")

