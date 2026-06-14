def create_tflite_interpreter(model_path):
    """Create a TFLite interpreter across TensorFlow/LiteRT package variants."""
    interpreter_imports = (
        ("ai_edge_litert.interpreter", "Interpreter"),
        ("tflite_runtime.interpreter", "Interpreter"),
    )

    for module_name, class_name in interpreter_imports:
        try:
            module = __import__(module_name, fromlist=[class_name])
            interpreter_class = getattr(module, class_name)
            print(f"Using {module_name}.{class_name}")
            return interpreter_class(model_path=model_path)
        except ImportError:
            pass

    import tensorflow as tf

    try:
        print("Using tensorflow.lite.Interpreter")
        return tf.lite.Interpreter(model_path=model_path)
    except TypeError as exc:
        if "CreateWrapperFromFile(): incompatible function arguments" not in str(exc):
            raise

        from tensorflow.lite.python import interpreter as interpreter_lib

        wrapper = interpreter_lib._interpreter_wrapper
        original_create_wrapper = wrapper.CreateWrapperFromFile

        def create_wrapper_from_file_compat(*args):
            try:
                return original_create_wrapper(*args)
            except TypeError:
                if len(args) >= 6:
                    try:
                        return original_create_wrapper(*args[:6])
                    except TypeError:
                        return original_create_wrapper(
                            args[0], args[1], args[2], args[4], args[5]
                        )
                raise

        wrapper.CreateWrapperFromFile = create_wrapper_from_file_compat
        print("Using tensorflow.lite.Interpreter with wrapper compatibility shim")
        return tf.lite.Interpreter(model_path=model_path)
