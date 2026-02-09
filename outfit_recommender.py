import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.neighbors import NearestNeighbors

class OutfitRecommender:
    def __init__(self, styles_csv):
        # Keep raw_df for metadata and df for encoding
        self.raw_df = pd.read_csv(styles_csv, on_bad_lines='skip', low_memory=False)
        self.df = self.raw_df.copy()
        self.encoders = {}
        self.features = ['gender', 'season', 'usage']
        self._prepare_data()

    def _prepare_data(self):
        for col in self.features:
            le = LabelEncoder()
            # Clean missing values and encode
            self.df[col] = le.fit_transform(self.df[col].astype(str))
            self.encoders[col] = le
            
        self.model = NearestNeighbors(n_neighbors=100, metric='euclidean')
        self.model.fit(self.df[self.features])

    def recommend(self, gender, season, usage, n_results=50):
        input_vec = []
        input_data = {'gender': gender, 'season': season, 'usage': usage}
        
        for col in self.features:
            le = self.encoders[col]
            val = input_data[col]
            if val not in le.classes_:
                val = le.classes_[0] # Fallback
            input_vec.append(le.transform([val])[0])
            
        distances, indices = self.model.kneighbors([input_vec], n_neighbors=n_results)
        return self.raw_df.iloc[indices[0]].to_dict(orient='records')