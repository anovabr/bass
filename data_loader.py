import pickle

# Load the pickle file
with open("bass.pkl", "rb") as f:
    data = pickle.load(f)

# Extract dataframes
df = data["df"]
df_bass = data["df_bass"]
