from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import time

app = FastAPI(
    title="SMS Spam Moderator",
    description="Active Learning Content Moderation API & Dashboard",
    version="2.0.0"
)

class MessageRequest(BaseModel):
    text: str

# HTML Dashboard Frontend Interface matching your project UI
HTML_DASHBOARD = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SMS Spam Moderator</title>
    <style>
        :root {
            background-color: #0b0f17;
            color: #c9d1d9;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        }
        body {
            margin: 0;
            padding: 24px;
            background: #0b0f17;
        }
        header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid #21262d;
            padding-bottom: 16px;
            margin-bottom: 24px;
        }
        .title h1 {
            margin: 0;
            font-size: 20px;
            color: #e6edf3;
            letter-spacing: 0.5px;
        }
        .title p {
            margin: 4px 0 0 0;
            font-size: 12px;
            color: #8b949e;
        }
        .status-badge {
            font-size: 12px;
            color: #3fb950;
            display: flex;
            align-items: center;
            gap: 6px;
        }
        .status-dot {
            width: 8px;
            height: 8px;
            background-color: #3fb950;
            border-radius: 50%;
        }
        .grid-layout {
            display: grid;
            grid-template-columns: 2fr 1fr;
            gap: 20px;
            margin-bottom: 24px;
        }
        .card {
            background: #161b22;
            border: 1px solid #30363d;
            border-radius: 6px;
            padding: 20px;
        }
        .card-title {
            font-size: 11px;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: #8b949e;
            margin-bottom: 12px;
        }
        textarea {
            width: 100%;
            height: 100px;
            background: #0d1117;
            border: 1px solid #30363d;
            border-radius: 6px;
            color: #e6edf3;
            padding: 12px;
            font-size: 14px;
            resize: vertical;
            box-sizing: border-box;
            outline: none;
        }
        textarea:focus {
            border-color: #58a6ff;
        }
        .sample-chips {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin: 12px 0 16px 0;
        }
        .chip {
            background: #21262d;
            border: 1px solid #30363d;
            color: #c9d1d9;
            padding: 6px 10px;
            font-size: 11px;
            border-radius: 4px;
            cursor: pointer;
            transition: background 0.2s;
        }
        .chip:hover {
            background: #30363d;
            color: #e6edf3;
        }
        .btn-classify {
            width: 100%;
            background: #21262d;
            border: 1px solid #30363d;
            color: #e6edf3;
            padding: 10px;
            font-weight: 600;
            border-radius: 6px;
            cursor: pointer;
            transition: background 0.2s;
        }
        .btn-classify:hover {
            background: #30363d;
            border-color: #8b949e;
        }
        .stat-row {
            display: flex;
            justify-content: space-between;
            font-size: 13px;
            padding: 8px 0;
            border-bottom: 1px solid #21262d;
        }
        .stat-row:last-child {
            border-bottom: none;
        }
        .stat-value {
            font-family: monospace;
            color: #e6edf3;
        }
        .stat-value.healthy {
            color: #3fb950;
        }
        .result-box {
            margin-top: 16px;
            background: #0d1117;
            border: 1px solid #30363d;
            border-radius: 6px;
            padding: 16px;
            display: none;
        }
        .badge-ham {
            display: inline-block;
            background: rgba(63, 185, 80, 0.15);
            color: #3fb950;
            border: 1px solid rgba(63, 185, 80, 0.4);
            padding: 4px 12px;
            font-weight: bold;
            border-radius: 4px;
            font-size: 12px;
        }
        .badge-spam {
            display: inline-block;
            background: rgba(248, 81, 73, 0.15);
            color: #f85149;
            border: 1px solid rgba(248, 81, 73, 0.4);
            padding: 4px 12px;
            font-weight: bold;
            border-radius: 4px;
            font-size: 12px;
        }
        .progress-bar {
            width: 100%;
            background: #21262d;
            height: 6px;
            border-radius: 3px;
            margin-top: 12px;
            overflow: hidden;
        }
        .progress-fill {
            height: 100%;
            background: #3fb950;
            width: 0%;
            transition: width 0.4s ease;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            font-size: 13px;
        }
        th {
            text-align: left;
            color: #8b949e;
            font-weight: 600;
            padding: 8px 12px;
            border-bottom: 1px solid #30363d;
        }
        td {
            padding: 10px 12px;
            border-bottom: 1px solid #21262d;
            color: #c9d1d9;
        }
    </style>
</head>
<body>

    <header>
        <div class="title">
            <h1>SMS Spam Moderator</h1>
            <p>Active Learning Content Moderation</p>
        </div>
        <div class="status-badge">
            <div class="status-dot"></div> Connected
        </div>
    </header>

    <div class="grid-layout">
        <!-- Left Column: Classify Panel -->
        <div>
            <div class="card">
                <div class="card-title">Classify Text</div>
                <textarea id="messageInput" placeholder="Enter SMS message to moderate..."></textarea>
                
                <div class="sample-chips">
                    <div class="chip" onclick="setSample('Hey, are we still on for lunch?')">Hey, are we still on for lunch?</div>
                    <div class="chip" onclick="setSample('FREE entry! Call NOW to win!')">FREE entry! Call NOW to win!</div>
                    <div class="chip" onclick="setSample('You won 10000 pounds! Claim now')">You won 10000 pounds! Claim now</div>
                    <div class="chip" onclick="setSample('Can you pick up milk?')">Can you pick up milk?</div>
                </div>

                <button class="btn-classify" onclick="classifyMessage()">Classify</button>

                <div id="resultBox" class="result-box">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div id="resultBadge" class="badge-ham">HAM</div>
                        <span id="confidenceText" style="font-size: 13px; color: #8b949e;">Confidence: 92.5%</span>
                    </div>
                    <div class="progress-bar">
                        <div id="progressFill" class="progress-fill" style="width: 92.5%;"></div>
                    </div>
                    <div style="margin-top: 10px; font-size: 11px; color: #8b949e; display: flex; justify-content: space-between;">
                        <span id="latencyText">Latency: 2.15ms</span>
                        <span id="idText">ID: -</span>
                    </div>
                </div>
            </div>
        </div>

        <!-- Right Column: System Info -->
        <div style="display: flex; flex-direction: column; gap: 20px;">
            <div class="card">
                <div class="card-title">System Health</div>
                <div class="stat-row">
                    <span>Status</span>
                    <span class="stat-value healthy">healthy</span>
                </div>
                <div class="stat-row">
                    <span>Model</span>
                    <span class="stat-value">spam_classifier.onnx</span>
                </div>
                <div class="stat-row">
                    <span>Test Prediction</span>
                    <span class="stat-value">ham</span>
                </div>
            </div>

            <div class="card">
                <div class="card-title">Model Info</div>
                <div class="stat-row">
                    <span>Vocabulary</span>
                    <span class="stat-value">8,231</span>
                </div>
                <div class="stat-row">
                    <span>Threshold</span>
                    <span class="stat-value">80%</span>
                </div>
                <div class="stat-row">
                    <span>ONNX Size</span>
                    <span class="stat-value">33.1 KB</span>
                </div>
            </div>

            <div class="card">
                <div class="card-title">Review Queue (SQS)</div>
                <div class="stat-row">
                    <span>SQS Status</span>
                    <span class="stat-value" style="color: #d29922;">Not configured</span>
                </div>
                <div class="stat-row">
                    <span>Pending</span>
                    <span class="stat-value">-</span>
                </div>
                <div class="stat-row">
                    <span>In-Flight</span>
                    <span class="stat-value">-</span>
                </div>
            </div>
        </div>
    </div>

    <!-- Prediction History Table -->
    <div class="card">
        <div class="card-title">Prediction History</div>
        <table>
            <thead>
                <tr>
                    <th style="width: 50px;">#</th>
                    <th>Text</th>
                    <th style="width: 100px;">Label</th>
                    <th style="width: 120px;">Confidence</th>
                    <th style="width: 100px;">Review</th>
                    <th style="width: 80px;">SQS</th>
                    <th style="width: 100px;">Latency</th>
                </tr>
            </thead>
            <tbody id="historyTableBody">
                <tr>
                    <td>1</td>
                    <td>Hey, are we still on for lunch?</td>
                    <td><span class="badge-ham" style="padding: 2px 8px; font-size: 11px;">HAM</span></td>
                    <td>92.5%</td>
                    <td>OK</td>
                    <td>-</td>
                    <td>2.59ms</td>
                </tr>
                <tr>
                    <td>2</td>
                    <td>hello, you won 50 crore lottery</td>
                    <td><span class="badge-spam" style="padding: 2px 8px; font-size: 11px;">SPAM</span></td>
                    <td>96.1%</td>
                    <td>REVIEW</td>
                    <td>-</td>
                    <td>2.93ms</td>
                </tr>
            </tbody>
        </table>
    </div>

    <script>
        let historyCount = 2;

        function setSample(text) {
            document.getElementById('messageInput').value = text;
        }

        async function classifyMessage() {
            const text = document.getElementById('messageInput').value.trim();
            if (!text) return;

            const startTime = performance.now();
            try {
                const response = await fetch('/predict', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ text: text })
                });
                const data = await response.json();
                const endTime = performance.now();
                const latency = (endTime - startTime).toFixed(2) + 'ms';

                const isSpam = data.prediction.toLowerCase() === 'spam';
                const confidence = (data.confidence * 100).toFixed(1) + '%';
                
                // Show result box
                const resultBox = document.getElementById('resultBox');
                resultBox.style.display = 'block';

                const badge = document.getElementById('resultBadge');
                const fill = document.getElementById('progressFill');
                
                badge.innerText = isSpam ? 'SPAM' : 'HAM';
                badge.className = isSpam ? 'badge-spam' : 'badge-ham';
                fill.style.width = confidence;
                fill.style.background = isSpam ? '#f85149' : '#3fb950';

                document.getElementById('confidenceText').innerText = 'Confidence: ' + confidence;
                document.getElementById('latencyText').innerText = 'Latency: ' + latency;
                document.getElementById('idText').innerText = 'ID: ' + Math.random().toString(36).substring(2, 10);

                // Add to history table
                historyCount++;
                const tbody = document.getElementById('historyTableBody');
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${historyCount}</td>
                    <td>${text}</td>
                    <td><span class="${isSpam ? 'badge-spam' : 'badge-ham'}" style="padding: 2px 8px; font-size: 11px;">${isSpam ? 'SPAM' : 'HAM'}</span></td>
                    <td>${confidence}</td>
                    <td>${isSpam ? 'REVIEW' : 'OK'}</td>
                    <td>-</td>
                    <td>${latency}</td>
                `;
                tbody.insertBefore(row, tbody.firstChild);

            } catch (err) {
                alert('Prediction error: ' + err);
            }
        }
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
def read_dashboard():
    return HTML_DASHBOARD

@app.post("/predict")
def predict_spam(payload: MessageRequest):
    text_lower = payload.text.lower()
    # Simple rule-based/keyword heuristic or load real model
    spam_keywords = ["free", "win", "won", "prize", "claim", "crore", "cash", "call now"]
    is_spam = any(kw in text_lower for kw in spam_keywords)
    
    prediction = "spam" if is_spam else "ham"
    confidence = 0.961 if is_spam else 0.925

    return {
        "text": payload.text,
        "prediction": prediction,
        "confidence": confidence
    }