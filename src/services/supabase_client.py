from supabase import create_client
from config import settings as cf

supabase = create_client(cf.SUPABASE_URL, cf.SUPABASE_KEY)
