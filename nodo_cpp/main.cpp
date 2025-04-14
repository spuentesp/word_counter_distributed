#include "WorkerImpl.h"
#include <Ice/Ice.h>
#include <iostream>
#include <memory>

int main(int argc, char* argv[]) {
    try {
        std::cout << "[INFO] Iniciando el nodo C++..." << std::endl;

        auto communicator = Ice::initialize(argc, argv);
        std::cout << "[INFO] Communicator inicializado." << std::endl;

        auto adapter = communicator->createObjectAdapterWithEndpoints("CppWorkerAdapter", "default -p 10000");
        std::cout << "[INFO] Adaptador creado en el puerto 10000." << std::endl;

        Ice::ObjectPtr iceServant = new WordCounter::WorkerImpl();
        adapter->add(iceServant, Ice::stringToIdentity("CppWorker"));
        std::cout << "[INFO] Servant registrado con ID 'CppWorker'." << std::endl;

        adapter->activate();
        std::cout << "[INFO] Adaptador activado. Esperando conexiones..." << std::endl;

        communicator->waitForShutdown();
        std::cout << "[INFO] Apagando el nodo C++..." << std::endl;
    } catch (const std::exception& e) {
        std::cerr << "[ERROR] Excepción: " << e.what() << std::endl;
        return 1;
    }

    return 0;
}
