from pdf2docx import Converter
import docx2txt 
import requests
import re
from lib.resumeAnalyzer.recommendationEngine import profile_similarity,recommended_courses
from lib.resumeAnalyzer.resAnalyzer_Visualization import plot_Score_Visualization, plot_keyWord_cloud, plot_miss_section_Visualization, plot_recommended_courses_visualization, plot_role_alignment_piechart, plot_role_match_visualization
from lib.resumeAnalyzer.resumeScores import extract_keywords_jobDescription,assign_score,ATS_Score
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd 
import os 
from data import college_data
from wordcloud import WordCloud




def Summarizer(input_resume):


    API_URL = "https://api-inference.huggingface.co/models/Falconsai/text_summarization"
    headers = {"Authorization": "Bearer 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"}

    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()
    try:      
        output = query({
            "inputs": input_resume,
        })
        output=output[0]['summary_text']
    except Exception as e:
        output=""
    # API_URL = "https://api-inference.huggingface.co/models/Samir001/ResumeSummary-t5-Wang-Arora"
    # headers = {"Authorization": "Bearer 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"}

    # def query(payload):
    #     response = requests.post(API_URL, headers=headers, json=payload)
    #     return response.json()
    # try:     
    #     output = query({
    #         "inputs": input_resume,
    #     })
    

    return output


def extract_skills(resume_text):
    skills_pattern = re.compile(r'Technical Skills\s*([\s\S]*?)(?:Projects|Education|Experience|$)', re.IGNORECASE)
    skills_pattern2 = re.compile(r'Skills\s*([\s\S]*?)(?:Projects|Education|Experience|$)', re.IGNORECASE)
    skills_match = skills_pattern.search(resume_text)
    if not skills_match:
        skills_match = skills_pattern2.search(resume_text)
    if skills_match:
        skills_section = skills_match.group(1).strip()
        # Split the skills section into individual skills and convert to set
        skills_set = {skill.strip() for skill in re.split(r',|\n', skills_section) if skill.strip()}
        return skills_set
    else:
        return {"Skills": "Skills section not found in the resume."}
   


def extract_education(resume_text):
    
    education_pattern = re.compile(r'(Education|QUALIFICATIONS|STRENGTHS AND EXPERTISE)\s*([\s\S]*?)(?:Projects|Experience|$)', re.IGNORECASE)
    education_matches = education_pattern.finditer(resume_text)
    education_set = set()
    for match in education_matches:
        education_section = match.group(2).strip()    
        entries = [entry.strip() for entry in re.split(r'\n', education_section) if entry.strip()]
        education_set.update(entries)
    return education_set


def check_tier(resume_colleges, big_colleges):
    # Compile regular expressions for each big college name
    college_patterns = [re.compile(re.escape(college), re.IGNORECASE) for college in big_colleges]

    # Check if any college from the resume matches the set of big colleges
    matching_colleges = []

    for pattern in college_patterns:
        for entry in resume_colleges:
            if pattern.search(entry):
                matching_colleges.append(entry)

    if matching_colleges:
        # Check for continuous matches
        continuous_matches = any(any(college in entry.lower() for entry in resume_colleges) for college in matching_colleges)
        
        if continuous_matches:
            return f"Congratulations! Your profile aligns well with the following prestigious colleges: {', '.join(matching_colleges)}."
        else:
            return "Congratulations! Your college is recognized as a Tier 1 institution, reflecting a high standard of education and excellence."
    else:
        return "Unfortunately, your college falls under Tier 2 or Tier 3. Nevertheless, there are numerous opportunities for growth and success, and we are here to support your journey."






def Analyzer(og_pdffile,doc_location,job_description=None):   
    
    cv = Converter(og_pdffile)
    docx_file = f'{doc_location}testing.docx'
    cv.convert(docx_file)
    cv.close()
    resume = docx2txt.process(docx_file)

    # summary=Summarizer(resume)

    extracted_Skills = extract_skills(resume)
    Role_Match = profile_similarity(extracted_Skills)
    
    #------------ Role Match Bar Graph--------------------    

    role_match_data = {
        'Role': list(Role_Match.keys()),
        'Percentage': list(Role_Match.values())
    }

    education = extract_education(resume)
    college_tier = check_tier(education, college_data.big_colleges_of_the_world)

    plot_role_match_visualization(role_match_data,doc_location)



    ## ----------------- Word Cloud-----------
    skills_text = ', '.join(extracted_Skills) if isinstance(extracted_Skills, set) else "No skills found"
    plot_keyWord_cloud(skills_text,doc_location)

    
   # Recommended Courses Plot the horizontal bar plot
    recommended_courses_dict = recommended_courses(Role_Match)
    plot_recommended_courses_visualization(recommended_courses_dict,doc_location)
  

    # Role Alignment Analysis 
    plot_role_alignment_piechart(role_match_data,doc_location)


    # ATS Score
    ATS_score, ATS_Recommendation,Missing_Sections,video_suggestions,score_viz,missing_sec_viz =ATS_Score(resume)

    # Score Visualization
    plot_Score_Visualization(score_viz,doc_location)
    plot_miss_section_Visualization(missing_sec_viz,doc_location)


    
       
    # if len(Missing_Sections)==1:
    #         Missing_Sections_text = "No Section is Missing"
    # elif len(Missing_Sections)>0:
    #     Missing_Sections_text  = f"Your Resume is missing {', '.join(Missing_Sections)} sections"



    if len(job_description) >5:
        job_keywords = extract_keywords_jobDescription(job_description)
        # score = assign_score(resume, job_keywords)*100
        # score = round(assign_score(resume, job_keywords) * 100, 2)
        score = round(assign_score(resume, job_keywords) * 100, 2)
        if score > 80:
            message = f"Your Resume Alignment Score, in accordance with the Job Description, stands at an impressive {score}%, reflecting a notable synergy between your professional profile and the outlined requirements."
        elif score < 70:
            message = f"Your Resume Score, aligned with the Job Description, is currently at {score}%, indicating potential areas for optimization. Tailoring your resume to closely align with the job description is pivotal for optimizing your candidacy, ensuring a strong and impactful representation of your professional qualifications."
    

        return {
        # 'summary': summary,
            'role_match': Role_Match,
            'recommended_courses': recommended_courses_dict,
            'og_pdffile':og_pdffile,
            'college_tier':college_tier,
            'similarity_score':score,
            'similarity_message':message,
            'ats_score':ATS_score,
            'ats_recommendation':ATS_Recommendation,
            'missing_sections':Missing_Sections,
            'video_suggestions':video_suggestions,
        }
   

    return {
            # 'summary': summary,
            'role_match': Role_Match,
            'recommended_courses': recommended_courses_dict,
            'og_pdffile':og_pdffile,
            'college_tier':college_tier,
            'ats_score':ATS_score,
            'ats_recommendation':ATS_Recommendation,
            'missing_sections':Missing_Sections,
            'video_suggestions':video_suggestions,
        }
        


    



 