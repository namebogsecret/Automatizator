
from time import time

from src.database import add_message

class GPTSoonEndedError(Exception):
    def __init__(self, message="GPT did not finish the response."):
        self.message = message
        super().__init__(self.message)

def write_answer_to_file(start_time, text, temp, rus_time, id, sql):
    """answers_dir = 'answers'
    if not exists(answers_dir):
        makedirs(answers_dir)
    with open(f'{answers_dir}/answer_{id}_{start_time}.txt', 'w') as f:
        f.write(f"Время запроса: {rus_time:.1f}c. temp = {temp}.\n {text}")"""
    add_message(sql, id, text, start_time, rus_time, temp)

def save_to_sql(sql,id,text, time_long):
    curs = sql.cursor()
    curs.execute(f"INSERT INTO gpt (id, text, time_long) VALUES ({id}, '{text}', {time_long})")
    sql.commit()
def ask_gpt(client, text, temp, timeout, id):
    start_time = time()
    response = client.complete_text(text, temperature=temp,timeout = timeout)
    if response['choices'][0]['finish_reason'] != 'stop':
        raise GPTSoonEndedError('GPT did not finish the response.')
        #raise Exception('GPT не дописал ответ.')
    rus_time = time() - start_time
    text = response['choices'][0]['message']['content']

    return text, rus_time
