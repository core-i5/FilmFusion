import os
from django.conf import settings
from django.apps import AppConfig
import pickle
import pandas as pd
import numpy as np

class RecommendationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'recommendations'

    def ready(self):
        
        base_dir = settings.BASE_DIR

        preprocessed_data_path = os.path.join(base_dir, 'recommendations/rec_model_components/preprocessed_data.csv')
        # preprocessed_data_path = os.path.join(base_dir, 'recommendations/rec_model_components/new_preprocessed_data.csv')
        # tfidf_vectorizer_path = os.path.join(base_dir, 'recommendations/rec_model_components/tfidf_vectorizer.pkl')
        # U_matrix_path = os.path.join(base_dir, 'recommendations/rec_model_components/U_matrix.pkl')
        # sigma_matrix_path = os.path.join(base_dir, 'recommendations/rec_model_components/sigma_matrix.pkl')
        # Vt_matrix_path = os.path.join(base_dir, 'recommendations/rec_model_components/Vt_matrix.pkl')
        cosine_sim_path = os.path.join(base_dir, 'recommendations/rec_model_components/cosine_sim.npy')
        predicted_ratings_df_path = os.path.join(base_dir, 'recommendations/rec_model_components/predicted_ratings_df.pkl')


        self.data = pd.read_csv(preprocessed_data_path)

        # with open(tfidf_vectorizer_path, 'rb') as f:
        #     self.tfidf_vectorizer = pickle.load(f)

        # with open(U_matrix_path, 'rb') as f:
        #     self.U = pickle.load(f)

        # with open(sigma_matrix_path, 'rb') as f:
        #     self.sigma = pickle.load(f)

        # with open(Vt_matrix_path, 'rb') as f:
        #     self.Vt = pickle.load(f)

        self.cosine_sim = np.load(cosine_sim_path)
        self.predicted_ratings_df = pd.read_pickle(predicted_ratings_df_path)
