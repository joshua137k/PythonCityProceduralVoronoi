@tool

class_name Draw3D
extends MeshInstance3D


@export var default_color: Color = Color.WHITE
@export var _default_material: StandardMaterial3D =  StandardMaterial3D.new()



func _ready() -> void:
	mesh = ImmediateMesh.new()
	_setup_materials()


func _setup_materials() -> void:
	_default_material.vertex_color_use_as_albedo = true
	_default_material.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED

func clear() -> void:
	mesh.clear_surfaces()


func _draw_primitive(
		primitive_type: int,
		vertices: Array,
		color: Color = default_color) -> void:

	if vertices[0] is Vector3:
		# we're dealing with a list of vertices
		mesh.surface_begin(primitive_type, null)
		for v in vertices:
			mesh.surface_set_color(color)
			mesh.surface_add_vertex(v)
		mesh.surface_end()

	var material =  _default_material

	var last_surface_idx = mesh.get_surface_count() - 1
	mesh.surface_set_material(last_surface_idx, material)



func draw_line(vertices: Array, w:int = 1, color: Color = default_color) -> void:
	#_draw_primitive(Mesh.PRIMITIVE_LINE_STRIP, vertices, color)
	for i in vertices:
		draw_rectangle(i[0],i[1],w,default_color)


func draw_rectangle(start: Vector3, end: Vector3, width: float, color: Color = default_color) -> void:
	var direction = end - start
	direction = direction.normalized()

	# Cálculo dos vetores perpendiculares para definir a largura do retângulo
	var up = Vector3(0, 1, 0) # Assumindo que 'up' é o eixo Y global
	var right = direction.cross(up).normalized() * width

	# Definindo os vértices do retângulo (paralelepípedo)
	var vertices = [
		start - right / 2.0, # Vértice 1
		end - right / 2.0, # Vértice 2
		end + right / 2.0, # Vértice 3
		start - right / 2.0, # Vértice 1 novamente, para fechar o primeiro triângulo
		end + right / 2.0, # Vértice 3 novamente, para o segundo triângulo
		start + right / 2.0  # Vértice 4
	]

	# Desenha os dois triângulos para formar um retângulo
	_draw_primitive(Mesh.PRIMITIVE_TRIANGLES, vertices, color)
