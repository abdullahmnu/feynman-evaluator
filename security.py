import bcrypt # المكتبة الجديدة مباشرة
import hashlib

def get_password_hash(password: str):
    # 1. نضغط الكلمة لـ 64 حرفاً (SHA-256) عشان نتفادى حد الـ 72 بايت للأبد
    pre_hash = hashlib.sha256(password.encode()).hexdigest()
    
    # 2. نحول النص إلى بايت (Bytes) لأن bcrypt يطلب ذلك
    password_bytes = pre_hash.encode('utf-8')
    
    # 3. نولد "ملح" (Salt) ونفرم الكلمة
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    
    # 4. نرجعها كنص عادي (String) عشان تتخزن في الداتا بيس بسهولة
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str):
    # 1. نضغط الكلمة اللي كتبها المستخدم الآن
    pre_hash = hashlib.sha256(plain_password.encode()).hexdigest()
    
    # 2. نحول الكلمتين لبايت عشان المقارنة
    user_password_bytes = pre_hash.encode('utf-8')
    stored_hash_bytes = hashed_password.encode('utf-8')
    
    # 3. دالة المقارنة الذكية من bcrypt (هي تعرف تطلع الملح وتقارن)
    return bcrypt.checkpw(user_password_bytes, stored_hash_bytes)