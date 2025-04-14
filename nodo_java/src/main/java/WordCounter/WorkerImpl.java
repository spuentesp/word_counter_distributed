package WordCounter;
import com.zeroc.Ice.*;

import java.io.*;
import java.util.*;

public class WorkerImpl implements Worker {

    @Override
    public SearchResult searchWordsWithContext(String chunk, String[] words, Current current) {
        System.out.println("[JavaWorker] Recibido chunk de texto para procesar...");
        // System.out.println(chunk);
        System.out.println("[JavaWorker] Palabras a buscar: " + Arrays.toString(words));
        System.out.println("[JavaWorker] Procesando chunk...");
        Map<String, Integer> counts = new HashMap<>();
        List<String> contexts = new ArrayList<>();

        Set<String> targetWords = new HashSet<>();
        for (String word : words) {
            targetWords.add(word.toLowerCase());
            counts.put(word.toLowerCase(), 0);
        }

        List<String> allWords = new ArrayList<>();
        try (Scanner scanner = new Scanner(chunk)) {
            while (scanner.hasNext()) {
                allWords.add(scanner.next());
            }
        }

        for (int i = 0; i < allWords.size(); i++) {
            String currentWord = allWords.get(i).toLowerCase();
            if (targetWords.contains(currentWord)) {
                counts.put(currentWord, counts.get(currentWord) + 1);

                int start = Math.max(0, i - 15);
                int end = Math.min(allWords.size(), i + 16);
                List<String> contextWords = allWords.subList(start, end);
                String contextLine = "[" +System.getenv().getOrDefault("WORKER_NAME", "JavaWorker")+"] ..." + String.join(" ", contextWords) + "...";
                contexts.add(contextLine);
            }
        }

        return new SearchResult(counts, contexts.toArray(new String[0]));
    }
}
