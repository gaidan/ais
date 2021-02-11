from sys import argv

tokenlist = [['start', 'nes'], ['end', 'nes'], ['integer', 'asn'], ['=', 'asn'], ['^', 'op'], ['sqrt', 'op'], ['*', 'op'], ['/', 'op'], ['+', 'op'], ['-', 'op'], ['print', 'fun']]

code = open(argv[1], 'r').read()

def isnumeric(string):
    isnumeric = True
    dotcount = 0
    numberinstring = False
    if string == '':
        isnumeric = False
    for i in range(0, len(string)):
        if string[i] == '-' and i!=0:
            isnumeric = False
        if string[i] == '.':
            dotcount += 1
        try:
            if string[i] != '-' and string[i] != '.':
                int(string[i])
                numberinstring = True
        except:
            isnumeric = False
    if not numberinstring:
        isnumeric = False
    if dotcount > 2:
        isnumeric = False
    return isnumeric

def parse(code):
    global tokenlist
    tokens = []
    phrases = []
    decs = []
    for phrase in code.split(';'):
        phrases.append(phrase.strip())
    for phrase in phrases:
        tokensz = []
        tokenss = phrase.split(' ')
        for token in tokenss:
            tok = []
            # intokenlist = False
            if isnumeric(token):
                tok.append(token)
                tok.append('val')
            else:
                intokenlist = False
                for t in tokenlist:
                    if t[0]==token:
                        intokenlist = True
                        tok.append(token)
                        tok.append(t[1])
                indecs = False
                for t in range(0, len(decs)):
                    if decs[t]==token:
                        indecs = True
                        tok.append(token)
                        tok.append('var')
                if not indecs and not intokenlist:
                    lasttoken = tokenss[tokenss.index(token)-1]
                    if lasttoken == 'integer' or lasttoken == 'float':
                        tok.append(token)
                        tok.append('var')
                        decs.append(token)
            tokensz.append(tok)
        tokens.append(tokensz)
    return tokens

def createCode(tokens):
    code = ''
    del tokens[len(tokens)-1]
    codez = []
    for phrase in tokens:
        codeorder = []
        order = ['asn', 'fun', 'op', 'var', 'val']
        codeord = []
        for token in phrase:
            if token:
                if token[1] != 'nes':
                    codeorder.append(token)
        flagchange = False
        for i in range(0, len(codeorder)):
            # if codeorder[i][1] == 'var':
            #     print(codeorder[i][0], codeorder[i-1][1], phrase)
            if codeorder:
                # check if code is a variable and doesn't have an assignement(INTEGER) or function(PRINT) or operation(+) before it;
                if codeorder[i][1] == 'var' and codeorder[i-1][1] != 'asn' and codeorder[i-1][1] != 'fun' and codeorder[i-1][1] != 'op':
                    # if it has an assignement in front of it (x = 5)
                    if codeorder[i+1][1] == 'asn':
                        codeord.append(1)
                        # just a flag so that the compiler knows
                        flagchange = True
                    #else:
                    #    codeord.append(order.index(codeorder[i][1])+1)
                    elif flagchange == False:
                        codeord.append(order.index(codeorder[i][1]))
                else:
                    codeord.append(order.index(codeorder[i][1])+1)
            else:
                pass
        ogcodeord = codeorder
        codeorder = [x for _,x in sorted(zip(codeord, codeorder))]
        for c in range(0, len(codeorder)):
            try:
                if codeorder[c][1] == 'val' or codeorder[c][1] == 'var' and codeorder[c-1][1] == 'op':
                    if codeorder[c+1][1] == 'val' or codeorder[c+1][1] == 'var':
                        ncodeorder = codeorder
                        # print(codeorder[c], codeorder[c+1])
                        a = codeorder[c]
                        b = codeorder[c+1]
                        # print(ogcodeord.index(a), ogcodeord.index(b), a, b)
                        if ogcodeord.index(a) < ogcodeord.index(b):
                            ncodeorder[c] = a
                            ncodeorder[c+1] = b
                        else:
                            ncodeorder[c] = b
                            ncodeorder[c+1] = a
                        codeorder = ncodeorder
            except:
                pass
        codez.append(codeorder)
    scode = ['import math \n']
    for codes in codez:
        if codes:
            for i in range(0, len(codes)-1):
                if codes[i][1] == 'asn' and codes[i][0] != '=':
                    scode.append('{} = 0 '.format(codes[i+1][0]))
                    break
                if codes[i][1] == 'asn' and codes[i][0] == '=':
                    # scode.append('{} = '.format(codes[i+1][0]))
                    hasop = False
                    for x in range(i, len(codes)-1):
                        if codes[x][1] == 'op':
                            hasop = True
                    if hasop:
                        scode.append('{} = '.format(codes[i+1][0]))
                    else:
                        scode.append('{} = {}'.format(codes[i+1][0], codes[i+2][0]))
                if codes[i][1] == 'op' and codes[i][0] == '-':
                    scode.append('{} - {}'.format(codes[i+1][0], codes[i+2][0]))
                if codes[i][1] == 'op' and codes[i][0] == '+':
                    scode.append('{} + {}'.format(codes[i+1][0], codes[i+2][0]))
                if codes[i][1] == 'op' and codes[i][0] == '/':
                    scode.append('{} / {}'.format(codes[i+1][0], codes[i+2][0]))
                if codes[i][1] == 'op' and codes[i][0] == '*':
                    scode.append('{} * {}'.format(codes[i+1][0], codes[i+2][0]))
                if codes[i][1] == 'fun' and codes[i][0] == 'print':
                    scode.append('print({})'.format(codes[i+1][0]))
                if codes[i][1] == 'op' and codes[i][0] == '^':
                    scode.append('{} ** {}'.format(codes[i+1][0], codes[i+2][0]))
                if codes[i][1] == 'op' and codes[i][0] == 'sqrt':
                    scode.append('math.sqrt({})'.format(codes[i+1][0]))
            scode = ''.join(scode)
            code = '{}\n{}'.format(code, scode)
            scode = []
    return code

phrased_tokens = parse(code)
wf = open('a.py', 'w')
wf.write(createCode(phrased_tokens))
wf.close()
