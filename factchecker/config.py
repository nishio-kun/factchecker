class SystemConfig:
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{user}:{password}@{host}/{db_name}?charset=utf8'.format(**{
        'user': 'nishio',
        'password': 'passnishio',
        'host': 'localhost',
        'db_name': 'factchecker'
    })


Config = SystemConfig
