package WordCounter;
import com.zeroc.Ice.*;

import java.io.*;
import java.util.*;

public class WorkerImpl implements Worker {

    @Override
    public SearchResult searchWordsWithContext(String filepath, String[] words, Current current) {
        Map<String, Integer> counts = new HashMap<>();
        List<String> contexts = new ArrayList<>();
        Map<String, BufferedWriter> wordWriters = new HashMap<>();

        try {
            for (String word : words) {
                counts.put(word, 0);
                File outFile = new File("/app/results/" + word + "_javaworker.txt");
                wordWriters.put(word, new BufferedWriter(new FileWriter(outFile)));
            }

            List<String> allWords = new ArrayList<>();
            try (Scanner scanner = new Scanner(new File(filepath))) {
                while (scanner.hasNext()) {
                    allWords.add(scanner.next());
                }
            }

            for (int i = 0; i < allWords.size(); i++) {
                String currentWord = allWords.get(i).toLowerCase();
                if (Arrays.asList(words).contains(currentWord)) {
                    counts.put(currentWord, counts.get(currentWord) + 1);

                    int start = Math.max(0, i - 15);
                    int end = Math.min(allWords.size(), i + 16);
                    List<String> contextWords = allWords.subList(start, end);
                    String contextLine = "[JavaWorker] ..." + String.join(" ", contextWords) + "...";
                    contexts.add(contextLine);

                    BufferedWriter writer = wordWriters.get(currentWord);
                    for (String w : contextWords) {
                        writer.write(w);
                        writer.newLine();
                    }
                    writer.flush();
                }
            }

            for (BufferedWriter writer : wordWriters.values()) {
                writer.close();
            }

        } catch (IOException e) {
            System.err.println("Error leyendo archivo: " + e.getMessage());
        }

        return new SearchResult(counts, contexts.toArray(new String[0]));
    }
}