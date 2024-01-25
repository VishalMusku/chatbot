import pdfplumber

def extract_text_save_to_file(pdf_path, output_file_path):
    """
    :param pdf_path: Path to the PDF file.
    :param output_file_path: Path where the extracted text will be saved.
    """
    with pdfplumber.open(pdf_path) as pdf:
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            for page in pdf.pages:
                # Extract text
                text = page.extract_text()
                if text:
                    output_file.write(text + "\n")
                
                # Extract tables
                tables = page.extract_tables()
                for table in tables:
                    for row in table:
                        # Convert each cell to string and handle None values
                        row = [str(cell) if cell is not None else '' for cell in row]
                        output_file.write(' | '.join(row) + '\n')
                    output_file.write('\n\n')
