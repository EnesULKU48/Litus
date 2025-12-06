from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, DecimalField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Optional, Email
from config import ALLOWED_EXTENSIONS


class ProductForm(FlaskForm):
    """Ürün ekleme/düzenleme formu"""
    name = StringField('Ürün Adı', validators=[DataRequired()])
    slug = StringField('Slug', validators=[DataRequired()])
    price = DecimalField('Fiyat', validators=[DataRequired(), NumberRange(min=0)])
    description = TextAreaField('Açıklama', validators=[Optional()])
    stock = IntegerField('Stok', validators=[DataRequired(), NumberRange(min=0)], default=0)
    category_id = SelectField('Kategori', coerce=int, validators=[DataRequired()])
    image = FileField('Ürün Görseli', validators=[FileAllowed(ALLOWED_EXTENSIONS, 'Sadece görsel dosyaları!')])
    submit = SubmitField('Kaydet')


class CategoryForm(FlaskForm):
    """Kategori ekleme formu"""
    name = StringField('Kategori Adı', validators=[DataRequired()])
    slug = StringField('Slug', validators=[DataRequired()])
    submit = SubmitField('Ekle')


class CommentForm(FlaskForm):
    """Yorum formu"""
    author_name = StringField('Adınız', validators=[DataRequired()])
    content = TextAreaField('Yorumunuz', validators=[DataRequired()])
    submit = SubmitField('Yorum Yap')


class ContactForm(FlaskForm):
    """İletişim formu"""
    name = StringField('Adınız', validators=[DataRequired()])
    email = StringField('E-posta', validators=[DataRequired(), Email()])
    subject = StringField('Konu', validators=[DataRequired()])
    message = TextAreaField('Mesajınız', validators=[DataRequired()])
    submit = SubmitField('Gönder')

