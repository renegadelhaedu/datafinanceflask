from dotenv import load_dotenv
import os
import psycopg2

load_dotenv()

db_config = {
    'host': os.getenv('DB_HOST'),
    'database': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'port': int(os.getenv('DB_PORT')),
}


def conectardb():
    return psycopg2.connect(**db_config)


def login(user, senha):
    con = conectardb()
    cur = con.cursor()
    sq = f"SELECT nome, profissao, email from usuario where email='{user}' and senha='{senha}'  "
    cur.execute(sq)
    saida = cur.fetchall()

    cur.close()
    con.close()

    return saida


def inserir_user(nome, email, profissao, senha):
    conn = conectardb()
    cur = conn.cursor()
    try:
        sql = f"INSERT INTO usuario (email, senha, nome, profissao) VALUES ('{email}','{senha}','{nome}', '{profissao}' )"
        cur.execute(sql)

        sql2 = f"INSERT INTO carteira (email_usuario) VALUES('{email}')"
        cur.execute(sql2)
        conn.commit()

    except psycopg2.Error as e:
        conn.rollback()
        exito = False
        print(e)
    else:
        exito = True

    cur.close()
    conn.close()
    return exito


def inserir_acao(email, codigo, qtde, preco_medio):
    conn = conectardb()
    cur = conn.cursor()

    try:
        sql = (f"INSERT INTO acao (email_usuario, simbolo, quantidade, preco_compra)"
               f" VALUES ('{email}','{codigo}','{qtde}', '{preco_medio}')")
        cur.execute(sql)
        conn.commit()
    except psycopg2.Error as e:
        conn.rollback()
        exito = False
        print(e)
    else:
        exito = True

    cur.close()
    conn.close()
    return exito


def excluir_acao(email, codigo):
    conn = conectardb()
    cur = conn.cursor()

    try:
        sql = f"DELETE FROM acao WHERE email_usuario = '{email}' and simbolo = '{codigo}';"

        cur.execute(sql)
        conn.commit()
    except psycopg2.Error as e:
        conn.rollback()
        exito = False
        print(e)
    else:
        exito = True

    cur.close()
    conn.close()
    return exito


def atualizar_acoes(email, acoes_modificadas):
    conn = conectardb()
    cur = conn.cursor()

    try:
        query = """
                    UPDATE acao
                    SET quantidade = CASE simbolo
                """

        for simbolo, nova_quantidade in acoes_modificadas.items():
            query += f" WHEN '{simbolo}' THEN {nova_quantidade}"

        query += " END WHERE email_usuario = %s AND simbolo IN %s;"

        simbolos = tuple(acoes_modificadas.keys())

        cur.execute(query, (email, simbolos))
        conn.commit()

    except psycopg2.Error as e:
        conn.rollback()
        exito = False
        print(e)
    else:
        exito = True

    cur.close()
    conn.close()
    return exito


def get_carteira(email):
    con = conectardb()
    cur = con.cursor()
    sql = (f"SELECT a.simbolo, a.quantidade FROM usuario u JOIN carteira c ON u.email = c.email_usuario "
           f"JOIN acao a ON c.email_usuario = a.email_usuario WHERE u.email = '{email}';")

    cur.execute(sql)
    saida = cur.fetchall()

    cur.close()
    con.close()

    acoes_dict = {simbolo: quantidade for simbolo, quantidade in saida}

    return acoes_dict


def criar_tabelas():
    con = conectardb()
    cur = con.cursor()

    create_table_query = """
    CREATE TABLE IF NOT EXISTS public.usuario(
        email VARCHAR(255) NOT NULL,
        senha VARCHAR(255) NOT NULL,
        nome VARCHAR(255)  NOT NULL,
        profissao text NOT NULL,
        CONSTRAINT usuarios_pkey PRIMARY KEY (email)
    );

    CREATE TABLE carteira (
        email_usuario VARCHAR(255) PRIMARY KEY REFERENCES usuario(email) ON DELETE CASCADE,
        data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE acao (
        id SERIAL PRIMARY KEY,
        email_usuario VARCHAR(255) REFERENCES carteira(email_usuario) ON DELETE CASCADE,
        simbolo VARCHAR(10) NOT NULL,
        quantidade INTEGER NOT NULL,
        preco_compra DECIMAL(10, 2) NOT NULL,
        data_compra TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """

    cur.execute(create_table_query)
    con.commit()
    con.close()


def getEmpresasListadasAntigas():
    return ['ABCB4', 'ABEV3', 'AGRO3', 'ALUP11', 'ARZZ3', 'B3SA3', 'BBAS3', 'BBDC4', 'BBSE3', 'BEEF3', 'BPAN4',
            'BRAP4', 'BRSR6', 'CAMB3', 'CCRO3', 'CIEL3', 'CMIG4', 'CPFE3', 'CPLE6', 'CSMG3', 'CSUD3', 'CYRE3',
            'DEXP3', 'EGIE3', 'ENGI11', 'EVEN3', 'FESA4', 'FLRY3', 'FRAS3', 'GGBR4', 'GOAU4', 'GRND3', 'HYPE3',
            'ITSA4', 'ITUB4', 'JHSF3', 'KEPL3', 'LEVE3', 'LREN3', 'MILS3', 'MULT3', 'ODPV3', 'PETR4', 'PINE4',
            'PNVL3', 'POMO4', 'POSI3', 'PSSA3', 'RANI3', 'RAPT4', 'RENT3', 'ROMI3', 'SANB11', 'SBSP3', 'SLCE3',
            'SMTO3', 'STBP3', 'TAEE11', 'TASA4', 'TGMA3', 'TIMS3', 'TOTS3', 'TRIS3', 'TRPL4', 'TUPY3', 'UGPA3',
            'UNIP6', 'VALE3', 'VIVT3', 'VLID3', 'VULC3', 'WEGE3']


def getMinhasEmpresasListadas():
    return ['BBSE3', 'PSSA3', 'BBAS3', 'BRSR6', 'ITSA4', 'EGIE3', 'ALUP11', 'TAEE11', 'KLBN4', 'VALE3', 'TUPY3',
            'FESA4']


def getCarteirastatic():
    return {'SIMH3': 30, 'TAEE11': 6, 'ALUP11': 13, 'EGIE3': 8, 'KLBN11': 11, 'ITSA4': 30,
            'PSSA3': 7, 'BBSE3': 9, 'VBBR3': 13, 'BRSR6': 22, 'TUPY3': 6, 'BBAS3': 6, 'VALE3': 3}


def getAcoesListadas():
    return ['ABCB4', 'ABEV3', 'AERI3', 'AESB3', 'AGRO3', 'ALLD3', 'ALOS3', 'ALPA4', 'ALPK3', 'ALUP11', 'AMBP3', 'AMER3',
            'ANIM3', 'ARML3', 'ASAI3', 'ATOM3', 'AURA33', 'AURE3', 'AZEV3', 'AZEV4', 'AZUL4', 'AZZA3', 'B3SA3', 'BBAS3',
            'BBDC3', 'BBDC4', 'BBSE3', 'BEEF3', 'BHIA3', 'BIOM3', 'BLAU3', 'BMEB4', 'BMGB4', 'BMOB3', 'BPAC11', 'BPAN4',
            'BRAP3', 'BRAP4', 'BRAV3', 'BRBI11', 'BRFS3', 'BRIT3', 'BRKM5', 'BRSR6', 'CAMB3', 'CAML3', 'CASH3', 'CBAV3',
            'CCRO3', 'CEAB3', 'CLSA3', 'CMIG3', 'CMIG4', 'CMIN3', 'COCE5', 'COGN3', 'CPFE3', 'CPLE3', 'CPLE6', 'CRFB3',
            'CRIV4', 'CSAN3', 'CSED3', 'CSMG3', 'CSNA3', 'CSUD3', 'CURY3', 'CVCB3', 'CXSE3', 'CYRE3', 'DASA3', 'DESK3',
            'DEXP3', 'DIRR3', 'DMVF3', 'DXCO3', 'ECOR3', 'EGIE3', 'ELET3', 'ELET6', 'ELMD3', 'EMBR3', 'ENEV3', 'ENGI11',
            'ENJU3', 'EQTL3', 'ETER3', 'EVEN3', 'EZTC3', 'FESA4', 'FIQE3', 'FLRY3', 'FRAS3', 'FRIO3', 'GFSA3', 'GGBR3',
            'GGBR4', 'GGPS3', 'GMAT3', 'GOAU3', 'GOAU4', 'GOLL4', 'GRND3', 'GUAR3', 'HAPV3', 'HBOR3', 'HBRE3', 'HBSA3',
            'HYPE3', 'IFCM3', 'IGTI11', 'INTB3', 'IRBR3', 'ISAE4', 'ITSA3', 'ITSA4', 'ITUB3', 'ITUB4', 'JALL3', 'JBSS3',
            'JHSF3', 'JSLG3', 'KEPL3', 'KLBN11', 'KLBN3', 'KLBN4', 'LAVV3', 'LEVE3', 'LIGT3', 'LJQQ3', 'LOGG3', 'LOGN3',
            'LREN3', 'LWSA3', 'MATD3', 'MBLY3', 'MDIA3', 'MDNE3', 'MEAL3', 'MELK3', 'MGLU3', 'MILS3', 'MLAS3', 'MOVI3',
            'MRFG3', 'MRVE3', 'MTRE3', 'MULT3', 'MYPK3', 'NEOE3', 'NGRD3', 'NTCO3', 'ODPV3', 'OIBR3', 'ONCO3', 'OPCT3',
            'ORVR3', 'PCAR3', 'PDGR3', 'PETR3', 'PETR4', 'PETZ3', 'PFRM3', 'PGMN3', 'PINE4', 'PLPL3', 'PNVL3', 'POMO3',
            'POMO4', 'PORT3', 'POSI3', 'PRIO3', 'PRNR3', 'PSSA3', 'PTBL3', 'QUAL3', 'RADL3', 'RAIL3', 'RAIZ4', 'RANI3',
            'RAPT4', 'RCSL3', 'RCSL4', 'RDOR3', 'RECV3', 'RENT3', 'ROMI3', 'SANB11', 'SANB3', 'SANB4', 'SAPR11',
            'SAPR3', 'SAPR4', 'SBFG3', 'SBSP3', 'SEER3', 'SEQL3', 'SHUL4', 'SIMH3', 'SLCE3', 'SMFT3', 'SMTO3', 'SOJA3',
            'SRNA3', 'STBP3', 'SUZB3', 'TAEE11', 'TAEE3', 'TAEE4', 'TASA4', 'TECN3', 'TEND3', 'TFCO4', 'TGMA3', 'TIMS3',
            'TOTS3', 'TPIS3', 'TRAD3', 'TRIS3', 'TTEN3', 'TUPY3', 'UGPA3', 'UNIP6', 'USIM3', 'USIM5', 'VALE3', 'VAMO3',
            'VBBR3', 'VITT3', 'VIVA3', 'VIVT3', 'VLID3', 'VTRU3', 'VULC3', 'VVEO3', 'WEGE3', 'YDUQ3', 'ZAMP3']

