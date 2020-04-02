from flask import Flask, request
import logging
import json

app = Flask(__name__)

logging.basicConfig(level=logging.INFO, filename='app.log', format='%(asctime)s %(levelname)s %(name)s %(message)s')

@app.route('/post', methods=['POST'])
def main():

    logging.info('Request: %r', request.json)

    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }

    handler(request.json)

    logging.info('Request: %r', response)

    return json.dumps(response)


def handler(event):
    """
    Точка входа для облачной функции.
    :param event: содержимое request.json().
    :param context: информация о текущем контексте выполнения.
    :return: ответ будет представлен в виде json автоматически.
    """
    text = 'Привет, я повторю все, что вы скажете'
    if 'request' in event and \
            'original_utterance' in event['request'] \
            and len(event['request']['original_utterance']) > 0:
        text = event['request']['original_utterance']
    return {
        'version': event['version'],
        'session': event['session'],
        'response': {
            'text': text,
            'end_session': 'false'
        },
    }

if __name__ == '__main__':
    app.run()