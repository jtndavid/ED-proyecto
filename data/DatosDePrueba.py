import json
from pathlib import Path
#data_file_path = Path(__file__).parent / "MOCK_DATA.json"
#data_file_path = Path(__file__).parent / "MOCK_DATA (10).json"
#data_file_path = Path(__file__).parent / "MOCK_DATA (100).json"
data_file_path = Path(__file__).parent / "MOCK_DATA_FINAL.json"
data_array = json.load(open(data_file_path))


