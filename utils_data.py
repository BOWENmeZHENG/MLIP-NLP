import torch
import json

def text2token(tokenizer, text):
    text_list = tokenizer.tokenize(text)
    token_list = tokenizer.convert_tokens_to_ids(text_list)
    token = torch.tensor(token_list)[None, :]
    return token

def list2token(tokenizer, text_list):
    token_list = tokenizer.convert_tokens_to_ids(text_list)
    token = torch.tensor(token_list)[None, :]
    return token

def read_data(json_file):
    data_list = []
    with open("train.json") as f:
        for jsonObj in f:
            record = json.loads(jsonObj)
            data_list.append(record)
    return data_list

def cat2digit(classes, cat_text):
    return [classes.get(item, item) for item in cat_text]