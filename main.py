import os
import importlib
from fastapi import FastAPI

# 1. Initialize the main FastAPI application (The Gateway)
app = FastAPI(title="City Pollution OS", description="Gateway for all city agents")

# 2. This function automatically finds all files inside the 'agents/' folder
def mount_all_agents():
    agents_dir = "agents"
    
    # Check if the folder exists
    if not os.path.exists(agents_dir):
        return

    # Loop through every file in the 'agents' folder
    for filename in os.listdir(agents_dir):
        # We only look for python files (e.g., simulation.py)
        if filename.endswith(".py") and filename != "__init__.py":
            agent_name = filename[:-3] # Removes the .py extension (so 'simulation.py' becomes 'simulation')
            
            try:
                # Dynamic import: It finds the file automatically
                module = importlib.import_module(f"agents.{agent_name}")
                
                # If that file has an 'app' (FastAPI), mount it
                if hasattr(module, "app"):
                    app.mount(f"/{agent_name}", module.app)
                    print(f"Successfully mounted: {agent_name} at /{agent_name}")
            except Exception as e:
                print(f"Error mounting {agent_name}: {e}")

# Call the function to setup everything
mount_all_agents()

@app.get("/")
def root():
    return {"message": "Pipeline is active! All agents are running."}