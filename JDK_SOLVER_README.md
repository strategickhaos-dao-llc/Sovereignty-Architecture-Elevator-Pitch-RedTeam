# CloudOS JDK Solver

**Java Development Kit Management System for Strategic Khaos Cloud Operating System**

## Overview

The CloudOS JDK Solver is a comprehensive Java Development Kit management system designed specifically for the Strategic Khaos Cloud Operating System. It provides seamless installation, version management, and integration of OpenJDK (including the latest OpenJDK 25) into the CloudOS environment.

## Features

- 🚀 **Multi-Version Support**: Install and manage multiple JDK versions (11, 17, 21, 25)
- 🔄 **Easy Version Switching**: Switch between JDK versions instantly
- ✅ **Automated Verification**: Built-in testing and verification of JDK installations
- 🐳 **Docker Integration**: Pre-configured Docker containers with JDK support
- 🏗️ **Build Tools Included**: Maven and Gradle pre-installed for Java project management
- 🔍 **Health Checks**: Automatic health monitoring for JDK services

## Quick Start

### Using the JDK Solver Script

```bash
# Make the script executable (first time only)
chmod +x jdk-solver.sh

# Install OpenJDK 25
./jdk-solver.sh install 25

# Set as active JDK
./jdk-solver.sh use 25

# Verify installation
./jdk-solver.sh verify

# List all installed JDKs
./jdk-solver.sh list
```

### Using with Docker (CloudOS)

```bash
# Build the JDK-enabled CloudOS container
docker build -f Dockerfile.jdk -t cloudos-jdk:latest .

# Start CloudOS with JDK support
docker compose -f docker-compose-cloudos.yml up -d jdk-workspace

# Access the JDK workspace
docker exec -it cloudos-jdk bash

# Inside the container, verify Java
java -version
javac -version
mvn -version
gradle -version
```

### Using with Full CloudOS Stack

```bash
# Start all CloudOS services including JDK workspace
docker compose -f docker-compose-cloudos.yml up -d

# Access the Java development environment
docker exec -it cloudos-jdk bash

# Or on Windows using PowerShell
.\start-cloudos.ps1
```

## JDK Solver Commands

### Installation Commands

```bash
# Install specific JDK version
./jdk-solver.sh install <version>

# Example: Install OpenJDK 25
./jdk-solver.sh install 25

# Example: Install OpenJDK 21
./jdk-solver.sh install 21
```

### Version Management

```bash
# Set active JDK version
./jdk-solver.sh use <version>

# Show current active JDK
./jdk-solver.sh current

# List all installed JDKs
./jdk-solver.sh list
```

### Verification & Testing

```bash
# Verify current JDK
./jdk-solver.sh verify

# Verify specific JDK version
./jdk-solver.sh verify 25

# Run comprehensive tests
./jdk-solver.sh test
```

### Maintenance

```bash
# Remove a JDK version
./jdk-solver.sh remove <version>

# Example: Remove JDK 17
./jdk-solver.sh remove 17
```

## Supported JDK Versions

| Version | Status | Description |
|---------|--------|-------------|
| **25** | ✅ Latest | OpenJDK 25 (Latest LTS) |
| **21** | ✅ Stable | OpenJDK 21 LTS |
| **17** | ✅ Stable | OpenJDK 17 LTS |
| **11** | ✅ Stable | OpenJDK 11 LTS |

## Environment Configuration

### Shell Integration

Add to your `~/.bashrc` or `~/.zshrc`:

```bash
# CloudOS JDK Configuration
export JDK_HOME_BASE=/opt/jdk
export JAVA_HOME=$JDK_HOME_BASE/current
export PATH=$JAVA_HOME/bin:$PATH

# Optional: Maven and Gradle
export MAVEN_HOME=/opt/maven
export GRADLE_HOME=/opt/gradle
export PATH=$MAVEN_HOME/bin:$GRADLE_HOME/bin:$PATH
```

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `JDK_HOME_BASE` | `/opt/jdk` | Base directory for JDK installations |
| `JAVA_HOME` | `/opt/jdk/current` | Active JDK home directory |
| `CLOUDOS_JDK_CONFIG` | `~/.cloudos/jdk-config.yaml` | JDK configuration file |

## Docker Integration

### JDK Workspace Service

The CloudOS JDK workspace provides:

- **OpenJDK 25** pre-installed and configured
- **Maven 3.9.6** for dependency management
- **Gradle 8.5** for build automation
- **Persistent workspace** at `/workspace`
- **Debug port** exposed on 5005
- **Application port** exposed on 8888

### Accessing Services

| Service | URL | Description |
|---------|-----|-------------|
| Java Workspace | `http://localhost:8888` | Java application port |
| Debug Port | `localhost:5005` | Remote debugging |
| Traefik Route | `http://java.localhost` | Traefik-routed access |

### Building Java Projects

```bash
# Enter the JDK workspace
docker exec -it cloudos-jdk bash

# Navigate to your project
cd /workspace/my-java-project

# Build with Maven
mvn clean install

# Build with Gradle
gradle build

# Run application
java -jar target/my-app.jar
```

## CloudOS Integration

### Architecture Overview

```
┌─────────────────────────────────────────────────┐
│           CloudOS Infrastructure                 │
├─────────────────────────────────────────────────┤
│                                                  │
│  ┌──────────────┐      ┌──────────────┐        │
│  │   Desktop    │      │   Terminal   │        │
│  │  (VS Code)   │      │   (Wetty)    │        │
│  └──────────────┘      └──────────────┘        │
│                                                  │
│  ┌──────────────────────────────────┐          │
│  │    JDK Workspace (NEW)            │          │
│  │  - OpenJDK 25                     │          │
│  │  - Maven & Gradle                 │          │
│  │  - Debug Support                  │          │
│  └──────────────────────────────────┘          │
│                                                  │
│  ┌──────────────┐      ┌──────────────┐        │
│  │  PostgreSQL  │      │    Redis     │        │
│  └──────────────┘      └──────────────┘        │
│                                                  │
│  ┌──────────────┐      ┌──────────────┐        │
│  │   Keycloak   │      │    MinIO     │        │
│  └──────────────┘      └──────────────┘        │
│                                                  │
└─────────────────────────────────────────────────┘
```

### Service Dependencies

The JDK workspace integrates with:
- **PostgreSQL**: Database connectivity via JDBC
- **Redis**: Caching and session management
- **Qdrant**: Vector database for AI features
- **MinIO**: Object storage for artifacts
- **Keycloak**: Authentication and authorization

## Example Use Cases

### 1. Spring Boot Application

```bash
# Create a new Spring Boot project
curl https://start.spring.io/starter.zip \
  -d dependencies=web,data-jpa,postgresql \
  -d javaVersion=25 \
  -d type=maven-project \
  -o demo.zip

# Extract and build
unzip demo.zip -d /workspace/demo
cd /workspace/demo
mvn spring-boot:run
```

### 2. Microservices Development

```bash
# Build multiple services
cd /workspace/service-a
mvn clean package

cd /workspace/service-b
gradle build

# Run with Docker Compose
docker compose up
```

### 3. Remote Debugging

```java
// In your IDE, configure remote debugging:
// Host: localhost
// Port: 5005

// Start your application with debug enabled
java -agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=*:5005 \
  -jar target/myapp.jar
```

## Troubleshooting

### JDK Not Found

```bash
# Verify installation
./jdk-solver.sh verify

# Check current JDK
./jdk-solver.sh current

# List all JDKs
./jdk-solver.sh list
```

### Docker Container Issues

```bash
# Check container logs
docker logs cloudos-jdk

# Restart container
docker restart cloudos-jdk

# Rebuild container
docker compose -f docker-compose-cloudos.yml build jdk-workspace
docker compose -f docker-compose-cloudos.yml up -d jdk-workspace
```

### Environment Variables Not Set

```bash
# Inside container, check environment
docker exec cloudos-jdk env | grep JAVA

# Manually set if needed
export JAVA_HOME=/opt/jdk/current
export PATH=$JAVA_HOME/bin:$PATH
```

### Compilation Errors

```bash
# Verify Java compiler
javac -version

# Check Java version
java -version

# Run verification test
./jdk-solver.sh verify
```

## Performance Optimization

### Memory Settings

```bash
# Set JVM memory options
export JAVA_OPTS="-Xms512m -Xmx2048m -XX:+UseG1GC"

# Run application with custom memory
java $JAVA_OPTS -jar myapp.jar
```

### Build Optimization

```bash
# Maven parallel builds
mvn clean install -T 4

# Gradle parallel builds
gradle build --parallel --max-workers=4
```

## Security Considerations

- ✅ JDK installations are verified with checksums
- ✅ Containers run as non-root user (`cloudos`)
- ✅ Debug port (5005) should be restricted in production
- ✅ Regular updates recommended for security patches

## Contributing

Contributions to improve the JDK Solver are welcome! Please follow the Strategic Khaos contribution guidelines.

## Support

- **Documentation**: This file
- **Issues**: GitHub Issues
- **Community**: [Discord Server](https://discord.gg/strategickhaos)
- **Wiki**: [CloudOS Documentation](https://wiki.strategickhaos.internal)

## License

MIT License - see [LICENSE](LICENSE) file

---

**Built with 🔥 by the Strategickhaos Swarm Intelligence collective**

*Empowering Java development on sovereign cloud infrastructure*
