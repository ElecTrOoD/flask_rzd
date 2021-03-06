# импортируем зависимости
import os
from sqlite3 import IntegrityError

from flask import Blueprint, render_template, redirect, url_for, send_from_directory, request, send_file
from flask_login import login_required
from sqlalchemy import desc

from mainapp.config import UPLOADED_PDF_DEST
from mainapp.extensions import db, qr
from mainapp.forms.main import TechMapForm, pdf, VideoTutorialForm, QRCodeForm
from mainapp.models import TechMap, VideoTutorial

# создаем и конфигурируем экземпляр "чертежа" главного приложения проекта, технологические карты и обучающие видео
main = Blueprint('main', __name__, url_prefix='/', static_folder='../static')


# контроллер главной страницы, отдает страницу с технологическими картами
@main.route('/')
def tech_maps():
    tech_maps_objects = TechMap.query.order_by(desc(TechMap.id))
    return render_template(
        'main/tech_maps_list.html', tech_maps=tech_maps_objects
    )


# контроллер страницы обучающих видео, отдает страницу с обучающими видео
@main.route('/videos')
def video_tutorials():
    videos = VideoTutorial.query.order_by(desc(VideoTutorial.id))
    return render_template(
        'main/tech_videos_list.html', videos=videos
    )


# контроллер страницы технологической карты, отдает PDF файл технологической карты
@main.route('/techmap/<int:tech_id>')
def tech_map_page(tech_id):
    tech_map = TechMap.query.get(tech_id)
    return send_from_directory(UPLOADED_PDF_DEST, tech_map.pdf)


# контроллер страницы обучающего видео, отдает страницу с видеоплеером
@main.route('/video/<int:video_id>')
def video_tutorial_page(video_id):
    video_tutorial = VideoTutorial.query.get(video_id)
    return render_template('main/video.html', video_tutorial=video_tutorial)


# контроллер публикации обучающего видео, отдает страницу с формой
@main.route('/add_vt', methods=['GET'])
@login_required
def add_video_tutorial():
    form = VideoTutorialForm(request.form)
    return render_template('main/add_video.html', form=form)


# контроллер публикации обучающего видео, срабатывает при POST запросе. Принимает и валидирует данные с формы.
# Если данные валидны, создаёт новое обучающее видео
@main.route('/add_vt', methods=['POST'])
@login_required
def add_video_tutorial_post():
    form = VideoTutorialForm()
    errors = []
    if form.validate_on_submit():
        if VideoTutorial.query.filter_by(name=form.name.data).count():
            form.name.errors.append('Введите уникальное название')
            return render_template('main/add_video.html', form=form)
        video_tutorial = VideoTutorial(
            name=form.name.data,
            link=form.link.data,
        )

        db.session.add(video_tutorial)
        try:
            db.session.commit()
        except IntegrityError:
            errors.append('Неизвестная ошибка. Попробуйте снова.')
            return render_template('main/add_video.html', form=form, errors=errors)
        else:
            return redirect(url_for('main.video_tutorials'))

    else:
        return render_template('main/add_video.html', form=form)


# контроллер публикации техгологической карты, отдает страницу с формой
@main.route('/add_tm', methods=['GET'])
@login_required
def add_tech_map():
    form = TechMapForm(request.form)
    return render_template('main/add_tech_map.html', form=form)


# контроллер публикации технологической карты, срабатывает при POST запросе. Принимает и валидирует данные с формы.
# Если данные валидны, создаёт новую технологическую карту
@main.route('/add_tm', methods=['POST'])
@login_required
def add_tech_pdf_post():
    form = TechMapForm()
    errors = []
    if form.validate_on_submit():
        if TechMap.query.filter_by(name=form.name.data).count():
            form.name.errors.append('Введите уникальное название')
            return render_template('main/add_tech_map.html', form=form)
        tech_map = TechMap(
            name=form.name.data,
            pdf=pdf.save(request.files['pdf']),
        )

        db.session.add(tech_map)
        try:
            db.session.commit()
        except IntegrityError:
            errors.append('Unexpected error. Try again.')
            return render_template('main/add_tech_map.html', form=form, errors=errors)
        else:
            return redirect(url_for('main.tech_maps'))

    else:
        return render_template('main/add_tech_map.html', form=form)


# контроллер удаления технологической карты
@main.route('/tm_delete/<int:tech_id>')
@login_required
def tech_map_delete(tech_id):
    tech = TechMap.query.get(tech_id)
    db.session.delete(tech)
    db.session.commit()
    os.remove(f'{UPLOADED_PDF_DEST}{tech.pdf}')
    return redirect(url_for('.tech_maps'))


# контроллер удаления обучающего видео
@main.route('/vt_delete/<int:video_id>')
@login_required
def video_tutorial_delete(video_id):
    video_tutorial = VideoTutorial.query.get(video_id)
    db.session.delete(video_tutorial)
    db.session.commit()
    return redirect(url_for('.video_tutorials'))


# контроллер страницы создания QR-кодов
@main.route('/qrcode', methods=['GET'])
def qrcode():
    form = QRCodeForm()
    return render_template('main/generate_qr.html', form=form)


# контроллер страницы создания QR-кодов, срабатывает при POST запросе. Принимает и валидирует данные с формы.
# Если данные валидны, отдаёт картинку QR-кода
@main.route('/qrcode', methods=['POST'])
def qrcode_post():
    form = QRCodeForm()
    if form.validate_on_submit():
        return send_file(
            qr.qrcode(form.link.data, mode='raw', box_size=10, border=2, error_correction='H',
                      icon_img=f'{main.static_folder}/images/favicon.png'),
            mimetype='image/png')
    else:
        return render_template('main/generate_qr.html', form=form)
