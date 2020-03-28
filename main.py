import sys
# insert at 1, 0 is the script path (or '' in REPL)
#sys.path.insert(1, 'squash')
#sys.path.insert(2, 'question-generation')
#sys.path.insert(3, 'question-answering')

from extract_answers.extract_answers import extract_answers
#from mod_interact import question_generation
from question_generation.mod_interact import question_generation
from question_answering.mod_run_squad import run_squad
#from combine_qa import combine_qa
import json

metadata = {"input_text": "Upon graduation, he declared for the 1996 NBA draft and was selected by the Charlotte Hornets with the 13th overall pick", "key": "test_123", "timestamp": "2020-03-14 22:00:54.296257", "settings": {"top_p": 0.9, "gen_frac": 0.5, "spec_frac": 0.8}}

output = extract_answers(metadata)
"""
Input: MetaData JSON   
Output: Input.pkl
"""
gen_questions = question_generation(output)
"""
Input: MetaData JSON, Input.pkl
Output: generated_questions.json
"""
"""
print(gen_questions)
f = open("gen_questions.json","w")
f.write(json.dumps(gen_questions))
f.close()
gen_questions = json.loads(open("gen_questions.json").read())
output = run_squad(gen_questions) # answer generation
print(output)
"""
"""
Input: PredictFile (generated_questions.json)
Output: 
"""
#combine_qa()
