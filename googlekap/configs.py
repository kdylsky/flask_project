class Config:
    """Flask Config"""
    SECRET_KEY = "secretkey"
    SESSION_COOKIE_NAME = "googlekap_session"
    # docker container mysql에 연결하기
    SQLALCHEMY_DATABASE_URI = "mysql+mysqldb://root:password@0.0.0.0:3308/googlekap?charset=utf8"
    # 로컬 mysql에 연결하기
    #SQLALCHEMY_DATABASE_URI="mysql+pymysql://root:password@localhost:3306/googlekap?charset=utf8"
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    SWAGGER_UI_DOC_EXPANSION="list"

class DevelopmentConfig(Config):
    """Flask Config for Dev"""
    DEBUG = True
    SEND_FILE_MAX_AGE_DEFAULT = 1
    WTF_CSRF_ENABLED = False

class ProductionConfig(DevelopmentConfig):
    pass