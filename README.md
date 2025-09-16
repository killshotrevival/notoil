# NoToil - SRE Automation CLI

> *"Toil is the kind of work tied to running a production service that tends to be manual, repetitive, automatable, tactical, devoid of enduring value, and that scales linearly as a service grows."*
> 
> — Chapter 5, Site Reliability Engineering: How Google Runs Production Systems

## Overview

**NoToil** is a production-grade CLI tool designed by an experienced SRE engineer to eliminate the repetitive, manual tasks that plague production environments. Built with enterprise-grade reliability in mind, this tool addresses the real-world challenges faced by SRE teams managing complex, distributed systems at scale.

## Why NoToil?

As an SRE engineer with 5+ years of experience managing production systems, I've learned that **automation is not just about efficiency—it's about survival**. When you're responsible for systems that serve millions of users, every manual step is a potential failure point. NoToil transforms those critical, time-sensitive operations into reliable, repeatable commands.

## Core Capabilities

### 🔐 **TOTP Token Generation**
```bash
notoil get-totp <secret_key>
```
Generate time-based one-time passwords for secure access to production systems. Essential for MFA-protected infrastructure and compliance requirements.

### 🌐 **Network Subnet Validation**
```bash
notoil ip-network <ip_address> <subnet>
```
Quickly validate IP addresses against CIDR blocks. Critical for firewall rules, load balancer configurations, and network security audits.

### ☸️ **Kubernetes Operations**

#### Pod Management
```bash
Usage: notoil k8s [OPTIONS] COMMAND [ARGS]...

  Kubernetes commands

Options:
  --help  Show this message and exit.

Commands:
  cnp  Create a network pod
  dnp  Delete a network pod
  lnp  List all network pods in a namespace
  mp   Match a pod by name (substring) in a namespace
  re   Create command to execute into pod as root user
```

## Architecture & Design Principles

### **Production-Ready Reliability**
- **Zero-downtime operations**: All commands are designed to be non-disruptive
- **Automatic cleanup**: Temporary resources are automatically managed and cleaned up
- **Error handling**: Comprehensive error handling with meaningful feedback
- **Resource management**: Efficient use of cluster resources with proper cleanup

### **Security-First Approach**
- **Least privilege access**: Commands only request the minimum permissions needed
- **Secure defaults**: All operations use secure configurations by default
- **Temporary credentials**: No persistent credentials are stored

### **Enterprise Integration**
- **Kubernetes-native**: Built using official Kubernetes Python client
- **Multi-cluster support**: Designed to work across different cluster configurations
- **Namespace awareness**: Proper namespace handling for multi-tenant environments
- **RBAC compatible**: Respects existing role-based access controls

## Installation

```bash
# From source
git clone <repository>
cd notoil
pip install -e .
```

## Dependencies

- **Python 3.8+**
- **Kubernetes Python Client** - For cluster operations
- **Click** - For robust CLI framework
- **PyOTP** - For TOTP generation

## Use Cases

### **Incident Response**
When a production incident occurs, every second counts. NoToil provides the commands you need to:
- Quickly identify affected containers
- Access nodes for emergency debugging
- Generate secure access tokens
- Validate network configurations

### **Day-to-Day Operations**
Eliminate the repetitive tasks that consume SRE time:
- Container ID lookups for monitoring integration
- Network validation for deployment pipelines
- TOTP generation for secure access
- Pod debugging without manual kubectl commands


## Contributing

This tool is built on the principle that **good SRE tools should be shared**. Contributions are welcome, especially:
- Additional Kubernetes operations
- Network security tools
- Monitoring integrations
- Performance optimizations

---

*"In production, automation isn't a luxury—it's a necessity. NoToil makes that automation accessible, reliable, and production-ready."*