#!/usr/bin/env python3
import sys
import traceback

try:
    print("Importing module...")
    import a2a.agent.product_management_agent as pm_module
    print("Module imported successfully")
    print(f"Module attributes: {dir(pm_module)}")

    print("Checking for the class...")
    if hasattr(pm_module, 'SemanticKernelProductManagementAgent'):
        print("Class found!")
        cls = getattr(pm_module, 'SemanticKernelProductManagementAgent')
        print(f"Class: {cls}")
    else:
        print("Class NOT found in module")

except Exception as e:
    print(f"Error: {e}")
    print("Full traceback:")
    traceback.print_exc()
