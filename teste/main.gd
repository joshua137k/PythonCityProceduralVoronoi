@tool
extends Node2D


# Called when the node enters the scene tree for the first time.
func _ready():
	var f = FileAccess.open("ro.txt",FileAccess.READ)
	var text = f.get_as_text()

	text = text.split("%")
	
	for i in text:
		i=i.split("/")
		var k = PackedVector2Array()
		var x = str_to_var(i[0].replace("[",""))
		var y=str_to_var(i[1].replace("]",""))
		if x and y:
			k.append(x)
			k.append(y)
			var t = Line2D.new()
			t.width=2
			t.points=k
			add_child(t)


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	pass
