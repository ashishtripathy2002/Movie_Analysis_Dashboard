from sqlalchemy.sql import text

class UserRepository:
    def __init__(self, db):
        self.db = db

    def find_user_by_email(self, email):
        query = text("""
        SELECT u.user_id, u.email, u.password, r.role_name
        FROM users u
        JOIN user_roles r ON u.role_id = r.role_id
        WHERE u.email = :email
        """)
        result = self.db.execute_dql_commands(query, {'email': email})
        return result.fetchone() if result else None

    def create_user(self, email, hashed_password, role_id):
        query = text("""
        INSERT INTO users (email, password, role_id)
        VALUES (:email, :password, :role_id)
        RETURNING user_id
        """)
        result = self.db.execute_ddl_and_dml_commands(
            query, {'email': email, 'password': hashed_password, 'role_id': role_id}
        )
        return result.fetchone()[0] if result else None


