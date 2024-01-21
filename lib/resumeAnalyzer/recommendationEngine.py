

from data import job_skill_data
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

tfidf = TfidfVectorizer()
job_titles_vectorized = tfidf.fit_transform(job_skill_data.df['Job Title'])

def profile_similarity(user_input, top_k=5, threshold=30):
    user_input = ' '.join(user_input)
    # Vectorize the user input skills
    user_input_vectorized = tfidf.transform([user_input])

    similarity_scores = cosine_similarity(user_input_vectorized, job_titles_vectorized)
    similarity_scores_flat = similarity_scores.flatten()

    top_indices = similarity_scores_flat.argsort()[::-1][:top_k]
    
    # Create a dictionary to store results
    result_dict = {}
    
    for i in top_indices:
        title = job_skill_data.df['Job Title'][i]
        similarity_percentage = similarity_scores_flat[i] * 100

        # Check if the similarity percentage is above the threshold
        if similarity_percentage >= threshold:
            result_dict[title] = similarity_percentage

    return result_dict




courses_data = job_skill_data.df['Courses']

# Function to recommend courses based on similarity scores
def recommended_courses(recommended_job_titles):
    recommended_courses_dict = {}

    for title in recommended_job_titles:
        # Get the index of the recommended job title in the DataFrame
        index = job_skill_data.df[job_skill_data.df['Job Title'] == title].index[0]

        # Retrieve the associated courses for the recommended job title
        courses_list = courses_data[index]
        recommended_courses_dict[title] = courses_list

    return recommended_courses_dict




 
