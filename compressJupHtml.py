import os
import sys
import shutil

# To save a Jupyter html, 


# Strip out all style.
def compressJupHtml(filename:str) -> None:
    docDir = 'docs/'
    inFilename = docDir + filename + '.html'
    outFilename = docDir + filename + 'Compress.html'
    copy = True
    doModification = True
    with open(inFilename, 'r') as inFile:
        with open(outFilename, 'w') as outFile:
            for line in inFile:
                if '<!-- Compressed Jupyter File -->' in line:
                    doModification = False
                    break
                if '<style' in line:
                    copy = False
                if copy:
                    line = line.replace('&#182;', '')
                    outFile.write(line)
                if '<!-- End of mathjax configuration' in line:
                    copy = True
                    outFile.write(getStyle())
                    outFile.write('\n</head>\n')
    if doModification:
        print('Modified file', filename)
        shutil.copyfile(outFilename, inFilename)
    os.remove(outFilename)

def getStyle():
    style = [
        '<!-- Compressed Jupyter File -->'
        '<style type="text/css">',
        '.jp-InputArea-editor {'
#          /* This is the non-active, default styling */
#          border: var(--jp-border-width) solid var(--jp-cell-editor-border-color);
        'border-radius: 0px;',
        'background: #f0f0f0;',
        '}',

        'body{',
#        'line-height:1.28581;',
        'line-height:1.6;',
#        'font-weight:400;',
        'font-size:14;',
        'font-weight:400;',
        'font-family:-apple-system, "BlinkMacSystemFont", "Segoe UI", "Roboto",',
        '"Oxygen", "Ubuntu", "Cantarell", "Open Sans", "Helvetica Neue", "Icons16", sans-serif;',
        '}',
        '</style>',
        ]
    return '\n'.join(style)


# Execute means that the code should be executed in Jupyter before exporting as html.
compressJupHtml('Flow')     # Execute
compressJupHtml('Images')       # No execute
compressJupHtml('Loops')    # Execute
compressJupHtml('Sound')        # No execute - No code yet
compressJupHtml('Steps')        # No execute - Has code, but no results
compressJupHtml('Storage')  # Execute
compressJupHtml('Values')   # Execute
