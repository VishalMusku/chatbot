import os
import glob
import re 
from pathlib import Path

def get_context():
    
    def get_most_recent_docx_file():
        downloads_folder = os.path.expanduser("~") + "/Downloads"  # Adjust the path for Windows if needed
        
        # List all .docx files in the Downloads folder
        docx_files = glob.glob(os.path.join(downloads_folder, "*.docx"))
        
        if not docx_files:
            return None  # No .docx files found
        
        # Get the most recently modified .docx file
        most_recent_docx = max(docx_files, key=os.path.getmtime)

        dir_name = os.path.dirname(most_recent_docx)
        base_name = os.path.basename(most_recent_docx)
        
        match = re.search(r'\(\d+\)', base_name)
        
        if match:
            new_base_name = re.sub(r'\(\d+\)', '', base_name)
        
        else:
            new_base_name = base_name

        # Combine the directory and new base name to form the new path
        new_path = os.path.join(dir_name, new_base_name)
        
        # Rename the file
        os.rename(most_recent_docx, new_path)


        return new_path
    

    return get_most_recent_docx_file()


get_context()
    
