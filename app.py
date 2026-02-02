from flask import Flask, request, jsonify # Flask para o app, request para ler o que o User envia e jsonify para transformar dicionarios de python em JSON
from models.task import Task # Estrutura de cada task criada na pasta model, para organização

app = Flask(__name__) # Cria a instância do servidor, o __name__ ajuda o flask a localizar nomes

# CRUD
# Create, Read, Update and Delete


tasks = [] # Lista para guardar os objetos ja que não estou usando um banco de dados
task_id_control = 1 # Contador manual para começar o ID de cada tarefa

# Rotas
@app.route("/tasks", methods=["POST"]) # Rota de criação utilizando o método POST, que envia dados para o servidor
def create_task(): 
    global task_id_control # "Avisa" o python que estou utilizando dados de fora da função
    data = request.get_json() # Transforma o JSON no postman em um dicionário em python chamada data
    new_task = Task(id=task_id_control, title=data["title"], description=data.get("description", ""))
    task_id_control += 1 
    tasks.append(new_task) # adiciona a nova tarefa no final da lista
    print(tasks)
    return jsonify({"message":"Nova Tarefa enviada com sucesso!"})

@app.route("/tasks", methods=["GET"]) # Rota para ver as tarefas existentes utilizando o método GET
def get_tasks():
    task_list = [task.to_dict() for task in tasks] # percorre cada objeto na lista tasks e chama o to_dict() que transforma o objeto em dicionário
    output = {
                "tasks": task_list,
                "total_tasks": len(tasks)
    }
    return jsonify(output)

@app.route("/tasks/<int:id>", methods=["GET"]) # Rota para ver uma tarefa específica por ID
def get_task(id):
    task = None
    for t in tasks: # pega a primeira tarefa na lista, chama ela de t
        if t.id == id: # compara o id da tarefa t ao id na url
            task = t
           
    if task == None:
        return jsonify({"message": "Não foi possível encontrar a tarefa"}), 404 # caso o usuario coloque uma tarefa invalida
    
    return jsonify(t.to_dict()) # se bater ele retorna a tarefa para o usuario

@app.route("/tasks/<int:id>", methods=["PUT"]) # Rota de atualização de uma tarefa 
def update_task(id): 
    task = None # define task como vazio
    for t in tasks: # mesma coisa do anterior, pega a tarefa na lista e atribui a t
        if t.id == id: # se o id bater com a URL 
            task = t # bota a tarefa em t temporariamente

    if task == None: # caso o id não bata, task continuara como None 
        return jsonify({"message": "Não foi possível encontrar a tarefa"}), 404

    data = request.get_json()
    task.title = data["title"]
    task.description = data["description"]
    task.completed = data["completed"]
    print(task)
    return jsonify({"message" : "Tarefa atualizada com sucesso"})

@app.route("/tasks/<int:id>", methods=["DELETE"]) # Rota para deletar uma tarefa
def delete_task(id):
    task = None 
    for t in tasks: 
        if t.id == id:
            task = t
                   
    if task == None:
        return jsonify({"Message" : "Não foi possível encontrar a tarefa"}), 404

    tasks.remove(task)
    return jsonify({"Message" : "Tarefa deletada com sucesso"})

    
if __name__ == "__main__": # Liga o servidor. O modo debug=True reinicia o servidor automaticamente toda vez que salvar o arquivo e mostra os erros detalhados
    app.run(debug=True)