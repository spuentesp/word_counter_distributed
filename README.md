# Proyecto: Contador de Palabras Distribuido

Este proyecto implementa un sistema distribuido usando ZeroC ICE, donde:
- Un nodo maestro (Python) distribuye trabajo.
- Nodos trabajadores (Java y C++) procesan archivos de texto.
- Los resultados son combinados para obtener estadísticas globales.

Estructura:
- `maestro`: Coordinador en Python.
- `nodo_java`: Trabajador en Java.
- `nodo_cpp`: Trabajador en C++.
- `shared`: Archivos compartidos (.ice).
- `texts`: Archivos de texto para procesar.

