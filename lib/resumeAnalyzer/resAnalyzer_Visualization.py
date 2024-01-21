import seaborn as sns
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import pandas as pd


def plot_Score_Visualization(score,save_location):

    colors = sns.color_palette('viridis', len(score))
    plt.style.use('dark_background')
    plt.figure(figsize=(10, 6))
    bars = plt.barh(list(score.keys()), list(score.values()), color=colors)
    for bar, score in zip(bars, list(score.values())):
        plt.text(bar.get_width() - 1, bar.get_y() + bar.get_height() / 2, f'{score}%', 
                va='center', ha='right', color='white', fontsize=10, fontweight='bold')
    plt.xlabel('Scores', fontsize=14, color='white')
    plt.ylabel('Resume Sections', fontsize=14, color='white')
    plt.title('Resume Score %', fontsize=16, color='white')
    plt.savefig(f'{save_location}resume_score_plot.png', bbox_inches='tight')


def plot_miss_section_Visualization(missing_sections,save_location):
    plt.figure(figsize=(10, 6))
    bars = plt.barh(list(missing_sections.keys()), list(missing_sections.values()), color='skyblue')
    plt.xlabel('Number of Missing Sections')
    plt.title('Missing Sections in Resume')
    plt.grid(axis='x', linestyle='--', alpha=0.6)

    # Display the values on the bars
    for bar in bars:
        plt.text(bar.get_width(), bar.get_y() + bar.get_height()/2, str(int(bar.get_width())), ha='left', va='center', fontsize=10)
    plt.savefig(f'{save_location}missing_section_plot.png', bbox_inches='tight')


def plot_role_match_visualization(role_match_data,save_location):
    
    plt.figure(figsize=(8, 6), facecolor='black')  # Set the background color to black
    sns.set(style="darkgrid", rc={'axes.facecolor': 'black', 'grid.color': 'grey'})  # Set the background style to dark
    ax = sns.barplot(x='Role', y='Percentage', data=role_match_data, color='red')  # Set the bar color to red

    ax.set_xticklabels(ax.get_xticklabels(), rotation=90, ha='right', color='white')  # Rotate x-axis labels vertically and set label color to white
    ax.set_xlabel('Role', color='white')
    ax.set_ylabel('Percentage', color='white')

    # Set Y-axis label color to white
    ax.yaxis.label.set_color('white')

    # Set Y-axis tick labels color to white
    ax.tick_params(axis='y', colors='white')

    plt.tight_layout()
    plt.savefig(f'{save_location}role_match_bar_graph.png', bbox_inches='tight', facecolor='black')


def plot_keyWord_cloud(skills_text,save_location):
    wordcloud = WordCloud(width=800, height=400, background_color="white").generate(skills_text)
# Display the generated word cloud using matplotlib
    plt.figure(figsize=(10, 5), facecolor='black')  # Set the background color to black
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")  # Turn off axis
    wordcloud.to_file(f'{save_location}wordcloud.png')


def plot_recommended_courses_visualization(recommended_courses_dict,save_location):
    data = pd.DataFrame([(role, course) for role, courses in recommended_courses_dict.items() for course in courses],
                        columns=['Role', 'Course'])

    sns.set_style("darkgrid")
    plt.figure(figsize=(18, 12), facecolor='black')  # Set the background color to black
    sns.countplot(y='Course', data=data, hue='Role', palette='viridis')
    plt.title('Distribution of Recommended Courses Across Roles', color='white')  # Set the title color to white
    plt.xlabel('Number of Recommended Courses', color='white')  # Set the x-axis label color to white
    plt.ylabel('Courses', color='white')  # Set the y-axis label color to white

    legend = plt.legend(title='Roles', bbox_to_anchor=(1.05, 1), loc='upper left')
    legend.get_title().set_color('white')  # Set legend title color to white

    for text in legend.get_texts():
        text.set_color('white')  # Set legend text color to white

    plt.tick_params(axis='x', colors='white')  # Set x-axis tick color to white
    plt.tick_params(axis='y', colors='white')  # Set y-axis tick color to white

    # Save the plot
    plt.tight_layout()
    plt.savefig(f'{save_location}recommended_courses_distribution.png', bbox_inches='tight', facecolor='black')



def plot_role_alignment_piechart(role_match_data,save_location):
    plt.figure(figsize=(7, 3), facecolor='black')  # Set the background color to black
    plt.pie(role_match_data['Percentage'], labels=role_match_data['Role'], autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired.colors, textprops={'color': 'white'})
    plt.title('Role Alignment Analysis', color='white')  # Set the title color to white
    plt.savefig(f'{save_location}role_alignment_analysis.png', bbox_inches='tight', facecolor='black')