from flask import render_template, request, redirect, url_for, flash, jsonify
from extensions import db
from models import BotConfig, PostHistory, BotLog
import pytz
from datetime import datetime
from flask import current_app as app

# Import bot_manager with proper error handling to avoid circular imports
try:
    from bot_manager import bot_manager
except ImportError:
    bot_manager = None

@app.route('/')
def dashboard():
    """Main dashboard view"""
    config = BotConfig.query.first()
    recent_posts = PostHistory.query.order_by(PostHistory.created_at.desc()).limit(5).all()
    recent_logs = BotLog.query.order_by(BotLog.created_at.desc()).limit(10).all()
    
    stats = {
        'total_posts': PostHistory.query.count(),
        'successful_posts': PostHistory.query.filter_by(status='sent').count(),
        'failed_posts': PostHistory.query.filter_by(status='failed').count(),
        'is_configured': config is not None,
        'is_active': config.is_active if config else False,
        'scheduler_running': bot_manager.is_running if bot_manager else False
    }
    
    return render_template('dashboard.html', 
                         config=config, 
                         stats=stats, 
                         recent_posts=recent_posts, 
                         recent_logs=recent_logs)

@app.route('/config', methods=['GET', 'POST'])
def config():
    """Bot configuration page"""
    if request.method == 'POST':
        bot_token = request.form.get('bot_token')
        channel_id = request.form.get('channel_id')
        openai_api_key = request.form.get('openai_api_key')
        system_prompt = request.form.get('system_prompt')
        timezone = request.form.get('timezone')
        posting_hour = int(request.form.get('posting_hour', 12))
        posting_minute = int(request.form.get('posting_minute', 0))
        is_active = 'is_active' in request.form
        
        # Get or create config
        config = BotConfig.query.first()
        if not config:
            config = BotConfig()
            db.session.add(config)
        
        # Update config
        config.bot_token = bot_token
        config.channel_id = channel_id
        config.openai_api_key = openai_api_key
        config.system_prompt = system_prompt
        config.timezone = timezone
        config.posting_hour = posting_hour
        config.posting_minute = posting_minute
        config.is_active = is_active
        
        db.session.commit()
        
        # Restart scheduler if active and bot_manager is available
        if bot_manager:
            if is_active:
                try:
                    bot_manager.stop_scheduler()
                    bot_manager.start_scheduler()
                    flash('Configuration saved and scheduler restarted!', 'success')
                except Exception as e:
                    flash(f'Configuration saved but scheduler failed: {str(e)}', 'warning')
            else:
                bot_manager.stop_scheduler()
                flash('Configuration saved!', 'success')
        else:
            flash('Configuration saved! Note: Bot manager not available.', 'warning')
        
        return redirect(url_for('dashboard'))
    
    config = BotConfig.query.first()
    timezones = ['Europe/Moscow', 'UTC', 'US/Eastern', 'US/Pacific', 'Europe/London', 'Asia/Tokyo']
    
    return render_template('config.html', config=config, timezones=timezones)

@app.route('/posts')
def posts():
    """View posting history"""
    page = request.args.get('page', 1, type=int)
    posts = PostHistory.query.order_by(PostHistory.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    return render_template('posts.html', posts=posts)

@app.route('/logs')
def logs():
    """View bot logs"""
    page = request.args.get('page', 1, type=int)
    logs = BotLog.query.order_by(BotLog.created_at.desc()).paginate(
        page=page, per_page=50, error_out=False
    )
    return render_template('logs.html', logs=logs)

@app.route('/generate_preview', methods=['POST'])
def generate_preview():
    """Generate a preview post"""
    if not bot_manager:
        return jsonify({'error': 'Bot manager not available'}), 500
        
    try:
        if not bot_manager.load_config():
            return jsonify({'error': 'Bot not configured'}), 400
        
        content = bot_manager.generate_post()
        return jsonify({'content': content})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/send_post', methods=['POST'])
def send_post():
    """Send a post manually"""
    if not bot_manager:
        flash('Bot manager not available', 'error')
        return redirect(url_for('dashboard'))
        
    try:
        content = request.form.get('content')
        if not content:
            flash('Post content is required', 'error')
            return redirect(url_for('dashboard'))
        
        if not bot_manager.load_config():
            flash('Bot not configured', 'error')
            return redirect(url_for('dashboard'))
        
        bot_manager.send_post(content, is_manual=True)
        flash('Post sent successfully!', 'success')
    except Exception as e:
        flash(f'Failed to send post: {str(e)}', 'error')
    
    return redirect(url_for('dashboard'))

@app.route('/test_connections')
def test_connections():
    """Test bot and API connections"""
    if not bot_manager:
        return jsonify({'error': 'Bot manager not available'}), 500
        
    try:
        if not bot_manager.load_config():
            return jsonify({'error': 'Bot not configured'}), 400
        
        results = bot_manager.test_connections()
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/toggle_scheduler', methods=['POST'])
def toggle_scheduler():
    """Toggle the automated scheduler"""
    if not bot_manager:
        flash('Bot manager not available', 'error')
        return redirect(url_for('dashboard'))
        
    try:
        config = BotConfig.query.first()
        if not config:
            flash('Bot not configured', 'error')
            return redirect(url_for('dashboard'))
        
        if bot_manager.is_running:
            bot_manager.stop_scheduler()
            config.is_active = False
            flash('Scheduler stopped', 'info')
        else:
            bot_manager.start_scheduler()
            config.is_active = True
            flash('Scheduler started', 'success')
        
        db.session.commit()
    except Exception as e:
        flash(f'Failed to toggle scheduler: {str(e)}', 'error')
    
    return redirect(url_for('dashboard'))