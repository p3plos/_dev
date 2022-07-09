import eel

eel.init('web', allowed_extensions=['.js', '.html'])


@eel.expose
def my_python_function(a, b):
    print(a, b, a + b)

eel.start('hello.html', size=(550, 550), position=(150, 150))
