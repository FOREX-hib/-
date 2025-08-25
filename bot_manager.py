import os
import logging
import asyncio
from datetime import datetime
from telegram import Bot
from apscheduler.schedulers.background import BackgroundScheduler
import pytz
import google.generativeai as genai
from app import db
from models import BotConfig, PostHistory, BotLog

class TelegramBotManager:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.bot = None
        self.is_running = False

    def load_config(self):
        self.config = BotConfig.query.first()
        if self.config:
            self.bot = Bot(token=self.config.bot_token)
            return True
        return False

    def generate_post(self):
        if not self.config:
            raise Exception("Bot not configured properly")

        # Используем только Google Gemini
        genai.configure(api_key="AIzaSyCX-fRnapjtFiLi13pr_EHYEsRv8EYnVlA")  # замените на свой
        model = genai.GenerativeModel("gemini-1.5-flash")

        prompt = f"{self.config.system_prompt}\nСгенерируй сегодняшний пост."
        response = model.generate_content(prompt)
        return response.text.strip()

    # ------------------------------------------------------------------
    # Остальные методы без изменений
    # ------------------------------------------------------------------
    def send_post(self, content, is_manual=False):
        if not self.config or not self.bot:
            raise Exception("Bot not configured properly")

        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(
                self.bot.send_message(
                    chat_id=self.config.channel_id,
                    text=content,
                    parse_mode="Markdown"
                )
            )
            loop.close()

            post = PostHistory(
                content=content,
                status='sent',
                sent_at=datetime.utcnow()
            )
            db.session.add(post)
            db.session.commit()

            tz = pytz.timezone(self.config.timezone)
            self.log_message("INFO", f"✅ Post sent at {datetime.now(tz)}")
            return True

        except Exception as e:
            post = PostHistory(
                content=content,
                status='failed',
                error_message=str(e)
            )
            db.session.add(post)
            db.session.commit()
            self.log_message("ERROR", f"Failed to send post: {str(e)}")
            raise

    def daily_post_job(self):
        try:
            content = self.generate_post()
            self.send_post(content)
        except Exception as e:
            self.log_message("ERROR", f"Daily post job failed: {str(e)}")

    def start_scheduler(self):
        if not self.load_config():
            raise Exception("No bot configuration found")

        if self.config.is_active and not self.is_running:
            tz = pytz.timezone(self.config.timezone)
            self.scheduler.remove_all_jobs()
            self.scheduler.add_job(
                self.daily_post_job,
                trigger='cron',
                hour=self.config.posting_hour,
                minute=self.config.posting_minute,
                timezone=tz,
                id='daily_post'
            )
            if not self.scheduler.running:
                self.scheduler.start()
            self.is_running = True
            self.log_message("INFO", f"Scheduler started at {self.config.posting_hour:02d}:{self.config.posting_minute:02d} {self.config.timezone}")

    def stop_scheduler(self):
        if self.scheduler.running:
            self.scheduler.remove_all_jobs()
            self.is_running = False
            self.log_message("INFO", "Scheduler stopped")

    def test_connections(self):
        results = {}
        try:
            if self.bot:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                info = loop.run_until_complete(self.bot.get_me())
                loop.close()
                results['telegram'] = {'status': 'success', 'bot_name': info.first_name, 'username': info.username}
            else:
                results['telegram'] = {'status': 'error', 'message': 'Bot not configured'}
        except Exception as e:
            results['telegram'] = {'status': 'error', 'message': str(e)}

        try:
            genai.configure(api_key="AIzaSyCX-fRnapjtFiLi13pr_EHYEsRv8EYnVlA")
            model = genai.GenerativeModel("gemini-1.5-flash")
            model.generate_content("test", generation_config={"max_output_tokens": 5})
            results['ai'] = {'status': 'success', 'engine': 'gemini'}
        except Exception as e:
            results['ai'] = {'status': 'error', 'message': str(e)}

        return results

    def log_message(self, level, message):
        log_entry = BotLog(level=level, message=message)
        db.session.add(log_entry)
        db.session.commit()
        logging.log(getattr(logging, level.upper()), message)

bot_manager = TelegramBotManager()