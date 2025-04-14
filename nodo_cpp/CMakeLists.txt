cmake_minimum_required(VERSION 3.10)
project(nodo_cpp)

set(CMAKE_CXX_STANDARD 17)

# Directorios de cabeceras
include_directories(
  ${CMAKE_CURRENT_SOURCE_DIR}
  /usr/include/Ice
  /usr/include/IceUtil
)

# Directorio de librerías
link_directories(
  /usr/lib/x86_64-linux-gnu
)

# Archivos fuente
add_executable(nodo_cpp
  main.cpp
  WorkerImpl.cpp
  WordCount.cpp
)

# Enlazar explícitamente con las bibliotecas
target_link_libraries(nodo_cpp
  Ice
  pthread
)
