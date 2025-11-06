#!/usr/bin/env python3
import sys
import traceback

try:
    print("Testing import...")
    from a2a.agent.product_management_agent import SemanticKernelProductManagementAgent
    print("Import successful!")
    print(f"Class: {SemanticKernelProductManagementAgent}")
except Exception as e:
    print(f"Import failed: {e}")
    print("Full traceback:")
    traceback.print_exc()
