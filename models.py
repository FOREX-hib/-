from datetime import datetime
from extensions import db

class BotConfig(db.Model):
    __tablename__ = 'bot_config'
    
    id = db.Column(db.Integer, primary_key=True)
    bot_token = db.Column(db.String(255), nullable=False)
    channel_id = db.Column(db.String(100), nullable=False)
    openai_api_key = db.Column(db.String(255), nullable=True)  # Сделаем необязательным, так как используем Gemini
    system_prompt = db.Column(db.Text, nullable=False)
    timezone = db.Column(db.String(50), default='Europe/Moscow')
    posting_hour = db.Column(db.Integer, default=12)
    posting_minute = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class PostHistory(db.Model):
    __tablename__ = 'post_history'
    
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='draft')  # draft, sent, failed
    sent_at = db.Column(db.DateTime, nullable=True)
    error_message = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class BotLog(db.Model):
    __tablename__ = 'bot_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    level = db.Column(db.String(10), nullable=False)  # INFO, WARNING, ERROR
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)