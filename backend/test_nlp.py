import sys
import os
sys.path.append(os.path.abspath('.'))

from app.services.nlp_parser import parse_prescription_text

test_text = """
1. Amoxicillin 500mg - Take 1 tablet daily
2. Dolo 650 - Take 1 tablet as needed
"""

result = parse_prescription_text(test_text)
print(result)
