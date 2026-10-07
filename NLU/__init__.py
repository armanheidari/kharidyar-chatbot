from pathlib import Path
import sys 

root_path = Path(__file__).parent.parent
sys.path.insert(1, str(root_path / "NLU"))