import pyodbc 
import time
import datetime
import sys
lista = []
lista_restaurada = []
database = str(input('Nome do banco: '))
d = int(input('Dia: '))
m = int(input('Mês: '))
y = int(input('Ano: '))


print('conectando ao banco...')
try:
    dados_conexao = (
    "Driver={SQL Server};"
    "Server=.\SQLEXPRESS;"
    f"Database={database};"
)

    conexao = pyodbc.connect(dados_conexao)
    cursor = conexao.cursor() 

       
except Exception as erro:
    print(erro)
    time.sleep(5)


else:
    print('Coletando dados...')
    try:
        cursor.execute("""SELECT
P.idTblPessoa as ID
FROM TblPessoasUnidades as G
INNER JOIN TblPessoa as P on G.idTblPessoa = P.idTblPessoa
WHERE P.intLixeira = 0 and P.strFotoPessoa like 'data%'
ORDER BY P.idTblPessoa""")
        lista = cursor.fetchall()

    except Exception as erro:
        print(erro)
        time.sleep(5)
        sys.exit()

    else:
        for x in lista:
            x = str(x)
            x = x.replace('(','').replace(')','').replace(',','')
            x = int(x)
            lista_restaurada.append(x)
morador60 = []
for x in lista_restaurada:
    eventos = []
    new_list = []

    try:
        cursor.execute(f"""select datDataEvento from TblLOGAcesso where idTblPessoa = {x}
order by datDataEvento""")
        eventos = cursor.fetchall()
        
    except Exception as erro:
        print(erro)
        time.sleep(5)
        sys.exit()
    else:
        try:
            if len(eventos) == 0:
                print(f'Id {x} sem eventos no logacesso!')
                print('')
                morador60.append(x)
            else:
                eventos.reverse()
                new_list.append(eventos[0])
                teste = new_list[0][0]
                teste = str(teste)
                teste = teste[0:10]
                ano = teste[0:4]
                mes = teste[5:7]
                dia = teste[8:10]
                dia = int(dia)
                mes = int(mes)
                ano = int(ano)
                print(f'Id = {x}')
                print(f'Último evento: {teste}')
                data1 = datetime.date(day=dia, month=mes, year=ano)
                data2 = datetime.date(day=d, month=m, year=y)
                data2-data1
                datetime.timedelta(123)
                diferenca = data2-data1
                print(f'Totais de dias sem acesso: {diferenca.days}')
                print('')
                if diferenca.days > 60:
                    morador60.append(x)

        except Exception as erro:
            print(erro)
            time.sleep(2)
            pass    
        

pos = 0
pos1 = 0
for x in morador60:
    try:
        arquivo = open('relatorio.txt','a')
        nome = []
        id_unidade = []
        unidade = []
        cursor.execute(f'select strNome from tblPessoa where idTblPessoa = {x}')        
        nome = cursor.fetchall()
        nome = str(nome)
        nome = nome.replace('(','').replace(')','').replace(',','').replace('[','').replace(']','').replace("'",'')

        cursor.execute(f"""select idtblunidade from TblPessoasUnidades
where intLixeira = 0 and idTblPessoa = {x}""")
        id_unidade = cursor.fetchall()
        id_unidade = str(id_unidade)
        id_unidade = id_unidade.replace('(','').replace(')','').replace(',','').replace('[','').replace(']','').replace("'",'')

        cursor.execute(f"""select strdescricao from TblUnidade
where intLixeira = 0 and idTblUnidade = {id_unidade}""")
        unidade = cursor.fetchall()
        unidade = str(unidade)
        unidade = unidade.replace('(','').replace(')','').replace(',','').replace('[','').replace(']','').replace("'",'')

        arquivo.write(nome+' - '+ unidade + '\n')
    except Exception as erro:
        pos += 1
        print('nome não registrado!')
        pass  

    else:
        print('nome registrado!')
        pos1 += 1  
        arquivo.close()


print(f'Total de nomes registrados: {pos1}')
print(f'Falhas: {pos}')
input('SAIR?')