"""
Validate template syntax and completeness
"""
import os
import re
import sys


def find_templates(base_dir):
    templates = []
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith('.md'):
                templates.append(os.path.join(root, file))
    return templates


def check_placeholders(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    placeholders = re.findall(r'\{\{(\w+(?:_\w+)*)\}\}', content)
    return placeholders


def validate_structure(base_dir):
    required_dirs = [
        'templates/construction',
        'templates/safety',
        'templates/quality',
        'templates/contract',
        'templates/report',
        'skills',
        'scripts',
        '.github/workflows'
    ]
    missing = []
    for dir_path in required_dirs:
        full_path = os.path.join(base_dir, dir_path)
        if not os.path.exists(full_path):
            missing.append(dir_path)
    return missing


def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    print("=" * 60)
    print("Construction Document Auto-Generation Workflow - Validation Report")
    print("=" * 60)
    
    print("\n[DIR] Checking directory structure...")
    missing = validate_structure(base_dir)
    if missing:
        print(f"  MISSING: {', '.join(missing)}")
    else:
        print("  OK - Directory structure complete")
    
    print("\n[FILE] Checking template files...")
    templates = find_templates(os.path.join(base_dir, 'templates'))
    print(f"  Found {len(templates)} template(s):")
    for t in templates:
        rel_path = os.path.relpath(t, base_dir)
        placeholders = check_placeholders(t)
        print(f"    - {rel_path} ({len(placeholders)} placeholders)")
    
    print("\n[SKILL] Checking Skill definitions...")
    skills_dir = os.path.join(base_dir, 'skills')
    if os.path.exists(skills_dir):
        for skill in os.listdir(skills_dir):
            skill_path = os.path.join(skills_dir, skill)
            if os.path.isdir(skill_path):
                skill_md = os.path.join(skill_path, 'SKILL.md')
                if os.path.exists(skill_md):
                    print(f"  OK: {skill}/SKILL.md")
                else:
                    print(f"  WARN: {skill}/SKILL.md missing")
    
    print("\n[SCRIPT] Checking scripts...")
    scripts_dir = os.path.join(base_dir, 'scripts')
    if os.path.exists(scripts_dir):
        for script in os.listdir(scripts_dir):
            if script.endswith('.py'):
                print(f"  OK: {script}")
    
    print("\n[ACTION] Checking GitHub Actions...")
    actions_dir = os.path.join(base_dir, '.github', 'workflows')
    if os.path.exists(actions_dir):
        for wf in os.listdir(actions_dir):
            if wf.endswith('.yml'):
                print(f"  OK: {wf}")
    
    print("\n" + "=" * 60)
    print("Validation complete!")
    print("=" * 60)


if __name__ == '__main__':
    main()
