import docx
from lxml import etree
import pandas as pd
import docx_path_finder
import os
from pathlib import Path

def extract_text_and_tables(docx_file, output_file_path):
    doc = docx.Document(docx_file)
    all_content_text = []
    
    for paragraph in doc.paragraphs:
        all_content_text.append((paragraph.text, paragraph._element))
    
    for i, table in enumerate(doc.tables):
        all_content_text.append((table, table._element))
    
    # Sort content based on the position in the document
    all_content_text.sort(key=lambda x: get_element_position(x[1]))
    
    li = {}
    
    for item in all_content_text:
        if isinstance(item[0], str):
            with open(output_file_path, 'a') as file:
                file.write(item[0] + '\n')
        else:
            df = convert_table_to_dataframe(item[0])
            table_dict_representation = convert_dataframe_to_dict(df)
            li[0] = table_dict_representation
            write_dicts_to_text_file(li, output_file_path)

def write_dicts_to_text_file(table_dicts, file_path):
    with open(file_path, 'a') as file:
        for table_index, table_dict in table_dicts.items():
            file.write(f"Below is a Dictionary representation of a Table. Each row represents a nested dictionary with keys as column name and values and cell value  :\n")
            for entry in table_dict:
                file.write(f"{entry}\n")
            file.write("\n")

def convert_table_to_dataframe(table):
    data = []
    for row in table.rows:
        row_data = [cell.text for cell in row.cells]
        data.append(row_data)
    df = pd.DataFrame(data[1:], columns=data[0])  # Assuming the first row contains column headers
    return df

def convert_dataframe_to_dict(df):
    dict_representation = df.to_dict(orient='records')
    return dict_representation

def get_element_position(element):
    """Get the position of the XML element in the document."""
    return int(element.xpath('count(./preceding::*)') + 1)

def main():
    docx_file_path = "{}".format(docx_path_finder.get_context())
    base_name = Path(os.path.basename(docx_file_path)).stem
    print('******',base_name)
    base_name=base_name+'2.txt'
    output_file_path = '{}'.format(base_name)

    try:
        extract_text_and_tables(docx_file_path, output_file_path)
    except Exception as e:
        print(f"Error: {e}")


