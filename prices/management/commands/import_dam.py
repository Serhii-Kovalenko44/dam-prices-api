import pandas as pd
import io
import requests
import xlrd
from django.core.management.base import BaseCommand
from prices.models import DamPrice


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            '--start-date',
            type=str,
            required=True,
            help='Start date in YYYY-MM-DD format'
        )
    
    def handle(self, *args, **options):
        start_date = options['start_date']
        end_date = pd.Timestamp.now().date() + pd.Timedelta(days=1)
        try:
            dates = pd.date_range(start=start_date, end=end_date)
        except ValueError:
            self.stdout.write('Invalid date format. Please use YYYY-MM-DD')
            return

        for current_date in dates:
            date_str = current_date.strftime('%d.%m.%Y')
            url = f'https://www.oree.com.ua/index.php/PXS/downloadxlsx/{date_str}/DAM/2'

            try:
                response = requests.post(url, timeout=15)
                if response.status_code == 200:
                    self.parse_and_save(response.content, current_date.date())
                    self.stdout.write(f'Successfully imported: {date_str}')
                else:
                    self.stdout.write(f'No data for {date_str}')
            except Exception as e:
                self.stdout.write(f'Error downloading for {date_str}: {e}')
        self.stdout.write('All data has been processed')

    def parse_and_save(self, file_contents, dam_date):
        file_stream = io.BytesIO(file_contents)
        df = pd.read_excel(
            file_stream, 
            engine='xlrd',
            engine_kwargs={'ignore_workbook_corruption': True}
        ).dropna(subset=['Година'])
        df['date'] = dam_date
        df['hour'] = df['Година'].astype(str).str.split(':').str[0].astype(int)
        df = df.rename(columns={
            'Ціна, грн/МВт.год': 'price',
            'Обсяг продажу, МВт.год': 'sales_volume', 
            'Обсяг купівлі, МВт.год': 'purchase_volume',
            'Заявлений обсяг продажу, МВт.год': 'declared_sales_volume',
            'Заявлений обсяг купівлі, МВт.год': 'declared_purchase_volume'
        })

        numeric_cols = ['price', 'sales_volume', 'purchase_volume', 'declared_sales_volume', 'declared_purchase_volume']
        for col in numeric_cols:
            if col in df.columns:
                df[col] = df[col].astype(str).str.replace(r'\s+', '', regex=True).str.replace(',', '.')

        columns_to_keep = ['date', 'hour', 'price', 'sales_volume', 'purchase_volume', 'declared_sales_volume', 'declared_purchase_volume']
        records = [DamPrice(**row) for row in df[columns_to_keep].to_dict('records')]
        DamPrice.objects.bulk_create(records, ignore_conflicts=True, batch_size=500)
