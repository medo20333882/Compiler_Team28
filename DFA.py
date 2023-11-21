import graphviz

dfa = graphviz.Digraph(
    'dfa', graph_attr={'rankdir': 'LR'})

dfa.attr('node', shape='doublecircle')
dfa.attr('node', fixedsize='true')
dfa.attr('node', width='1')
dfa.attr('edge', shape='normal')


dfa.node('start_reserved_words', shape='point', width='0')
dfa.node('s0', shape='circle', width='1')
dfa.node('s150', 's150: \nidentifier')
dfa.edge('start_reserved_words', 's0', label='start')


# Program
dfa.node('s1', 's1: \nidentifier')
dfa.node('s2', 's2: \nidentifier')
dfa.node('s3', 's3: \nidentifier')
dfa.node('s4', 's4: \nidentifier')
dfa.node('s5', 's5: \nidentifier')
dfa.node('s6', 's6: \nidentifier')
dfa.node('s7', 's7: \nProgram')


dfa.edge('s0', 's1', label='p')
dfa.edge('s1', 's2', label='r')
dfa.edge('s2', 's3', label='o')
dfa.edge('s3', 's4', label='g')
dfa.edge('s4', 's5', label='r')
dfa.edge('s5', 's6', label='a')
dfa.edge('s6', 's7', label='m')
dfa.edge('s7', 's150', label='[a-zA-Z0-9]')


# Parameter
dfa.node('s8', 's8: \nidentifier')
dfa.node('s9', 's9: \nidentifier')
dfa.node('s10', 's10: \nidentifier')
dfa.node('s11', 's11: \nidentifier')
dfa.node('s12', 's12: \nidentifier')
dfa.node('s13', 's13: \nidentifier')
dfa.node('s13', 's13: \nidentifier')
dfa.node('s14', 's14: \nidentifier')
dfa.node('s15', 's15: \nParameter')


dfa.edge('s1', 's8', label='a')
dfa.edge('s8', 's9', label='r')
dfa.edge('s9', 's10', label='a')
dfa.edge('s10', 's11', label='m')
dfa.edge('s11', 's12', label='e')
dfa.edge('s12', 's13', label='t')
dfa.edge('s13', 's14', label='e')
dfa.edge('s14', 's15', label='r')
dfa.edge('s15', 's150', label='[a-zA-Z0-9]')

# Print
dfa.node('s16', 's16: \nidentifier')
dfa.node('s17', 's17: \nidentifier')
dfa.node('s18', 's18: \nidentifier')
dfa.node('s19', 's19: \nPrint')


dfa.edge('s1', 's16', label='r')
dfa.edge('s16', 's17', label='i')
dfa.edge('s17', 's18', label='n')
dfa.edge('s18', 's19', label='t')
dfa.edge('s19', 's150', label='[a-zA-Z0-9]')

# Integer
dfa.node('s20', 's20: \nidentifier')
dfa.node('s21', 's21: \nidentifier')
dfa.node('s22', 's22: \nidentifier')
dfa.node('s23', 's23: \nidentifier')
dfa.node('s24', 's24: \nidentifier')
dfa.node('s25', 's25: \nidentifier')
dfa.node('s26', 's26: \nInteger')

dfa.edge('s0', 's20', label='i')
dfa.edge('s20', 's21', label='n')
dfa.edge('s21', 's22', label='t')
dfa.edge('s22', 's23', label='e')
dfa.edge('s23', 's24', label='g')
dfa.edge('s24', 's25', label='e')
dfa.edge('s25', 's26', label='r')
dfa.edge('s26', 's150', label='[a-zA-Z0-9]')

# If
dfa.node('s27', 's27: \nIf')


dfa.edge('s20', 's27', label='f')
dfa.edge('s27', 's150', label='[a-zA-Z0-9]')



#Implicit
dfa.node('s28', 's28: \nidentifier')
dfa.node('s29', 's29: \nidentifier')
dfa.node('s30', 's30: \nidentifier')
dfa.node('s31', 's31: \nidentifier')
dfa.node('s32', 's32: \nidentifier')
dfa.node('s33', 's33: \nidentifier')
dfa.node('s34', 's34: \nImplicit')

dfa.edge('s20', 's28', label='m')
dfa.edge('s28', 's29', label='p')
dfa.edge('s29', 's30', label='l')
dfa.edge('s30', 's31', label='i')
dfa.edge('s31', 's32', label='c')
dfa.edge('s32', 's33', label='i')
dfa.edge('s33', 's34', label='t')
dfa.edge('s34', 's150', label='[a-zA-Z0-9]')

# End
dfa.node('s35', 's35: \nidentifier')
dfa.node('s36', 's36: \nidentifier')
dfa.node('s37', 's37: \nEnd')

dfa.edge('s0', 's35', label='e')
dfa.edge('s35', 's36', label='n')
dfa.edge('s36', 's37', label='d')
dfa.edge('s37', 's150', label='[a-zA-Z0-9]')

# Else
dfa.node('s38', 's38: \nidentifier')
dfa.node('s39', 's39: \nidentifier')
dfa.node('s40', 's40: \nElse')

dfa.edge('s35', 's38', label='l')
dfa.edge('s38', 's39', label='s')
dfa.edge('s39', 's40', label='e')
dfa.edge('s40', 's150', label='[a-zA-Z0-9]')

# Real
dfa.node('s41', 's41: \nidentifier')
dfa.node('s42', 's42: \nidentifier')
dfa.node('s43', 's43: \nidentifier')
dfa.node('s44', 's44: \nReal')

dfa.edge('s0', 's41', label='r')
dfa.edge('s41', 's42', label='e')
dfa.edge('s42', 's43', label='a')
dfa.edge('s43', 's44', label='l')
dfa.edge('s44', 's150', label='[a-zA-Z0-9]')

# Read
dfa.node('s45', 's45: \nRead')

dfa.edge('s43', 's45', label='d')
dfa.edge('s45', 's150', label='[a-zA-Z0-9]')

# Complex
dfa.node('s46', 's46: \nidentifier')
dfa.node('s47', 's47: \nidentifier')
dfa.node('s48', 's48: \nidentifier')
dfa.node('s49', 's49: \nidentifier')
dfa.node('s50', 's50: \nidentifier')
dfa.node('s51', 's51: \nidentifier')
dfa.node('s52', 's52: \nComplex')


dfa.edge('s0', 's46', label='c')
dfa.edge('s46', 's47', label='o')
dfa.edge('s47', 's48', label='m')
dfa.edge('s48', 's49', label='p')
dfa.edge('s49', 's50', label='l')
dfa.edge('s50', 's51', label='e')
dfa.edge('s51', 's52', label='x')
dfa.edge('s52', 's150', label='[a-zA-Z0-9]')

# Character
dfa.node('s53', 's53: \nidentifier')
dfa.node('s54', 's54: \nidentifier')
dfa.node('s55', 's55: \nidentifier')
dfa.node('s56', 's56: \nidentifier')
dfa.node('s57', 's57: \nidentifier')
dfa.node('s58', 's58: \nidentifier')
dfa.node('s59', 's59: \nidentifier')
dfa.node('s60', 's60: \nCharacter')


dfa.edge('s46', 's53', label='h')
dfa.edge('s53', 's54', label='a')
dfa.edge('s54', 's55', label='r')
dfa.edge('s55', 's56', label='a')
dfa.edge('s56', 's57', label='c')
dfa.edge('s57', 's58', label='t')
dfa.edge('s58', 's59', label='e')
dfa.edge('s59', 's60', label='r')
dfa.edge('s60', 's150', label='[a-zA-Z0-9]')

# Complex
dfa.node('s61', 's61: \nidentifier')
dfa.node('s62', 's62: \nidentifier')
dfa.node('s63', 's63: \nidentifier')
dfa.node('s64', 's64: \nidentifier')
dfa.node('s65', 's65: \nidentifier')
dfa.node('s66', 's66: \nidentifier')
dfa.node('s67', 's67: \nLogical')

# Logical
dfa.edge('s0', 's61', label='l')
dfa.edge('s61', 's62', label='o')
dfa.edge('s62', 's63', label='g')
dfa.edge('s63', 's64', label='i')
dfa.edge('s64', 's65', label='c')
dfa.edge('s65', 's66', label='a')
dfa.edge('s66', 's67', label='l')
dfa.edge('s67', 's150', label='[a-zA-Z0-9]')

# Len
dfa.node('s68', 's68: \nidentifier')
dfa.node('s69', 's69: \nLen')


dfa.edge('s61', 's68', label='e')
dfa.edge('s68', 's69', label='n')
dfa.edge('s69', 's150', label='[a-zA-Z0-9]')

# True
dfa.node('s70', 's70: \nidentifier')
dfa.node('s71', 's71: \nidentifier')
dfa.node('s72', 's72: \nidentifier')
dfa.node('s73', 's73: \nTrue')

dfa.edge('s0', 's70', label='t')
dfa.edge('s70', 's71', label='r')
dfa.edge('s71', 's72', label='u')
dfa.edge('s72', 's73', label='e')
dfa.edge('s73', 's150', label='[a-zA-Z0-9]')

# Then
dfa.node('s74', 's74: \nidentifier')
dfa.node('s75', 's75: \nidentifier')
dfa.node('s76', 's76: \nThen')

dfa.edge('s70', 's74', label='h')
dfa.edge('s74', 's75', label='e')
dfa.edge('s75', 's76', label='n')
dfa.edge('s76', 's150', label='[a-zA-Z0-9]')

# Do
dfa.node('s77', 's77: \nidentifier')
dfa.node('s78', 's78: \nDo')

dfa.edge('s0', 's77', label='d')
dfa.edge('s77', 's78', label='o')
dfa.edge('s78', 's150', label='[a-zA-Z0-9]')

# False
dfa.node('s79', 's79: \nidentifier')
dfa.node('s80', 's80: \nidentifier')
dfa.node('s81', 's81: \nidentifier')
dfa.node('s82', 's82: \nidentifier')
dfa.node('s83', 's83: \nFalse')

dfa.edge('s0', 's79', label='f')
dfa.edge('s79', 's80', label='a')
dfa.edge('s80', 's81', label='l')
dfa.edge('s81', 's82', label='s')
dfa.edge('s82', 's83', label='e')
dfa.edge('s83', 's150', label='[a-zA-Z0-9]')

# None
dfa.node('s84', 's84: \nidentifier')
dfa.node('s85', 's85: \nidentifier')
dfa.node('s86', 's86: \nidentifier')
dfa.node('s87', 's87: \nNone')

dfa.edge('s0', 's84', label='n')
dfa.edge('s84', 's85', label='o')
dfa.edge('s85', 's86', label='n')
dfa.edge('s86', 's87', label='e')
dfa.edge('s87', 's150', label='[a-zA-Z0-9]')

# <=
dfa.node('s88', 's88: \nSymbol')
dfa.node('s89', 's89: \nSymbol')


dfa.edge('s0', 's88', label='<')
dfa.edge('s88', 's89', label='=')

# >=
dfa.node('s90', 's90: \nSymbol')
dfa.node('s91', 's91: \nSymbol')


dfa.edge('s0', 's90', label='>')
dfa.edge('s90', 's91', label='=')

# ==
dfa.node('s92', 's92: \nSymbol')
dfa.node('s93', 's93: \nSymbol')


dfa.edge('s0', 's92', label='=')
dfa.edge('s92', 's93', label='=')

# /=
dfa.node('s94', 's94: \nSymbol')
dfa.node('s95', 's95: \nSymbol')


dfa.edge('s0', 's94', label='/')
dfa.edge('s94', 's95', label='=')

# +
dfa.node('s96', 's96: \nSymbol')

dfa.edge('s0', 's96', label='+')

# -
dfa.node('s97', 's97: \nSymbol')

dfa.edge('s0', 's97', label='-')

# *
dfa.node('s98', 's98: \nSymbol')

dfa.edge('s0', 's96', label='*')

# (
dfa.node('s99', 's99: \nSymbol')

dfa.edge('s0', 's99', label='(')

# )
dfa.node('s100', 's100: \nSymbol')

dfa.edge('s0', 's100', label=')')

# :
dfa.node('s101', 's101: \nSymbol')

dfa.edge('s0', 's101', label=':')

# .
dfa.node('s102', 's102: \nSymbol')

dfa.edge('s0', 's102', label='.')

# ,
dfa.node('s103', 's103: \nSymbol')

dfa.edge('s0', 's103', label=',')

# Digits
dfa.node('s104', 's104: \nDigit')

dfa.edge('s0', 's104', label='Digit')
dfa.edge('s104', 's104', label='Digit')

dfa.render(directory='dfa', view=True)