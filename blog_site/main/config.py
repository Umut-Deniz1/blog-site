import os

class Config:
    SECRET_KEY = "c31a51da8800036c52 bc36f78b163c221"
    SQLALCHEMY_DATABASE_URI = "sqlite:///site.db"
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get("EMAIL_USER") 
    MAIL_PASSWORD = os.environ.get("EMAIL_PASS") 
