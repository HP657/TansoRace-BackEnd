from Modules.Module_Basic import *
from Utils.Util_Env import get_env


envValue = get_env()


class check_SQL:
    def get_mysql():
        try:
            db = pymysql.connect(
                host=envValue.get("MYSQL_HOST"),
                user=envValue.get("MYSQL_USER"),
                password=envValue.get("MYSQL_PASSWORD"),
                db=envValue.get("MYSQL_DB"),
                charset="utf8",
            )
            SQL = db.cursor()
            return db, SQL
        except Exception as e:
            print(e)
            return False, False


class globalSQLController:
    def getPw(user_id: str):
        db, SQL = check_SQL.get_mysql()
        if not db:
            return False
        try:
            SQL.execute(f"SELECT user_pw FROM users WHERE user_id = '{user_id}'")
            result = SQL.fetchone()[0]
            return result

        except Exception as e:
            return False
    
    def getUserName(user_id: str):
        db, SQL = check_SQL.get_mysql()
        if not db: return False
        try:
            SQL.execute(f"SELECT user_name FROM users WHERE user_id = '{user_id}'")
            result = SQL.fetchone()[0]
            return result

        except Exception as e:
            return False
    
    def getUserType(user_id: str):
        db, SQL = check_SQL.get_mysql()
        if not db: return False
        try:
            SQL.execute(f"SELECT user_type FROM users WHERE user_id = '{user_id}'")
            result = SQL.fetchone()[0]
            return result

        except Exception as e:
            return False


class authSQLController:
    def checkUserData(user_id: str, user_pw: str):
        db, SQL = check_SQL.get_mysql()  # MySQL 데이터베이스 연결 설정
        if not db:
            return 500, "DB 연결이 불안정 합니다."
        
        _result = globalSQLController.getPw(user_id)  # 주어진 user_id에 해당하는 비밀번호 해시 값 가져오기
        if isinstance(_result, str):
            _result = _result.encode("UTF-8")

        pwResult = bcrypt.checkpw(user_pw.encode("UTF-8"), _result)  # 입력된 비밀번호와 해시 값 비교
        return 200, {"pwResult": pwResult}  # 성공 시 상태 코드 200과 결과 반환


    def insertUserData(userInsertData):
        db, SQL = check_SQL.get_mysql()
        if db == False:
            return 500, "DB 연결이 불안정 합니다."

        try:
            password = (bcrypt.hashpw(userInsertData.user_pw.encode("UTF-8"), bcrypt.gensalt().decode())).decode("utf-8")
            SQL.execute(f"INSERT INTO users(user_id, role_type, user_pw, user_name, user_type, user_role, user_code, create_at) VALUES('{userInsertData.user_id}', '{userInsertData.role_type}', '{password}', '{userInsertData.user_name}', '{userInsertData.user_type}', '{userInsertData.user_role}', '{userInsertData.user_code}', '{datetime.now()}')")
            db.commit()
            return 200, "유저 데이터가 정상적으로 생성 되었습니다."

        except Exception as e:
            print(e)
            return 500, e

    def getUserData(user_id):
        db, SQL = check_SQL.get_mysql()
        if db == False:
            return 500, "DB 연결이 불안정 합니다."

        try:
            SQL.execute(
                f"SELECT user_id, role_type, user_name, user_type, user_role, user_code, point, create_at FROM users WHERE user_id = '{user_id}'"
            )
            users = SQL.fetchone()
            return 200, {
                "user_id":   users[0],
                "role_type": users[1],
                "user_name": users[2],
                "user_type": users[3],
                "user_role": users[4],
                "user_code": users[5],
                "point":     users[6],
                "create_at": str(users[7]),
            }

        except Exception as e:
            print(e)
            return 500, e

    def deleteUserData(user_id):
        db, SQL = check_SQL.get_mysql()
        if db == False:
            return 500, "DB 연결이 불안정 합니다."

        try:
            SQL.execute(f"DELETE FROM users WHERE user_id = '{user_id}'")
            db.commit()
            return 200, user_id

        except Exception as e:
            print(e)
            return 500, e

    def getUsersData():
        db, SQL = check_SQL.get_mysql()
        resultUserData = []
        if db == False:
            return 500, "DB 연결이 불안정 합니다."

        try:
            SQL.execute(
                f"SELECT user_id, role_type, user_name, user_type, user_role, user_code, point, create_at FROM users"
            )
            users = SQL.fetchall()
            for user in users:
                resultUserData.append(
                    {
                        user[0]: {
                            "user_id":   user[0],
                            "role_type": user[1],
                            "user_name": user[2],
                            "user_type": user[3],
                            "user_role": user[4],
                            "user_code": user[5],
                            "point":     user[6],
                            "create_at": user[7],
                        }
                    }
                )
            return 200, resultUserData

        except Exception as e:
            print(e)
            return 500, e


class pointSQLController:
    def getUserPoint(user_id):
        db, SQL = check_SQL.get_mysql()
        if db == False:
            return 500, "DB 연결이 불안정 합니다."

        try:
            SQL.execute(f"SELECT user_id, point FROM users WHERE user_id = '{user_id}'")
            users = SQL.fetchone()
            return 200, {
                "user_id":   users[0],
                "point":     users[1],
            }

        except Exception as e:
            return 500, e
    

    def updateUserPoint(input_type, user_id, point_count):
        db, SQL = check_SQL.get_mysql()
        if db == False:
            return 500, "DB 연결이 불안정 합니다."

        if input_type == "add":
            try:
                SQL.execute(f"UPDATE users SET point = point + {point_count} WHERE user_id = '{user_id}'")
                db.commit()
                return 200, "정상적으로 추가 되었습니다."

            except Exception as e:
                return 500, {"message": str(e)}

        elif input_type == "remove":
            try:
                SQL.execute(f"UPDATE users SET point = point - {point_count} WHERE user_id = '{user_id}'")
                db.commit()
                return 200, "정상적으로 차감 되었습니다."

            except Exception as e:
                return 500, {"message": str(e)}

        else:
            return 500, {"message": "알 수 없는 명령어 입니다."}


    def setUserPointSet(user_id, point_count):
        db, SQL = check_SQL.get_mysql()
        if db == False:
            return 500, "DB 연결이 불안정 합니다."

        try:
            SQL.execute(f"UPDATE users SET point = {point_count} WHERE user_id = '{user_id}'")
            db.commit()
            return 200, f"{user_id}님의 포인트를 {point_count}로 설정 하였습니다."

        except Exception as e:
            print(e)
            return 500, e


class chatbotSQLController:
    def insertLogData(user_id, user_text, user_distance):
        db, SQL = check_SQL.get_mysql()
        if db == False:
            return 500, "DB 연결이 불안정 합니다."

        try:
            SQL.execute(f"INSERT INTO chatbot_logs(user_id, user_text, text_distance) VALUES('{user_id}', '{user_text}', '{user_distance}')")
            db.commit()
            return 200, "정상적 로깅"

        except Exception as e:
            print(e)
            return 500, e


class rankingSQLController:
    def getMyRanking(user_id):
        db, SQL = check_SQL.get_mysql()
        if not db:
            return 500, "DB 연결이 불안정 합니다."

        try:
            SQL.execute("SELECT user_id, user_name, count FROM user_quests ORDER BY count DESC")
            users = SQL.fetchall()
            
            rank = 1
            for user in users:
                if user[0] == user_id:
                    return 200, {
                        "user_id": user[0],
                        "user_name": user[1],
                        "user_type": globalSQLController.getUserType(user[0]),
                        "count": user[2],
                        "ranking": rank
                    }
                rank += 1
            
            return 404, "해당 유저를 찾을 수 없습니다."
        
        except Exception as e:
            print(e)
            return 500, "에러가 발생했습니다."
    
    def getRankings():
        db, SQL = check_SQL.get_mysql()
        userRankDatas = []
        if not db:
            return 500, "DB 연결이 불안정 합니다."

        try:
            SQL.execute("SELECT user_id, user_name, count FROM user_quests ORDER BY count DESC")
            users = SQL.fetchall()

            rank = 1
            for userData in users:
                userRankDatas.append({
                    "user_id": userData[0],
                    "user_name": userData[1],
                    "user_type": globalSQLController.getUserType(userData[0]),
                    "count": userData[2],
                    "ranking": rank
                })
                rank += 1
            return 200, userRankDatas
    
        except Exception as e:
            print(e)
            return 500, "에러가 발생했습니다."


class questSQLController:
    def getUserQuest(user_id):
        db, SQL = check_SQL.get_mysql()
        if db == False:
            return 500, "DB 연결이 불안정 합니다."

        try:
            SQL.execute(f"SELECT user_id, user_name, count, quest_data FROM user_quests WHERE user_id = '{user_id}'")
            users = SQL.fetchone()
            return 200, {
                "user_id":   users[0],
                "user_name": users[1],
                "count":     users[2],
                "quest_data":     json.loads(users[3]),
            }

        except Exception as e:
            return 500, e


    def getUserToDayQuest(user_id):
        db, SQL = check_SQL.get_mysql()
        if db == False:
            return 500, "DB 연결이 불안정 합니다."

        try:
            SQL.execute(f"SELECT user_id, user_name, count, quest_data FROM user_quests WHERE user_id = '{user_id}'")
            users = SQL.fetchone()
            return 200, {
                "user_id":   users[0],
                "user_name": users[1],
                "count":     users[2],
                "quest_data":     json.loads(users[3])[datetime.now().strftime("%Y-%m-%d")],
            }

        except Exception as e:
            return 500, e


    def updateUserQuest(input_type, user_id, quest_point):
        db, SQL = check_SQL.get_mysql()
        if db == False:
            return 500, "DB 연결이 불안정 합니다."

        if input_type == "add":
            try:
                SQL.execute(f"UPDATE user_quests SET count = count + {quest_point} WHERE user_id = '{user_id}'")
                db.commit()
                return 200, "정상적으로 추가 되었습니다."

            except Exception as e:
                return 500, {"message": str(e)}

        elif input_type == "remove":
            try:
                SQL.execute(f"UPDATE user_quests SET count = count - {quest_point} WHERE user_id = '{user_id}'")
                db.commit()
                return 200, "정상적으로 차감 되었습니다."

            except Exception as e:
                return 500, {"message": str(e)}

        else:
            return 500, {"message": "알 수 없는 명령어 입니다."}


    def setUserQuest(user_id, quest_point):
        db, SQL = check_SQL.get_mysql()
        if db == False:
            return 500, "DB 연결이 불안정 합니다."

        try:
            SQL.execute(f"UPDATE user_quests SET count = {quest_point} WHERE user_id = '{user_id}'")
            db.commit()
            return 200, f"{user_id}님의 퀘스트 카운트를 {quest_point}로 설정 하였습니다."

        except Exception as e:
            print(e)
            return 500, e


    def clearUserQuest(user_id, clearQuestName):
        db, SQL = check_SQL.get_mysql()
        if db == False:
            return 500, "DB 연결이 불안정 합니다."

        try:
            db.begin() # 트랜잭션 시작

            SQL.execute(f"SELECT user_id, user_name, count, quest_data FROM user_quests WHERE user_id = '{user_id}'")
            users = SQL.fetchone()
            quest_data = json.loads(users[3])
            current_date = datetime.now().strftime("%Y-%m-%d")
            givePointCount = quest_data[current_date][clearQuestName]['givePoint']

            if current_date in quest_data and clearQuestName in quest_data[current_date]:
                del quest_data[current_date][clearQuestName]

            updated_quest_data = json.dumps(quest_data, ensure_ascii=False)
            SQL.execute(f"UPDATE user_quests SET quest_data = %s WHERE user_id = %s", (updated_quest_data, user_id))
            SQL.execute(f"UPDATE user_quests SET count = count + 1 WHERE user_id = %s", (user_id))
            
            givePointResultCode, givePointResultData = pointSQLController.updateUserPoint(input_type="add", user_id=user_id, point_count=givePointCount)            
            if givePointResultCode == 200:
                db.commit()
                return 200, {
                    "user_id": user_id,
                    "clear_name": clearQuestName,
                    "message": "퀘스트를 정상적으로 완료 하였습니다!"
                }
            else:
                db.rollback()
                return 500, {"message": "퀘스트를 완료 중 문제가 발생 하였습니다. 잠시 후 다시 시도해주세요."}

        except Exception as e:
            print(e)
            db.rollback()
            return 500, {"message": "퀘스트를 완료 중 문제가 발생 하였습니다. 잠시 후 다시 시도해주세요.", "errorCode": str(e)}
