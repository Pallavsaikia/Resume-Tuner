from crewai.tools import BaseTool
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re
from collections import Counter
import numpy as np

class TextAnalysisTool(BaseTool):
    name: str = "Text Analysis Tool"
    description: str = "Performs advanced text analysis including cosine similarity, jaccard similarity, and TF-IDF analysis between CV and JD"
    
    def _run(self, cv_text: str, jd_text: str) -> dict:
        """Calculate various text similarity metrics"""
        print(cv_text,jd_text)
        try:
            # Preprocess texts
            cv_clean = self._preprocess_text(cv_text)
            jd_clean = self._preprocess_text(jd_text)
            
            # TF-IDF Cosine Similarity
            vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))
            tfidf_matrix = vectorizer.fit_transform([cv_clean, jd_clean])
            cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            
            # Jaccard Similarity
            cv_words = set(cv_clean.lower().split())
            jd_words = set(jd_clean.lower().split())
            jaccard_sim = len(cv_words.intersection(jd_words)) / len(cv_words.union(jd_words))
            
            # Word overlap percentage
            overlap_ratio = len(cv_words.intersection(jd_words)) / len(jd_words) if jd_words else 0
            
            return {
                "cosine_similarity": round(cosine_sim * 100, 2),
                "jaccard_similarity": round(jaccard_sim * 100, 2),
                "word_overlap_percentage": round(overlap_ratio * 100, 2),
                "cv_word_count": len(cv_words),
                "jd_word_count": len(jd_words),
                "common_words": list(cv_words.intersection(jd_words))[:20]  # Top 20 common words
            }
        except Exception as e:
            return {"error": str(e)}
    
    def _preprocess_text(self, text: str) -> str:
        """Clean and preprocess text"""
        text = re.sub(r'[^\w\s]', ' ', text.lower())
        text = re.sub(r'\s+', ' ', text).strip()
        return text