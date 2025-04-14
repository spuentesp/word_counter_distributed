#include "WorkerImpl.h"
#include <sstream>
#include <unordered_set>
#include <iostream>
#include <algorithm>
#include <cctype>

using namespace WordCounter;

// Función para convertir a minúsculas (ASCII seguro)
std::string to_lower(const std::string& input) {
    std::string result;
    result.reserve(input.size());
    for (char ch : input) {
        result += std::tolower(static_cast<unsigned char>(ch));
    }
    return result;
}

// Limpia puntuación al inicio y final de la palabra
std::string clean_word(const std::string& word) {
    size_t start = word.find_first_of("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789");
    size_t end = word.find_last_of("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789");

    if (start == std::string::npos) return "";
    return word.substr(start, end - start + 1);
}

SearchResult WorkerImpl::searchWordsWithContext(const std::string& chunk, const StringList& words, const Ice::Current&) {
    std::cout << "[INFO] WorkerImpl::searchWordsWithContext called with " << words.size() << " words.\n";
    std::cout << "[INFO] Chunk size: " << chunk.size() << "\n";

    if (chunk.size() > 300)
        std::cout << "[INFO] Chunk preview: " << chunk.substr(0, 300) << "...\n";
    else
        std::cout << "[INFO] Chunk preview: " << chunk << "\n";

    std::map<std::string, int> counts;
    StringList contexts;
    std::unordered_set<std::string> targets;

    // Normaliza las palabras objetivo
    for (const auto& w : words) {
        targets.insert(to_lower(clean_word(w)));
    }

    std::istringstream input(chunk);
    std::string line;

    while (std::getline(input, line)) {
        std::istringstream stream(line);
        std::string word;
        bool matched = false;

        while (stream >> word) {
            std::string cleaned = to_lower(clean_word(word));
            if (targets.count(cleaned)) {
                counts[cleaned]++;
                matched = true;
            }
        }

        if (matched) {
            contexts.push_back(line);
        }
    }

    SearchResult result;
    result.counts = counts;
    result.contexts = contexts;
    return result;
}
