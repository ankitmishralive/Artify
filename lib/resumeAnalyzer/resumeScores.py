

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer

from nltk.tokenize import word_tokenize








def extract_keywords_jobDescription(job_description):
    stop_words = set(stopwords.words('english'))
    ps = PorterStemmer()

    # Tokenize and remove stop words
    job_tokens = [ps.stem(word.lower()) for word in word_tokenize(job_description) if word.isalnum() and word.lower() not in stop_words]

    # Extract only unique stemmed words
    unique_keywords = list(set(job_tokens))

    return unique_keywords

def assign_score(resume, job_keywords):
    resume_tokens = set([word.lower() for word in word_tokenize(resume) if word.isalnum()])
    matching_keywords = set()

    for keyword in job_keywords:
        keyword_lower = keyword.lower()
        if any(keyword_lower in resume_token or resume_token in keyword_lower for resume_token in resume_tokens):
            matching_keywords.add(keyword_lower)

    score = len(matching_keywords) / len(job_keywords)

    # Thresholds
    if score > 0.9:
        score -=0.04
    elif 0.75 <= score < 0.8:
        score -= 0.1
    elif 0.7 <= score < 0.75:
        score -= 0.3
    elif 0.65 <= score < 0.7:
        score -= 0.4
    elif 0.6 <= score < 0.65:
        score -= 0.5
    elif score < 0.6:
        score -= 0.5

    return max(0, score) 





def ATS_Score(resume_text):
    Insight = {} 
    score_suggestion = {}
    resume_score = 0
    section_recommendations = set()
    video_suggestions = set()

    missing_sections = {
    'Experience/Internships': 1,
    'Certifications': 1,
    'Achievements': 1,
    'Projects': 1,
    'Technical Skills': 1,
    'Education Background': 1,
    'You got every section covered': 0,
}

    if "professional experience" in resume_text.lower() or "experience" in resume_text.lower() or "internships" in resume_text.lower() or "research" in resume_text.lower() or "work experience" in resume_text.lower() or "work" in resume_text.lower():
        resume_score += 35
        Insight['professional experience'] = 35

    else:
        score_suggestion["Add Experience"] = [
            "Consider adding a 'Professional Experience' section to showcase your work history.",
            "Include details about any relevant internships, research, or projects you've worked on.",
            "Highlight your key responsibilities and achievements in each role."
        ]
        section_recommendations.add('Experience/Internships')

        video_suggestions.update([
            """<iframe width="270" height="215" src="https://www.youtube.com/embed/HhPN_xkL4Gk?si=opQKW0geb4ZYa91o" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>  """,
            
    
            """<iframe width="270" height="215" src="https://www.youtube.com/embed/dvUJlGpptQg?si=fYVh1FrVqan0qEdx" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe> """,

            """<iframe width="270" height="215" src="https://www.youtube.com/embed/t4oXdhilvcY?si=hZNJPijEgSxl_B45" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe> """,

            """<iframe width="270" height="215" src="https://www.youtube.com/embed/79JL8xq0UzY?si=Sf_GLB9q9aO_79F0" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe> """,
        ]
        )

        missing_sections['Experience/Internships'] = 0

        

    if "certification" in resume_text.lower() or "certifications" in resume_text.lower() or "certificate" in resume_text.lower():
        resume_score += 5
        Insight['certification'] = 5
    else:
        score_suggestion["Certifications"] = [
            "Add a 'Certifications' section to highlight any relevant certifications you've earned.",
            "Consider obtaining certifications in your field to enhance your resume.",
            "Include the certification name, issuing organization, and date of completion."
        ]
        section_recommendations.add('Certifications')

        video_suggestions.update([
            """<iframe width="270" height="215" src="https://www.youtube.com/embed/eYlfOmM06pQ?si=x86A3o5cq7kn_oMz" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>""",
            """<iframe width="270" height="215" src="https://www.youtube.com/embed/Ft8R1LuC1Xg?si=D5S5sq-wyOYOAPmz" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>""",         
        ])

        missing_sections['Certifications']=0

    if "achievement" in resume_text.lower() or "achievements" in resume_text.lower() or "award" in resume_text.lower() or "awards" in resume_text.lower():
        resume_score += 10
        Insight['achievement'] = 10
    else:
        score_suggestion["Achievements"] = [
            "Create an 'Achievements' section to showcase your notable accomplishments.",
            "Highlight any awards, honors, or recognitions you have received.",
            "Quantify your achievements with specific metrics to make them more impactful."
        ]
        section_recommendations.add('Achievements')

        video_suggestions.update([
            """<iframe width="270" height="215" src="https://www.youtube.com/embed/LuBUisj7SXA?si=7eQdoAttsEOlOj7U" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>""",
            """<iframe width="270" height="215" src="https://www.youtube.com/embed/oKDuKFcYPzg?si=PY3Pzf5lwVcUYOCz" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>""",
            """<iframe width="270" height="215" src="https://www.youtube.com/embed/4absaBUNvyI?si=FKMgl7jQalWqZiHu" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>""",
           
        ])

        missing_sections['Achievements']=0

    if "project" in resume_text.lower() or "projects" in resume_text.lower():
        resume_score += 35
        Insight['project'] = 35
    else:
        score_suggestion["Projects"] = [
            "Include a 'Projects' section to showcase your relevant work and initiatives.",
            "Highlight key projects you've worked on, detailing your role and contributions.",
            "Quantify the impact of your projects, such as cost savings, efficiency improvements, or revenue generation."
        ]
        section_recommendations.add('Projects')

        video_suggestions.update([
            """<iframe width="270" height="215" src="https://www.youtube.com/embed/zDm-e4yHmOY?si=Vpgby5EVlxhEa9Pz" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>""",
            """<iframe width="270" height="215" src="https://www.youtube.com/embed/06sSWmWG3TM?si=89gjqN7lCupDMg2u" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>""",
        
        ])

        missing_sections['Projects'] = 0

    if "skills" in resume_text.lower() or "skill" in resume_text.lower() or "technical skills" in resume_text.lower():
        resume_score += 10
        Insight['skills'] = 10
    else:
        score_suggestion["Skills"] = [
            "Add a dedicated 'Skills' section to showcase your technical and soft skills.",
            "Integrate relevant skills within the 'Professional Experience' and 'Projects' sections.",
            "Align your skills with the specific requirements of the job you're applying for."
        ]
        section_recommendations.add('Technical Skills')

        video_suggestions.update([
            """<iframe width="270" height="215" src="https://www.youtube.com/embed/JjKzuDfuk1w?si=5MVcC5apwfJMaDFY" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>""",
           """<iframe width="270" height="215" src="https://www.youtube.com/embed/G-J0wm9Iorc?si=j5IhPvzrSBLUSv8a" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>""",
            """<iframe width="270" height="215" src="https://www.youtube.com/embed/MbD4xn3mNaA?si=OaYAvqV586z5Vh5s" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>""",
            
            """<iframe width="270" height="215" src="https://www.youtube.com/embed/w6QbsjvCk1s?si=2WrYGBxJesnMTyAu" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>""",
        ])

        missing_sections['Technical Skills']=0

    if "education" in resume_text.lower():
        resume_score += 5
        Insight['education'] = 5
    else:
         score_suggestion["Education"] = [
            "Include an 'Education' section to highlight your academic background.",
            "Provide details such as your degree, major, institution, graduation date, and GPA (if strong).",
            "Highlight any relevant coursework or academic achievements."
        ]
         section_recommendations.add('Education Background')

         video_suggestions.update([
             """<iframe width="270" height="215" src="https://www.youtube.com/embed/KKbdcg_dC6M?si=gNTyUmTe_4NXovg-" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>""",
            """<iframe width="270" height="215" src="https://www.youtube.com/embed/Kkq0Ef8U1Lw?si=gLAh4TEKnvINUgEw" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>""",
             """<iframe width="270" height="215" src="https://www.youtube.com/embed/oZ5bV6RhBIc?si=j0ryW8xrXIVhLpnA" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>""",

         ])

         missing_sections['Education Background']=0

    if not score_suggestion:
        score_suggestion["Your Resume is Appropriate Contains All Important Sections"] = [
            "Customize your resume for each job application. Highlight the skills and experiences most relevant to the specific job.",
            "Showcase your accomplishments rather than just listing job duties. Use quantifiable metrics to demonstrate your impact.",
            "Start bullet points with strong action verbs to convey a sense of accomplishment and responsibility in your previous roles.",
            "Aim for a one-page resume, especially if you're early in your career. For more experienced professionals, a two-page resume is generally acceptable"
        ]
       
       

        video_suggestions.update([
          """<iframe width="270" height="215" src="https://www.youtube.com/embed/KQI3nG70Ra8?si=dd3xKc_4_i3TAu9S" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>""",
         """<iframe width="270" height="215" src="https://www.youtube.com/embed/chYzEcc6R4c?si=r5C970bRKenkIz-v" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>""",
          """<iframe width="270" height="215" src="https://www.youtube.com/embed/o3Kh4Ez3X0I?si=AM0O1JxmusQFZYwu" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>""",
         """<iframe width="270" height="215" src="https://www.youtube.com/embed/BYUy1yvjHxE?si=clCo_ALQDRj5Gz6U" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>""",
        ])

        missing_sections['You got every section covered'] =1
        missing_sections['Technical Skills']=0
        missing_sections['Achievements']=0
        missing_sections['Certifications']=0
        missing_sections['Education Background']=0
        missing_sections['Experience/Internships']=0
        missing_sections['Projects']=0

    



    return resume_score, score_suggestion, section_recommendations,video_suggestions,Insight,missing_sections

