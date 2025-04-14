FROM gradle:8.5-jdk21

WORKDIR /app

# Copy just what's needed
COPY nodo_java/ ./nodo_java/
COPY shared/ ./shared/

# Switch to the correct subproject
WORKDIR /app/nodo_java

# Create the fat JAR
RUN gradle shadowJar

EXPOSE 10000

CMD ["java", "-jar", "build/libs/nodo_java-all.jar"]
