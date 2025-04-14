import sys
import Ice
import os
from pathlib import Path
from collections import Counter

Ice.loadSlice('../shared/WordCount.ice')
import WordCounter

def merge_counts(counts_list):
    total = Counter()
    for c in counts_list:
        total.update(c)
    return total

def split_file(filepath, num_chunks):
    Path("/tmp/chunks").mkdir(parents=True, exist_ok=True)
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()

    chunk_size = len(lines) // num_chunks
    chunks = []

    for i in range(num_chunks):
        start = i * chunk_size
        end = None if i == num_chunks - 1 else (i + 1) * chunk_size
        chunk_lines = lines[start:end]

        chunk_path = f"/tmp/chunks/chunk_{i}.txt"
        with open(chunk_path, "w", encoding="utf-8") as chunk_file:
            chunk_file.writelines(chunk_lines)

        chunks.append(chunk_path)

    return chunks

def main():
    with Ice.initialize(sys.argv) as communicator:
        workers = [
            ("JavaWorker", "nodo_java", 10000),
            ("CppWorker", "nodo_cpp", 10001),
        ]

        print("📂 Ruta del archivo a procesar:")
        filepath = input("> ").strip()

        if not os.path.isfile(filepath):
            print("❌ Archivo no encontrado.")
            return

        print("🔍 Palabras a buscar (separadas por espacio):")
        palabras = input("> ").strip().lower().split()
        if not palabras:
            print("❌ Debes ingresar al menos una palabra.")
            return

        chunk_paths = split_file(filepath, len(workers))

        proxies = []
        for name, host, port in workers:
            proxy = WordCounter.WorkerPrx.checkedCast(
                communicator.stringToProxy(f"{name}:default -h {host} -p {port}")
            )
            if not proxy:
                print(f"❌ No se pudo conectar con {name}")
                return
            proxies.append(proxy)

        all_counts = []
        all_contexts = []

        for i, (proxy, chunk_path) in enumerate(zip(proxies, chunk_paths)):
            print(f"📤 Enviando chunk {i} → {proxy.ice_getIdentity().name}")
            result = proxy.searchWordsWithContext(chunk_path, palabras)
            all_counts.append(result.counts)
            all_contexts.extend(result.contexts)

        final_counts = merge_counts(all_counts)

        print("\n📊 Conteo total de palabras:")
        for word in palabras:
            print(f"{word}: {final_counts.get(word, 0)}")

        respuesta = input("\n📝 ¿Deseas guardar las referencias encontradas en un archivo? (y/n): ").strip().lower()
        if respuesta == "y":
            output_path = "referencias_output.txt"
            with open(output_path, "w", encoding="utf-8") as f:
                for ctx in all_contexts:
                    f.write(ctx + "\n")
            print(f"✅ Referencias guardadas en {output_path}")
        else:
            print("❎ Referencias descartadas.")

if __name__ == "__main__":
    main()
