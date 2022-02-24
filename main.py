from ast import For, Return
from contextlib import redirect_stderr
from itertools import count
from unittest import result
from fastapi import FastAPI, Request
import uvicorn
from database import mycursor, mydb
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles



app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def exibir_prod(request: Request):
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM `produtos` ")
    myresult = mycursor.fetchall()
    return templates.TemplateResponse("index.html", {"request": request, 'resultado':myresult})

   
@app.get("/listadesejos", response_class=HTMLResponse)
async def exibir_desejos(request: Request):
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM `listdesejos` ")
    myresult = mycursor.fetchall()          
    return templates.TemplateResponse("listadesejos.html", {"request": request, 'lista':myresult})


@app.get("/pag_produto/{id_item_prod}", response_class=HTMLResponse)
async def exibir_desejos(request: Request, id_item_prod: int):
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM `produtos` WHERE id_produto =%s", [id_item_prod])
    myresult = mycursor.fetchall()          
    return templates.TemplateResponse("pag_produto.html", {"request": request, 'produto': myresult })



@app.get("/inserir/{item_prod}", response_class=HTMLResponse)
async def inserir_desejo(request: Request, item_prod: int):
    sql = "INSERT INTO `listdesejos`(`id_lista`, `id_produto`, `id_cliente`) VALUES (%s,%s,%s)"
    val = ('null',item_prod,'id_cliente')
    mycursor.execute(sql, val)
    mydb.commit()
    myresult = mycursor.fetchall()  
    return templates.TemplateResponse('listadesejos.html', {'request': request, 'lts':myresult })
   
       
    
@app.get("/", response_class=HTMLResponse)
async def cont_item(request: Request):
    mycursor = mydb.cursor()
    mycursor.execute("SELECT COUNT(*) FROM listdesejos ")
    contagem=mycursor.fetchall()
    return templates.TemplateResponse('index.html', {'request': request, 'contagem': contagem })
    

@app.get("/deletar/{item_id}", response_class=HTMLResponse)
async def del_prod(request: Request, item_id: int):
    mycursor = mydb.cursor()
    mycursor.execute("DELETE FROM `listdesejos` WHERE id_lista=%s", [item_id])     
    mydb.commit()
    result=mycursor.rowcount
    return templates.TemplateResponse('/listadesejos.html/', {'request': request})
  
    

       
                

   