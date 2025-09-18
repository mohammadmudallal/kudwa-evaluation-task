import json as jn

def read_cache(file_path):
    try:
        if not file_path.exists():
            return {}
        
        with open(file_path, "r") as f:
            data = jn.load(f)
            
        return data
    except Exception as e:
        print(f"Error reading cache: {e}")
        return {}
    
def write_cache(file_path, data):
    try:
        with open(file_path, "w") as f:
            jn.dump(data, f, indent=2)
    except Exception as e:
        print(f"Error writing cache: {e}")