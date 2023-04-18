import os
import re
import pdfplumber 

class PDF:
    # default args
    default_pattern = r'(^[A-Z][A-Za-z-\s()ôêóáíé]+)\s([0-9]+\s+[0-9]+\s+[0-9]+\s+[0-9]+\s+[0-9]+\s+[0-9]+\s+)'
    default_columns = ['Instituto/Curso', 'Canc.por Reopção', 'Decurso de Prazo Máximo P/ Conclusão de Curso', 'Desistência', 'Prescrito',
                    'Transferência para outra IES','Transferência Interna (administrativa)', 'Total geral']
    
    def __init__(self, output_path='data', pattern=default_pattern, pdf_file=None):
       self.output_path = os.path.abspath(output_path)
       self.pattern =  re.compile(pattern, flags=re.MULTILINE)
       self.pdf_file = pdf_file

    
    @property
    def pdf_file(self):
        return self._pdf_file

    @pdf_file.setter
    def pdf_file(self, pdf_file):
        self._pdf_file = pdf_file

    @property
    def output_path(self):
        return self._output_path

    @output_path.setter
    def output_path(self, output_path):
        self._output_path = output_path


    def folder(self, **kwargs):
        instance_pdf = re.compile(r'.*.pdf')
        
        if 'path' in kwargs:
            folder_check = os.listdir(kwargs['path'])
        else:
            folder_check = os.listdir()
        
        list_pdf = instance_pdf.findall("\n".join(folder_check))
        return list_pdf 

    def raw_read(self):
        try:
            raw_string = ""
            with pdfplumber.open(self.pdf_file) as line:
                for page in range(len(line.pages)):
                    raw_string += line.pages[page].extract_text() 
            return raw_string
        except AttributeError:
            return 'PDF file not provided'     
    
    def read(self):
            raw_string = self.raw_read()
            tuple_matches = self.pattern.findall(raw_string) 
            n = len(tuple_matches)
            list_matches = []
            for i in range(n):
                list_matches.append(list(tuple_matches[i]))
            string_csv = []
            for element in range(n):
                data = list_matches[element][1].split(' ')
                i = list_matches[element][0]+','.join(data)+'\n'

                string_csv.append(i)
            return string_csv
    
    def save_pdf(self, columns=default_columns):
        string_csv = self.read()
        string_csv.insert(0,', '.join(columns)+'\n')
        csv = ''.join(string_csv)

        ptt = re.compile(r'\w*.pdf')
        name = input('Enter a name for the file:\n')

        filename = self.output_path + "/" + name + '.csv'

        with open(filename, 'w') as file:
            file.write(csv)

if __name__ == '__main__':
    pass
