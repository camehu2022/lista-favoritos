from ast import Return
from unittest import result
from fastapi import FastAPI
from mysqlx import Result
from database import mycursor, mydb


app = FastAPI()

@app.get("/")
async def exibir_prod():
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM `produtos` ")
    myresult = mycursor.fetchall()
    return myresult


@app.get("/inserir")
async def inserir_prod():
    sql = "INSERT INTO produtos (produto, quantidade) VALUES (%s, %s)"
    val = ("Caneta gel Cacto Branca",1)
    mycursor.execute(sql, val)
    mydb.commit()
    result=mycursor.rowcount, "record inserted."
    return{result}

@app.get("/editar/{item_id}")
async def editar_prod(item_id, qtd: int, valor_prd: float):
    mycursor = mydb.cursor()
    mycursor.execute("UPDATE `produtos` SET `quantidade`= %s,`valor_produto`=%s WHERE id_produto=%s", [qtd, valor_prd, item_id] )
    mydb.commit()
    return {mycursor.rowcount, "record(s) affected"}
   
   

@app.get("/deletar/{item_id}")
async def del_prod(item_id: int):
    mycursor = mydb.cursor()
    mycursor.execute("DELETE FROM produtos WHERE id_produto=%s", [item_id])     
    mydb.commit()
    result=mycursor.rowcount
    if result==1:
        return {"Item deletado com Sucesso!"}  
    elif result==0:
        return {"Item não existe no sistema!"}