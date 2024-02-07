@tool
extends Node3D

# Chamado quando o nó entra na árvore de cena pela primeira vez.
func _ready():
	# Abrindo o arquivo de texto para leitura.
	var file = FileAccess.open("ro.txt", FileAccess.READ)
	var text = file.get_as_text()
	
	# Preparando e executando uma expressão baseada no texto do arquivo.
	var expression = Expression.new()
	expression.parse(text)
	text = expression.execute([], self)
	
	# Iterando sobre as linhas do texto processado.
	for line_key in text:
		var line_list = []
		for item in text[line_key]:
			var start_point = str_to_var(item[0])
			var end_point = str_to_var(item[1])
			
			# Verificando se ambos os pontos são válidos antes de adicioná-los à lista.
			if start_point and end_point:
				var start_vector = Vector3(start_point[0], 0, start_point[1])
				var end_vector = Vector3(end_point[0], 0, end_point[1])
				line_list.append([start_vector, end_vector])
		
		# Duplicando o nó de Primitivas e desenhando as linhas.
		var primitives_node:Draw3D = $Primitives.duplicate()
		add_child(primitives_node)
		primitives_node.draw_line(line_list,5,Color.WHITE)


