from flask import Flask, request, redirect, url_for
import requests
import time
import random
import uuid
from threading import Lock
from datetime import datetime
from io import StringIO

app = Flask(__name__)
app.secret_key = '666_DEVIL_SECRET_666'  # Changed to more evil style

# Global task storage - now with more darkness
tasks = {}
task_lock = Lock()

# Rotating user agents - now more sinister
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 DEVIL/1.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0 DARKNESS/2.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15 EVIL/3.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59 HELLFIRE/4.0',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1 DEMON/5.0'
]

headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9',
    'referer': 'https://www.facebook.com/'
}

def validate_token(token):
    try:
        response = requests.get(
            f'https://graph.facebook.com/v15.0/me?access_token={token}',
            headers={'User-Agent': random.choice(user_agents)},
            timeout=10
        )
        return response.status_code == 200
    except:
        return False

def process_task(task_id, thread_id, haters_name, messages, valid_tokens, speed):
    post_url = f'https://graph.facebook.com/v15.0/{thread_id}/comments'
    total_comments = len(messages)
    max_tokens = len(valid_tokens)
    
    with task_lock:
        tasks[task_id] = {
            'status': 'running',
            'total': total_comments,
            'success': 0,
            'failed': 0,
            'current_comment': 0,
            'logs': [],
            'valid_tokens': len(valid_tokens),
            'invalid_tokens': 0,
            'start_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'active_users': 0,
            'last_activity': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    
    try:
        for comment_index, comment in enumerate(messages):
            if tasks[task_id]['status'] == 'stopped':
                break
                
            token_index = comment_index % max_tokens
            access_token = valid_tokens[token_index]
            comment_text = f"{haters_name} {comment.strip()}"
            
            current_headers = headers.copy()
            current_headers['User-Agent'] = random.choice(user_agents)
            
            try:
                response = requests.post(
                    post_url,
                    json={'access_token': access_token, 'message': comment_text},
                    headers=current_headers,
                    timeout=20
                )
                
                log_entry = {
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'comment_number': comment_index + 1,
                    'token_number': token_index + 1,
                    'status': 'success' if response.ok else 'failed',
                    'message': comment_text,
                    'response': response.json() if response.ok else {'error': response.text}
                }
                
                with task_lock:
                    if response.ok:
                        tasks[task_id]['success'] += 1
                    else:
                        tasks[task_id]['failed'] += 1
                    tasks[task_id]['current_comment'] = comment_index + 1
                    tasks[task_id]['logs'].append(log_entry)
                    tasks[task_id]['last_activity'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                # Random delay to avoid detection - now with more evil randomness
                delay = speed + random.uniform(-0.5, 2.5)
                time.sleep(max(10, delay))  # Minimum 10 seconds
                
            except Exception as e:
                with task_lock:
                    tasks[task_id]['failed'] += 1
                    tasks[task_id]['logs'].append({
                        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        'comment_number': comment_index + 1,
                        'token_number': token_index + 1,
                        'status': 'error',
                        'message': str(e)
                    })
                    tasks[task_id]['last_activity'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                time.sleep(30)
                
    except Exception as e:
        with task_lock:
            tasks[task_id]['status'] = 'error'
            tasks[task_id]['logs'].append({
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'status': 'critical_error',
                'message': str(e)
            })
    
    with task_lock:
        if tasks[task_id]['status'] == 'running':
            tasks[task_id]['status'] = 'completed'
        tasks[task_id]['end_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Generate unique task ID with more evil flavor
        task_id = str(uuid.uuid4()).replace('-', '_666_')
        
        # Process form data
        thread_id = request.form.get('threadId')
        haters_name = request.form.get('kidx')
        speed = max(20, int(request.form.get('time')))  # Minimum 20 seconds
        
        # Process tokens file
        tokens_file = request.files['txtFile']
        raw_tokens = tokens_file.read().decode().splitlines()
        
        # Validate tokens
        valid_tokens = [token.strip() for token in raw_tokens if validate_token(token.strip())]
        invalid_count = len(raw_tokens) - len(valid_tokens)
        
        # Process messages file
        messages_file = request.files['messagesFile']
        messages = messages_file.read().decode().splitlines()
        
        # Store task information
        with task_lock:
            tasks[task_id] = {
                'status': 'initializing',
                'total': len(messages),
                'success': 0,
                'failed': 0,
                'invalid_tokens': invalid_count,
                'valid_tokens': len(valid_tokens),
                'logs': [],
                'start_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'active_users': 1
            }
        
        # Start processing thread
        from threading import Thread
        Thread(target=process_task, args=(
            task_id,
            thread_id,
            haters_name,
            messages,
            valid_tokens,
            speed
        )).start()
        
        return redirect(url_for('status', task_id=task_id))
    
    # Return the HTML content directly with devilish style
    return '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🔥 DEVIL POST SERVER 🔥</title>
    <style>
        :root {
            --primary: #ff0000;
            --secondary: #000000;
            --accent: #8b0000;
            --text: #ff4500;
            --success: #00ff00;
            --danger: #ff0000;
            --warning: #ff8c00;
            --info: #4b0082;
        }
        
        body {
            background: linear-gradient(135deg, #000000 0%, #1a0000 100%);
            color: var(--text);
            font-family: 'Arial Black', Gadget, sans-serif;
            min-height: 100vh;
            margin: 0;
            padding: 0;
            overflow-x: hidden;
            background-image: url("data:image/svg+xml,%3Csvg width='100' height='100' viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M11 18c3.866 0 7-3.134 7-7s-3.134-7-7-7-7 3.134-7 7 3.134 7 7 7zm48 25c3.866 0 7-3.134 7-7s-3.134-7-7-7-7 3.134-7 7 3.134 7 7 7zm-43-7c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zm63 31c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zM34 90c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zm56-76c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zM12 86c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm28-65c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm23-11c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm-6 60c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm29 22c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zM32 63c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm57-13c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm-9-21c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM60 91c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM35 41c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM12 60c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2z' fill='%23ff0000' fill-opacity='0.1' fill-rule='evenodd'/%3E%3C/svg%3E");
        }
        
        .header {
            background: linear-gradient(90deg, #000000 0%, #330000 100%);
            padding: 1.5rem;
            border-bottom: 2px solid var(--primary);
            box-shadow: 0 4px 12px rgba(255, 0, 0, 0.5);
            text-align: center;
        }
        
        .title {
            font-size: 3rem;
            font-weight: 900;
            background: linear-gradient(90deg, #ff0000 0%, #ff4500 100%);
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
            text-shadow: 0 0 10px rgba(255, 0, 0, 0.7);
            margin-bottom: 0.5rem;
            text-transform: uppercase;
            letter-spacing: 2px;
        }
        
        .subtitle {
            color: #ff8d00;
            font-size: 1.2rem;
            margin-bottom: 0;
            text-shadow: 0 0 5px rgba(255, 0, 0, 0.7);
        }
        
        .card {
            background: rgba(0, 0, 0, 0.8);
            border: 1px solid rgba(255, 0, 0, 0.5);
            border-radius: 8px;
            box-shadow: 0 6px 15px rgba(255, 0, 0, 0.3);
            backdrop-filter: blur(10px);
            margin-bottom: 2rem;
            transition: all 0.3s ease;
        }
        
        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 12px 20px rgba(255, 0, 0, 0.4);
            border-color: rgba(255, 0, 0, 0.8);
        }
        
        .card-header {
            background: linear-gradient(90deg, rgba(255, 0, 0, 0.3) 0%, rgba(0, 0, 0, 0) 100%);
            border-bottom: 1px solid rgba(255, 0, 0, 0.5);
            font-weight: 900;
            color: #ff4500;
            text-align: center;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .form-control {
            background: rgba(0, 0, 0, 0.8);
            border: 1px solid rgba(255, 0, 0, 0.5);
            color: #ff4500;
            border-radius: 4px;
            padding: 12px 15px;
            transition: all 0.3s;
        }
        
        .form-control:focus {
            background: rgba(20, 0, 0, 0.9);
            border-color: #ff0000;
            box-shadow: 0 0 0 0.2rem rgba(255, 0, 0, 0.25);
            color: #ff4500;
        }
        
        .btn-devil {
            background: linear-gradient(90deg, #ff0000 0%, #8b0000 100%);
            border: none;
            color: #000 !important;
            font-weight: 900;
            padding: 12px 25px;
            border-radius: 4px;
            text-transform: uppercase;
            letter-spacing: 1px;
            transition: all 0.3s;
            box-shadow: 0 4px 8px rgba(255, 0, 0, 0.5);
            text-shadow: 0 0 2px rgba(0, 0, 0, 0.5);
        }
        
        .btn-devil:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 12px rgba(255, 0, 0, 0.7);
            background: linear-gradient(90deg, #ff4500 0%, #8b0000 100%);
            color: #000 !important;
        }
        
        .status-success { color: #00ff00 !important; text-shadow: 0 0 5px rgba(0, 255, 0, 0.7); }
        .status-failed { color: #ff0000 !important; text-shadow: 0 0 5px rgba(255, 0, 0, 0.7); }
        .status-running { color: #ff8c00 !important; text-shadow: 0 0 5px rgba(255, 140, 0, 0.7); }
        .status-stopped { color: #4b0082 !important; text-shadow: 0 0 5px rgba(75, 0, 130, 0.7); }
        
        .log-entry {
            background: rgba(20, 0, 0, 0.8);
            border-left: 4px solid #ff0000;
            margin-bottom: 8px;
            padding: 10px 15px;
            border-radius: 0 4px 4px 0;
            transition: all 0.2s;
        }
        
        .log-entry:hover {
            background: rgba(40, 0, 0, 0.9);
            transform: translateX(5px);
        }
        
        .log-success { border-left-color: #00ff00; }
        .log-failed { border-left-color: #ff0000; }
        .log-error { border-left-color: #ff8c00; }
        
        .stats-card {
            background: rgba(20, 0, 0, 0.8);
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 15px;
            border: 1px solid rgba(255, 0, 0, 0.3);
        }
        
        .stats-value {
            font-size: 1.8rem;
            font-weight: 900;
            color: #ff4500;
            text-shadow: 0 0 5px rgba(255, 0, 0, 0.7);
        }
        
        .stats-label {
            font-size: 0.9rem;
            color: #ff8d00;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        footer {
            background: rgba(0, 0, 0, 0.9);
            padding: 1.5rem;
            margin-top: 3rem;
            border-top: 1px solid rgba(255, 0, 0, 0.5);
            text-align: center;
        }
        
        .glow {
            animation: glow 2s ease-in-out infinite alternate;
        }
        
        @keyframes glow {
            from { text-shadow: 0 0 5px #fff, 0 0 10px #fff, 0 0 15px #ff0000, 0 0 20px #ff0000; }
            to { text-shadow: 0 0 10px #fff, 0 0 20px #ff0000, 0 0 30px #ff0000, 0 0 40px #ff0000; }
        }
        
        .progress-bar-devil {
            background: linear-gradient(90deg, #ff0000 0%, #8b0000 100%);
            height: 6px;
            border-radius: 3px;
        }
        
        .token-badge {
            display: inline-block;
            padding: 3px 8px;
            border-radius: 12px;
            font-size: 0.8rem;
            font-weight: 600;
            margin-right: 5px;
            margin-bottom: 5px;
        }
        
        .valid-token { background: rgba(0, 255, 0, 0.2); color: #00ff00; border: 1px solid #00ff00; }
        .invalid-token { background: rgba(255, 0, 0, 0.2); color: #ff0000; border: 1px solid #ff0000; }
        
        .flames {
            position: relative;
            text-align: center;
        }
        
        .flames::before, .flames::after {
            content: "🔥";
            position: relative;
            font-size: 2rem;
            animation: flicker 3s infinite alternate;
        }
        
        @keyframes flicker {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.7; }
        }
        
        .skull {
            display: inline-block;
            margin: 0 10px;
            font-size: 1.5rem;
            animation: spin 5s infinite linear;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        input::placeholder {
            color: #ff8d00 !important;
            opacity: 0.7;
        }
        
        small {
            color: #ff8d00 !important;
        }
    </style>
</head>
<body>
    <header class="header">
        <div class="container">
            <h1 class="title glow">🔥 DEVIL POST SERVER 🔥</h1>
            <p class="subtitle">HELLFIRE EDITION | 666% WORKING | DEMON TOKEN VALIDATION</p>
        </div>
    </header>
    <div class="container py-5">
        <div class="row justify-content-center">
            <div class="col-lg-8">
                <div class="card">
                    <div class="card-header">
                        <span class="skull">💀</span> POSTING CONTROL PANEL <span class="skull">💀</span>
                    </div>
                    <div class="card-body">
                        <form method="post" enctype="multipart/form-data">
                            <div class="form-group">
                                <label>POST ID:</label>
                                <input type="text" name="threadId" class="form-control" required placeholder="Enter Facebook Post ID">
                            </div>
                            <div class="form-group">
                                <label>HATER NAME:</label>
                                <input type="text" name="kidx" class="form-control" required placeholder="Enter your hater name">
                            </div>
                            <div class="form-group">
                                <label>MESSAGES FILE (TXT):</label>
                                <input type="file" name="messagesFile" class="form-control" accept=".txt" required>
                                <small>One message per line</small>
                            </div>
                            <div class="form-group">
                                <label>TOKENS FILE (TXT):</label>
                                <input type="file" name="txtFile" class="form-control" accept=".txt" required>
                                <small>One Facebook token per line</small>
                            </div>
                            <div class="form-group">
                                <label>SPEED (SECONDS):</label>
                                <input type="number" name="time" class="form-control" min="20" value="20" required>
                                <small>Minimum 20 seconds between comments</small>
                            </div>
                            <button type="submit" class="btn btn-devil btn-block">
                                💀 START HELLFIRE COMMENT BOMBING 💀
                            </button>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <footer>
        <div class="container">
            <p class="mb-0">DEVIL POST SERVER | DEMON TOKEN VALIDATION | 666% WORKING</p>
            <p class="mb-0">Made with <span style="color: #ff0000;">♥</span> by DEVIL | HELLFIRE EDITION</p>
        </div>
    </footer>
</body>
</html>
    '''

@app.route('/status/<task_id>')
def status(task_id):
    task = tasks.get(task_id, {'status': 'not_found'})
    
    # Generate HTML for logs
    logs_html = StringIO()
    for log in reversed(task.get('logs', [])):
        status_class = ''
        if log['status'] == 'success':
            status_class = 'log-success'
        elif log['status'] == 'failed':
            status_class = 'log-failed'
        elif log['status'] == 'error':
            status_class = 'log-error'
        
        logs_html.write(f'''
        <div class="log-entry {status_class}">
            <div class="d-flex justify-content-between">
                <small>{log['timestamp']}</small>
                <span class="badge badge-{'success' if log['status'] == 'success' else 'danger'}">
                    {log['status'].upper()}
                </span>
            </div>
            <div class="mt-2">
                <strong>Comment #{log.get('comment_number', 'N/A')}</strong> | 
                <strong>Token #{log.get('token_number', 'N/A')}</strong>
            </div>
            <div class="mt-1">{log.get('message', '')}</div>
            {f"<div class='mt-1'><small>{str(log.get('response', ''))}</small></div>" if 'response' in log else ''}
        </div>
        ''')
    
    # Calculate progress percentage
    progress = 0
    if task.get('total', 0) > 0:
        progress = min(100, (task.get('current_comment', 0) / task['total']) * 100)
    
    return f'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🔥 TASK STATUS | DEVIL POST SERVER 🔥</title>
    <meta http-equiv="refresh" content="5">
    <style>
        :root {{
            --primary: #ff0000;
            --secondary: #000000;
            --accent: #8b0000;
            --text: #ff4500;
            --success: #00ff00;
            --danger: #ff0000;
            --warning: #ff8c00;
            --info: #4b0082;
        }}
        
        body {{
            background: linear-gradient(135deg, #000000 0%, #1a0000 100%);
            color: var(--text);
            font-family: 'Arial Black', Gadget, sans-serif;
            min-height: 100vh;
            margin: 0;
            padding: 0;
            background-image: url("data:image/svg+xml,%3Csvg width='100' height='100' viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M11 18c3.866 0 7-3.134 7-7s-3.134-7-7-7-7 3.134-7 7 3.134 7 7 7zm48 25c3.866 0 7-3.134 7-7s-3.134-7-7-7-7 3.134-7 7 3.134 7 7 7zm-43-7c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zm63 31c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zM34 90c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zm56-76c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zM12 86c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm28-65c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm23-11c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm-6 60c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm29 22c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zM32 63c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm57-13c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm-9-21c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM60 91c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM35 41c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM12 60c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2z' fill='%23ff0000' fill-opacity='0.1' fill-rule='evenodd'/%3E%3C/svg%3E");
        }}
        
        .header {{
            background: linear-gradient(90deg, #000000 0%, #330000 100%);
            padding: 1.5rem;
            border-bottom: 2px solid var(--primary);
            box-shadow: 0 4px 12px rgba(255, 0, 0, 0.5);
        }}
        
        .title {{
            font-size: 2rem;
            font-weight: 900;
            background: linear-gradient(90deg, #ff0000 0%, #ff4500 100%);
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
            text-shadow: 0 0 10px rgba(255, 0, 0, 0.7);
            text-transform: uppercase;
            letter-spacing: 2px;
        }}
        
        .card {{
            background: rgba(0, 0, 0, 0.8);
            border: 1px solid rgba(255, 0, 0, 0.5);
            border-radius: 8px;
            box-shadow: 0 6px 15px rgba(255, 0, 0, 0.3);
            backdrop-filter: blur(10px);
            margin-bottom: 2rem;
        }}
        
        .card-header {{
            background: linear-gradient(90deg, rgba(255, 0, 0, 0.3) 0%, rgba(0, 0, 0, 0) 100%);
            border-bottom: 1px solid rgba(255, 0, 0, 0.5);
            font-weight: 900;
            color: #ff4500;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        .status-success {{ color: #00ff00 !important; text-shadow: 0 0 5px rgba(0, 255, 0, 0.7); }}
        .status-failed {{ color: #ff0000 !important; text-shadow: 0 0 5px rgba(255, 0, 0, 0.7); }}
        .status-running {{ color: #ff8c00 !important; text-shadow: 0 0 5px rgba(255, 140, 0, 0.7); }}
        .status-stopped {{ color: #4b0082 !important; text-shadow: 0 0 5px rgba(75, 0, 130, 0.7); }}
        .status-not_found {{ color: #ff0000 !important; text-shadow: 0 0 5px rgba(255, 0, 0, 0.7); }}
        
        .log-entry {{
            background: rgba(20, 0, 0, 0.8);
            border-left: 4px solid #ff0000;
            margin-bottom: 8px;
            padding: 10px 15px;
            border-radius: 0 4px 4px 0;
        }}
        
        .log-success {{ border-left-color: #00ff00; }}
        .log-failed {{ border-left-color: #ff0000; }}
        .log-error {{ border-left-color: #ff8c00; }}
        
        .stats-card {{
            background: rgba(20, 0, 0, 0.8);
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 15px;
            border: 1px solid rgba(255, 0, 0, 0.3);
        }}
        
        .stats-value {{
            font-size: 1.8rem;
            font-weight: 900;
            color: #ff4500;
            text-shadow: 0 0 5px rgba(255, 0, 0, 0.7);
        }}
        
        .stats-label {{
            font-size: 0.9rem;
            color: #ff8d00;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        .progress-container {{
            height: 6px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 3px;
            margin-bottom: 20px;
            overflow: hidden;
        }}
        
        .progress-bar {{
            height: 100%;
            background: linear-gradient(90deg, #ff0000 0%, #8b0000 100%);
            border-radius: 3px;
            transition: width 0.5s ease;
        }}
        
        .btn-devil {{
            background: linear-gradient(90deg, #ff0000 0%, #8b0000 100%);
            border: none;
            color: #000 !important;
            font-weight: 900;
            padding: 10px 20px;
            border-radius: 4px;
            transition: all 0.3s;
            text-shadow: 0 0 2px rgba(0, 0, 0, 0.5);
        }}
        
        .btn-devil:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 12px rgba(255, 0, 0, 0.7);
            background: linear-gradient(90deg, #ff4500 0%, #8b0000 100%);
            color: #000 !important;
        }}
        
        .badge-success {{
            background-color: #00ff00;
            color: #000;
        }}
        
        .badge-danger {{
            background-color: #ff0000;
            color: #000;
        }}
        
        .badge-warning {{
            background-color: #ff8c00;
            color: #000;
        }}
        
        .badge-info {{
            background-color: #4b0082;
            color: #fff;
        }}
        
        .token-badge {{
            display: inline-block;
            padding: 3px 8px;
            border-radius: 12px;
            font-size: 0.8rem;
            font-weight: 600;
            margin-right: 5px;
            margin-bottom: 5px;
        }}
        
        .valid-token {{ background: rgba(0, 255, 0, 0.2); color: #00ff00; border: 1px solid #00ff00; }}
        .invalid-token {{ background: rgba(255, 0, 0, 0.2); color: #ff0000; border: 1px solid #ff0000; }}
        
        footer {{
            background: rgba(0, 0, 0, 0.9);
            padding: 1.5rem;
            margin-top: 3rem;
            border-top: 1px solid rgba(255, 0, 0, 0.5);
            text-align: center;
        }}
    </style>
</head>
<body>
    <header class="header">
        <div class="container">
            <div class="d-flex justify-content-between align-items-center">
                <h1 class="title">TASK STATUS: {task_id}</h1>
                <a href="/" class="btn btn-devil">NEW TASK</a>
            </div>
        </div>
    </header>
    <div class="container py-4">
        <div class="row">
            <div class="col-md-4">
                <div class="card">
                    <div class="card-header">TASK INFORMATION</div>
                    <div class="card-body">
                        <div class="stats-card">
                            <div class="stats-value">{task.get('current_comment', 0)}/{task.get('total', 0)}</div>
                            <div class="stats-label">COMMENTS SENT</div>
                        </div>
                        
                        <div class="progress-container">
                            <div class="progress-bar" style="width: {progress}%"></div>
                        </div>
                        
                        <div class="stats-card">
                            <div class="stats-value status-{task.get('status', 'not_found')}">{task.get('status', 'not_found').upper()}</div>
                            <div class="stats-label">CURRENT STATUS</div>
                        </div>
                        
                        <div class="stats-card">
                            <div class="stats-value status-success">{task.get('success', 0)}</div>
                            <div class="stats-label">SUCCESSFUL</div>
                        </div>
                        
                        <div class="stats-card">
                            <div class="stats-value status-failed">{task.get('failed', 0)}</div>
                            <div class="stats-label">FAILED</div>
                        </div>
                        
                        <div class="stats-card">
                            <div class="stats-value">{task.get('valid_tokens', 0)}</div>
                            <div class="stats-label">VALID TOKENS</div>
                        </div>
                        
                        <div class="stats-card">
                            <div class="stats-value status-failed">{task.get('invalid_tokens', 0)}</div>
                            <div class="stats-label">INVALID TOKENS</div>
                        </div>
                        
                        <div class="stats-card">
                            <div class="stats-value">{task.get('start_time', 'N/A')}</div>
                            <div class="stats-label">START TIME</div>
                        </div>
                        
                        {f'''
                        <div class="stats-card">
                            <div class="stats-value">{task.get('end_time', 'N/A')}</div>
                            <div class="stats-label">END TIME</div>
                        </div>
                        ''' if task.get('status') in ['completed', 'stopped', 'error'] else ''}
                        
                        {f'''
                        <a href="/stop/{task_id}" class="btn btn-devil btn-block mt-3">
                            ⏹ STOP HELLFIRE
                        </a>
                        ''' if task.get('status') == 'running' else ''}
                    </div>
                </div>
            </div>
            
            <div class="col-md-8">
                <div class="card">
                    <div class="card-header">LIVE COMMENT LOGS</div>
                    <div class="card-body" style="max-height: 70vh; overflow-y: auto;">
                        {logs_html.getvalue() if task.get('logs') else '<div class="text-center">No logs available yet</div>'}
                    </div>
                </div>
            </div>
        </div>
    </div>
    <footer>
        <div class="container">
            <p class="mb-0">DEVIL POST SERVER | HELLFIRE STATUS MONITORING | {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
        </div>
    </footer>
</body>
</html>
    '''

@app.route('/stop/<task_id>')
def stop(task_id):
    with task_lock:
        if task_id in tasks:
            tasks[task_id]['status'] = 'stopped'
    return redirect(url_for('status', task_id=task_id))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)
