# EXASPERATION Project Organization

## Directory Structure Reorganization

The EXASPERATION project has been reorganized to follow a more structured approach, improving both maintainability and GitHub compatibility. This document summarizes the changes made.

## Key Changes

1. **Script Organization**
   - Created a structured `scripts` directory with subdirectories:
     - `run/`: Scripts for running and controlling services
     - `setup/`: Installation and configuration scripts
     - `db/`: Database management scripts
     - `tests/`: Testing scripts
     - `utilities/`: Miscellaneous utility scripts

2. **Path References**
   - Updated scripts to use relative paths that work regardless of installation location
   - Implemented the PROJECT_ROOT pattern in scripts for consistent path resolution

3. **Documentation Improvements**
   - Created README files for each script directory explaining its purpose
   - Created FILETREE.md documenting the entire project structure
   - Added usage examples to script documentation

4. **Cleanup**
   - Removed temporary files and backups
   - Moved miscellaneous scripts to appropriate directories
   - Cleaned up Python cache files

5. **Backwards Compatibility**
   - Added symlinks in the root directory for key scripts (start_all.sh, stop_all.sh)
   - Maintained consistent script behavior regardless of call location

## Root Directory

The root directory now contains only the essential files:
- Documentation (README.md, FILETREE.md, etc.)
- Configuration files (docker-compose.yml, .env.example)
- Requirement files (*.requirements.txt)
- Symlinks to key scripts

## Script Standardization

All scripts now follow a standardized pattern:
1. Determine the project root directory using relative path resolution
2. Use consistent color-coded output formatting
3. Include error handling and prerequisite checking
4. Provide helpful messages when errors occur

## GitHub Integration

The reorganization makes the project more GitHub-friendly by:
1. Using relative paths that work in any clone location
2. Following standard open-source project conventions
3. Providing clear documentation for contributors
4. Maintaining a clean root directory