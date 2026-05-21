import pandas as pd

# Read the current dataset
df = pd.read_csv('dataset/crop_production.csv')

# Map to assign proper Indian states (cycling through major Indian states)
indian_states = [
    'Maharashtra', 'Karnataka', 'Punjab', 'Uttar Pradesh', 'Gujarat', 
    'Rajasthan', 'Tamil Nadu', 'West Bengal', 'Bihar', 'Madhya Pradesh',
    'Andhra Pradesh', 'Telangana', 'Haryana', 'Himachal Pradesh', 'Jharkhand',
    'Odisha', 'Kerala', 'Assam', 'Uttarakhand', 'Chhattisgarh'
]

# District mapping for each state
district_mapping = {
    'Maharashtra': 'Pune',
    'Karnataka': 'Bangalore',
    'Punjab': 'Amritsar',
    'Uttar Pradesh': 'Lucknow',
    'Gujarat': 'Ahmedabad',
    'Rajasthan': 'Jaipur',
    'Tamil Nadu': 'Chennai',
    'West Bengal': 'Kolkata',
    'Bihar': 'Patna',
    'Madhya Pradesh': 'Bhopal',
    'Andhra Pradesh': 'Hyderabad',
    'Telangana': 'Secunderabad',
    'Haryana': 'Faridabad',
    'Himachal Pradesh': 'Shimla',
    'Jharkhand': 'Ranchi',
    'Odisha': 'Bhubaneswar',
    'Kerala': 'Kochin',
    'Assam': 'Guwahati',
    'Uttarakhand': 'Dehradun',
    'Chhattisgarh': 'Raipur'
}

# Assign states
n_states = len(indian_states)
df['State_Name'] = df.index.map(lambda x: indian_states[x % n_states])
df['District_Name'] = df['State_Name'].map(district_mapping)

# Save the updated dataset
df.to_csv('dataset/crop_production.csv', index=False)

print('Dataset updated with Indian states!')
print('Total records:', len(df))
print('Unique states:', df['State_Name'].nunique())
print()
print('Sample of updated data:')
print(df[['State_Name', 'District_Name', 'Crop', 'Production']].head(10))
