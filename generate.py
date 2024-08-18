from vllm import LLM, SamplingParams
import datasets
from Text_labeling.AIDetect.prompts import *



def load_conv(model_name, msg):
    if 'Llama-2' in model_name:
        return llama2_template.format(user_message=msg)
    elif 'Llama-3' in model_name:
        return llama3_template.format(user_message=msg)
    elif 'Mistral' in model_name:
        return mistral_template.format(user_message=msg)
    else:
        raise ValueError(f'Is the prompt of model {model_name} defined?')

def load_cfg(model):
    if 'Llama-2' in model_name:
        return {'temperature':0.6,'top_p':0.9,}
    elif 'Llama-3' in model_name:
        return {'temperature':0.6,'top_p':0.9,}
    elif 'Mistral' in model_name:
        return {'temperature':0.8, 'top_p':0.95}
    else:
        raise ValueError(f'Is the config of model {model_name} defined?')


def main(path, cat, task_id, output_file, num_gpu=1):
    data = datasets.load_dataset('/data1/dataset/AIGen-HUMAN/MGT-human.py', trust_remote_code=True)
    if cat not in data:
        raise ValueError('category is invalid')
    chats=[]
    for item in data[cat]:
        if task_id==1:
            #completion task, count the token
            tmp = item['text'].split(' ')
            fmats = {'X':len(tmp)//2, 'input':' '.join(tmp[:len(tmp)//2])}
        else:
            fmats = {'input': item['text']}

        if 'arxiv' in item['file']:
            chats.append( load_conv(path, arxiv_prompt[task_id].format(**fmats)) ) 
        elif 'wiki' in item['file']:
            chats.append( load_conv(wiki_prompt[task_id].format(**fmats) ))
        elif 'gutenberg' in item['file']:
            chats.append( load_conv(gutendex_prompt[task_id].format(**fmats) ))

    cfg = load_cfg(path)
    sampling_params = SamplingParams(max_tokens=4096, **cfg)
    llm = LLM(model=path,tensor_parallel_size=num_gpu,quantization='awq')
    outputs = llm.generate(chats, sampling_params)
    # For debug
    for idx, output in enumerate(outputs):
            out.append({'prompt': output.prompt, 'answer': output.outputs[0].text})
    #         print('\n\n\n')
    #         print('>>> sample - %d' % idx)
    #         print('prompt = ', question_dataset[idx])
    #         print('answer = ', output.outputs[0].text)
    
    if output_file is not None:
        with open(output_file, 'w') as f:
            for li in out:
                f.write(json.dumps(li))
                f.write("\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process model name.")
    parser.add_argument('--path', type=str, help="Path to the dataset")
    parser.add_argument('--cat', type=str, help="Category name")
    parser.add_argument('--task_id', type=int, help="Task ID")
    parser.add_argument('--num_gpu', type=int, default=1, help="Number of GPUs to use (default: 1)")
    parser.add_argument('--output_file', type=int, default=1, help="output_file")

    args = parser.parse_args()
    
    main(args.path, args.cat, args.task_id,output_file, args.num_gpu)
    args = parser.parse_args()
    
    main(args.model_name)
