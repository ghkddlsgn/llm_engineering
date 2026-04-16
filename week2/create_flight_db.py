from sqlalchemy import create_engine, text

# 1. DB 엔진 생성 (파일이 없으면 자동으로 새로 만들어줍니다)
DB_URL = "sqlite:///prices.db"
engine = create_engine(DB_URL)

def setup_mock_database():
    with engine.connect() as conn:
        # 2. prices 테이블 생성 (기존에 없으면 만들기)
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS prices (
                city TEXT PRIMARY KEY,
                price INTEGER
            )
        """))
        
        # (선택) 여러 번 실행했을 때 데이터가 중복되지 않도록 기존 데이터 삭제
        conn.execute(text("DELETE FROM prices"))
        
        # 3. 예시 데이터 준비 (방금 배우신 딕셔너리 형태를 묶어서 리스트로 만듭니다)
        mock_data = [
            {"city": "seoul", "price": 400},
            {"city": "tokyo", "price": 300},
            {"city": "new york", "price": 1200},
            {"city": "paris", "price": 950},
            {"city": "london", "price": 1000}
        ]
        
        # 4. 데이터 삽입 (리스트를 전달하면 여러 번 알아서 실행해 줍니다)
        conn.execute(
            text("INSERT INTO prices (city, price) VALUES (:city, :price)"),
            mock_data
        )
        
        # 5. 변경사항 저장 (데이터베이스에 쓰기 작업을 할 때는 commit 필수!)
        conn.commit()
        
        print("데이터베이스 세팅 및 예시 데이터 삽입이 완료되었습니다!")

setup_mock_database()