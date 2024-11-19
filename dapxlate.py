#!/usr/bin/env python3

"""DAPXlate - Dictionary-Assisted Pretrained Translate
  v0.4 - Silas S. Brown 2024 - public domain, no warranty

  - Prompts an LLM to translate with the aid of
    pre-provided specialist phrase translations.
    Extracts first draft of these from CedPane
    or a file in the same format you've edited.

  - Resulting translation still needs checking.

Beware: trust_remote_code=True is set below.
"""

example_setup_on_Ubuntu_2404_with_Nvidia_GPU = """
# THIS IS NOT YET WORKING on a 2018 laptop with Quadro P1000 GPU.
# You might be able to get it to work on some other piece of kit,
# but it might not work anyway: a preliminary session on the character.ai LLM
# suggests LLMs do not always follow the additional instructions.
# LLMs are however more likely than NMT to handle pre-substituted L2 phrases in the L1 input,
# if you're sure of which word to use (not just listing options).
# There may also be a sentence length limit on LLMs (long sentences need splitting)
# and yes the output DOES need proofreading.

sudo apt install nvidia-cuda-toolkit
pip install --break-system-packages torch modelscope transformers sentencepiece sentencepiece accelerate flash-attn
# torch: 22.04 has package, 24.04 needs pip
# flash-attn takes ~15 hours to compile: https://github.com/Dao-AILab/flash-attention/issues/1038
mkdir -p model
while ! PATH=~/.local/bin:$PATH huggingface-cli download Tele-AI/TeleChat2-115B --local-dir $(pwd)/model; do if df --output=avail -h .|tail -1|[1-9][0-9]*G; then echo Retry in 1 minute; sleep 60; else echo Disk full error; exit 1; fi; done
# - above is best done on wired network (and don't allow machine to suspend; some implementations even seem to stop the download when screensaver is in use)
# - and that 115B model is 423 gigabytes (not counting the approximately 15 gigabytes required for the tools) so I hope you have space on your hard drive: a "500G" drive is NOT likely to be sufficient once OS and inode usage is taken out.
# And it doesn't work anyway:  .cache/huggingface/modules/transformers_modules/model/modeling_telechat.py", line 187, in forward: assert all((i.is_cuda for i in (q, k, v)))
# (after 1 hour 5 minutes running on a 100Mbps network drive; probably about 14 minutes on a local disk)
# Meanwhile, donloading a smaller model instead: Tele-AI/telechat-7B (takes 14 gigabytes for the model)
# gets: RuntimeError: FlashAttention only supports Ampere GPUs or newer.
"""

example_uninstall = """
pip uninstall --break-system-packages accelerate einops filelock flash_attn fsspec functorch hopper huggingface_hub modelscope mpmath networkx nvidia safetensors sentencepiece sympy tokenizers torch torchgen tqdm transformers triton typing-extensions $(pip list --user|grep nvidia-|sed -e 's/ .*//')
sudo apt purge nvidia-cuda-toolkit
sudo apt --purge autoremove
# and remove any unwanted models
"""

import torch, transformers, re, sys

def read_CedPane(cedpane_file):
    "Extract potential specialist translations and names from CedPane, for editing"
    e2c = {}
    for en,zh in [l.split("\t")[:2] for l in open(cedpane_file).read().split("\n")[1:-1]]:
        if "translation" in en or "incorrect" in en or re.search(r"\btypo\b",en): continue # alternate translation, old translation, typo, etc
        en = re.sub(" ([^)]*name[^)]*)","",en) # "X (surname)" is ok if X is capitals only
        for en in [een.strip() for een in re.sub("[(][^)]*[)]","",en).split(';')]: e2c[en] = zh
    return e2c

def main():
    if len(sys.argv) < 2:
        sys.stderr.write(f"Syntax: {sys.argv[0]} cedpane.txt < input-sentences.txt\n")
        sys.exit(1)
    e2c = read_CedPane(sys.argv[1])
    txt = sys.stdin.read()
    tokeniser,model,gcfg=transformers.AutoTokenizer.from_pretrained("model",trust_remote_code=True),transformers.AutoModelForCausalLM.from_pretrained("model",device_map="auto",torch_dtype=torch.float16,trust_remote_code=True),transformers.GenerationConfig.from_pretrained("model")
    sentences = re.findall(r"[^ .!?].*?(?:$|[.!?])(?=$|\s+)",txt,flags=re.DOTALL)
    history = []
    for s in sentences:
        answer,history=model.chat(tokenizer=tokeniser,question=f"请把这个英文句子翻译成汉语：【{s}】做这个翻译，以下个词典条目也许有用：{'；'.join(f'{k}={v}' for k in e2c.items() if k.lower() in s.lower())}",history=history,generation_config=gcfg,stream=False)
        print (answer)
        sys.stdout.flush() # in case watching

if __name__=="__main__": main()
