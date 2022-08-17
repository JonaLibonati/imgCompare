# imgCompare.py
This tool compares images and highlights the differences between them.

## Running the tool
Running the script by using the python3 and the [script-path]:
```
python3 <script-path>
```
For example, if you are located in the script folder:
```
python3 imgCompare.py
```

By the main menu, you will be able to choose between two compare mode.

## Mode 1 - Simple compare
By choosing the simple compare, the tool will ask for two inputs.  

The inputs should be images and they could be named with different names.  
  
When the inputs are defined, the simple HTTP server is started and the default browser is opened. The browser uses Canvas to compare images and highlight the differences between them. The tool has and range selector to set the compare sensivility.  
  
The server is automatically closed after the images are loaded.

## Mode 2 - Multiple compare
By choosing the multiple compare, the tool will ask for two inputs.  
  
The inputs should be directories and the images should be inside them.  
  
The tool creates image pairs by comparing the images name of each diretory. Therefore, the images to compare should have the same name. The directories name could be diferent each other.
  
When the inputs are defined, the simple HTTP server is started and the default browser is opened. The browser uses Canvas to compare images and highlight the differences between them. The tool has and range selector to set the compare sensivility.  
  
The server is automatically closed after the images are loaded.