# 1. Navigate to the backend directory
cd "d:\Coding Programs\WebDev\MediShield AI\backend"

# 2. Create a virtual environment (recommended)
python -m venv venv

# 3. Activate the virtual environment
.\venv\Scripts\Activate

# 4. Install the dependencies
pip install -r requirements.txt

# 5. Start the FastAPI server
uvicorn app.main:app --reload