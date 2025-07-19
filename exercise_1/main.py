import pandas as pd
import matplotlib.pyplot as plt


class QualityReport:
    def __init__(self, input_file):
        '''
            Carrega os dados do arquivo Excel especificado.
        '''
    
        self.df = pd.read_excel(input_file)
        
    def filter_data(self):
        '''
            Filtra os dados para manter apenas os registros do site SCTIO05.
        '''
        
        self.df = self.df[self.df['Site'] == 'SCTIO05']
    
    def order_data(self):
        '''
            Ordena os dados por data.
        '''
        self.df = self.df.sort_values(by='Date')
        
    def add_status_data(self):
        '''
            Adiciona uma coluna de status com base na qualidade do sinal.
        '''
        
        
        self.df['Status'] = self.df['Quality'].apply(lambda x: 'OK' if x > 70 else 'NOK')
    
    def generate_report(self):
        '''
            Gera um relatório em Excel com as colunas Site, Cell, Date, Quality e Status.
        '''
        
        columns = ['Site', 'Cell', 'Date', 'Quality', 'Status']
        self.df[columns].to_excel('relatorio_qualidade.xlsx', index=False)
    
    def generate_graph(self):
        '''
            Gera um gráfico da média diária da qualidade do sinal por célula.
        '''
        #filtered_data = self.df[self.df["Cell"] == "N1SCTIO053"]
        #daily_avg = filtered_data.groupby("Date")["Quality"].mean()
        daily_avg = self.df.groupby(['Date', 'Cell'])['Quality'].mean().unstack()
        print(daily_avg)

        plt.figure(figsize=(12, 6))
        for cell in daily_avg.columns:
            print(daily_avg[cell])
            print(daily_avg.index)
            
            plt.plot(daily_avg.index, daily_avg[cell], marker='o', label=f'Cell {cell}')
        
        # plt.figure(figsize=(10, 5))
        # plt.plot(daily_avg.index, daily_avg.values, marker="o", linestyle="-", color="b", label="N1SCTIO053")

        plt.xlabel('Data')
        plt.ylabel('Qualidade do Sinal (%)')
        plt.title('Média Diária da Qualidade do Sinal por Célula')
        plt.legend()
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('grafico_qualidade_sinal.png')
    
    def executor(self):
        '''
            Executa o processo de geração do relatório e gráfico.
        '''
        
        self.filter_data()
        self.order_data()
        self.add_status_data()
        self.generate_report()
        self.generate_graph()

if __name__ == "__main__":
    report = QualityReport('exercise_1/Dados.xlsx')
    report.executor()
    