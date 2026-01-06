import json
from flask import render_template, Blueprint, request, redirect, url_for, session, flash
from generator_app.website.services.generate_subject import *
from generator_app.website.services.generate_verb import generate_verb

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        level = request.form.get('level')
        if not level:
            flash('Proszę wybrać poziom')
            return redirect(url_for('views.index'))
        session.clear()
        session['level'] = level
        return redirect(url_for('views.subject'))
    return render_template('home.html')


@views.route('/restart')
def restart():
    session.clear()
    return redirect(url_for('views.index'))


@views.route('/subject', methods=['GET', 'POST'])
def subject():
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
    args_dict = json.loads(arguments)
    print(args_dict)

    level = session.get("level", "A2_B1")

    subject_tuple = generate_subject(args_dict, level)
    subject_key = subject_tuple[0]
    subject_phrase = subject_tuple[1]

    from generator_app.website.services.choose_random_word import verb_for_subject
    try:
        verb_base = verb_for_subject(subject_key, level)
    except ValueError as e:
        flash(f'Błąd: {e}')
        return redirect(url_for('views.complement', arguments=arguments))

    complement_args = args_dict.get("complement")
    if not complement_args:
         complement_phrase = ""
    else:
         try:
             complement_tuple = generate_complement(
                 complement_args,
                 level,
                 subject_key=subject_key,
                 verb=verb_base
             )
             complement_phrase = complement_tuple[1]
         except ValueError as e:
             flash(f'Błąd: {e}')
             return redirect(url_for('views.complement', arguments=arguments))


    sentence_str = generate_verb(
        subject_phrase,
        verb_base,
        complement_phrase,
        args_dict["tense"],
        args_dict["number"],
        args_dict["mood"],
        args_dict["question"],
        args_dict["noun"]
    )

    return render_template('display.html', sentence=sentence_str, arguments=arguments)

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
