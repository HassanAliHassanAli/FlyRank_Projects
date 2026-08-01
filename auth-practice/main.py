import os
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from supabase import create_client, Client
from dotenv import load_dotenv

# قراءة المتغيرات من ملف .env
load_dotenv()

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

# تهيئة عميل Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# تهيئة تطبيق FastAPI
app = FastAPI()

# --- تعريف شكل البيانات المطلوبة (الإيميل والباسورد) ---
class UserCredentials(BaseModel):
    email: str
    password: str

# ---------------------------------------------------
# Stage 1: Open Auth Routes
# ---------------------------------------------------

# 1. مسار إنشاء الحساب
@app.post("/auth/signup", status_code=status.HTTP_201_CREATED)
def signup(credentials: UserCredentials):
    # التحقق من وجود البيانات
    if not credentials.email or not credentials.password:
        raise HTTPException(status_code=400, detail="Email and password are required")
    
    try:
        # إرسال البيانات لـ Supabase لإنشاء الحساب
        response = supabase.auth.sign_up({
            "email": credentials.email,
            "password": credentials.password
        })
        return response
    except Exception as e:
        # إذا حدث خطأ (مثلاً الإيميل مسجل مسبقاً)
        raise HTTPException(status_code=400, detail=str(e))

# 2. مسار تسجيل الدخول
@app.post("/auth/login")
def login(credentials: UserCredentials):
    if not credentials.email or not credentials.password:
        raise HTTPException(status_code=400, detail="Email and password are required")
    
    try:
        # محاولة تسجيل الدخول
        response = supabase.auth.sign_in_with_password({
            "email": credentials.email,
            "password": credentials.password
        })
        # إرجاع التوكن في حالة النجاح
        return {
            "access_token": response.session.access_token,
            "refresh_token": response.session.refresh_token
        }
    except Exception as e:
        # في حالة أن الباسورد أو الإيميل خطأ
        raise HTTPException(status_code=401, detail="Invalid login credentials")

# ---------------------------------------------------

# مسار التجربة (Stage 0)
@app.get("/")
def read_root():
    return {"message": "Server running and connected to Supabase"}
from fastapi import Request # ضف دي فوق مع باقي الاستدعاءات

# ---------------------------------------------------
# Stage 2 & 3: The Public & Protected Gates + Token Verification
# ---------------------------------------------------

# 1. المسار العام (مفتوح للجميع)
@app.get("/public/info")
def public_info():
    return {"message": "Welcome stranger! This info is public."}

# 2. المسار المحمي والتحقق الفعلي من التوكن
@app.get("/protected/profile")
def protected_profile(request: Request):
    # (Stage 2) استخراج التوكن من الهيدر
    auth_header = request.headers.get("Authorization")
    
    # لو التوكن مش موجود أو مكتوب بصيغة غلط
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Access token required")
    
    # فصل كلمة Bearer عن التوكن نفسه
    token = auth_header.split(" ")[1]
    
    # (Stage 3) التحقق من صحة التوكن مع Supabase
    try:
        user_response = supabase.auth.get_user(token)
        # لو التوكن سليم، نرجع بيانات المستخدم
        return {"message": "Access Granted", "user": user_response.user}
    except Exception as e:
        # لو التوكن منتهي الصلاحية أو مزيف
        raise HTTPException(status_code=401, detail="Invalid or expired token")