FROM eclipse-temurin:11

ARG VERSION=0.8.1

ADD https://github.com/SPARQL-Anything/sparql.anything/releases/download/v${VERSION}/sparql-anything-${VERSION}.jar /opt/sparql-anything.jar

ENTRYPOINT ["java", "-jar", "/opt/sparql-anything.jar"]

