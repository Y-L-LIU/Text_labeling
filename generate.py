from vllm import LLM, SamplingParams
import json

TASK3_wiki = '''Please act as an expert paper writer and exapand the given summary to
write a {section} for a paper to make it fluent and elegant.  Here are the specific requirements: 1.
Enable readers to grasp the main points or essence of the paper
quickly. 2. Allow readers to understand the important informa-
tion, analysis, and arguments throughout the entire paper. 3.
Help readers remember the key points of the paper. 4. Please
clearly state the innovative aspects of your research in the ab-
stract, emphasizing your contributions. 5. Use concise and clear
language to describe your findings and results, making it easier
for reviewers to understand the paper. Please only include the written
{section} section in your answer. Here is the summary:
"{input}" 
 '''
# Sample prompts.
datas = json.load(open("/home/lyl/projects/AIdetect/Text_labeling/data/Statistics_wiki.json",'r'))


# Create a sampling params object.
sampling_params = SamplingParams(temperature=0.8, top_p=0.95,max_tokens=1024,min_tokens=100)

# Create an LLM.
llm = LLM(model="/data1/models/Llama-2-13b-chat-hf")
# Generate texts from the prompts. The output is a list of RequestOutput objects
# that contain the prompt, generated text, and other information.
for ind in range(1,4):
    prompts = [TASK3_wiki.format(input=data["text"], section='introduction') for data in datas]
print(len(prompts))
import time
outputs = llm.generate(prompts[:3], sampling_params)
# Print the outputs.
for output in outputs[:1]:
    prompt = output.prompt
    generated_text = output.outputs[0].text
    print(f"Prompt: {prompt!r}, Generated text: {generated_text}")