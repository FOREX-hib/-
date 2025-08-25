# Telegram Marketing Bot Dashboard

## Overview

This is a Flask-based web application that manages an automated Telegram marketing bot. The system allows users to configure a Telegram bot that automatically generates and posts marketing content to a specified channel using OpenAI's GPT models. The application features a comprehensive dashboard for monitoring bot activity, managing configurations, viewing post history, and analyzing system logs.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Backend Framework
The application uses Flask as the primary web framework, chosen for its simplicity and rapid development capabilities. The modular structure separates concerns across different files:
- `app.py` handles application initialization and database setup
- `routes.py` manages web endpoints and user interactions
- `bot_manager.py` contains the core Telegram bot logic
- `models.py` defines the database schema

### Database Layer
The system uses SQLAlchemy ORM with SQLite as the default database, configurable via environment variables to support other databases like PostgreSQL in production. The database schema includes three main entities:
- `BotConfig` - Stores bot configuration including API keys, prompts, and scheduling settings
- `PostHistory` - Tracks all generated posts with their status and metadata
- `BotLog` - Maintains system logs for monitoring and debugging

### Bot Management System
The `TelegramBotManager` class handles the core bot functionality using the APScheduler library for automated posting. The system integrates with:
- Telegram Bot API for sending messages to channels
- OpenAI API (specifically GPT-4o model) for content generation
- Timezone-aware scheduling for automated posting

### Frontend Architecture
The web interface uses Bootstrap with a dark theme for the dashboard UI. The frontend is template-based using Jinja2, with separate pages for:
- Main dashboard with statistics and recent activity
- Configuration management for bot settings
- Post history with status tracking
- System logs for troubleshooting

### Security Considerations
The application implements basic security measures including:
- Environment variable-based configuration for sensitive data
- Session management with configurable secret keys
- Proxy fix middleware for deployment behind reverse proxies

### Scheduling and Automation
The bot uses APScheduler for automated posting at configured times with timezone support. Posts are generated using customizable system prompts and can be manually triggered or automatically scheduled.

## External Dependencies

### Third-Party APIs
- **Telegram Bot API**: Core integration for sending messages to Telegram channels
- **OpenAI API**: Used for automated content generation with the GPT-4o model

### Python Libraries
- **Flask**: Web framework for the dashboard application
- **SQLAlchemy**: Database ORM for data persistence
- **APScheduler**: Background task scheduling for automated posting
- **python-telegram-bot**: Telegram API wrapper
- **OpenAI**: Official OpenAI API client

### Frontend Dependencies
- **Bootstrap**: UI framework with dark theme support
- **Font Awesome**: Icon library for enhanced UI elements

### Database
- **SQLite**: Default database (configurable to PostgreSQL or other databases)
- Connection pooling and health checks configured for production use

### Development Tools
- **Werkzeug**: WSGI utilities including proxy fix middleware
- Environment-based configuration support for different deployment scenarios