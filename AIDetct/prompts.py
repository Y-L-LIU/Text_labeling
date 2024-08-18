instruct_begin = '[INST]'
instruct_end = '[/INST]'
llama2_template = """
<s>[INST] {user_message} [/INST]
"""
llama3_template = """
<|begin_of_text|><|start_header_id|>user<|end_header_id|>

{user_message}<|eot_id|><|start_header_id|>assistant<|end_header_id|>
"""
mistral_template = """
<s>[INST] {user_message} [/INST]

"""
llama_system_prompt = "You are a helpful and harmless assistant"
mistral_system_prompt = ("Always assist with care, respect, and truth. Respond with utmost utility yet securely. Avoid "
                         "harmful, unethical, prejudiced, or negative content. Ensure replies promote fairness and "
                         "positivity.")

                         
TASK1_arxiv = '''Please act as an expert paper writer and expand the given summary to
write a section for a paper to make it fluent and elegant.  Here are the specific requirements: 1.
Enable readers to grasp the main points or essence of the paper
quickly. 2. Allow readers to understand the important informa-
tion, analysis, and arguments throughout the entire paper. 3.
Help readers remember the key points of the paper. 4. Please
clearly state the innovative aspects of your research in the ab-
stract, emphasizing your contributions. 5. Use concise and clear
language to describe your findings and results, making it easier
for reviewers to understand the paper. Please only include the written
section section in your answer. Here is the summary:
"{input}" 
 You should only return the generated content.
 '''

TASK2_arxiv = '''
Please act as an expert paper writer and complete the
second half of the given first half of an section section to make it fluent and elegant.
Please only include the second half of the section in your
answer. Here are the specific requirements: 1. The length of the
second half should be about {X} words. 2. The existing content
should serve as the foundation, and the new portion should
seamlessly integrate with it. 3. Use your expertise and maintain
its technical accuracy and clarity. 4. Ensure a coherent and
logical flow between the first and second halves. 5. Use clear and
academic language, making it easier for reviewers to understand
the paper. Here is the first half of the paper section:
"{input}"
You should only return the second half of the paper.
'''

TASK3_arxiv = '''
Please act as an expert paper editor and revise a section of the paper to make it more fluent and elegant. 
Please only include the revised section in your answer. Here are the specific
requirements: 1. Enable readers to grasp the main points or
essence of the paper quickly. 2. Allow readers to understand
the important information, analysis, and arguments throughout
the entire paper. 3. Help readers remember the key points of
the paper. 4. Please clearly state the innovative aspects of your
research in the section, emphasizing your contributions. 5. Use
concise and clear language to describe your findings and results,
making it easier for reviewers to understand the paper. Here is
the original section of the paper: 
"{input}"
You should only return the revised section.
'''
arxiv_prompt = [TASK1_arxiv, TASK2_arxiv, TASK3_arxiv]

TASK1_gutendex = '''Please act as an expert book writer and expand the given summary to
write a book to make it fluent and elegant. Please only include the written
book in your answer. Here are the specific requirements:
1. Clarity: Ensure that your writing is clear and easy to understand. 
Avoid jargon and complex language that may confuse the reader. 
2. Relevance: Make sure that the content you are writing is relevant
 to the topic at hand. Do not deviate from the main subject.
3. Accuracy: Ensure that all the information you provide is 
accurate and up-to-date. This includes statistics, facts, and theories.
4. Brevity: Keep your writing concise. Avoid unnecessary words or 
phrases that do not add value to the content.
Here is the summary:
 "{input}" 
 You should only return the generated text.

'''

TASK2_gutendex = '''
Please act as an expert paper writer and complete the
second half of the given first half of an book content from the
perspective of a paper reviewer to make it fluent and elegant.
Please only include the second half of the book content in your
answer. Here are the specific requirements: 1. The length of the
second half should be about {X} words. 2. The existing content
should serve as the foundation, and the new portion should
seamlessly integrate with it. 3. Use your expertise and maintain
its technical accuracy and clarity. 4. Ensure a coherent and
logical flow between the first and second halves. 5. Use clear and
academic language, making it easier for reviewers to understand
the paper. Here is the first half of the book content:
"{input}"
You should only return the second half of the book content.

'''

TASK3_gutendex = '''
Please act as an expert book editor and revise the
book content from the perspective of a book editor
to make it fluent and elegant.
1. Clarity: Ensure that your writing is clear and easy to understand. 
Avoid jargon and complex language that may confuse the reader. 
2. Relevance: Make sure that the content you are writing is relevant
 to the topic at hand. Do not deviate from the main subject.
3. Accuracy: Ensure that all the information you provide is 
accurate and up-to-date. This includes statistics, facts, and theories.
4. Brevity: Keep your writing concise. Avoid unnecessary words or 
phrases that do not add value to the content.
Here is the original book content:
 "{input}" 
 You should only return the revised book.
'''
gutendex_prompt = [TASK1_gutendex,TASK2_gutendex,TASK3_gutendex]
TASK1_wiki = '''Please act as an expert Wiki writer and write expand the given summary to
write a wiki page from the perspective of a wiki editor
to make it fluent and elegant. Here are the specific requirements:
1. You should provide accurate and comprehensive information.
Use reliable sources and cross-check your information to ensure its accuracy.
2. Wiki articles should be neutral and unbiased. Avoid expressing 
personal opinions or promoting a particular viewpoint. Instead, present all relevant 
information and let the readers form their own opinions.3. Your writing should be clear and easy to understand. Avoid using complex sentences 
and unnecessary words. Remember, your goal is to convey information, not to 
showcase your vocabulary. Please only include the written
page in your answer. Here is the summary: \n
"{input}" 
'''


TASK2_wiki = '''
Please act as an expert Wiki writer and complete the
second half of the given first half of an Wiki page from the
perspective of a Wiki reviewer to make it fluent and elegant.
 Here are the specific requirements: 1. The length of the
second half should be about {X} words. 2. The existing content
should serve as the foundation, and the new portion should
seamlessly integrate with it. 3. Use your expertise and maintain
its technical accuracy and clarity. 4. Ensure a coherent and
logical flow between the first and second halves. 5. Use clear and
academic language, making it easier for reviewers to understand
the Wiki. Please only include the second half of the Wiki page in your
answer. Here is the first half of the Wiki:\n
"{input}"
You should only return the second half of the wiki page.
'''


TASK3_wiki = '''Please act as an expert wiki editor and revise the
wiki content from the perspective of a wiki editor
to make it fluent and elegant. Here are the specific requirements:
1. You should provide accurate and comprehensive information.
Use reliable sources and cross-check your information to ensure its accuracy.
2. Wiki articles should be neutral and unbiased. Avoid expressing 
personal opinions or promoting a particular viewpoint. Instead, present all relevant 
information and let the readers form their own opinions.3. Your writing should be clear and easy to understand. Avoid using complex sentences 
and unnecessary words. Remember, your goal is to convey information, not to 
showcase your vocabulary. Please only include the written wiki page in your answer.
Here is the original wiki page:\n
"{input}" 
You should only return the revised page '''

wiki_prompt=[TASK1_wiki,TASK2_wiki,TASK3_wiki]