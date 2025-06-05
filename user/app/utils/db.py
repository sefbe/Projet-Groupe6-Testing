# import pymysql
# from app.config import Config

# def get_db_connection():
#     connection = pymysql.connect(
#         host=Config.MYSQL_HOST,
#         user=Config.MYSQL_USER,
#         password=Config.MYSQL_PASSWORD,
#         database=Config.MYSQL_DB,
#         port=Config.MYSQL_PORT,
#         cursorclass=pymysql.cursors.DictCursor
#     )
#     return connection