import pytest

import csv
import os
import tempfile

from main import create_report


class TestCreateReport:
    def setup_class(self):
        self.data1 = [
        ['student_name', 'teacher_name',  'grade'],
        ['Иван Иванов',' Ковалева Анна','5'],
        ['Петр Петров', 'Ткаченко Наталья','4'],
        ['Иван Иванов','Сидоров Иван', '4']
    ]
        self.data2 = [
        ['student_name', 'grade'],
        ['Иван Иванов', '3'],
        ['Мария Истомина', '4'],
        ['Олеся Иванова', '3']
    ]

        self.value = 'student'


    def teardown_class(self):
        if os.path.exists('report.csv'):
            os.remove('report.csv')


    def create_temp_csv(self, data):
        temp_file = tempfile.NamedTemporaryFile(
            mode='w',
            suffix='.csv',
            delete=False,
            encoding='utf-8'
        )

        with temp_file:
            writer = csv.writer(temp_file)
            writer.writerows(data)

        return temp_file.name

    def test_report_creation_and_content(self):
        """Тест создания отчета и его содержимого"""
        from main import create_report

        students_csv = self.create_temp_csv(self.data1)
        create_report([students_csv], 'report.csv', self.value)


        assert os.path.exists('report.csv')
        print("✓ Файл отчета создан")
        try:
            with open('report.csv', 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                rows = list(reader)

                assert rows[0] == ['Student Name', 'Grade']

                data_dict = {row[0]: row[1] for row in rows[1:]}
                assert data_dict['Иван Иванов'] == '4.5'
                assert data_dict['Петр Петров'] == '4'
                assert len(data_dict) == 2

                print("✓ Содержимое отчета корректно")
        finally:
            if os.path.exists(students_csv):
                os.unlink(students_csv)

    def test_sorting(self):
        """Тест сортировки по убыванию оценок"""
        from main import create_report

        students_csv = self.create_temp_csv(self.data1)

        try:
            create_report([students_csv], 'report.csv', self.value)

            with open('report.csv', 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                rows = list(reader)

                grades = [float(row[1]) for row in rows[1:]]  # пропускаем заголовок
                assert grades == sorted(grades, reverse=True)
                print("✓ Сортировка по убыванию работает")

        finally:
            if os.path.exists(students_csv):
                os.unlink(students_csv)

    def test_multiple_files(self):
        """Тест обработки нескольких файлов"""
        from main import create_report

        file1 = self.create_temp_csv(self.data1)
        file2 = self.create_temp_csv(self.data2)

        try:
            create_report([file1, file2], 'report.csv', self.value)

            with open('report.csv', 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                rows = list(reader)
                data_dict = {row[0]: row[1] for row in rows[1:]}

                assert data_dict['Иван Иванов'] == '4'
                assert len(data_dict) == 4

                print("✓ Обработка нескольких файлов работает")

        finally:
            for file_path in [file1, file2]:
                if os.path.exists(file_path):
                    os.unlink(file_path)

    def test_other_value(self):
        file = self.create_temp_csv(self.data1)

        try:
            create_report([file], 'report.csv', 'teacher')
            with open('report.csv', 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                rows = list(reader)
                assert rows[0] == ['Teacher Name', 'Grade']
        finally:
            for file_path in [file]:
                if os.path.exists(file_path):
                    os.unlink(file_path)
