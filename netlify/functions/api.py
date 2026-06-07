import sys
import os

# إضافة المجلد الرئيسي للمشروع إلى مسار النظام للتمكن من استيراد main.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from mangum import Mangum
from main import app

# المحول البرمجي (Handler) الذي سيستخدمه Netlify لتشغيل FastAPI
handler = Mangum(app)
