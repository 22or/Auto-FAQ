import numpy as np
from transformers import AutoModelForQuestionAnswering, AutoTokenizer
from mlserver import MLModel
from mlserver.codecs import decode_args
import torch
from typing import List
import spacy

class FaqModel(MLModel):
	async def load(self) -> bool:
		model_name = "bert-large-uncased-whole-word-masking-finetuned-squad"
		self._tokenizer = AutoTokenizer.from_pretrained(model_name)
		self._model = AutoModelForQuestionAnswering.from_pretrained(model_name)

		self._nlp = spacy.load("en_core_web_sm")
	
	@decode_args
	async def predict(self,question: List[str], context: List[str]) -> np.ndarray:

		inputs = self._tokenizer(question,context,return_tensors="pt")
		outputs = self._model(**inputs)
		start_logits = outputs.start_logits
		end_logits = outputs.end_logits

		max_start_logit = torch.max(start_logits).item()
		max_end_logit = torch.max(end_logits).item()
		confidence_score = (max_start_logit + max_end_logit) / 2

		answer_start = torch.argmax(start_logits)
		answer_end = torch.argmax(end_logits) + 1
		answer = self._tokenizer.convert_tokens_to_string(self._tokenizer.convert_ids_to_tokens(inputs["input_ids"][0][answer_start:answer_end]))

		doc = self._nlp(answer)
		capitalized_answer = ""
		first = True
		for token in doc:
			if token.is_punct: 
				capitalized_answer += token.text
			elif token.text.isupper():
				capitalized_answer += ' ' + token.text
			elif first:
				capitalized_answer += ' ' + token.text.capitalize()
				first = False
			elif token.pos_ in["PROPN","NNP"]:
				capitalized_answer += ' ' + token.text.capitalize()
			else:
				capitalized_answer += ' ' + token.text
		capitalized_answer = capitalized_answer.strip()

		return np.array([confidence_score,capitalized_answer])