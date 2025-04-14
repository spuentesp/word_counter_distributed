#include "WorkerImpl.h"
#include <fstream>
#include <sstream>
#include <unordered_set>
#include <filesystem>

using namespace WordCounter;

SearchResult WorkerImpl::searchWordsWithContext(const std::string& filepath, const StringList& words, const Ice::Current&) {
    std::map<std::string, int> counts;
    StringList contexts;
    std::unordered_set<std::string> targets(words.begin(), words.end());

    // Abrir el archivo
    std::ifstream file(filepath);
    if (!file.is_open()) {
        throw std::runtime_error("No se pudo abrir el archivo: " + filepath);
    }

    // Leer línea por línea
    std::string line;
    while (std::getline(file, line)) {
        std::istringstream stream(line);
        std::string word;
        while (stream >> word) {
            if (targets.count(word)) {
                counts[word]++;
                contexts.push_back(line);
            }
        }
    }

    file.close();

    // Devolver los resultados
    SearchResult result;
    result.counts = counts;
    result.contexts = contexts;
    return result;
}