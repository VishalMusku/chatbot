import os
import glob


def get_context():
    
    def get_most_recent_docx_file():
        downloads_folder = os.path.expanduser("~") + "/Downloads"  # Adjust the path for Windows if needed
        
        # List all .docx files in the Downloads folder
        docx_files = glob.glob(os.path.join(downloads_folder, "*.docx"))
        
        if not docx_files:
            return None  # No .docx files found
        
        # Get the most recently modified .docx file
        most_recent_docx = max(docx_files, key=os.path.getmtime)
        
        return most_recent_docx

    def rename_to_context(docx_file):
        new_name = os.path.join(os.path.dirname(docx_file), "context.docx")
        os.rename(docx_file, new_name)
        return str(new_name)


    return rename_to_context(get_most_recent_docx_file())

get_context()
    

