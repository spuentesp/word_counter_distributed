module WordCounter {

    sequence<string> StringList;

    dictionary<string, int> WordCountMap;

    struct SearchResult {
        WordCountMap counts;
        StringList contexts;
    };

    interface Worker {
        SearchResult searchWordsWithContext(string filepath, StringList words);
    };
};

