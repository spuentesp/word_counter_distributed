#!/bin/bash

echo "🔄 Regenerando slices..."

# Python
slice2py shared/WordCount.ice --output-dir maestro/

# Java
slice2java shared/WordCount.ice --output-dir nodo_java/src/main/java

# C++
slice2cpp shared/WordCount.ice --output-dir nodo_cpp/

echo "✅ Slices regenerados correctamente."
