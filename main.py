import streamlit as st
import json
import pandas as pd
import matplotlib.pyplot as plt

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


if __name__=="__main__":
    main()
