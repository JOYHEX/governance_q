import streamlit as st
import json
import pandas as pd
import matplotlib.pyplot as plt
import openai
from io import StringIO

openai.api_key ='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'

# custom css for the final result
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>",unsafe_allow_html=True)

def plot_score_analysis(df_cal):
    # Grouped bar chart
    fig, ax = plt.subplots()
    bar_width = 0.35
    index = df_cal.index

    # Plotting bars
    rects1 = ax.bar(index, df_cal['total_score'], bar_width, label='Score', color="#fbceb1")
    rects2 = ax.bar(index + bar_width, df_cal['ideal_total_score'], bar_width, label='Target Score', color="#72e279")

    # X-axis labels
    ax.set_xticks(index + bar_width / 2)
    ax.set_xticklabels(df_cal['category'],rotation=90,fontsize=6)

    # X-axis labels
    ax.set_yticklabels(df_cal['ideal_total_score'],fontsize=6)
    # Legend
    ax.legend()

    # Labels and title
    ax.set_xlabel('Category')
    ax.set_ylabel('Scores vs Target')
    ax.set_title('Score Analysis')

    # Display chart in Streamlit
    st.pyplot(fig)


def comp(PROMPT, MaxToken=50, outputs=3):
    # using OpenAI's Completion module that helps execute 
    # any tasks involving text 
    response = openai.Completion.create(
        # model name used here is text-davinci-003
        # there are many other models available under the 
        # umbrella of GPT-3
        model="text-davinci-003",
        # passing the user input 
        prompt=PROMPT,
        # generated output can have "max_tokens" number of tokens 
        max_tokens=MaxToken,
        # number of outputs generated in one call
        n=outputs
    )
    # creating a list to store all the outputs
    output = list()
    for k in response['choices']:
        output.append(k['text'].strip())
    return output

# Function to convert
def listToString(s):
 
    # initialize an empty string
    str1 = " "
 
    # return string
    return (str1.join(s))   

def main():

    sel_option=[]

    # read the file for the questions and the hints
    st.header("Data Governance Maturity Evaluator")

    q_file=open("questions.json")
    input_data=json.load(q_file)

    # create the drop down menu by category
    for category in input_data:
        with st.expander(category["category"]):
            for question in category["QList"]:
                id = question["name"]
                #ans=question["hints"]
                sel_option.append(st.radio
                    (
                        question["question"],
                        ("yes", "no","unsure","partial","in-progress"),
                        key=f"{id}",
                        horizontal=True
                    )
                )
        
    df=pd.DataFrame(sel_option)
    df.columns=['selection']
    df_cal=pd.DataFrame(input_data)

    # add the score from the selection
    s=[]
    score = 0
    for idx,row in df.iterrows() :

        if row['selection']=='yes':
            score = score + 5
        if row['selection']=='partial':
            score = score + 4
        if row['selection']=='in-progress':
            score = score + 3
        if row['selection']=='no':
            score = score + 1
        if row['selection']=='unsure':
            score = score + 2
        if (idx+1)%4 ==0:
            s.append(score)
            score = 0
        
    # calculate the score
    df_cal['total_score']=s
    df_cal['ideal_total_score']=20
    df_cal["total_score"] = df_cal["category_wt"] * df_cal["total_score"] /100
    df_cal["ideal_total_score"] = df_cal["category_wt"] * 20 /100



    # plot
    plot_score_analysis(df_cal)

    # final score display
    final_score = (df_cal[["total_score"]].sum())*100/20
    result = final_score[0]
    delta_score=round(((result-100)*100/100),2)
    st.metric("Your current score is",round(result,2),delta=delta_score)

    # prompt for query
    st.markdown(f"### Ask how to improve")
    prompt_query = st.text_input('',placeholder='enter your query')

    res_box=st.empty()

    if prompt_query != '':
        m=[]
        response= comp(prompt_query, MaxToken=3000, outputs=3)
        res=listToString(response)
        res_box.markdown(f'{res}')


#create a data strategy for claims data

if __name__=="__main__":
    main()


