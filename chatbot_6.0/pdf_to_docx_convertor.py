import time
from pynput.keyboard import Controller as KeyboardController, Key
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def pdf_to_docx(pdf_file_path):
    
    # Step 1: Replace 'your_file_path.pdf' with the actual path to your PDF file
    
    # Step 2: Open the browser and go to the specified webpage

    driver = webdriver.Chrome()
    driver.get("https://www.ilovepdf.com/pdf_to_word")

    try:
        # Step 3: Wait for the 'Select PDF File' button to be clickable
        select_pdf_button_class = "uploader__btn"
        select_pdf_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, select_pdf_button_class)))
        select_pdf_button.click()

        # Step 4: Wait for the dialog to open
        time.sleep(3)

        # Step 5: Use pynput to type the file path and press Enter
        keyboard = KeyboardController()

        keyboard = KeyboardController()
        for char in pdf_file_path:
            keyboard.press(char)
            keyboard.release(char)
            time.sleep(0.1)
        
        time.sleep(7)  # Wait to ensure the path is fully entered
        
        keyboard.press(Key.enter)  # Press Enter
        keyboard.release(Key.enter)


        time.sleep(10)
        
        keyboard.press(Key.enter)  # Press Enter
        keyboard.release(Key.enter)
        
        time.sleep(10)
        
        # Step 6: Wait for the upload to complete
        WebDriverWait(driver, 60).until(EC.invisibility_of_element_located((By.CLASS_NAME, 'progress-bar')))
        
        time.sleep(10)
        
        convert_button_class = "btn--process"
        convert_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, convert_button_class)))
        convert_button.click()
        
        time.sleep(10)
        
        
        download_button_class = "downloader__btn"
        download_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, download_button_class)))
        download_button.click()
        
        time.sleep(10)
    
    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        driver.quit()



    