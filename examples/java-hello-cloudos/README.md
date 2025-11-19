# HelloCloudOS - Java Example Application

A demonstration Java application showcasing the CloudOS JDK Solver capabilities.

## Features

- Modern Java syntax (Java 25 features)
- Text blocks, records, and pattern matching
- System and runtime information display
- Memory management visualization

## Building and Running

### Option 1: Direct Compilation

```bash
# Compile
javac HelloCloudOS.java

# Run
java HelloCloudOS
```

### Option 2: Using JDK Solver

```bash
# Ensure JDK 25 is active
../../jdk-solver.sh use 25

# Compile and run
javac HelloCloudOS.java
java HelloCloudOS
```

### Option 3: In CloudOS Docker Container

```bash
# Start CloudOS with JDK support
cd ../..
./start-cloudos-jdk.sh start

# Access the container
docker exec -it cloudos-jdk bash

# Inside the container
cd /home/cloudos/cloudos-repo/examples/java-hello-cloudos
javac HelloCloudOS.java
java HelloCloudOS
```

## Expected Output

```
╔═══════════════════════════════════════════╗
║   CloudOS - Java Development Platform    ║
║   Strategic Khaos DAO LLC                 ║
╚═══════════════════════════════════════════╝

🚀 CloudOS JDK Solver Demo Application
========================================

📊 System Information:
  OS Name:        Linux
  OS Version:     ...
  OS Arch:        amd64
  User:           cloudos
  Working Dir:    /workspace

☕ Java Runtime Information:
  Java Version:   25.0.1
  Java Vendor:    Eclipse Adoptium
  Java Home:      /opt/jdk/current
  VM Name:        OpenJDK 64-Bit Server VM
  VM Version:     25.0.1+8

💾 Memory Information:
  Max Memory:     ...
  Total Memory:   ...
  Free Memory:    ...
  Used Memory:    ...

🎯 CloudOS Java Features:
  ✓ Text Blocks (Java 15+)
  ✓ Records (Java 16+)
  ✓ Pattern Matching (Java 17+)
  ✓ Sequenced Collections (Java 21+)
  ✓ Virtual Threads (Java 21+)
  ✓ OpenJDK 25 Features Available

  Example Record: CloudOSService[name=JDK Solver, version=1.0.0, active=true]
  Pattern Match: String length is 7

✅ CloudOS JDK Solver - Working Perfectly!
🔥 Built with love by the Strategickhaos Swarm Intelligence collective
```

## Requirements

- OpenJDK 25 (installed via JDK Solver)
- CloudOS environment (optional)

## License

MIT License - Part of the Strategic Khaos Sovereignty Architecture project
