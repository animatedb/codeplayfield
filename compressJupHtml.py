import os
import sys

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
                    doModification = True
                    break
                if '<style' in line:
                    copy = False
                if copy:
                    outFile.write(line)
                if '<!-- End of mathjax configuration' in line:
                    copy = True
                    outFile.write(getStyle())
                    outFile.write('\n</head>\n')
    if doModification:
        print('copyfile')
    else:
        print('deletefile')

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
        '</style>',
        ]
    return '\n'.join(style)


#compressJupHtml('Images')
#compressJupHtml('Loops')
#compressJupHtml('Sound')
#compressJupHtml('Steps')
compressJupHtml('Storage')
#compressJupHtml('Values')
