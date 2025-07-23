from flask import Flask, request, jsonify, render_template_string
import requests
import os

app = Flask(__name__)
OLLAMA_API_URL = os.environ.get("OLLAMA_API_URL", "http://localhost:11434")

HTML = """
<!DOCTYPE html>
<html>
<head>
  <title>Ollama LLM Prompt</title>
</head>
<body>
  <h2>Ask Ollama</h2>
  <form id="prompt-form">
    <textarea name="prompt" rows="4" cols="50" placeholder="Enter your prompt here..."></textarea><br>
    <button type="submit">Send</button>
  </form>
  <pre id="response"></pre>

  <script>
    const form = document.getElementById('prompt-form');
    const responseElem = document.getElementById('response');

    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const formData = new FormData(form);
      const prompt = formData.get("prompt");

      responseElem.textContent = "Waiting for response...";
      const res = await fetch("/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt })
      });
      const data = await res.json();
      responseElem.textContent = data.response || "No response";
    });
  </script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML)

@app.route("/ask", methods=["POST"])
def ask():
    user_prompt = request.json.get("prompt", "")
    response = requests.post(f"{OLLAMA_API_URL}/api/generate", json={
        "model": "llama3",
        "prompt": user_prompt,
    })
    output = response.json()
    return jsonify({"response": output.get("response", "Error")})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
