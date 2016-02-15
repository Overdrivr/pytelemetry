import pypandoc
try:
    pypandoc.convert('README.md', 'rst', outputfile="README.rst")
except(IOError, ImportError) as e:
    print("Error during conversion")
    print(e)
