"""
Check repository size before pushing to GitHub
Helps identify large files that should be excluded
"""

import os
from pathlib import Path
import subprocess

def get_dir_size(path):
    """Calculate directory size in bytes"""
    total = 0
    try:
        for entry in os.scandir(path):
            if entry.is_file():
                total += entry.stat().st_size
            elif entry.is_dir():
                total += get_dir_size(entry.path)
    except PermissionError:
        pass
    return total

def format_size(bytes):
    """Format bytes to human readable"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes < 1024.0:
            return f"{bytes:.2f} {unit}"
        bytes /= 1024.0
    return f"{bytes:.2f} TB"

def check_git_files():
    """Check what files will be committed to Git"""
    print("=" * 80)
    print("🔍 REPOSITORY SIZE CHECK")
    print("=" * 80)
    
    # Check if git is initialized
    if not Path(".git").exists():
        print("\n⚠️ Git not initialized. Run 'git init' first.")
        print("\nShowing all files (not just Git-tracked):\n")
        show_all_files = True
    else:
        show_all_files = False
    
    # Get list of files
    if show_all_files:
        # Show all files
        files = []
        for root, dirs, filenames in os.walk("."):
            # Skip .git directory
            if ".git" in root:
                continue
            for filename in filenames:
                filepath = os.path.join(root, filename)
                try:
                    size = os.path.getsize(filepath)
                    files.append((filepath, size))
                except:
                    pass
    else:
        # Show only Git-tracked files
        try:
            result = subprocess.run(
                ["git", "ls-files"],
                capture_output=True,
                text=True,
                check=True
            )
            files = []
            for filepath in result.stdout.strip().split('\n'):
                if filepath:
                    try:
                        size = os.path.getsize(filepath)
                        files.append((filepath, size))
                    except:
                        pass
        except subprocess.CalledProcessError:
            print("❌ Error running git command")
            return
    
    # Sort by size
    files.sort(key=lambda x: x[1], reverse=True)
    
    # Calculate total
    total_size = sum(size for _, size in files)
    
    # Show summary
    print(f"\n📊 SUMMARY:")
    print(f"Total files: {len(files)}")
    print(f"Total size: {format_size(total_size)}")
    
    # Check if size is acceptable
    if total_size > 1_000_000_000:  # 1GB
        print(f"\n🚨 WARNING: Repository is {format_size(total_size)} (> 1GB)")
        print("   GitHub recommends repositories < 1GB")
        print("   Consider excluding large files")
    elif total_size > 100_000_000:  # 100MB
        print(f"\n⚠️ CAUTION: Repository is {format_size(total_size)} (> 100MB)")
        print("   This is acceptable but consider optimizing")
    else:
        print(f"\n✅ GOOD: Repository size is acceptable")
    
    # Show largest files
    print(f"\n📁 TOP 20 LARGEST FILES:")
    print("-" * 80)
    print(f"{'Size':<12} {'File':<68}")
    print("-" * 80)
    
    for filepath, size in files[:20]:
        # Highlight large files
        if size > 100_000_000:  # 100MB
            marker = "🚨"
        elif size > 10_000_000:  # 10MB
            marker = "⚠️"
        else:
            marker = "✅"
        
        print(f"{format_size(size):<12} {marker} {filepath:<65}")
    
    # Check for common large file patterns
    print(f"\n🔍 CHECKING FOR LARGE FILE PATTERNS:")
    print("-" * 80)
    
    patterns = {
        "Model files": [".h5", ".pt", ".pth", ".onnx", ".pb"],
        "Data files": [".csv", ".xlsx", ".json", ".xml"],
        "Image files": [".jpg", ".jpeg", ".png", ".gif", ".bmp"],
        "Video files": [".mp4", ".avi", ".mov", ".mkv"],
        "Archive files": [".zip", ".tar", ".gz", ".rar"],
        "Log files": [".log", ".txt"],
    }
    
    for category, extensions in patterns.items():
        matching_files = [
            (f, s) for f, s in files 
            if any(f.lower().endswith(ext) for ext in extensions)
        ]
        if matching_files:
            total_cat_size = sum(s for _, s in matching_files)
            print(f"\n{category}:")
            print(f"  Count: {len(matching_files)}")
            print(f"  Total size: {format_size(total_cat_size)}")
            if total_cat_size > 100_000_000:
                print(f"  🚨 WARNING: Consider excluding these files")
    
    # Check .gitignore
    print(f"\n📋 GITIGNORE CHECK:")
    print("-" * 80)
    
    if Path(".gitignore").exists():
        print("✅ .gitignore exists")
        
        with open(".gitignore", "r") as f:
            gitignore_content = f.read()
        
        important_patterns = [
            ".env",
            "*.h5",
            "*.pt",
            "data/",
            "__pycache__",
        ]
        
        for pattern in important_patterns:
            if pattern in gitignore_content:
                print(f"  ✅ {pattern} is ignored")
            else:
                print(f"  ⚠️ {pattern} is NOT ignored (consider adding)")
    else:
        print("❌ .gitignore NOT found")
        print("   Create .gitignore to exclude large files")
    
    # Recommendations
    print(f"\n💡 RECOMMENDATIONS:")
    print("-" * 80)
    
    if total_size > 100_000_000:
        print("1. Exclude large datasets from Git")
        print("2. Exclude trained models (*.h5, *.pt)")
        print("3. Provide download links for data/models")
        print("4. Use Git LFS for files 100MB-2GB")
        print("5. Consider demo mode without large files")
    else:
        print("✅ Repository size looks good!")
        print("✅ Safe to push to GitHub")
    
    print("\n" + "=" * 80)

if __name__ == "__main__":
    check_git_files()
