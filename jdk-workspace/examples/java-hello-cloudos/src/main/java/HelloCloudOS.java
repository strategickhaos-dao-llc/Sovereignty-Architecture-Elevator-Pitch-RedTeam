/**
 * Hello CloudOS - Strategickhaos JDK Workspace Example
 * 
 * A simple Java application demonstrating the CloudOS JDK workspace.
 * 
 * LLM Directive: This is a minimal example. Extend to demonstrate:
 * - Spring Boot integration
 * - Kubernetes client usage
 * - Discord bot SDK integration
 */
public class HelloCloudOS {
    
    private static final String VERSION = "0.1.0";
    private static final String WORKSPACE = System.getenv("WORKSPACE_DIR") != null 
        ? System.getenv("WORKSPACE_DIR") 
        : "/workspace";
    
    public static void main(String[] args) {
        System.out.println("╔════════════════════════════════════════════════╗");
        System.out.println("║     Strategickhaos CloudOS JDK Workspace       ║");
        System.out.println("║     Sovereignty Architecture Control Plane     ║");
        System.out.println("╚════════════════════════════════════════════════╝");
        System.out.println();
        
        printSystemInfo();
        printJavaInfo();
        
        if (args.length > 0) {
            System.out.println("\nArguments received:");
            for (int i = 0; i < args.length; i++) {
                System.out.printf("  [%d] %s%n", i, args[i]);
            }
        }
        
        System.out.println("\n🚀 CloudOS JDK workspace is ready!");
        System.out.println("   Debug port: 5005");
        System.out.println("   Workspace:  " + WORKSPACE);
    }
    
    private static void printSystemInfo() {
        System.out.println("System Information:");
        System.out.println("  OS:        " + System.getProperty("os.name") + " " + System.getProperty("os.version"));
        System.out.println("  Arch:      " + System.getProperty("os.arch"));
        System.out.println("  User:      " + System.getProperty("user.name"));
        System.out.println("  Home:      " + System.getProperty("user.home"));
    }
    
    private static void printJavaInfo() {
        System.out.println("\nJava Information:");
        System.out.println("  Version:   " + System.getProperty("java.version"));
        System.out.println("  Vendor:    " + System.getProperty("java.vendor"));
        System.out.println("  VM:        " + System.getProperty("java.vm.name"));
        System.out.println("  Runtime:   " + System.getProperty("java.runtime.version"));
        System.out.println("  JAVA_HOME: " + System.getenv("JAVA_HOME"));
    }
}
