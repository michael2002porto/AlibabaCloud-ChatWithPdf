# For download the models
# !pip install huggingface_hub

# model_name_or_path = "TheBloke/Llama-2-13B-chat-GGML"
# model_basename = "llama-2-13b-chat.ggmlv3.q5_1.bin" # the model is in bin format
model_name_or_path = "TheBloke/Llama-2-7B-GGML"
model_basename = "llama-2-7b.ggmlv3.q5_1.bin" # the model is in bin format


from huggingface_hub import hf_hub_download

model_path = hf_hub_download(repo_id=model_name_or_path, filename=model_basename)
# model_path= "/root/.cache/huggingface/hub/models--TheBloke--Llama-2-13B-chat-GGML"

# !pip install llama-cpp-python
# CPU
# from llama_cpp import Llama

# lcpp_llm = Llama(
#     model_path=model_path,
#     n_threads=64, # CPU cores
#     )

prompt = "Write a linear regression in python"
prompt_template=f'''SYSTEM: You are a helpful, respectful and honest assistant. Always answer as helpfully.

USER: {prompt}

ASSISTANT:
'''

# response = lcpp_llm(
#     prompt=prompt_template,
#     max_tokens=256,
#     temperature=0.5,
#     top_p=0.95,
#     repeat_penalty=1.2,
#     top_k=50,
#     echo=True
#     )

# print(response["choices"][0]["text"])

# Inference with langchain

# !pip -q install langchain

# lcpp_llm.reset()
# lcpp_llm.set_cache(None)
# lcpp_llm = None
# del lcpp_llm

# from langchain.llms import LlamaCpp
from langchain import PromptTemplate, LLMChain
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from huggingface_hub import hf_hub_download
# from langchain.embeddings import LlamaCppEmbeddings, HuggingFaceEmbeddings, HuggingFaceInstructEmbeddings

template = """USER: {question}
ASSISTANT: Let's work this out in a step by step way to be sure we have the right answer."""
prompt = PromptTemplate(template=template, input_variables=["question"])

# Callbacks support token-wise streaming
callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
# Verbose is required to pass to the callback manager

model_repo = 'daryl149/llama-2-13b-chat-hf'
# Loading model,
llmLlama2 = AutoModelForCausalLM.from_pretrained(
            model_repo,
            load_in_4bit=True,
            device_map='auto',
            torch_dtype=torch.float16,
            low_cpu_mem_usage=True,
            trust_remote_code=True
            )

max_len = 8192

embeddingsllama2 = LlamaCppEmbeddings(model_path=model_path)
embeddings_model_name = "hkunlp/instructor-base"

embeddings_minilm = HuggingFaceInstructEmbeddings(model_name=embeddings_model_name)

llm_chain = LLMChain(prompt=prompt, llm=llmLlama2)


question = "Write a linear regression in python"

# llm_chain.run(question)