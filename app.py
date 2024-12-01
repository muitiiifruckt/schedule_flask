
from flask import Flask, request, render_template
import logging


# Настройка логгирования
logging.basicConfig(level=logging.DEBUG)  # Устанавливаем уровень логирования
logger = logging.getLogger(__name__)  # Получаем логгер для текущего модуля

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('index.html')
    
    
@app.route('/submit', methods=['POST'])
def submit():
    selected_option = request.form.get('option')  # Выбранный вариант
    
    # Логирование полученных данных
    logger.info(f"Получены данные:  option={selected_option}")
    
    return f"Вы выбрали: {selected_option}"









if __name__ == '__main__':
    app.run(debug=True)
