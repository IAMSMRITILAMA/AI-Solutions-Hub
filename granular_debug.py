import os
import sys
import traceback

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai_solutions_project.settings')

try:
    import django
    django.setup()
    print("Django setup OK")
    
    print("Importing core.models...")
    import core.models
    print("core.models imported OK")
    
    print("Importing core.views...")
    import core.views
    print("core.views imported OK")
    
    print("All imports SUCCESSFUL")
except Exception:
    traceback.print_exc()
