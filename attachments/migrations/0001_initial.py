# Generated by Django 5.2.4 on 2025-07-12 19:58

import django.core.files.storage
import django.db.models.deletion
import tinymce.models
import utility.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authentication', '0001_initial'),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Icon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=300, null=True, verbose_name='title')),
                ('icon_fa', models.CharField(blank=True, max_length=50, null=True, verbose_name='icon fa')),
                ('icon_material', models.CharField(blank=True, max_length=50, null=True, verbose_name='material_icon')),
                ('icon_svg', models.TextField(blank=True, null=True, verbose_name='svg_icon')),
                ('color', models.CharField(choices=[('success', 'success'), ('danger', 'danger'), ('warning', 'warning'), ('primary', 'primary'), ('muted', 'muted'), ('secondary', 'secondary'), ('info', 'info'), ('light', 'light'), ('rose', 'rose'), ('dark', 'dark')], default='primary', max_length=50, verbose_name='color')),
                ('width', models.IntegerField(blank=True, null=True, verbose_name='عرض آیکون')),
                ('height', models.IntegerField(blank=True, null=True, verbose_name='ارتفاع آیکون')),
                ('priority', models.IntegerField(default=1000, verbose_name='priority')),
                ('image_origin', models.ImageField(blank=True, null=True, upload_to='attachments/images/Icon/', verbose_name='تصویر آیکون')),
            ],
            options={
                'verbose_name': 'Icon',
                'verbose_name_plural': 'Icons',
            },
            bases=(models.Model, utility.models.LinkHelper),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', tinymce.models.HTMLField(verbose_name='comment')),
                ('datetime_added', models.DateTimeField(auto_now_add=True, verbose_name='date_added')),
                ('page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.page', verbose_name='page')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.profile', verbose_name='profile')),
            ],
            options={
                'verbose_name': 'Comment',
                'verbose_name_plural': 'Comments',
            },
            bases=(models.Model, utility.models.DateTimeHelper),
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='title')),
                ('description', tinymce.models.HTMLField(blank=True, max_length=50000, null=True, verbose_name='توضیحات')),
                ('priority', models.IntegerField(default=1000, verbose_name='priority')),
                ('thumbnail_origin', models.ImageField(blank=True, null=True, upload_to='attachments/images/ImageBase/Thumbnail/', verbose_name='تصویر کوچک')),
                ('image_main_origin', models.ImageField(blank=True, null=True, upload_to='attachments/images/ImageBase/Main/', verbose_name='تصویر اصلی')),
                ('image_header_origin', models.ImageField(blank=True, null=True, upload_to='attachments/images/ImageBase/Header/', verbose_name='تصویر سربرگ')),
                ('date_added', models.DateTimeField(auto_now_add=True, verbose_name='date_added')),
                ('creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='authentication.profile', verbose_name='profile')),
                ('page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.page', verbose_name='page')),
            ],
            options={
                'verbose_name': 'Image',
                'verbose_name_plural': 'تصاویر',
            },
            bases=(models.Model, utility.models.LinkHelper, utility.models.DateTimeHelper),
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_added', models.DateTimeField(auto_now_add=True, verbose_name='datetime_added')),
                ('page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.page', verbose_name='page')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.profile', verbose_name='profile')),
            ],
            options={
                'verbose_name': 'Like',
                'verbose_name_plural': 'Likes',
            },
            bases=(models.Model, utility.models.DateTimeHelper),
        ),
        migrations.CreateModel(
            name='Download',
            fields=[
                ('icon_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='attachments.icon')),
                ('file', models.FileField(blank=True, null=True, storage=django.core.files.storage.FileSystemStorage(base_url='/uploads', location='f:\\private_html\\phoenix11\\upload'), upload_to='attachments/downloads', verbose_name='فایل ضمیمه')),
                ('mirror_link', models.CharField(blank=True, max_length=10000, null=True, verbose_name='آدرس بیرونی')),
                ('date_added', models.DateTimeField(auto_now_add=True, verbose_name='افزوده شده در')),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='اصلاح شده در')),
                ('download_counter', models.IntegerField(default=0, verbose_name='download_counter')),
                ('is_open', models.BooleanField(default=False, verbose_name='is_open?')),
                ('page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.page', verbose_name='page')),
                ('profile', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='authentication.profile', verbose_name='profile')),
                ('profiles', models.ManyToManyField(blank=True, related_name='profile_downloads', to='authentication.profile', verbose_name='profiles')),
            ],
            options={
                'verbose_name': 'Download',
                'verbose_name_plural': 'Downloads',
            },
            bases=('attachments.icon',),
        ),
        migrations.CreateModel(
            name='Link',
            fields=[
                ('icon_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='attachments.icon')),
                ('url', models.CharField(max_length=2000, verbose_name='url')),
                ('new_tab', models.BooleanField(default=False, verbose_name='new_tab')),
                ('page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.page', verbose_name='page')),
                ('profile', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='authentication.profile', verbose_name='profile')),
            ],
            options={
                'verbose_name': 'Link',
                'verbose_name_plural': 'Links',
            },
            bases=('attachments.icon', utility.models.LinkHelper),
        ),
    ]
