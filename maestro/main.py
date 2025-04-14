import Ice
import os
import time
from flask import Flask, request, render_template_string
from pathlib import Path
from collections import Counter

Ice.loadSlice('./shared/WordCount.ice')
import WordCounter

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head><title>Word Counter</title></head>
<body>
  <h1>Word Counter</h1>
  <form action="/count" method="post" enctype="multipart/form-data">
    <label>Upload .txt file:</label><br>
    <input type="file" name="file" accept=".txt" required><br><br>
    <label>Words to search (space-separated):</label><br>
    <input type="text" name="words" required><br><br>
    <input type="checkbox" name="with_context"> With context<br><br>
    <input type="submit" value="Process">
  </form>
  {% if error %}
    <p style="color:red;"><strong>Error:</strong> {{ error }}</p>
  {% endif %}
  {% if results %}
    <h2>Results:</h2>
    <ul>
      {% for word, count in results.items() %}
        <li>{{ word }}: {{ count }}</li>
      {% endfor %}
    </ul>
    {% if contexts %}
      <h3>Contexts:</h3>
      <pre>{{ contexts }}</pre>
    {% endif %}
  {% endif %}
</body>
</html>
"""
# Combina múltiples resultados parciales de conteo de palabras
def merge_counts(counts_list):
    total = Counter()
    for c in counts_list:
        total.update(c)
    return total

# Divide el texto completo en `num_chunks` partes basadas en palabras
def split_text(text, num_chunks):
    words = text.split()
    chunk_size = len(words) // num_chunks
    chunks = []

    for i in range(num_chunks):
        start = i * chunk_size
        end = None if i == num_chunks - 1 else (i + 1) * chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)

    return chunks

# Ruta raíz: formulario de entrada
@app.route('/', methods=['GET'])
def index():
    return render_template_string(HTML)

# Procesa el archivo subido y busca palabras en los workers
@app.route('/count', methods=['POST'])
def count():
    # Obtener archivo y palabras a buscar
    file = request.files['file']
    words = request.form['words'].strip().lower().split()
    with_context = 'with_context' in request.form

    # Leer texto y dividir en chunks
    text = file.read().decode('utf-8')
    

    results = Counter()
    all_contexts = []

    # Lista de workers disponibles (nombre lógico, host, puerto)
    workers = [
        ("JavaWorker1", "nodo_java_1", 10000),
        ("JavaWorker2", "nodo_java_2", 10000),
        ("JavaWorker3", "nodo_java_3", 10000),
        ("JavaWorker4", "nodo_java_4", 10000),
    ]

    chunks = split_text(text, len(workers))
    proxies = []

    # Inicializa la comunicación ICE
    with Ice.initialize([]) as communicator:
        # Conecta con cada worker
        for name, host, port in workers:
            max_retries = 5
            retry_delay = 1
            proxy = None

            for attempt in range(1, max_retries + 1):
                try:
                    print(f"🔌 Attempt {attempt}: connecting to {name} at {host}:{port}")
                    proxy = WordCounter.WorkerPrx.checkedCast(
                        communicator.stringToProxy(f"{name}:default -h {host} -p {port}")
                    )
                    if proxy:
                        print(f"✅ Connected to {name}")
                        break
                except Exception as e:
                    last_error = str(e)
                    print(f"❌ Error connecting to {name} (attempt {attempt}): {last_error}")
                time.sleep(retry_delay)
                retry_delay *= 2

            if not proxy:
                return render_template_string(
                    HTML,
                    error=f"❌ No se pudo conectar con {name} en {host}:{port} después de {max_retries} intentos. Último error: {last_error}"
                )

            proxies.append(proxy)

        # Enviar cada chunk al worker correspondiente
        for i, (proxy, chunk) in enumerate(zip(proxies, chunks)):
            try:
                print(f"📤 Sending chunk {i} to {proxy.ice_getIdentity().name}")
                result = proxy.searchWordsWithContext(chunk, words)
                results.update(result.counts)
                if with_context:
                    all_contexts.extend(result.contexts)
            except Exception as e:
                return render_template_string(
                    HTML,
                    error=f"❌ Fallo al procesar con {proxy.ice_getIdentity().name}: {e}"
                )

    # Mostrar resultados en la misma página
    return render_template_string(
        HTML,
        results=results,
        contexts="\n".join(all_contexts) if with_context else None
    )

# Iniciar el servidor Flask
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)