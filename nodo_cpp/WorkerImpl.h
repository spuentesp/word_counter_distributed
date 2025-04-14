#pragma once
#include <WordCount.h>
#include <map>
#include <vector>
#include <string>

namespace WordCounter {

class WorkerImpl : public Worker {
public:
    virtual SearchResult searchWordsWithContext(const std::string& chunk, const StringList& words, const Ice::Current&) override;
};

}
