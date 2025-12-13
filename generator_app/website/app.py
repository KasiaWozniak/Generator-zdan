import json
from flask import render_template, Blueprint, request, redirect, url_for
from generator_app.website.services.generate_subject import *
from generator_app.website.services.generate_verb import generate_verb

views = Blueprint('views', __name__)

@views.route('/', methods=["GET", "POST"])
def index():
    if request.method == 'POST':
        arguments = get_noun_phrase(request.form)
        return redirect(url_for('views.predicate', arguments=json.dumps(arguments)))

    return render_template('subject.html')


@views.route('/predicate/<arguments>', methods=["GET", "POST"])
def predicate(arguments):
    arguments = json.loads(arguments)
    if request.method == 'POST':
        tense = request.form.get("tense")
        mood = request.form.get("mood")
        question = request.form.get("question")

        arguments["tense"] = tense

        if mood == "positive":
            arguments["mood"] = True
        elif mood == "negative":
            arguments["mood"] = False

        if question == "true":
            arguments["question"] = True
        elif question == "false":
            arguments["question"] = False

        return redirect(url_for('views.complement', arguments=json.dumps(arguments)))

    return render_template('predicate.html')


@views.route('/complement/<arguments>', methods=["GET", "POST"])
def complement(arguments):
    arguments = json.loads(arguments)
    if request.method == 'POST':
        complement = get_noun_phrase(request.form)
        arguments["complement"] = complement

        return redirect(url_for('views.sentence', arguments=json.dumps(arguments)))

    return render_template('complement.html')


@views.route('/sentence/<arguments>')
def sentence(arguments):
    arguments = json.loads(arguments)
    print(arguments)

    subject = generate_subject(arguments)
    complement = generate_subject(arguments["complement"])
    sentence = generate_verb(subject, arguments["tense"], arguments["number"], arguments["mood"], arguments["question"],
                             arguments["pronoun_or_article"], arguments["noun"], complement)

    return render_template('display.html', sentence=sentence)


def get_noun_phrase(form):
    pronoun = form.get("pronoun_or_article")
    number = form.get("number")

    if form.get("noun_phrase") == "true":
        noun = True
    else:
        noun = False

    if form.get("adjective") == "true":
        adjective = True
    else:
        adjective = False

    return {"pronoun_or_article": pronoun,
            "adjective": adjective,
            "number": number,
            "noun": noun}
