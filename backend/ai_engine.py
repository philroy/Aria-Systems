import os
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import sqlite3
import git

class AriaAI:
    def __init__(self):
        # Load quantized Mistral CPU model
        self.model_name = "mixtral-8x7b-8bit"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForCausalLM.from_pretrained(self.model_name)
        self.model.to("cpu")
        torch.set_num_threads(8)
        
        # Persistent memory
        self.conn = sqlite3.connect("memory.db", check_same_thread=False)
        self._init_db()

        # GitHub repo
        self.repo_path = os.path.expanduser("~/Aria-Systems")
        if not os.path.exists(self.repo_path):
            git.Repo.clone_from("https://github.com/philroy/Aria-Systems.git", self.repo_path)
        self.repo = git.Repo(self.repo_path)

    def _init_db(self):
        c = self.conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS memory(key TEXT PRIMARY KEY, value TEXT)''')
        self.conn.commit()

    def chat(self, prompt):
        # Add persistent memory retrieval here if needed
        inputs = self.tokenizer(prompt, return_tensors="pt")
        outputs = self.model.generate(**inputs, max_new_tokens=128)
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return response

    def execute_code(self, code):
        try:
            local_vars = {}
            exec(code, {}, local_vars)
            return str(local_vars)
        except Exception as e:
            return str(e)

    def sync_repo(self):
        self.repo.git.add(A=True)
        self.repo.git.commit(m="AI auto-update")
        self.repo.git.push()
