document.addEventListener('DOMContentLoaded', function () {
  const box = document.getElementById('chatMessages');
  const input = document.getElementById('chatInput');
  const send = document.getElementById('chatSend');

  function addMsg(text, who) {
    const div = document.createElement('div');
    div.className = 'msg ' + who;
    div.textContent = text;
    box.appendChild(div);
    box.scrollTop = box.scrollHeight;
  }

  function ask() {
    const text = input.value.trim();
    if (!text) return;
    addMsg(text, 'user');
    input.value = '';
    const thinking = document.createElement('div');
    thinking.className = 'msg bot';
    thinking.textContent = '…';
    box.appendChild(thinking);
    box.scrollTop = box.scrollHeight;

    fetch('/api/ai/assistant', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: text })
    })
      .then(r => r.json())
      .then(data => { thinking.textContent = data.reply; })
      .catch(() => { thinking.textContent = "I couldn't reach the AI engine — please try again."; });
  }

  send.addEventListener('click', ask);
  input.addEventListener('keydown', e => { if (e.key === 'Enter') ask(); });
});
