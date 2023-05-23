import os
import re

id_pattern = re.compile(r'^.\d+$')


class Config:
    API_ID = int(os.environ.get("API_ID", "26784866"))
    ADMINS = [int(admin) if id_pattern.search(admin) else admin for admin in os.environ.get(
        'ADMINS', '6069226956 1288398723').split()]
    API_HASH = os.environ.get("API_HASH", "5078bf823d7e8248776f5230ffc26a09")
    DB_URL = os.environ.get(
        "DB_URL", "mongodb+srv://uvew:xyz@cluster0.qnsajle.mongodb.net/?retryWrites=true&w=majority")
    DB_NAME = os.environ.get("DB_NAME", "FO21664C08986")
    BOT_TOKEN = os.environ.get(
        "BOT_TOKEN", "5820214092:AAGKU17Ww8g34euND-rvL4PnTnos0TyfCsU")
    DOWNLOAD_LOCATION = os.environ.get("DOWNLOAD_LOCATION", "./DOWNLOADS")
    USER_SESSION_STRING = os.environ.get("USER_SESSION_STRING", "BQCdyCKGh1iAMXPHlUWunlzBZPLt5wlOBtqR_lBO3HKqekSuI95NpZGUdkAQm3NLf9lBDQXvQbyaIhZNbMCLj_6eM33Xdk1RDIGMfCiF_QTCZsp4Fcg-9bTZbrcSOVMXeqomvuiTVngqtOF3CSlG4LsKAg2Vyn3tNUCe1225KTHb2-55urAdi5AC45Q8C-7Cy4oVk3uppwP7qWo8OjFHoW1SoK3DGcWIFWMBDPRGukmlmh7fxj71L_yAHUYxVx2qNqIBJNtd5k1urVxShEYf87kamPxSKf3ge6dnmP_r4qKm3-tQjmDdMxjIoALpPnpTgEiSJIUR3I9WW_ps0c0FUGfgAAAAAWnBDcwA")
    LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", "-1001501263659"))
