from dpr import get_robis_pairs, get_amstar_pairs
import json

import instructor
from litellm import completion
from pydantic import BaseModel


API_Endpoint_Address = "your API endpoint"

class Answer(BaseModel):
    answer_class: str
    quote: str

def get_answer_quote(question_type, question_id, context):
    client = instructor.from_litellm(completion)

    robis_ID_lst = ['1.1', '1.2', '1.3', '1.4', '1.5', '2.1', '2.2', '2.3', '2.4', '2.5',
                        '3.1', '3.2', '3.3', '3.4', '3.5', '4.1', '4.2', '4.3', '4.4', '4.5', '4.6',
                        'A', 'B', 'C']
    
    amstar_ID_lst = ['2', '1', '3', '4', '5', '6', '7', '8', '9', '11', '14', '15', '12', '10', '16', '13']

    robis_query_lst = ["Did the review adhere to pre-defined objectives and eligibility criteria?", 
                "Were the eligibility crieria appropriate for the review question?", 
                "Were eligibility criteria unambiguous?", 
                "Were all restrictions in eligibility crieria based on study characteristics appropriate (e.g. date, sample size, study quality, outcomes measured)? If yes, indicate which study characteristic was an inclusion/exclusion criteria", 
                "Were any restrictions in eligibility criteria based on sources of info appropriate (e.g. publication status or format, language, availability of data)?", 
                "Did the search include an appropriate range of databases/ electronic sources for published and unpublished reports?", 
                "Were methods additional to database searching used to identify relevant reports?", 
                "Were the terms and structure of the search strategy likely to retrieve as many eligible studies as possible?", 
                "Were search strategy restrictions based on date, publication format, or language appropriate?", 
                "Were efforts made to minimise error in selection of studies?", 
                "Were efforts made to minimise error in data collection?", 
                "Were sufficient study characteristics considered for both review authors and readers to be able to interpret the results?", 
                "Were all relevant study results collected for use in the synthesis?", 
                "Was risk of bias (or methodological quality) formally assessed using appropriate criteria?", 
                "Were efforts made to minimise error in risk of bias assessment?", 
                "Did the synthesis include all studies that it should?", 
                "Were all pre-defined analyses reported or departures explained?",
                "Was the synthesis appropriate given the nature and similarity in the research questions, study designs and outcomes across included studies?",
                "Was between-study variation (heterogeneity) minimal or addressed in the synthesis?", 
                "Were the findings robust, e.g. as demonstrated through funnel plot or sensitivity analyses?", 
                "Were biases in primary studies minimal or addressed in the synthesis?", 
                "Did the interpretation of findings address all of the concerns identified in Domains 1 to 4?", 
                "Was the relevance of identified studies to the review's research question appropriately considered?", 
                "Did the reviewers avoid emphasizing results on the basis of their statistical significance?"]

    amstar_query_lst = [
            "Did the report of the review contain an explicit statement that the review methods were established prior to the conduct of the review and did the report justify any significant deviations from the protocol?", 
            "Did the research questions and inclusion criteria for the review include the components of PICO?", 
            "Did the review authors explain their selection of the study designs for inclusion in the review?", 
            "Did the review authors use a comprehensive literature search strategy?", 
            "Did the review authors perform study selection in duplicate?", 
            "Did the review authors perform data extraction in duplicate?", 
            "Did the review authors provide a list of excluded studies and justify the exclusions?", 
            "Did the review authors describe the included studies in adequate detail?", 
            "Did the review authors use a satisfactory technique for assessing the risk of bias (RoB) in individual studies that were included in the review?", 
            "If meta-analysis was performed did the review authors use appropriate methods for statistical combination of results?", 
            "Did the review authors provide a satisfactory explanation for, and discussion of, any heterogeneity observed in the results of the review?", 
            "If they performed quantitative synthesis did the review authors carry out an adequate investigation of publication bias (small study bias) and discuss its likely impact on the results of the review?", 
            "If meta-analysis was performed, did the review authors assess the potential impact of RoB in individual studies on the results of the meta-analysis?", 
            "Did the review authors report on the sources of funding for the studies included in the review?", 
            "Did the review authors report any potential sources of conflict of interest, including any funding they received for conducting the review?", 
            "Did the review authors account for RoB in individual studies when interpreting/ discussing the results of the review?"]
    
    if question_type == 'ROBIS':
        question_index = robis_ID_lst.index(question_id)
        query = robis_query_lst[question_index]
    else:
        question_index = amstar_ID_lst.index(question_id)
        query = amstar_query_lst[question_index]
        
    resp = client.chat.completions.create(
        model="ollama/llama3.1",
        max_tokens=1024,
        messages=[{"content": "I am going to provide a question and a context. Answer the question based on the context given.","role": "user"},
                {"content": "The question is: " + query + " Please answer the question by choosing 'Yes' or 'No'. Then provide a quote that supports your answer.","role": "user"},
                {"content": "The context is: " + context, "role": "user"}],
        api_base=API_Endpoint_Address,
        response_model=Answer,
    )
    answer_class = resp.answer_class
    quote = resp.quote
    return answer_class, quote



