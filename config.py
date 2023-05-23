import os
import re

id_pattern = re.compile(r'^.\d+$')


class Config:
    API_ID = int(os.environ.get("API_ID", "26784866"))
    ADMINS = [int(admin) if id_pattern.search(admin) else admin for admin in os.environ.get(
        'ADMINS', '6069226956 1288398723').split()]
    API_HASH = os.environ.get("API_HASH", "5078bf823d7e8248776f5230ffc26a09")
    DB_URL = os.environ.get(
        "DB_URL", )
    DB_NAME = os.environ.get("DB_NAME", "FO21664C08986")
    BOT_TOKEN = os.environ.get(
        "BOT_TOKEN", "5820214092:AAGKU17Ww8g34euND-rvL4PnTnos0TyfCsU")
    DOWNLOAD_LOCATION = os.environ.get("DOWNLOAD_LOCATION", "./DOWNLOADS")
    USER_SESSION_STRING = os.environ.get("USER_SESSION_STRING", "BQCgG9Ct8sWBosee6pom20tI60kbJH9hoQ9hYzZdiJIL0DekKS5H_ZRzQzBAbJJLb0wj_XKE6BS86_FPDTobWYZPwrrcDCvIQBiGemR_Q74YXaXTJ6xXT04-I6PjMJa2fVnt0slE9NdZ0YHRJbPFal9V51LFyPdyl-HJryuG8UJeYnmQj9H9MGpvHZgXYfP-anfFWwgjgSXLEwtv8TyezvEDiDSrnlvsfL1YGMfyq5O7MlVqozrS7f57bsplNYjHTFO06uGHt8pfcsEp-RX8mMe69D4CMV9-Pkdv21cvlh24EaqIIghL-qhEXjg3fFPkTd8T0bcI4u9teP2hUrFcbJQLAAAAAWnBDcwA")
    LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", "-1001501263659"))
