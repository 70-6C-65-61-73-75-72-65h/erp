# Generated by Django 2.2.6 on 2019-12-03 17:41

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Simulation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateField(auto_now_add=True)),
                ('today', models.DateField()),
                ('status', models.BooleanField(default=False)),
                ('today_time', models.DateTimeField()),
                ('auto_populated', models.BooleanField(default=False)),
                ('percent_pre_buy', django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(), size=2)),
                ('percent_pre_buy_max_prob', models.FloatField(verbose_name=0.7)),
                ('minimal_zp', models.IntegerField()),
                ('pharmacys_sizes', models.FloatField()),
                ('department_size', models.FloatField()),
                ('tax_property_size_limit', models.FloatField()),
                ('pharmacys_spendingds', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), size=2)),
                ('ph_sp_max_prob', models.FloatField(verbose_name=0.5)),
                ('department_spendingds', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), size=2)),
                ('dpt_sp_max_prob', models.FloatField(verbose_name=0.5)),
                ('veh_repair_price_month', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), size=2)),
                ('v_r_max_prob', models.FloatField(verbose_name=0.5)),
                ('vehicles_purchase_num', models.IntegerField()),
                ('vehicles_whtransfer_num', models.IntegerField()),
                ('vehicles_num', models.IntegerField()),
                ('vehicle_name', models.CharField(default='Ford Transit FT-190L', max_length=200)),
                ('vehicle_price', models.FloatField()),
                ('fuel_price', models.FloatField()),
                ('fuel_type', models.CharField(max_length=100)),
                ('vehicle_consumption', models.FloatField()),
                ('delivery_added_time_koef', models.FloatField()),
                ('num_of_phs_on_1_vehicle', models.IntegerField()),
                ('warehouse_num', models.IntegerField(default=44)),
                ('number_to_dispatch', models.IntegerField(default=300)),
                ('normal_purch_days', models.IntegerField(default=28)),
                ('threshold_days', models.IntegerField(default=7)),
                ('number_of_products_names', models.IntegerField()),
                ('product_markup_rate', django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(), size=2)),
                ('product_cost_price', django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(), size=2)),
                ('product_cost_price_max_prob', models.FloatField(default=0.15)),
                ('whp_self_rate', django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(), size=2)),
                ('whp_quantity', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), size=2)),
                ('day_quantity_range', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), size=2)),
                ('d_q_r_max_prob', models.FloatField(default=0.7)),
                ('salary_pharmacist', models.FloatField(default=7000.0)),
                ('pharmacist_per_wh', models.IntegerField(default=3)),
                ('pharmacist_num', models.IntegerField()),
                ('salary_HR', models.FloatField(default=11000.0)),
                ('HR_num', models.IntegerField(default=6)),
                ('salary_accounting_manager', models.FloatField(default=8000.0)),
                ('accounting_manager_num', models.IntegerField(default=2)),
                ('salary_director', models.FloatField(default=15000.0)),
                ('salary_cleaner', models.FloatField(default=5000.0)),
                ('cleaner_per_wh', models.IntegerField(default=2)),
                ('cleaner_num', models.IntegerField()),
                ('salary_loader', models.FloatField(default=7000.0)),
                ('loader_per_vehicle', models.IntegerField(default=2)),
                ('loader_num', models.IntegerField()),
                ('salary_driver', models.FloatField(default=10000.0)),
                ('driver_per_vehicle', models.IntegerField(default=2)),
                ('driver_num', models.IntegerField()),
                ('salary_sys_admin', models.FloatField(default=10000.0)),
                ('sys_admin_num', models.IntegerField(default=2)),
                ('num_of_clients', models.IntegerField(default=88)),
                ('that_user_password', models.CharField(default='that_user_111', max_length=30)),
                ('assesm_to_delete_worker', models.IntegerField(default=2)),
                ('threshold_bad_assesses', models.IntegerField(default=4)),
                ('prob_delete_worker', models.FloatField(default=0.3)),
                ('prob_of_client_assessment', models.FloatField(default=0.1)),
                ('prob_max_assesm_client', models.FloatField(default=0.8)),
                ('assesment_range', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), size=2)),
                ('prob_of_worker_fired_dir', models.FloatField(default=0.01)),
                ('prob_of_worker_fired_hr', models.FloatField(default=0.05)),
                ('prob_of_worker_fired_am', models.FloatField(default=0.05)),
                ('prob_of_worker_fired_sa', models.FloatField(default=0.08)),
                ('prob_of_worker_fired_cl', models.FloatField(default=0.3)),
                ('prob_of_worker_fired_ld', models.FloatField(default=0.4)),
                ('prob_of_worker_fired_dr', models.FloatField(default=0.15)),
                ('prob_of_worker_fired_ph', models.FloatField(default=0.1)),
            ],
        ),
    ]
