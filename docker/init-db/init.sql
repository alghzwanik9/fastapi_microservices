-- إنشاء قواعد البيانات للخدمات المصغرة
CREATE DATABASE products_db;
CREATE DATABASE orders_db;

-- منح الصلاحيات للمستخدم (اختياري، حسب إعداداتك)
GRANT ALL PRIVILEGES ON DATABASE products_db TO postgres;
GRANT ALL PRIVILEGES ON DATABASE orders_db TO postgres;
