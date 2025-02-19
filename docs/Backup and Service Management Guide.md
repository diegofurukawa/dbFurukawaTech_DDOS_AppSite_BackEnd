# Backend Backup and Service Management Guide

This guide outlines the procedures for managing and backing up the DDoS Protection Backend Application.

## Table of Contents
- [Service Management](#service-management)
- [Backup Process](#backup-process)
- [File Structure](#file-structure)
- [Quick Reference Commands](#quick-reference-commands)

## Service Management

### Starting the Service
1. Navigate to the project directory:
   ```bash
   cd Documents/GitHub/dbFurukawaTech_DDOS_AppSite_BackEnd/
   ```

2. Start the API service:
   ```bash
   ./scripts/run_api.sh
   ```

## Backup Process

### Viewing File Structure
Before performing a backup, you can view the current file structure while excluding unnecessary directories:

```bash
tree -I '.pytest_cache*|logs*|.venv|venv|backup*|__pycache__'
```

### Performing Backup
1. Navigate to the project directory:
   ```bash
   cd Documents/GitHub/dbFurukawaTech_DDOS_AppSite_BackEnd/
   ```

2. Execute the backup script:
   ```bash
   ./scripts/backup_backend.sh
   ```

The backup script will:
- Create a timestamped backup directory
- Copy all relevant files while excluding unnecessary directories
- Generate a backup log with details of the operation

## File Structure

To view the current file structure excluding specific directories:

```bash
cd Documents/GitHub/dbFurukawaTech_DDOS_AppSite_BackEnd/
tree -I '.pytest_cache*|logs*|old*|.venv|venv|backup*|__pycache__'
```

## Quick Reference Commands

Here's a quick reference for common operations:

```bash
# Start Service
cd Documents/GitHub/dbFurukawaTech_DDOS_AppSite_BackEnd/
./scripts/run_api.sh

# View File Structure
cd Documents/GitHub/dbFurukawaTech_DDOS_AppSite_BackEnd/
tree -I '.pytest_cache*|logs*|old*|.venv|venv|backup*|__pycache__'

# Perform Backup
cd Documents/GitHub/dbFurukawaTech_DDOS_AppSite_BackEnd/
./scripts/backup_backend.sh
```

## Notes

- The backup script excludes the following directories:
  - `.pytest_cache`
  - `logs`
  - `.venv`
  - `venv`
  - `backup`
  - `__pycache__`
- Backups are timestamped for easy identification
- A log file is generated with each backup containing details of the operation

## Troubleshooting

If you encounter issues:

1. Check if you have proper permissions to execute the scripts:
   ```bash
   chmod +x scripts/*.sh
   ```

2. Ensure you're in the correct directory before running commands

3. Verify that all required scripts exist in the `scripts` directory