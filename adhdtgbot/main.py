import os
import logging
import subprocess
import threading
import time
from flask import Flask, render_template, request, jsonify, redirect, url_for

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "default-secret-key")

# Global variables to track bot process
bot_process = None
bot_status = "stopped"
bot_output = []
MAX_OUTPUT_LINES = 100

# Check if BOT_TOKEN environment variable is set
def is_token_set():
    return os.environ.get("BOT_TOKEN") is not None

def start_bot():
    global bot_process, bot_status, bot_output
    
    if not is_token_set():
        logger.error("BOT_TOKEN environment variable is not set")
        bot_output.append("Error: BOT_TOKEN environment variable is not set")
        bot_status = "error"
        return False
    
    try:
        bot_process = subprocess.Popen(
            ["python", "simple_bot.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )
        
        # Start a thread to read the output
        def read_output():
            global bot_output
            while bot_process.poll() is None:
                line = bot_process.stdout.readline()
                if line:
                    logger.info(f"Bot output: {line.strip()}")
                    bot_output.append(line.strip())
                    # Keep only the last MAX_OUTPUT_LINES lines
                    if len(bot_output) > MAX_OUTPUT_LINES:
                        bot_output = bot_output[-MAX_OUTPUT_LINES:]
                time.sleep(0.1)
        
        output_thread = threading.Thread(target=read_output)
        output_thread.daemon = True
        output_thread.start()
        
        bot_status = "running"
        logger.info("Bot started successfully")
        return True
    except Exception as e:
        logger.error(f"Error starting bot: {e}")
        bot_output.append(f"Error starting bot: {e}")
        bot_status = "error"
        return False

def stop_bot():
    global bot_process, bot_status
    
    if bot_process is not None:
        try:
            bot_process.terminate()
            bot_process.wait(timeout=5)
            logger.info("Bot stopped successfully")
            bot_status = "stopped"
            return True
        except Exception as e:
            logger.error(f"Error stopping bot: {e}")
            try:
                bot_process.kill()
                logger.info("Bot killed forcefully")
            except:
                pass
            bot_status = "error"
            return False
    return True

@app.route('/', methods=['GET'])
def index():
    bot_token_set = is_token_set()
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>ADHD Support Bot</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link href="https://cdn.replit.com/agent/bootstrap-agent-dark-theme.min.css" rel="stylesheet">
        <style>
            .container {{ max-width: 800px; margin-top: 50px; }}
            .console {{ 
                background-color: #1e1e1e; 
                color: #ccc; 
                padding: 15px; 
                border-radius: 5px; 
                height: 300px; 
                overflow-y: auto; 
                font-family: monospace;
                white-space: pre-wrap;
                margin-bottom: 20px;
            }}
            .status-badge {{
                padding: 5px 10px;
                border-radius: 10px;
                font-weight: bold;
            }}
            .status-running {{ background-color: var(--bs-success); color: white; }}
            .status-stopped {{ background-color: var(--bs-secondary); color: white; }}
            .status-error {{ background-color: var(--bs-danger); color: white; }}
        </style>
    </head>
    <body data-bs-theme="dark">
        <div class="container">
            <h1>ADHD Support Telegram Bot</h1>
            <p class="lead">Manage your Telegram bot that helps people with ADHD.</p>
            
            <div class="card mb-4">
                <div class="card-header d-flex justify-content-between align-items-center">
                    <span>Bot Status</span>
                    <span class="status-badge status-{bot_status}">{bot_status.upper()}</span>
                </div>
                <div class="card-body">
                    <p>
                        <strong>BOT_TOKEN:</strong> 
                        {('✅ Set' if bot_token_set else '❌ Not set')}
                    </p>
                    <div class="d-flex gap-2">
                        <a href="/start" class="btn btn-success" {'disabled' if bot_status == 'running' or not bot_token_set else ''}>Start Bot</a>
                        <a href="/stop" class="btn btn-danger" {'disabled' if bot_status != 'running' else ''}>Stop Bot</a>
                        <a href="/restart" class="btn btn-warning" {'disabled' if not bot_token_set else ''}>Restart Bot</a>
                    </div>
                </div>
            </div>
            
            <div class="card">
                <div class="card-header">Bot Console Output</div>
                <div class="card-body">
                    <div class="console" id="console">{'<br>'.join(bot_output) if bot_output else 'No output yet.'}</div>
                    <a href="/clear_output" class="btn btn-secondary">Clear Output</a>
                </div>
            </div>
            
            <hr>
            <div class="card mt-4">
                <div class="card-header">How to Use</div>
                <div class="card-body">
                    <p>1. Make sure your BOT_TOKEN environment variable is set</p>
                    <p>2. Start the bot using the Start Bot button</p>
                    <p>3. Visit your bot on Telegram (@lifeisquestbot) and send the /start command</p>
                    <p>4. If you need to stop the bot, use the Stop Bot button</p>
                </div>
            </div>
        </div>
    </body>
    </html>
    """

@app.route('/start', methods=['GET'])
def start_bot_route():
    if bot_status != "running":
        start_bot()
    return redirect(url_for('index'))

@app.route('/stop', methods=['GET'])
def stop_bot_route():
    if bot_status == "running":
        stop_bot()
    return redirect(url_for('index'))

@app.route('/restart', methods=['GET'])
def restart_bot_route():
    stop_bot()
    time.sleep(1)
    start_bot()
    return redirect(url_for('index'))

@app.route('/clear_output', methods=['GET'])
def clear_output():
    global bot_output
    bot_output = []
    return redirect(url_for('index'))

if __name__ == "__main__":
    # Start the Flask web app
    app.run(host="0.0.0.0", port=5000, debug=True)
