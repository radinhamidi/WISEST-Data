from convert_text import convert_to_text
from generate_passage import txt_to_json
from dpr import get_robis_pairs, get_amstar_pairs
from LLM import get_answer_quote
import json



def get_dict(paper_ID: int, pdf_path: str):
    results_lst = []
    text = convert_to_text(paper_ID, pdf_path)
    txt_file_path = '../Data/text/' + str(paper_ID) + '_text' + '.txt'
    passage_file_path = '../Data/passage/' + str(paper_ID) + '_passage.json'
    txt_to_json(txt_file_path, passage_file_path)

    with open(passage_file_path, 'r') as json_file:
        passage  = json.load(json_file)

    robis_pairs = get_robis_pairs(passage)
    amstar_pairs = get_amstar_pairs(passage)
    
    #ROBIS
    question_type = "ROBIS"
    questions_lst = []
    for pair in robis_pairs:
        question_id = pair['question ID']
        context = pair['context']
        answer_class, quote = get_answer_quote(question_type, question_id, context)
        item_dict = {"question ID": question_id, "context": context, "answer class": answer_class, "answer quote": quote}
        questions_lst.append(item_dict)
        print(questions_lst)
    temp_dic = {"question type": "ROBIS", "questions": questions_lst}
    results_lst.append(temp_dic)

    question_type = "AMSTAR"
    questions_lst = []
    for pair in amstar_pairs:
        question_id = pair['question ID']
        context = pair['context']
        answer_class, quote = get_answer_quote(question_type, question_id, context)
        item_dict = {"question ID": question_id, "context": context, "answer class": answer_class, "answer quote": quote}
        questions_lst.append(item_dict)
        print(questions_lst)
    temp_dic = {"question type": "AMSTAR", "questions": questions_lst}
    results_lst.append(temp_dic)

    return results_lst


### Sample code
# pdf_path = '../Data/PDFs/5621_Checchio_2017.pdf'
# paper_ID = 5621

# results = get_dict(paper_ID, pdf_path)

# output_file_path = '../Data/output/' + str(paper_ID) + '_output' + '.json'
# with open(output_file_path, 'w') as file:
#     json.dump(results, file, indent=4, ensure_ascii=False)
