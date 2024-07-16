///usr/bin/true; exec /usr/bin/env go run "$0" "$@"

package main

import (
	"fmt"
	"os"
	"os/exec"
	"strconv"
	"strings"
)

// Function to write a NATS configuration file
func writeConfigFile(filename string, clientPort, clusterPort int, routes []string) error {

	serverName := strings.TrimSuffix(filename, ".conf")
	logFile := fmt.Sprintf("%s.log", serverName)

	configContent := fmt.Sprintf(`
port: %d
server_name: %s

log_file: "%s"
debug: false
trace: true

accounts: {
  SYSDBA: {
    users: [{user: sys, password: pass}]
  }
}


system_account: SYSDBA

cluster {
  name: test-cluster
  listen: 0.0.0.0:%d

  routes = [
    %s
  ]
}
`, clientPort, serverName, logFile, clusterPort, strings.Join(routes, "\n    "))
	return os.WriteFile(filename, []byte(configContent), 0644)

}

// Function to start a NATS server in a tmux session
func startNatsServer(sessionName, configFile string) error {
	fmt.Printf ("config: %s\n", configFile)
	cmd := exec.Command("tmux", "new-session", "-d", "-s", sessionName, "nats-server", "-c", configFile)
	return cmd.Run()
}

func main() {
	numServers := 3
	var err error = nil
	if len(os.Args) > 1 {
		numServers, err = strconv.Atoi(os.Args[1])
		if err != nil {
			fmt.Println("Invalid number of servers")
			return
		}
	}

	err = os.Mkdir("/tmp/nats", 0755) // 0755 is the permission mode for the directory
	if err != nil {
		fmt.Printf("Directory: %v\n", err)
	}

	// Base ports for the servers
	baseClientPort := 4222
	baseClusterPort := 6222

	for i := 0; i < numServers; i++ {
		clientPort := baseClientPort + i
		clusterPort := baseClusterPort + i
		configFilename := fmt.Sprintf("/tmp/nats/nats%d.conf", i)

		// Generate routes for the cluster configuration
		var routes []string
		for j := 0; j < numServers; j++ {
			if j != i {
				routes = append(routes, fmt.Sprintf("nats-route://localhost:%d", baseClusterPort+j))
			}
		}

		if err := writeConfigFile(configFilename, clientPort, clusterPort, routes); err != nil {
			fmt.Printf("Failed to write configuration file: %s\n", configFilename)
			continue
		}

		sessionName := fmt.Sprintf("nats%d", i)
		if err := startNatsServer(sessionName, configFilename); err != nil {
			fmt.Printf("Failed to start NATS server in tmux session: %s\n", sessionName)
			continue
		}
	}

	fmt.Printf("Started %d NATS servers in tmux sessions.\n", numServers)
}
