from app.models.database import get_connection
from passlib.context import CryptContext;


pwd_context = CryptContext(
        schemes = ["bcrypt"],
        deprecated="auto"
    );


def create_table():
    
    conn = get_connection();

    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            hash_password TEXT NOT NULL              
        )
        """    
    )

    conn.commit();
    conn.close();

def generate_hash(password):
    return pwd_context.hash(password);
# Hasheia a senha digitada pelo usuário


def create_user(username, hash_password):

    conn = get_connection();
    # Conn = "database.db"

    conn.execute(
        "INSERT INTO users (username, hash_password) VALUES (?, ?)",
        (username, hash_password)
    );

    conn.commit();
    conn.close();


def get_user_by_username(username):

    conn = get_connection();

    cursor = conn.execute(
        "SELECT * FROM users WHERE username = ?",
        (username,)
    );

    user = cursor.fetchone();
    conn.close();

    return user;


def verify_password(password, hash_password):
    pwd_context.verify(
        password,
        hash_password
    );
# Retorna True ou False.x                      