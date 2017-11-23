import tensorflow as tf
import keras as k

# Init() returns a loaded model and a graph
def init(): 
	json_file = open('model/model.json','r')
	loaded_model_json = json_file.read()
	json_file.close()
	loaded_model = k.models.model_from_json(loaded_model_json)
	#load weights into new model
	loaded_model.load_weights("model/model.h5")
	print("Loaded Model from disk")

	# compile the loaded model
	loaded_model.compile(loss='categorical_crossentropy',optimizer='adam',metrics=['accuracy'])
    # use tensorflow to get graph
	graph = tf.get_default_graph()

    # Return loaded model and graph
	return loaded_model,graph