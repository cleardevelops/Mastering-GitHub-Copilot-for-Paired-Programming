import os
import random

from dotenv import load_dotenv
from flask import Flask, render_template_string, request

load_dotenv()

app = Flask(__name__)

CHOICES = ("rock", "paper", "scissors")
BEATS = {"rock": "scissors", "paper": "rock", "scissors": "paper"}

PAGE = """
<!doctype html>
<html lang="en">
<head><meta charset="utf-8"><title>{{ title }}</title></head>
<body>
  <h1>{{ title }}</h1>
  <form method="post">
    {% for c in choices %}
      <button type="submit" name="choice" value="{{ c }}">{{ c|capitalize }}</button>
    {% endfor %}
  </form>
  {% if result %}
    <p>You chose <b>{{ player }}</b>, computer chose <b>{{ computer }}</b>: {{ result }}</p>
  {% endif %}
</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def index():
    player = computer = result = None
    if request.method == "POST":
        player = request.form.get("choice")
        if player in CHOICES:
            computer = random.choice(CHOICES)
            if player == computer:
                result = "It's a tie!"
            elif BEATS[player] == computer:
                result = "You win!"
            else:
                result = "You lose!"
    return render_template_string(
        PAGE,
        title=os.getenv("APP_TITLE", "Rock Paper Scissors"),
        choices=CHOICES,
        player=player,
        computer=computer,
        result=result,
    )


if __name__ == "__main__":
    app.run(debug=os.getenv("FLASK_DEBUG") == "1")

