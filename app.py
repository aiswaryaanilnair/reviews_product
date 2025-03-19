import streamlit as st
import asyncio
from gpt_researcher import GPTResearcher
import os
import requests
import time
import json
import pandas as pd
import base64
import shutil
from dotenv import load_dotenv
from langchain.schema import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

load_dotenv()

if 'report1' not in st.session_state:
    st.session_state.report1 = None
if 'report2' not in st.session_state:
    st.session_state.report2 = None
if 'path' not in st.session_state:
    st.session_state.path = None
if 'product' not in st.session_state:
    st.session_state.product = None
if 'analysis_result' not in st.session_state:
    st.session_state.analysis_result = None

OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
TAVILY_API_KEY = st.secrets["TAVILY_API_KEY"]

llm = ChatOpenAI(
    openai_api_base="https://api.openai.com/v1",
    openai_api_key=st.secrets["OPENAI_API_KEY"],
    model_name="gpt-4o-mini",
)

async def get_report(query: str, report_type: str) -> str:
    researcher = GPTResearcher(query, report_type)
    research_result = await researcher.conduct_research()
    report = await researcher.write_report()
    research_context = researcher.get_research_context()
    research_sources = researcher.get_research_sources()
    return report, research_context, research_sources
 
def extract_reviews_and_append_csv(json_data, csv_filename):
    """
    Extract reviews from JSON data and append to an existing CSV file.
    Creates the file if it doesn't exist.
    
    Args:
        json_data: JSON data containing reviews (string or dict)
        csv_filename: Path to the CSV file
    
    Returns:
        int: Number of reviews extracted and appended
    """
    try:
        data = json.loads(json_data) if isinstance(json_data, str) else json_data
        
        if "Results" not in data:
            print("No 'Results' field found in the JSON data")
            return 0
        
        reviews_data = []
        for item in data["Results"]:
            review = {
                "UserNickname": item.get("UserNickname"),
                "Title": item.get("Title"),
                "ReviewText": item.get("ReviewText"),
                "Rating": item.get("Rating")
            }
            reviews_data.append(review)
        
        df = pd.DataFrame(reviews_data)
        
        if df.empty:
            print("No reviews found in the data")
            return 0
            
        file_exists = os.path.isfile(csv_filename)
        
        df.to_csv(csv_filename, 
                  mode='a' if file_exists else 'w',
                  header=not file_exists,
                  index=False, 
                  encoding='utf-8')
        
        print(f"{'Appended' if file_exists else 'Created new file with'} {len(df)} reviews")
        return len(df)
            
    except json.JSONDecodeError:
        print("Error decoding JSON data")
        return 0
    except Exception as e:
        print(f"Error processing reviews: {str(e)}")
        return 0

def samsung():
    for i in range(1, 101):
        url = f"https://api.bazaarvoice.com/data/reviews.json?resource=reviews&action=REVIEWS_N_STATS&filter=productid%3Aeq%3ASM-F741BZYGEUB&filter=contentlocale%3Aeq%3Asq*%2Cbs*%2Cbg*%2Cca*%2Chr*%2Ccs*%2Cda*%2Cnl*%2Cen*%2Cet*%2Cfi*%2Cfr*%2Cde*%2Cel*%2Chu*%2Cit*%2Clv*%2Clt*%2Cmk*%2Cno*%2Cpl*%2Cpt*%2Cro*%2Csr*%2Csk*%2Csl*%2Ces*%2Csv*%2Cuk*%2Cen_IE%2Cen_IE&filter=isratingsonly%3Aeq%3Afalse&filter_reviews=contentlocale%3Aeq%3Asq*%2Cbs*%2Cbg*%2Cca*%2Chr*%2Ccs*%2Cda*%2Cnl*%2Cen*%2Cet*%2Cfi*%2Cfr*%2Cde*%2Cel*%2Chu*%2Cit*%2Clv*%2Clt*%2Cmk*%2Cno*%2Cpl*%2Cpt*%2Cro*%2Csr*%2Csk*%2Csl*%2Ces*%2Csv*%2Cuk*%2Cen_IE%2Cen_IE&include=authors%2Cproducts%2Ccomments&filteredstats=reviews&Stats=Reviews&limit={i}&offset=2&limit_comments=2&sort=isfeatured%3Adesc&passkey=ca0eIctl9puZawFxpTPjOEyC3adiBoUBMIcG4lq6DURb8&apiversion=5.5&displaycode=29539-en_ie"

        payload = {}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)
        data = response.text
        data_dir = json.loads(data)
        os.makedirs("samsung_data", exist_ok=True)
        with open(f'samsung_data/data{i}.json', 'w') as json_file:
            json.dump(data_dir, json_file, indent=4)
        
        if i%20 == 0:
            time.sleep(5)
            
    paths= []
    for i in range(1, 101):
        file_path = f"samsung_data/data{i}.json"
        paths.append(file_path)
    
    for path in paths:
        with open(path, 'r', encoding='utf-8') as file:
            json_data = file.read()
            
        csv_path = "extract_reviews_samsung.csv"
        extract_reviews_and_append_csv(json_data, csv_path)

    if os.path.exists("samsung_data"):
        shutil.rmtree("samsung_data")
    return csv_path

def dyson():
    for i in range(1, 101):
        url = f"https://api.bazaarvoice.com/data/reviews.json?resource=reviews&action=REVIEWS_N_STATS&filter=productid%3Aeq%3Asv25-absolute&filter=contentlocale%3Aeq%3Aar*%2Czh*%2Chr*%2Ccs*%2Cda*%2Cnl*%2Cen*%2Cet*%2Cfi*%2Cfr*%2Cde*%2Cel*%2Che*%2Chu*%2Cid*%2Cit*%2Cja*%2Cko*%2Clv*%2Clt*%2Cms*%2Cno*%2Cpl*%2Cpt*%2Cro*%2Csk*%2Csl*%2Ces*%2Csv*%2Cth*%2Ctr*%2Cvi*%2Cen_IN%2Cen_IN&filter=isratingsonly%3Aeq%3Afalse&filter_reviews=contentlocale%3Aeq%3Aar*%2Czh*%2Chr*%2Ccs*%2Cda*%2Cnl*%2Cen*%2Cet*%2Cfi*%2Cfr*%2Cde*%2Cel*%2Che*%2Chu*%2Cid*%2Cit*%2Cja*%2Cko*%2Clv*%2Clt*%2Cms*%2Cno*%2Cpl*%2Cpt*%2Cro*%2Csk*%2Csl*%2Ces*%2Csv*%2Cth*%2Ctr*%2Cvi*%2Cen_IN%2Cen_IN&include=authors%2Cproducts%2Ccomments&filteredstats=reviews&Stats=Reviews&limit={i}&offset=8&limit_comments=3&sort=ContentLocale%3Aen_IN%2Cen_AU%2Cen_US%2Cen_GB%2Cen_SG&passkey=caa1NAv81VaHgxw7mDvXGRPl0tPLLgs8B9ZJqrMEy3h6g&apiversion=5.5&displaycode=17317_4_0-en_in"

        payload = {}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)
        data = response.text
        data_dir = json.loads(data)
        os.makedirs("dyson_data", exist_ok=True)
        with open(f'dyson_data/data{i}.json', 'w') as json_file:
            json.dump(data_dir, json_file, indent=4)
        
        if i%20 == 0:
            time.sleep(5)
            
    paths= []
    for i in range(1, 101):
        file_path = f"dyson_data/data{i}.json"
        paths.append(file_path)
    
    for path in paths:
        with open(path, 'r', encoding='utf-8') as file:
            json_data = file.read()
        csv_path = "extract_reviews_dyson.csv"
        extract_reviews_and_append_csv(json_data, csv_path)

    if os.path.exists("dyson_data"):
        shutil.rmtree("dyson_data")
    return csv_path

def analyze_data(path):
    data_csv = pd.read_csv(path)
    prompt = f"""
1. Analyze the data given in the excel file and return the following summary information.
2. Summarise all reviews under each rating.
3. Display most mentioned 4-5 tags from 5 star reviews such as "Great battery life," "Poor durability", etc.
4. Only return output in the following format, do not include any other text.
5. Provide summary of the review in 4-5 points and tags associated.

INPUT: {data_csv}

OUTPUT FORMAT:
### 5 Star Rating
- Summary of all five star ratings as 4-5 points. No separate subheading required.
- Tags: "Tag 1", "Tag 2"

### 4 Star Rating
- Summary of all four star ratings as 4-5 points. No separate subheading required.
- Tags: "Tag 1", "Tag 2"

### 3 Star Rating
- Summary of all three star ratings as 4-5 points. No separate subheading required.
- Tags: "Tag 1", "Tag 2"

### 2 Star Rating
- Summary of all two star ratings as 4-5 points. No separate subheading required.
- Tags: "Tag 1", "Tag 2"

### 1 Star Rating
- Summary of all one star ratings as 4-5 points. No separate subheading required.
- Tags: "Tag 1", "Tag 2"
"""
    messages = [
                    SystemMessage(content = "You are a content analyser for products."),
                    HumanMessage(content = prompt)
                ]
                
    response = llm(messages)
    result = response.content
    return result

def get_download_link(file_path, file_name):
    with open(file_path, "rb") as f:
        csv_data = f.read()
    b64 = base64.b64encode(csv_data).decode()

    href = f'<a href="data:text/csv;base64,{b64}" download="{file_name}">{file_name}</a>'
    return href

def main():
    st.title("Product Research Assistant")
    a = "Deep Research for User Reviews"
    b = "Sentiment Analysis and Comprehensive Feedback"
    option = st.selectbox("Select an option:", (a, b))
    
    if option == b:
        user_query = st.text_input("Enter Product Name:")
        if st.button("Get Report"):
            if user_query:
                if 'report1' in st.session_state:
                    st.session_state.report1 = None
                if 'report2' in st.session_state:
                    st.session_state.report2 = None
                with st.spinner("Collecting information..."):
                    query1 = f"""
Generate all content under each heading marked in '##'.
## Sentiment Analysis and Market Insights Report for {user_query}

Conduct a structured sentiment analysis and market insights report for {user_query}:
Consider additional websites like Amazon India, Flipkart, Myntra, Snapdeal, etc as well while generating market insights.

### Overview:
Summarize the product's key features, specifications, and qualities in a professional and concise manner. Include atleast 3 key features in the overview within the summary and make sure to mark the key features and specifications in bold.

### 1. Key Features & Specifications
Provide key features and the specifications for {user_query} as bullet points,it should be precise and to the point.

### 2. Key Pain Points & Issues (Negative Sentiment)
Provide a list of top 3 key pain points and issues with a small description for each, as A, B, C list format. Include a **direct link** to the relevant discussion post so users can access it for further details.
       A. 
       B. 
       C. 
    
### 3. Positive Feedback & Strengths (Positive Sentiment)
Provide a list of top 3 positive feedback and strengths with a small description for each, as A, B, C list format. Include a **direct link** to the relevant discussion post so users can access it for further details.
       A. 
       B. 
       C. 
    
### 4. Feature Requests & User Expectations
    
### 5. Market Trends & Regional Performance
       Format the output as a table with the following columns:
       Region | Sales Performance | Key Strengths | Challenges
    
### 6. Actionable Recommendations (For Brand Strategy & Optimization)

       A. 
       B. 
       C. 
    
### 7. Key Insights for Brand Analysis
       - Product Strengths to Leverage
       - Pain Points to Address
       - Market-Specific Strategy
       
### 8. Comparison Table Across E-Commerce Platforms:
Create a table comparing the product across different websites. Only include websites that have information about the product. The table should include the following columns:
| Website | Product Name | Price | Discount | User Rating | Number of Reviews | Shipping Options | Stock Availability | Return Policy | Seller Name/Verified | Additional Perks |
Websites to consider: Amazon India, Flipkart, Myntra, Snapdeal, Tata CLiQ, AJIO, Paytm Mall, JioMart, Meesho, and IndiaMART.

    
    Provide a final takeaway with the most critical strategic direction.
    
    Overall Sentiment Summary: 
    Add *The Overall Sentiment Summary reflects customer opinions on key product aspects, showing the percentage of positive, negative, and neutral mentions.* line
     Format the following output in % as a table with the following:
    Columns:   Positive Mentions | Negative Mentions | Neutral Mentions
    Rows:   Design & Build Quality | Display & Camera | Battery Performance | Software & Performance | Pricing & Value | Availability & Supply

## Comprehensive Feedback and Expectations Analysis for {user_query}
 
Instructions for GPT Researcher:  
1. Collect feedback from at least **5 different sources**, maily from **Reddit**, **Quora**, **Stack Overflow**, and other relevant public forums or online communities. Ensure you cover both positive and negative aspects of user feedback.  
2. Categorize the feedback into key areas:  
   - **Bugs/Frustrations**: Identify specific issues users face.  
   - **Positive Feedback**: Showcase what users appreciate and love about the product.  
   - **Feature Requests**: Highlight any suggestions for product improvement or enhancements.  
   - **Recurring Patterns**: Identify common trends or repeated issues across discussions.  
3. For each point, include a **direct link** to the relevant discussion post so users can access it for further details.  
4. The report should be **clear, concise, and professional**, with actionable insights based on the feedback. Ensure the content is balanced and informative, providing a comprehensive overview of user sentiment.
5.stricly follow the Output format defined (no need for introduction,conclusion for the report), but include titles for each bug/feature request .so that its more easily readable.
Instructions for Tavily:  
1. Crawl relevant platforms (Reddit, Quora, Stack Overflow/Stack Exchange, and at least 2 other public forums or communities) to gather user feedback.  
2. Apply NLP techniques to analyze the content, extracting useful feedback and categorizing the sentiment (positive/negative).  
3. Deliver the feedback with proper links to each source for validation.
 
Output Format:  
- **Bugs/Frustrations**:  
  - Issue: [Detailed description of the problem in 2-3 sentences for each point, e.g., "App crashes when loading the dashboard."]  
  - Source: [Link to the specific post on Reddit/Quora/Stack Overflow]  
 
- **Positive Feedback**:  
  - Praise: [Positive aspect of the product in 2-3 sentences for each point, e.g., "Intuitive user interface and great customer support."]  
  - Source: [Link to the specific post on Reddit/Quora/Stack Overflow]  
 
- **Feature Requests**:  
  - Request: [Detailed feature request in 2-3 sentences for each point, e.g., "Allow exporting data to CSV."]  
  - Source: [Link to the specific post on Reddit/Quora/Stack Overflow]  
 
- **Recurring Patterns**:  
  - Theme: [Summary of common trends or sentiments in 2-3 sentences for each point, e.g., "Users are generally happy with the pricing model but complain about the lack of integrations."]  
  - Insights: [Provide insights or context from the discussions.]
  
End this report with and go to next report:    
- Actionable recommendations for improving user experience or emphasizing positive feedback in marketing strategies.

At the end of the report, provide a section with **all individual sources** compiled in a list of clickable links for user reference. Make sure the refrences from both the reports are included.  
"""
                    query2 = f"""
## User Reviews from E-Commerce Websites for {user_query}

Instructions for GPT Researcher:
1. Gather reviews from at least 3 Indian e-commerce sites (Amazon India + Tata Cliq, Snapdeal, Flipkart, Reliance Digital) and optionally Best Buy, Walmart, or other relevant platforms.
2. Collect at least 10 reviews per year from the last five years per rating (5★, 4★, 3★, 2★, 1★) per platform for balanced representation.
3. Include:
    - Star rating (out of 5)
    - Summary of common themes per rating
    - Top 3 individual reviews under each rating per platform
    - Tags summarizing key points for individual reviews (e.g., "Great battery life," "Poor durability")
    - Mentions of specific features, durability, value for money, customer service
4. Report must include Amazon + **at least 3** Indian platforms
5. Summarise all reviews under each rating heading separating them by retailer name.
6. For each source website, note the overall product rating and total number of reviews.
7. Under each retailer heading, all rating heading (5★, 4★, 3★, 2★, 1★) must be present.
7. Must format the exact OUTPUT FORMAT given below.

Instructions for Tavily/Search:
1. Use advanced web scraping to access user review data from Amazon, Indian e-commerce sites, and other relevant platforms.
2. Please prioritize Tata Cliq, Snapdeal, Flipkart, Reliance Digital and Amazon India for Indian market reviews.
3. Provide direct URLs to each specific product page containing the reviews.
4. If Flipkart access remains problematic, ignore it.
 
Output Format:  
## User Reviews from E-Commerce Websites for {user_query}
### Product Overview
#### Amazon
Product Overview

Average Rating: [X.X]/5 from [XXXX] reviews

5 Star Reviews
Summary: [Brief summary of common themes in 5-star reviews]
- Review 1 : [Review Content]
  Tags: "Tag 1", "Tag 2", etc
- Review 2 : [Review Content]
  Tags: "Tag 1", "Tag 2", etc
- Review 3 : [Review Content]
  Tags: "Tag 1", "Tag 2", etc
  
4 Star Reviews
Summary: [Brief summary of common themes in 4-star reviews]
- Review 1 : [Review Content]
  Tags: "Tag 1", "Tag 2", etc
- Review 2 : [Review Content]
  Tags: "Tag 1", "Tag 2", etc
- Review 3 : [Review Content]
  Tags: "Tag 1", "Tag 2", etc
  
3 Star Reviews
Summary: [Brief summary of common themes in 3-star reviews]
- Review 1 : [Review Content]
  Tags: "Tag 1", "Tag 2", etc
- Review 2 : [Review Content]
  Tags: "Tag 1", "Tag 2", etc
- Review 3 : [Review Content]
  Tags: "Tag 1", "Tag 2", etc
  
2 Star Reviews
Summary: [Brief summary of common themes in 2-star reviews]
- Review 1 : [Review Content]
  Tags: "Tag 1", "Tag 2", etc
- Review 2 : [Review Content]
  Tags: "Tag 1", "Tag 2", etc
- Review 3 : [Review Content]
  Tags: "Tag 1", "Tag 2", etc
  
1 Star Reviews
Summary: [Brief summary of common themes in 1-star reviews]
- Review 1 : [Review Content]
  Tags: "Tag 1", "Tag 2", etc
- Review 2 : [Review Content]
  Tags: "Tag 1", "Tag 2", etc
- Review 3 : [Review Content]
  Tags: "Tag 1", "Tag 2", etc
  
#### [Indian E-commerce Site 1] (e.g., Tata Cliq, Flipkart, etc.)
Product Overview

Average Rating: [X.X]/5 from [XXXX] reviews

5 Star Reviews
Summary: [Brief summary of common themes in 5-star reviews]
- Review 1 : [Review Content]
  Tags: "Tag 1", "Tag 2", etc
- Review 2 : [Review Content]
  Tags: "Tag 1", "Tag 2", etc
- Review 3 : [Review Content]
  Tags: "Tag 1", "Tag 2", etc
  
4 Star Reviews
Summary: [Brief summary of common themes in 4-star reviews]
- Review 1 : [Review Content]
  Tags: "Tag 1", "Tag 2", etc
- Review 2 : [Review Content]
  Tags: "Tag 1", "Tag 2", etc
- Review 3 : [Review Content]
  Tags: "Tag 1", "Tag 2", etc
  
3 Star Reviews
Summary: [Brief summary of common themes in 3-star reviews]
- Review 1 : [Review Content]
  Tags: "Tag 1", "Tag 2", etc
- Review 2 : [Review Content]
  Tags: "Tag 1", "Tag 2", etc
- Review 3 : [Review Content]
  Tags: "Tag 1", "Tag 2", etc
  
2 Star Reviews
Summary: [Brief summary of common themes in 2-star reviews]
- Review 1 : [Review Content]
  Tags: "Tag 1", "Tag 2", etc
- Review 2 : [Review Content]
  Tags: "Tag 1", "Tag 2", etc
- Review 3 : [Review Content]
  Tags: "Tag 1", "Tag 2", etc
  
1 Star Reviews
Summary: [Brief summary of common themes in 1-star reviews]
- Review 1 : [Review Content]
  Tags: "Tag 1", "Tag 2", etc
- Review 2 : [Review Content]
  Tags: "Tag 1", "Tag 2", etc
- Review 3 : [Review Content]
  Tags: "Tag 1", "Tag 2", etc
  
#### [Indian E-commerce Site 2] (e.g., Tata Cliq, Flipkart, etc.)
Product Overview

Average Rating: [X.X]/5 from [XXXX] reviews

5 Star Reviews
Summary: [Brief summary of common themes in 5-star reviews]
- Review 1 : [Review Content]
  Tags: "Tag 1", "Tag 2", etc
- Review 2 : [Review Content]
  Tags: "Tag 1", "Tag 2", etc
- Review 3 : [Review Content]
  Tags: "Tag 1", "Tag 2", etc
  
4 Star Reviews
Summary: [Brief summary of common themes in 4-star reviews]
- Review 1 : [Review Content]
  Tags: "Tag 1", "Tag 2", etc
- Review 2 : [Review Content]
  Tags: "Tag 1", "Tag 2", etc
- Review 3 : [Review Content]
  
3 Star Reviews
Summary: [Brief summary of common themes in 3-star reviews]
- Review 1 : [Review Content]
  Tags: "Tag 1", "Tag 2", etc
- Review 2 : [Review Content]
  Tags: "Tag 1", "Tag 2", etc
- Review 3 : [Review Content]
  Tags: "Tag 1", "Tag 2", etc
  
2 Star Reviews
Summary: [Brief summary of common themes in 2-star reviews]
- Review 1 : [Review Content]
  Tags: "Tag 1", "Tag 2", etc
- Review 2 : [Review Content]
  Tags: "Tag 1", "Tag 2", etc
- Review 3 : [Review Content]
  Tags: "Tag 1", "Tag 2", etc
  
1 Star Reviews
Summary: [Brief summary of common themes in 1-star reviews]
- Review 1 : [Review Content]
  Tags: "Tag 1", "Tag 2", etc
- Review 2 : [Review Content]
  Tags: "Tag 1", "Tag 2", etc
- Review 3 : [Review Content]
  Tags: "Tag 1", "Tag 2", etc
  
#### [Additional Website] (e.g., Best Buy, Walmart, etc.)
[Follow same format as above]

### Common Themes in Reviews
- Positive Points: [List 3-5 recurring positive aspects mentioned across reviews]
- Critical Points: [List 3-5 recurring negative aspects mentioned across reviews]
"""
                    report_type = "research_report"
                    
                    if not st.session_state.report1:
                        report1, context, sources = asyncio.run(get_report(query1, report_type))
                        st.session_state.report1 = report1
                    
                    st.write(st.session_state.report1)
                
                with st.spinner("Analysing E-Commerce Platforms..."):
                    if not st.session_state.report2:
                        report2, context, sources = asyncio.run(get_report(query2, report_type))
                        st.session_state.report2 = report2
                    
                    st.write(st.session_state.report2)
            else:
                st.error("Please enter a valid query.")
                
    elif option == a:
        st.write("## Deep Research Reviews")
        p1 = "Samsung Galaxy Z Flip 6"
        p2 = "Dyson V8 Advanced Cordless Vacuum Cleaner"
        product = st.selectbox("Select an option:", (p1, p2))
        
        if st.button("Fetch Reviews"):
            if not st.session_state.path or st.session_state.product != product:
                with st.spinner("Fetching all user reviews..."):
                    if product == p1:
                        path = samsung()
                        url = "https://shop.samsung.com/ie/galaxy-z-flip6-yellow-256-gb"
                    elif product == p2:
                        path = dyson()
                        url = "https://www.dyson.in/dyson-v8-absolute-vacuum?utm_id=sa_71700000098898369_58700008722595581&utm_source=google&utm_medium=cpc&utm_campaign=fc_v8_healthy-home&utm_content=do_text_1x1_floor-care&utm_term=dyson+v8+cordless&gad_source=1&gclid=Cj0KCQjws-S-BhD2ARIsALssG0ZZta6U0coZqCHxau8K4g--oJTrZBWgt_jukhIVfSVd0zu9fqM2mpYaAn3BEALw_wcB&gclsrc=aw.ds"
                        
                    st.session_state.path = path
                    st.session_state.product = product
                    
                    result = analyze_data(path)
                    st.session_state.analysis_result = result
            st.write("### Source:")
            st.link_button("Visit Website", url)
            st.markdown(st.session_state.analysis_result)
            download_link = get_download_link(st.session_state.path, f"Reviews_{st.session_state.product}.csv")
            st.markdown(download_link, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
