import os
from flask import Flask, render_template_string, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app) # Permite que qualquer pessoa acesse de qualquer lugar

# Armazenamento em memória (Para chat permanente 24h, o ideal seria um Banco de Dados Redis)
mensagens = [{"u": "Sistema", "m": "Bem-vindo ao Chat Global 2026!", "c": "green"}]

HTML = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chat Global</title>
    <style>
        body { background: #0a0a0a; color: white; font-family: sans-serif; margin: 0; display: flex; flex-direction: column; height: 100vh; }
        #chat { flex-grow: 1; overflow-y: auto; padding: 15px; background: #000; }
        .input-area { padding: 15px; background: #161616; display: flex; gap: 10px; }
        input { flex-grow: 1; padding: 12px; border-radius: 5px; border: 1px solid #444; background: #222; color: white; }
        button { padding: 12px; border: none; border-radius: 5px; background: #3498db; color: white; font-weight: bold; cursor: pointer; }
        .purple { color: #a29bfe; font-weight: bold; }
        .green { color: #55efc4; font-weight: bold; }
        .red { color: #ff7675; font-weight: bold; }
        #setup { position: fixed; inset: 0; background: #0a0a0a; display: flex; flex-direction: column; justify-content: center; align-items: center; z-index: 100; }
    </style>
</head>
<body>
    <div id="setup">
        <h2>Enter Your NickName:</h2>
        <input type="text" id="u" style="max-width: 300px;" placeholder="Nickname...">
        <div style="margin: 15px 0;">
            <button onclick="setCol('purple')" style="background:#8e44ad">Roxo</button>
            <button onclick="setCol('green')" style="background:#27ae60">Verde</button>
            <button onclick="setCol('red')" style="background:#c0392b">Vermelho</button>
        </div>
        <button onclick="join()" style="width: 300px;">ENTRAR</button>
    </div>

    <div id="chat"></div>
    <div class="input-area">
        <input type="text" id="m" placeholder="Escreva...">
        <button onclick="send()">Enviar</button>
    </div>

    <script>
        let nick = "", cor = "purple";
        function setCol(c) { cor = c; }
        function join() {
            nick = document.getElementById('u').value.trim();
            if(nick) {
                document.getElementById('setup').style.display='none';
                setInterval(atualizar, 1500);
            }
        }
        function send() {
            let msg = document.getElementById('m').value;
            if(!msg) return;
            fetch('/send', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({u: nick, m: msg, c: cor})
            });
            document.getElementById('m').value = '';
        }
        async function atualizar() {
            let res = await fetch('/get_messages');
            let data = await res.json();
            let chat = document.getElementById('chat');
            chat.innerHTML = data.map(msg => `<p><span class="${msg.c}">[${msg.u}]:</span> ${msg.m}</p>`).join('');
            chat.scrollTop = chat.scrollHeight;
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index(): return render_template_string(HTML)

@app.route('/send', methods=['POST'])
def send():
    data = request.json
    mensagens.append(data)
    if len(mensagens) > 50: mensagens.pop(0)
    return jsonify({"ok": True})

@app.route('/get_messages')
def get(): return jsonify(mensagens)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
