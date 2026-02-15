#!/usr/bin/env python3
"""
Breeze Options Trader PRO - System Verification Script

Run this to verify your installation is complete and working.
"""

import sys
import os
from pathlib import Path

# ANSI color codes
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def print_header():
    print("\n" + "="*70)
    print("   Breeze Options Trader PRO - System Verification")
    print("="*70 + "\n")

def print_success(msg):
    print(f"{GREEN}✓{RESET} {msg}")

def print_error(msg):
    print(f"{RED}✗{RESET} {msg}")

def print_warning(msg):
    print(f"{YELLOW}⚠{RESET} {msg}")

def print_info(msg):
    print(f"{BLUE}ℹ{RESET} {msg}")

def check_python_version():
    """Check Python version."""
    print("Checking Python version...")
    version = sys.version_info
    
    if version >= (3, 8):
        print_success(f"Python {version.major}.{version.minor}.{version.micro} (Required: 3.8+)")
        return True
    else:
        print_error(f"Python {version.major}.{version.minor}.{version.micro} (Required: 3.8+)")
        return False

def check_dependencies():
    """Check if required packages are installed."""
    print("\nChecking dependencies...")
    
    required = {
        'streamlit': 'Streamlit',
        'pandas': 'Pandas',
        'numpy': 'NumPy',
        'plotly': 'Plotly',
        'breeze_connect': 'Breeze Connect',
    }
    
    all_installed = True
    
    for package, name in required.items():
        try:
            __import__(package)
            print_success(f"{name} installed")
        except ImportError:
            print_error(f"{name} NOT installed")
            all_installed = False
    
    return all_installed

def check_files():
    """Check if required files exist."""
    print("\nChecking required files...")
    
    required_files = [
        'app_enhanced.py',
        'breeze_api_complete.py',
        'option_chain_processor.py',
        'persistence.py',
        'user_config.py',
        'requirements.txt',
    ]
    
    optional_files = [
        'README_PRO.md',
        'QUICKSTART.txt',
        'CHANGELOG_v9.md',
    ]
    
    all_present = True
    
    for file in required_files:
        if Path(file).exists():
            print_success(f"{file}")
        else:
            print_error(f"{file} NOT FOUND")
            all_present = False
    
    print("\nOptional files:")
    for file in optional_files:
        if Path(file).exists():
            print_success(f"{file}")
        else:
            print_warning(f"{file} missing (optional)")
    
    return all_present

def check_directories():
    """Check if required directories exist."""
    print("\nChecking directories...")
    
    required_dirs = ['data', 'logs', 'exports', '.streamlit']
    
    all_present = True
    
    for directory in required_dirs:
        path = Path(directory)
        if path.exists() and path.is_dir():
            print_success(f"{directory}/")
        else:
            print_warning(f"{directory}/ NOT FOUND (will be created)")
            # Create if missing
            try:
                path.mkdir(parents=True, exist_ok=True)
                print_info(f"  Created {directory}/")
            except Exception as e:
                print_error(f"  Failed to create {directory}/: {e}")
                all_present = False
    
    return all_present

def check_database():
    """Check database initialization."""
    print("\nChecking database...")
    
    try:
        from persistence import TradeDB
        db = TradeDB()
        print_success("Database initialized successfully")
        
        # Check if database file exists
        db_path = Path("data/breeze_trader.db")
        if db_path.exists():
            size = db_path.stat().st_size
            print_info(f"  Database file: {size} bytes")
        
        return True
    except Exception as e:
        print_error(f"Database initialization failed: {e}")
        return False

def check_configuration():
    """Check configuration files."""
    print("\nChecking configuration...")
    
    try:
        import user_config
        print_success("user_config.py loaded successfully")
        
        # Validate configuration
        errors = user_config.validate_config()
        if errors:
            print_warning("Configuration validation warnings:")
            for error in errors:
                print(f"  - {error}")
        else:
            print_success("Configuration validated")
        
        return len(errors) == 0
    except Exception as e:
        print_error(f"Configuration error: {e}")
        return False

def check_imports():
    """Check if main modules can be imported."""
    print("\nChecking module imports...")
    
    modules = [
        ('breeze_api_complete', 'Complete API Client'),
        ('option_chain_processor', 'Option Chain Processor'),
        ('persistence', 'Database Manager'),
        ('session_manager', 'Session Manager'),
        ('risk_monitor', 'Risk Monitor'),
    ]
    
    all_imported = True
    
    for module, name in modules:
        try:
            __import__(module)
            print_success(f"{name}")
        except Exception as e:
            print_error(f"{name}: {str(e)[:50]}")
            all_imported = False
    
    return all_imported

def run_verification():
    """Run all verification checks."""
    print_header()
    
    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies),
        ("Required Files", check_files),
        ("Directories", check_directories),
        ("Database", check_database),
        ("Configuration", check_configuration),
        ("Module Imports", check_imports),
    ]
    
    results = []
    
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print_error(f"Check failed: {e}")
            results.append((name, False))
    
    # Summary
    print("\n" + "="*70)
    print("   Verification Summary")
    print("="*70 + "\n")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = f"{GREEN}PASS{RESET}" if result else f"{RED}FAIL{RESET}"
        print(f"{status}  {name}")
    
    print("\n" + "-"*70)
    print(f"\nResult: {passed}/{total} checks passed")
    
    if passed == total:
        print(f"\n{GREEN}✓ System verification complete! All checks passed.{RESET}")
        print(f"\n{BLUE}🚀 You're ready to start the application!{RESET}")
        print("\nTo start:")
        print("  Windows: run.bat")
        print("  Linux/Mac: ./run.sh")
        print("\n" + "="*70 + "\n")
        return 0
    else:
        print(f"\n{RED}✗ Some checks failed. Please review errors above.{RESET}")
        print("\nCommon solutions:")
        print("  1. Run setup script: setup.bat (Windows) or ./setup.sh (Linux/Mac)")
        print("  2. Install missing dependencies: pip install -r requirements.txt")
        print("  3. Check README_PRO.md for detailed instructions")
        print("\n" + "="*70 + "\n")
        return 1

if __name__ == "__main__":
    exit_code = run_verification()
    sys.exit(exit_code)
