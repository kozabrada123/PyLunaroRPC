from rich.console import Console

appid = 970782366815641620
hotkey = 'o'

#Experinental auto mode, eliminates the need to press tab after the first time
#auto = True

ocr_solution = "tesseract"
#tesseract default, if you can't run / install tesseract replace with "easyocr"


tesseract_path = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

console = Console(color_system="auto",soft_wrap=True)

console.rule("LunaroRPC")